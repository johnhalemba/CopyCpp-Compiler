"""Function management for CopyCpp compiler"""
import llvmlite.ir as ir
from ...ast.nodes import FunctionDeclNode, ConstructorDeclNode

class FunctionManager:
    def __init__(self, module, types_manager, debug=False):
        self.module = module
        self.types_manager = types_manager
        self.debug = debug
        self.functions = {}
        self.current_function = None

    def log(self, message):
        if self.debug:
            print(f"DEBUG FUNC: {message}")

    def declare_function_signature(self, node: FunctionDeclNode):
        """Declare a function signature"""
        if node.name in self.functions:
            self.log(f"Function '{node.name}' already declared")
            return

        param_llvm_types = [
            self.types_manager.get_llvm_type(p['type'], p['dimensions'])
            for p in node.params
        ]

        if node.is_generator:
            return_llvm_type = ir.PointerType(ir.IntType(8))
        else:
            return_llvm_type = self.types_manager.get_llvm_type(node.type_name)

        func_type = ir.FunctionType(return_llvm_type, param_llvm_types)
        self.functions[node.name] = ir.Function(self.module, func_type, name=node.name)
        self.log(f"Declared function signature: {node.name}")

    def declare_method_signature(self, type_name: str, method_node: FunctionDeclNode):
        """Declare a method signature for struct or class"""
        mangled_name = f"{type_name}_{method_node.name}"
        if mangled_name in self.functions:
            return

        # First parameter is always 'this' pointer
        # Check if it's a struct or class
        if type_name in self.types_manager.structs:
            type_info = self.types_manager.structs[type_name]["type"]
        elif type_name in self.types_manager.classes:
            type_info = self.types_manager.classes[type_name]["type"]
        else:
            raise NameError(f"Type '{type_name}' not found in structs or classes")

        param_types = [ir.PointerType(type_info)]

        # Add method parameters
        param_types.extend([
            self.types_manager.get_llvm_type(p['type'], p['dimensions'])
            for p in method_node.params
        ])

        ret_type = self.types_manager.get_llvm_type(method_node.type_name)
        func_type = ir.FunctionType(ret_type, param_types)
        self.functions[mangled_name] = ir.Function(self.module, func_type, name=mangled_name)
        self.log(f"Declared method signature: {mangled_name}")

    def declare_constructor_signature(self, class_name: str, ctor_node: ConstructorDeclNode):
        """Declare a constructor signature"""
        mangled_name = f"{class_name}_constructor"
        if mangled_name in self.functions:
            return

        # First parameter is 'this' pointer
        class_type = self.types_manager.classes[class_name]["type"]
        param_types = [ir.PointerType(class_type)]

        # Add constructor parameters
        param_types.extend([
            self.types_manager.get_llvm_type(p['type'], p['dimensions'])
            for p in ctor_node.params
        ])

        # Constructors return void
        func_type = ir.FunctionType(ir.VoidType(), param_types)
        self.functions[mangled_name] = ir.Function(self.module, func_type, name=mangled_name)
        self.log(f"Declared constructor signature: {mangled_name}")

    def get_function(self, name):
        """Get a function by name"""
        return self.functions.get(name)

    def get_method(self, class_name, method_name):
        """Get a method by class and method name"""
        mangled_name = f"{class_name}_{method_name}"
        return self.functions.get(mangled_name)

    def get_constructor(self, class_name):
        """Get a constructor by class name"""
        mangled_name = f"{class_name}_constructor"
        return self.functions.get(mangled_name)

    def set_current_function(self, function):
        """Set the current function being processed"""
        self.current_function = function

    def get_current_function(self):
        """Get the current function being processed"""
        return self.current_function