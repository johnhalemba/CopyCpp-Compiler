"""String literal management for CopyCpp compiler"""
import llvmlite.ir as ir

class StringManager:
    def __init__(self, module, debug=False):
        self.module = module
        self.debug = debug
        self.string_constants = {}

    def log(self, message):
        if self.debug:
            print(f"DEBUG STR: {message}")

    def get_or_create_global_string(self, string_val_with_null, name_hint):
        """Get or create a global string constant"""
        if string_val_with_null in self.string_constants:
            return self.string_constants[string_val_with_null]

        str_bytes = bytearray(string_val_with_null.encode("utf-8"))
        str_type = ir.ArrayType(ir.IntType(8), len(str_bytes))

        unique_name = self.module.get_unique_name(name_hint)

        g_var = ir.GlobalVariable(self.module, str_type, name=unique_name)
        g_var.initializer = ir.Constant(str_type, str_bytes)
        g_var.global_constant = True
        g_var.linkage = 'internal'

        self.string_constants[string_val_with_null] = g_var
        self.log(f"Created global string '{unique_name}' for \"{string_val_with_null.replace(chr(0), '')}\"")
        return g_var

    def create_string_literal(self, builder, string_value):
        """Create a string literal and return a pointer to it"""
        if not string_value.endswith('\0'):
            string_value += '\0'

        str_global = self.get_or_create_global_string(string_value, "str_lit")
        return builder.gep(str_global, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])

    def clear_constants(self):
        """Clear all string constants (useful for testing)"""
        self.string_constants.clear()
        self.log("Cleared all string constants")