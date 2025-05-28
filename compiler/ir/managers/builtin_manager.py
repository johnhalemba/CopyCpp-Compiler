"""Builtin functions management for CopyCpp compiler"""
import llvmlite.ir as ir


class BuiltinManager:
    def __init__(self, module, string_manager, debug=False):
        self.module = module
        self.string_manager = string_manager
        self.debug = debug
        self.builtin_functions = {}

        # Determine size_t type
        ptr_size_in_bytes = 8  # Assuming 64-bit
        self.size_t_type = ir.IntType(ptr_size_in_bytes * 8)

        self._declare_system_functions()
        self._create_print_wrappers()
        self._create_read_wrappers()

    def log(self, message):
        if self.debug:
            print(f"DEBUG BUILTIN: {message}")

    def _declare_system_functions(self):
        """Declare system functions like printf, scanf, malloc, free"""
        # printf
        printf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        self.builtin_functions["printf"] = ir.Function(self.module, printf_ty, name="printf")

        # scanf
        scanf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        self.builtin_functions["scanf"] = ir.Function(self.module, scanf_ty, name="scanf")

        # malloc
        malloc_ty = ir.FunctionType(ir.PointerType(ir.IntType(8)), [self.size_t_type])
        self.builtin_functions["malloc"] = ir.Function(self.module, malloc_ty, name="malloc")

        # free
        free_ty = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))])
        self.builtin_functions["free"] = ir.Function(self.module, free_ty, name="free")

        self.log("Declared system functions")

    def _create_print_wrappers(self):
        """Create print wrapper functions for different types"""
        self._create_print_wrapper("int", ir.IntType(32), "%d\n\0")
        self._create_print_wrapper("float32", ir.FloatType(), "%f\n\0")
        self._create_print_wrapper("float64", ir.DoubleType(), "%f\n\0")
        self._create_print_wrapper("bool", ir.IntType(1), "%s\n\0")
        self._create_print_wrapper("string", ir.PointerType(ir.IntType(8)), "%s\n\0")

    def _create_print_wrapper(self, type_name_suffix, llvm_arg_type, fmt_str_val):
        """Create a print wrapper for a specific type"""
        fmt_global = self.string_manager.get_or_create_global_string(fmt_str_val, f".fmt_print_{type_name_suffix}")
        fn_name = f"print_{type_name_suffix}"

        if fn_name in self.builtin_functions:
            return

        fn_type = ir.FunctionType(ir.VoidType(), [llvm_arg_type])
        fn = ir.Function(self.module, fn_type, name=fn_name)

        builder = ir.IRBuilder(fn.append_basic_block(name="entry"))

        fmt_ptr = builder.gep(fmt_global, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])

        arg_to_print = fn.args[0]
        if type_name_suffix == "bool":
            true_g = self.string_manager.get_or_create_global_string("true\0", ".str_true")
            false_g = self.string_manager.get_or_create_global_string("false\0", ".str_false")
            true_ptr = builder.gep(true_g, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
            false_ptr = builder.gep(false_g, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
            selected_str = builder.select(arg_to_print, true_ptr, false_ptr)
            builder.call(self.builtin_functions["printf"], [fmt_ptr, selected_str])
        else:
            builder.call(self.builtin_functions["printf"], [fmt_ptr, arg_to_print])

        builder.ret_void()
        self.builtin_functions[fn_name] = fn
        self.log(f"Created print wrapper: {fn_name}")

    def _create_read_wrappers(self):
        """Create read wrapper functions for different types"""
        self._create_read_wrapper("int", ir.IntType(32), "%d\0")
        self._create_read_wrapper("float32", ir.FloatType(), "%f\0")
        self._create_read_wrapper("float64", ir.DoubleType(), "%lf\0")

    def _create_read_wrapper(self, type_name_suffix, llvm_arg_type_pointee, fmt_str_val):
        """Create a read wrapper for a specific type"""
        fmt_global = self.string_manager.get_or_create_global_string(fmt_str_val, f".fmt_read_{type_name_suffix}")
        fn_name = f"read_{type_name_suffix}"

        if fn_name in self.builtin_functions:
            return

        fn_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(llvm_arg_type_pointee)])
        fn = ir.Function(self.module, fn_type, name=fn_name)

        builder = ir.IRBuilder(fn.append_basic_block(name="entry"))

        fmt_ptr = builder.gep(fmt_global, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])

        builder.call(self.builtin_functions["scanf"], [fmt_ptr, fn.args[0]])
        builder.ret_void()

        self.builtin_functions[fn_name] = fn
        self.log(f"Created read wrapper: {fn_name}")

    def get_function(self, name):
        """Get a builtin function by name"""
        return self.builtin_functions.get(name)

    def get_all_functions(self):
        """Get all builtin functions"""
        return self.builtin_functions.copy()