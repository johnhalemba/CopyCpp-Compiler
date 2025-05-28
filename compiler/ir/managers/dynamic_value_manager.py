"""Dynamic value management for CopyCpp compiler"""
import llvmlite.ir as ir
from ...ast.nodes import LiteralNode, NullLiteralNode

class DynamicValueManager:
    def __init__(self, module, data_layout, string_manager, debug=False):
        self.module = module
        self.data_layout = data_layout
        self.string_manager = string_manager
        self.debug = debug

        self.dynamic_value_type_tag_llvm = ir.IntType(32)
        self.dynamic_value_data_llvm_type = ir.ArrayType(ir.IntType(8), 8)
        self.dynamic_value_llvm_struct = self.module.context.get_identified_type("struct.DynamicValue")

        # Type tags
        self.TYPE_TAG_NULL = 0
        self.TYPE_TAG_INT = 1
        self.TYPE_TAG_FLOAT64 = 2
        self.TYPE_TAG_BOOL = 3
        self.TYPE_TAG_STRING = 4
        self.TYPE_TAG_GENERATOR = 5

        self._init_dynamic_value_struct()

    def log(self, message):
        if self.debug:
            print(f"DEBUG DYN: {message}")

    def _init_dynamic_value_struct(self):
        """Initialize the dynamic value structure"""
        if self.dynamic_value_llvm_struct.is_opaque:
            self.dynamic_value_llvm_struct.set_body(
                self.dynamic_value_type_tag_llvm,
                self.dynamic_value_data_llvm_type
            )
            self.log("Initialized DynamicValue struct")

    def get_dynamic_value_type(self):
        """Get the dynamic value LLVM type (pointer to DynamicValue)"""
        return ir.PointerType(self.dynamic_value_llvm_struct)

    def create_dynamic_value_object(self, builder, value_ast_node, malloc_func):
        """Create a dynamic value object for an AST node"""
        self.log(f"Creating dynamic value object for {type(value_ast_node).__name__}")

        # Allocate memory for DynamicValue
        obj_size = self.dynamic_value_llvm_struct.get_abi_size(self.data_layout)
        size_const = ir.Constant(ir.IntType(64), obj_size)  # Assuming 64-bit size_t
        raw_mem_ptr = builder.call(malloc_func, [size_const], name="dyn_val_raw_mem")
        dyn_obj_ptr = builder.bitcast(raw_mem_ptr, ir.PointerType(self.dynamic_value_llvm_struct), name="dyn_val_obj")

        # Get pointers to tag and data fields
        tag_field_ptr = builder.gep(dyn_obj_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)],
                                    name="dyn_tag_ptr")
        data_storage_ptr = builder.gep(dyn_obj_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 1)],
                                       name="dyn_data_storage_ptr")

        # Store the value based on its type
        self._store_value_in_dynamic_object(builder, value_ast_node, tag_field_ptr, data_storage_ptr)

        return dyn_obj_ptr

    def _store_value_in_dynamic_object(self, builder, value_ast_node, tag_ptr, data_ptr):
        """Store a value in a dynamic object based on its AST node type"""
        from ..ir_generator import IRGenerator  # Import here to avoid circular imports

        if isinstance(value_ast_node, LiteralNode):
            if value_ast_node.type_name == "int":
                builder.store(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_INT), tag_ptr)
                # Store as i64 in the data field
                data_as_i64_ptr = builder.bitcast(data_ptr, ir.PointerType(ir.IntType(64)))
                int_val = ir.Constant(ir.IntType(32), value_ast_node.value)
                int_val_i64 = builder.sext(int_val, ir.IntType(64))
                builder.store(int_val_i64, data_as_i64_ptr)

            elif value_ast_node.type_name in ["float64", "float32"]:
                builder.store(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_FLOAT64), tag_ptr)
                data_as_double_ptr = builder.bitcast(data_ptr, ir.PointerType(ir.DoubleType()))
                float_val = ir.Constant(ir.DoubleType(), value_ast_node.value)
                builder.store(float_val, data_as_double_ptr)

            elif value_ast_node.type_name == "bool":
                builder.store(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_BOOL), tag_ptr)
                data_as_i64_ptr = builder.bitcast(data_ptr, ir.PointerType(ir.IntType(64)))
                bool_val = ir.Constant(ir.IntType(1), 1 if value_ast_node.value else 0)
                bool_val_i64 = builder.zext(bool_val, ir.IntType(64))
                builder.store(bool_val_i64, data_as_i64_ptr)

            elif value_ast_node.type_name == "string":
                builder.store(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_STRING), tag_ptr)
                data_as_i8_ptr_ptr = builder.bitcast(data_ptr, ir.PointerType(ir.PointerType(ir.IntType(8))))
                # Get string from string manager
                str_val = value_ast_node.value
                if not str_val.endswith('\0'):
                    str_val += '\0'
                str_global = self.string_manager.get_or_create_global_string(str_val, "str_lit")
                str_ptr = builder.gep(str_global, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                builder.store(str_ptr, data_as_i8_ptr_ptr)

        elif isinstance(value_ast_node, NullLiteralNode):
            builder.store(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_NULL), tag_ptr)
            data_as_i64_ptr = builder.bitcast(data_ptr, ir.PointerType(ir.IntType(64)))
            builder.store(ir.Constant(ir.IntType(64), 0), data_as_i64_ptr)

    def generate_dynamic_value_print(self, builder, dyn_obj_ptr, current_function, print_functions):
        """Generate code to print a dynamic value"""
        # Create blocks for the switch statement
        after_print_block = current_function.append_basic_block("after_dyn_print")
        process_block = current_function.append_basic_block("process_dyn_val")
        null_obj_block = current_function.append_basic_block("dyn_obj_is_null")

        # Check if dynamic object pointer is null
        is_null_cond = builder.icmp_signed("==", dyn_obj_ptr, ir.Constant(dyn_obj_ptr.type, None))
        builder.cbranch(is_null_cond, null_obj_block, process_block)

        # Handle null object
        builder.position_at_end(null_obj_block)
        null_str = self.string_manager.get_or_create_global_string("null (dynamic)\n\0", "str_dyn_null")
        null_str_ptr = builder.gep(null_str, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        builder.call(print_functions["print_string"], [null_str_ptr])
        builder.branch(after_print_block)

        # Process non-null dynamic value
        builder.position_at_end(process_block)
        tag_ptr = builder.gep(dyn_obj_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        tag_val = builder.load(tag_ptr, name="dyn_tag_val")
        data_ptr = builder.gep(dyn_obj_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 1)])

        # Create switch cases
        int_case = current_function.append_basic_block("dyn_print_int")
        float_case = current_function.append_basic_block("dyn_print_float")
        bool_case = current_function.append_basic_block("dyn_print_bool")
        string_case = current_function.append_basic_block("dyn_print_string")
        null_case = current_function.append_basic_block("dyn_print_null")
        default_case = current_function.append_basic_block("dyn_print_default")

        switch_inst = builder.switch(tag_val, default_case)
        switch_inst.add_case(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_INT), int_case)
        switch_inst.add_case(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_FLOAT64), float_case)
        switch_inst.add_case(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_BOOL), bool_case)
        switch_inst.add_case(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_STRING), string_case)
        switch_inst.add_case(ir.Constant(self.dynamic_value_type_tag_llvm, self.TYPE_TAG_NULL), null_case)

        # Implement each case
        self._implement_print_cases(builder, data_ptr, print_functions, after_print_block,
                                    int_case, float_case, bool_case, string_case, null_case, default_case)

        builder.position_at_end(after_print_block)

    def _implement_print_cases(self, builder, data_ptr, print_functions, after_block,
                               int_case, float_case, bool_case, string_case, null_case, default_case):
        """Implement the print cases for dynamic values"""
        # INT case
        builder.position_at_end(int_case)
        data_as_i64_ptr = builder.bitcast(data_ptr, ir.PointerType(ir.IntType(64)))
        int_val_i64 = builder.load(data_as_i64_ptr)
        int_val_i32 = builder.trunc(int_val_i64, ir.IntType(32))
        builder.call(print_functions["print_int"], [int_val_i32])
        builder.branch(after_block)

        # FLOAT case
        builder.position_at_end(float_case)
        data_as_double_ptr = builder.bitcast(data_ptr, ir.PointerType(ir.DoubleType()))
        double_val = builder.load(data_as_double_ptr)
        builder.call(print_functions["print_float64"], [double_val])
        builder.branch(after_block)

        # BOOL case
        builder.position_at_end(bool_case)
        data_as_i64_ptr_bool = builder.bitcast(data_ptr, ir.PointerType(ir.IntType(64)))
        bool_val_i64 = builder.load(data_as_i64_ptr_bool)
        bool_val_i1 = builder.trunc(bool_val_i64, ir.IntType(1))
        builder.call(print_functions["print_bool"], [bool_val_i1])
        builder.branch(after_block)

        # STRING case
        builder.position_at_end(string_case)
        data_as_str_ptr_ptr = builder.bitcast(data_ptr, ir.PointerType(ir.PointerType(ir.IntType(8))))
        string_val_ptr = builder.load(data_as_str_ptr_ptr)
        builder.call(print_functions["print_string"], [string_val_ptr])
        builder.branch(after_block)

        # NULL case
        builder.position_at_end(null_case)
        null_str = self.string_manager.get_or_create_global_string("null\n\0", "str_dyn_internal_null")
        null_str_ptr = builder.gep(null_str, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        builder.call(print_functions["print_string"], [null_str_ptr])
        builder.branch(after_block)

        # DEFAULT case
        builder.position_at_end(default_case)
        unknown_str = self.string_manager.get_or_create_global_string("Unknown dynamic type\n\0", "str_unknown_dyn")
        unknown_str_ptr = builder.gep(unknown_str, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        builder.call(print_functions["print_string"], [unknown_str_ptr])
        builder.branch(after_block)