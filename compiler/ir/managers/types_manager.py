"""Type management for CopyCpp compiler"""
import llvmlite.ir as ir
from ...ast.nodes import StructDeclNode, ClassDeclNode, VarDeclarationNode, FunctionDeclNode, ConstructorDeclNode

class TypesManager:
    def __init__(self, module, data_layout, debug=False):
        self.module = module
        self.data_layout = data_layout
        self.debug = debug

        # Initialize basic types
        ptr_size_in_bytes = 8  # Assuming 64-bit
        self.size_t_type = ir.IntType(ptr_size_in_bytes * 8)

        # Type dictionaries
        self.structs = {}
        self.classes = {}

    def log(self, message):
        if self.debug:
            print(f"DEBUG TYPES: {message}")

    def get_llvm_type(self, type_name_str, dimensions_ast_nodes=None):
        """Get LLVM type for a given type name"""
        self.log(f"Getting LLVM type for: {type_name_str}, dimensions: {len(dimensions_ast_nodes or [])}")

        base_llvm_type = None
        if type_name_str == "int":
            base_llvm_type = ir.IntType(32)
        elif type_name_str == "float32":
            base_llvm_type = ir.FloatType()
        elif type_name_str == "float64":
            base_llvm_type = ir.DoubleType()
        elif type_name_str == "bool":
            base_llvm_type = ir.IntType(1)
        elif type_name_str == "string":
            base_llvm_type = ir.PointerType(ir.IntType(8))
        elif type_name_str == "void":
            return ir.VoidType()
        elif type_name_str == "generator":
            base_llvm_type = ir.PointerType(ir.IntType(8))
        elif type_name_str in self.structs:
            base_llvm_type = self.structs[type_name_str]['type']
        elif type_name_str in self.classes:
            base_llvm_type = ir.PointerType(self.classes[type_name_str]['type'])
        else:
            raise ValueError(f"Unknown type name: {type_name_str}")

        if dimensions_ast_nodes and len(dimensions_ast_nodes) > 0:
            return ir.PointerType(base_llvm_type)
        return base_llvm_type

    def declare_struct_type_opaque(self, name):
        """Declare an opaque struct type"""
        if name in self.structs:
            return
        llvm_st = self.module.context.get_identified_type(f"struct.{name}")
        self.structs[name] = {
            "type": llvm_st,
            "field_names": [],
            "field_types": [],
            "methods_ast": {}
        }
        self.log(f"Declared opaque struct type: {name}")

    def declare_class_type_opaque(self, name, parent_class):
        """Declare an opaque class type"""
        if name in self.classes:
            return
        llvm_ct = self.module.context.get_identified_type(f"class.{name}")
        self.classes[name] = {
            "type": llvm_ct,
            "field_names": [],
            "field_types": [],
            "methods_ast": {},
            "ctor_ast": None,
            "parent": parent_class
        }
        self.log(f"Declared opaque class type: {name}")

    def define_struct_body(self, node: StructDeclNode):
        """Define the body of a struct type"""
        struct_info = self.structs[node.name]
        llvm_st = struct_info["type"]

        if not llvm_st.is_opaque:
            return

        fields_llvm, names_list, methods_ast_map = [], [], {}

        for member_node in node.members:
            if isinstance(member_node, VarDeclarationNode):
                names_list.append(member_node.var_name)
                fields_llvm.append(self.get_llvm_type(member_node.type_name, member_node.dimensions))
            elif isinstance(member_node, FunctionDeclNode):
                methods_ast_map[member_node.name] = member_node

        llvm_st.set_body(*fields_llvm)
        struct_info.update({
            "field_names": names_list,
            "field_types": fields_llvm,
            "methods_ast": methods_ast_map
        })
        self.log(f"Defined struct body for '{node.name}'. Fields: {names_list}")

    def define_class_body(self, node: ClassDeclNode):
        """Define the body of a class type"""
        class_info = self.classes[node.name]
        llvm_class_type = class_info["type"]

        if not llvm_class_type.is_opaque:
            return

        fields_llvm, names_list, methods_ast_map, ctor_ast = [], [], {}, None

        # Process all members from all sections
        member_sections = (node.private_members or []) + (node.public_members or []) + (node.protected_members or [])

        for member_ast in member_sections:
            if isinstance(member_ast, VarDeclarationNode):
                names_list.append(member_ast.var_name)
                fields_llvm.append(self.get_llvm_type(member_ast.type_name, member_ast.dimensions))
            elif isinstance(member_ast, FunctionDeclNode):
                methods_ast_map[member_ast.name] = member_ast
            elif isinstance(member_ast, ConstructorDeclNode):
                ctor_ast = member_ast

        # Handle inheritance
        final_fields, final_names = list(fields_llvm), list(names_list)
        if node.parent_class:
            if node.parent_class not in self.classes or self.classes[node.parent_class]["type"].is_opaque:
                raise Exception(f"Parent class '{node.parent_class}' for '{node.name}' is not defined or still opaque.")
            parent_info = self.classes[node.parent_class]
            final_fields = parent_info["field_types"] + final_fields
            final_names = parent_info["field_names"] + final_names

        llvm_class_type.set_body(*final_fields)
        class_info.update({
            "field_names": final_names,
            "field_types": final_fields,
            "methods_ast": methods_ast_map,
            "ctor_ast": ctor_ast
        })
        self.log(f"Defined class body for '{node.name}'. Fields: {final_names}")

    def get_field_index(self, type_name, field_name):
        """Get the index of a field in a struct or class"""
        if type_name in self.structs:
            if field_name in self.structs[type_name]["field_names"]:
                return self.structs[type_name]["field_names"].index(field_name)
        elif type_name in self.classes:
            if field_name in self.classes[type_name]["field_names"]:
                return self.classes[type_name]["field_names"].index(field_name)
        raise AttributeError(f"Field '{field_name}' not found in type '{type_name}'")

    def has_field(self, type_name, field_name):
        """Check if a type has a specific field"""
        if type_name in self.structs:
            return field_name in self.structs[type_name]["field_names"]
        elif type_name in self.classes:
            return field_name in self.classes[type_name]["field_names"]
        return False