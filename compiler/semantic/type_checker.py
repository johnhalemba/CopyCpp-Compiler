from ..ast.nodes import *

class TypeChecker:
    def __init__(self):
        self.errors = []
        self.symbol_table = {}
        self.current_function_return_type = None
        self.current_class = None

    def check(self, ast_node):
        """Main entry point for type checking"""
        self.errors = []
        self.visit(ast_node)
        return self.errors

    def error(self, message, node=None):
        """Add an error message"""
        self.errors.append(f"Type error: {message}")

    def visit(self, node):
        """Generic visit method"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Default visitor"""
        if hasattr(node, '__dict__'):
            for attr_name, attr_value in node.__dict__.items():
                if isinstance(attr_value, list):
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            self.visit(item)
                elif isinstance(attr_value, ASTNode):
                    self.visit(attr_value)

    def visit_ProgramNode(self, node):
        """Visit program node"""
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDeclarationNode(self, node):
        """Check variable declarations"""
        # Add to symbol table
        self.symbol_table[node.var_name] = {
            'type': node.type_name,
            'is_array': len(node.dimensions) > 0
        }

        # Check initializer type compatibility
        if node.initial_value:
            init_type = self.get_expression_type(node.initial_value)
            if not self.are_types_compatible(node.type_name, init_type):
                self.error(
                    f"Cannot initialize variable '{node.var_name}' of type '{node.type_name}' with value of type '{init_type}'")

    def visit_AssignmentNode(self, node):
        """Check assignments"""
        target_type = self.get_expression_type(node.target)
        value_type = self.get_expression_type(node.value)

        if target_type and value_type:
            if not self.are_types_compatible(target_type, value_type):
                self.error(f"Cannot assign value of type '{value_type}' to variable of type '{target_type}'")

    def visit_FunctionDeclNode(self, node):
        """Check function declarations"""
        old_return_type = self.current_function_return_type
        self.current_function_return_type = node.type_name

        # Add parameters to symbol table
        old_symbols = self.symbol_table.copy()
        for param in node.params:
            self.symbol_table[param['name']] = {
                'type': param['type'],
                'is_array': len(param.get('dimensions', [])) > 0
            }

        # Check function body
        self.visit(node.body)

        # Restore
        self.symbol_table = old_symbols
        self.current_function_return_type = old_return_type

    def visit_ReturnStatementNode(self, node):
        """Check return statements"""
        if self.current_function_return_type == "void" and node.value:
            self.error("Cannot return value from void function")
        elif self.current_function_return_type != "void" and not node.value:
            self.error(f"Must return value of type '{self.current_function_return_type}'")
        elif node.value:
            return_type = self.get_expression_type(node.value)
            if not self.are_types_compatible(self.current_function_return_type, return_type):
                self.error(
                    f"Return type '{return_type}' does not match function return type '{self.current_function_return_type}'")

    def get_expression_type(self, expr):
        """Get the type of an expression"""
        if isinstance(expr, LiteralNode):
            return expr.type_name
        elif isinstance(expr, VarReferenceNode):
            var_info = self.symbol_table.get(expr.name)
            return var_info['type'] if var_info else None
        elif isinstance(expr, BinaryOpNode):
            left_type = self.get_expression_type(expr.left)
            right_type = self.get_expression_type(expr.right)
            return self.get_binary_op_result_type(expr.op, left_type, right_type)
        elif isinstance(expr, FunctionCallNode):
            # Would need function table to determine return type
            return "unknown"
        else:
            return "unknown"

    def get_binary_op_result_type(self, op, left_type, right_type):
        """Determine result type of binary operation"""
        if op in ['==', '!=', '<', '>', '<=', '>=', '&&', '||']:
            return "bool"
        elif op in ['+', '-', '*', '/', '%']:
            if left_type == "float64" or right_type == "float64":
                return "float64"
            elif left_type == "float32" or right_type == "float32":
                return "float32"
            else:
                return "int"
        return left_type  # Default

    def are_types_compatible(self, target_type, source_type):
        """Check if types are compatible"""
        if target_type == "var" or source_type == "var":
            return True  # Dynamic typing allows anything
        if target_type == source_type:
            return True

        # Allow numeric conversions
        numeric_types = {"int", "float32", "float64"}
        if target_type in numeric_types and source_type in numeric_types:
            return True

        return False