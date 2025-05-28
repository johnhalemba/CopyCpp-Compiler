from compiler.ast_builder import *

class TypeChecker:
    def __init__(self):
        # Use a list as a stack for scopes
        self.scopes = [{}]  # Global scope initially
        self.functions = {}  # function name -> FunctionType
        self.current_function = None  # current function return type
        self.errors = []

        # Add built-in functions
        self._add_builtin_functions()

        # Add boolean literals to the global scope
        self.scopes[0]["true"] = Type("bool")
        self.scopes[0]["false"] = Type("bool")

    def _add_builtin_functions(self):
        # print function for various types
        self.functions["print"] = FunctionType(Type("void"), [Type("any")])  # Accept any type

        # read function for various types
        self.functions["read"] = FunctionType(Type("void"), [Type("any")])

    def _enter_scope(self):
        self.scopes.append({})

    def _exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def _declare_variable(self, name, var_type):
        # Check if variable already exists in the *current* scope
        current_scope = self.scopes[-1]
        if name in current_scope:
            self.errors.append(f"Variable {name} already declared in this scope")
            return False
        current_scope[name] = var_type
        return True

    def _lookup_variable(self, name):
        # Look up variable starting from the innermost scope
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def check(self, ast):
        if isinstance(ast, ProgramNode):
            for stmt in ast.statements:
                self.check_statement(stmt)
        return self.errors

    def check_statement(self, stmt):
        if isinstance(stmt, VarDeclarationNode):
            self.check_var_declaration(stmt)
        elif isinstance(stmt, AssignmentNode):
            self.check_assignment(stmt)
        elif isinstance(stmt, IfStatementNode):
            self.check_if_statement(stmt)
        elif isinstance(stmt, WhileStatementNode):
            self.check_while_statement(stmt)
        elif isinstance(stmt, ForStatementNode):
            self.check_for_statement(stmt)
        elif isinstance(stmt, FunctionDeclNode):
            self.check_function_declaration(stmt)
        elif isinstance(stmt, FunctionCallNode):
            # Function call as a statement needs semicolon check in parser
            self.check_function_call(stmt)
        elif isinstance(stmt, ReturnStatementNode):
            self.check_return_statement(stmt)
        elif isinstance(stmt, PrintStatementNode):
            self.check_print_statement(stmt)
        elif isinstance(stmt, ReadStatementNode):
            self.check_read_statement(stmt)
        elif isinstance(stmt, BlockNode):
            self._enter_scope()
            self.check_block(stmt)
            self._exit_scope()

    def check_var_declaration(self, node):
        # Add to symbol table (current scope)
        var_type = Type(node.type_name,
                        is_array=len(node.dimensions) > 0,
                        array_dimensions=node.dimensions)

        declared = self._declare_variable(node.var_name, var_type)
        if not declared:
            return

        # Check initial value if provided
        if node.initial_value:
            value_type = self.check_expr(node.initial_value)
            # Pass is_declaration=True to allow float64 literal -> float32 var
            if value_type and not self._types_compatible(var_type, value_type, is_declaration=True):
                self.errors.append(
                    f"Type mismatch in declaration of {node.var_name}: "
                    f"expected {var_type.name}, got {value_type.name}")

    def check_assignment(self, node):
        # Check if variable exists
        var_type = self._lookup_variable(node.var_name)
        if not var_type:
            self.errors.append(f"Undefined variable {node.var_name}")
            return

        value_type = self.check_expr(node.value)

        # Check if trying to assign to array element but variable is not array
        if node.indices and not var_type.is_array:
            self.errors.append(f"{node.var_name} is not an array or matrix")
            return

        # For array assignments, check indices
        if node.indices and var_type.is_array:
            expected_dims = len(var_type.array_dimensions) if var_type.array_dimensions else (
                1 if "[][]" not in str(var_type) else 2)  # Heuristic if dimensions unknown
            if len(node.indices) != expected_dims:
                self.errors.append(
                    f"Wrong number of indices for {node.var_name}: expected "
                    f"{expected_dims}, got {len(node.indices)}")
                return

            # Check that indices are integers
            for i, index in enumerate(node.indices):
                index_type = self.check_expr(index)
                if index_type and index_type.name != "int":
                    self.errors.append(f"Array index must be an integer, got {index_type.name}")

            # Check type compatibility for the element being assigned
            element_type = Type(var_type.name)  # Base type of the array
            if value_type and not self._types_compatible(element_type, value_type, is_declaration=True):
                self.errors.append(
                    f"Type mismatch in assignment to {node.var_name}[...]: "
                    f"expected {element_type.name}, got {value_type.name}")
            return

        # Check type compatibility for non-array assignments
        # Pass is_declaration=True to allow float64 literal -> float32 var
        if value_type and not self._types_compatible(var_type, value_type, is_declaration=True):
            self.errors.append(
                f"Type mismatch in assignment to {node.var_name}: "
                f"expected {var_type.name}, got {value_type.name}")

    def check_if_statement(self, node):
        # Check condition type
        cond_type = self.check_expr(node.condition)
        if cond_type and cond_type.name != "bool":
            self.errors.append(f"Condition in if statement must be boolean, got {cond_type.name}")

        # Check then branch (potentially new scope if it's a block)
        self.check_statement(node.then_branch)
        # Check else branch (potentially new scope if it's a block)
        if node.else_branch:
            self.check_statement(node.else_branch)

    def check_while_statement(self, node):
        # Check condition type
        cond_type = self.check_expr(node.condition)
        if cond_type and cond_type.name != "bool":
            self.errors.append(f"Condition in while statement must be boolean, got {cond_type.name}")

        # Check body (potentially new scope if it's a block)
        self.check_statement(node.body)

    def check_for_statement(self, node):
        # For loops often introduce a new scope
        self._enter_scope()
        # Check initialization
        self.check_statement(node.init)

        # Check condition
        cond_type = self.check_expr(node.condition)
        if cond_type and cond_type.name != "bool":
            self.errors.append(f"Condition in for statement must be boolean, got {cond_type.name}")

        # Check update expression
        self.check_expr(node.update)

        # Check body (already in the for loop's scope)
        self.check_statement(node.body)
        self._exit_scope()

    def check_function_declaration(self, node):
        # Check if function already exists
        if node.name in self.functions:
            self.errors.append(f"Function {node.name} already declared")
            # Still define it to allow checking the body

        # --- Define function signature before entering scope ---
        param_types = []
        param_names = []
        for param_info in node.params:
            if len(param_info) == 2:  # Simple parameter (type, name)
                param_type, _ = param_info
                param_types.append(Type(param_type))
            elif len(param_info) == 3:  # Array parameter (type, name, dimensions)
                param_type, _, dimensions = param_info
                is_array = dimensions is not None  # dimensions can be [None] or [None, None]
                param_types.append(Type(param_type, is_array=is_array, array_dimensions=dimensions))
            param_names.append(param_info[1])  # Store name

        # Register function in the outer scope's function table
        self.functions[node.name] = FunctionType(Type(node.type_name), param_types)
        # -------------------------------------------------------

        # --- Enter function scope and check body ---
        old_function = self.current_function
        self.current_function = Type(node.type_name)
        self._enter_scope()  # Enter function body scope

        # Add parameters to the function's scope
        for i, param_info in enumerate(node.params):
            self._declare_variable(param_names[i], param_types[i])

        # Check function body
        self.check_block(node.body)  # check_block doesn't manage scope itself

        self._exit_scope()  # Exit function body scope
        self.current_function = old_function
        # -------------------------------------------

    def check_function_call(self, node):
        # Check if function exists
        if node.name not in self.functions:
            # Special handling for built-ins if needed, otherwise error
            if node.name not in ["print", "read"]:  # Example built-ins
                self.errors.append(f"Undefined function {node.name}")
                return None
            # Handle built-ins like print/read - they might accept 'any'
            if node.name == "print":
                if len(node.args) != 1:
                    self.errors.append(f"Function 'print' expects 1 argument, got {len(node.args)}")
                else:
                    self.check_expr(node.args[0])  # Check the argument expression
                return Type("void")
            if node.name == "read":
                if len(node.args) != 1:
                    self.errors.append(f"Function 'read' expects 1 argument, got {len(node.args)}")
                elif not isinstance(node.args[0], VarReferenceNode):
                    self.errors.append(f"Argument to 'read' must be a variable")
                else:
                    self.check_expr(node.args[0])  # Check the variable exists
                return Type("void")

        # Regular function call
        func_type = self.functions[node.name]

        # Check number of arguments
        if len(node.args) != len(func_type.param_types):
            self.errors.append(
                f"Wrong number of arguments for function {node.name}: "
                f"expected {len(func_type.param_types)}, got {len(node.args)}")
            # Return expected type anyway to potentially reduce cascaded errors
            return func_type.return_type

        # Check argument types
        for i, arg in enumerate(node.args):
            arg_type = self.check_expr(arg)
            expected_param_type = func_type.param_types[i]
            if arg_type and expected_param_type.name != "any" and not self._types_compatible(expected_param_type,
                                                                                             arg_type):
                self.errors.append(
                    f"Type mismatch in argument {i + 1} of function {node.name}: "
                    f"expected {expected_param_type}, got {arg_type}")  # More detailed error

        return func_type.return_type

    def check_return_statement(self, node):
        # Check if return is inside a function
        if not self.current_function:
            self.errors.append("Return statement outside of function")
            return

        # Check return value type
        if node.value:
            value_type = self.check_expr(node.value)
            if self.current_function.name == "void":
                self.errors.append(f"Cannot return a value from a void function")
            elif value_type and not self._types_compatible(self.current_function, value_type):
                self.errors.append(
                    f"Type mismatch in return statement: "
                    f"expected {self.current_function.name}, got {value_type.name}")
        elif self.current_function.name != "void":
            self.errors.append(
                f"Missing return value for function returning {self.current_function.name}")

    def check_print_statement(self, node):
        # Delegate to function call check
        self.check_function_call(FunctionCallNode("print", [node.value]))

    def check_read_statement(self, node):
        # Delegate to function call check
        var_ref = VarReferenceNode(node.var_name)
        self.check_function_call(FunctionCallNode("read", [var_ref]))

    def check_block(self, node):
        # Check statements within the current scope
        for stmt in node.statements:
            self.check_statement(stmt)

    def check_expr(self, expr):
        if isinstance(expr, LiteralNode):
            # Check if float literal needs specific type
            if expr.type_name == "float64" and '.' in str(expr.value):  # Basic check
                # Keep it as float64, compatibility check handles assignment
                return Type("float64")
            return Type(expr.type_name)

        elif isinstance(expr, VarReferenceNode):
            var_type = self._lookup_variable(expr.name)
            if not var_type:
                self.errors.append(f"Undefined variable {expr.name}")
                return None

            # Check array/matrix access
            if expr.indices:
                if not var_type.is_array:
                    self.errors.append(f"{expr.name} is not an array or matrix")
                    return None

                expected_dims = len(var_type.array_dimensions) if var_type.array_dimensions else (
                    1 if "[][]" not in str(var_type) else 2)
                if len(expr.indices) != expected_dims:
                    self.errors.append(
                        f"Wrong number of indices for {expr.name}: expected "
                        f"{expected_dims}, got {len(expr.indices)}")
                    return None

                # Check that indices are integers
                for i, index in enumerate(expr.indices):
                    index_type = self.check_expr(index)
                    if index_type and index_type.name != "int":
                        self.errors.append(f"Array index must be an integer, got {index_type.name}")

                # Return element type (not array)
                return Type(var_type.name)

            return var_type  # Return the full type (could be array)

        elif isinstance(expr, BinaryOpNode):
            left_type = self.check_expr(expr.left)
            right_type = self.check_expr(expr.right)

            if not left_type or not right_type:
                return None  # Error already reported

            # --- Type Coercion/Promotion for Binary Ops ---
            # Determine the resulting type based on operands
            result_type = None
            if left_type.name in ["float64", "float32", "int"] and \
                    right_type.name in ["float64", "float32", "int"]:
                if left_type.name == "float64" or right_type.name == "float64":
                    result_type = Type("float64")
                elif left_type.name == "float32" or right_type.name == "float32":
                    result_type = Type("float32")
                else:
                    result_type = Type("int")
            elif left_type.name == "bool" and right_type.name == "bool":
                result_type = Type("bool")
            elif left_type.name == "string" and right_type.name == "string" and expr.op in ['+', '==', '!=']:
                result_type = Type("string") if expr.op == '+' else Type("bool")
            # ---------------------------------------------

            # Handle logical operators
            if expr.op in ["&&", "||", "^"]:
                if left_type.name != "bool" or right_type.name != "bool":
                    self.errors.append(
                        f"Logical operator '{expr.op}' requires boolean operands, "
                        f"got {left_type.name} and {right_type.name}")
                return Type("bool")  # Logical ops always return bool

            # Handle comparison operators
            if expr.op in ["<", ">", "<=", ">=", "==", "!="]:
                # Check if types are comparable
                allowed_numeric = ["int", "float32", "float64"]
                is_left_numeric = left_type.name in allowed_numeric
                is_right_numeric = right_type.name in allowed_numeric
                is_left_string = left_type.name == "string"
                is_right_string = right_type.name == "string"

                if not ((is_left_numeric and is_right_numeric) or
                        (is_left_string and is_right_string and expr.op in ["==", "!="])):
                    self.errors.append(
                        f"Cannot apply operator '{expr.op}' to operands of type "
                        f"{left_type.name} and {right_type.name}")
                return Type("bool")  # Comparisons always return bool

            # Handle arithmetic operators
            if expr.op in ["+", "-", "*", "/", "%"]:
                # String concatenation
                if expr.op == "+" and (left_type.name == "string" or right_type.name == "string"):
                    if left_type.name != "string" or right_type.name != "string":
                        self.errors.append(
                            f"String concatenation requires both operands to be strings, "
                            f"got {left_type.name} and {right_type.name}")
                    return Type("string")

                # Numeric operations
                allowed_numeric = ["int", "float32", "float64"]
                if left_type.name not in allowed_numeric or right_type.name not in allowed_numeric:
                    self.errors.append(
                        f"Arithmetic operator '{expr.op}' requires numeric operands, "
                        f"got {left_type.name} and {right_type.name}")
                    return None  # Indicate error

                # Modulo only for integers
                if expr.op == '%' and (left_type.name != "int" or right_type.name != "int"):
                    self.errors.append(
                        f"Operator '%' requires integer operands, got {left_type.name} and {right_type.name}")

                return result_type  # Return promoted numeric type

            # Unknown operator
            self.errors.append(f"Unsupported operator '{expr.op}' for types {left_type.name} and {right_type.name}")
            return None

        elif isinstance(expr, UnaryOpNode):
            operand_type = self.check_expr(expr.expr)

            if not operand_type:
                return None

            if expr.op == "-":
                if operand_type.name not in ["int", "float32", "float64"]:
                    self.errors.append(
                        f"Unary minus requires numeric operand, got {operand_type.name}")
                    return None
                return operand_type  # Type doesn't change

            elif expr.op == "!":
                if operand_type.name != "bool":
                    self.errors.append(
                        f"Logical NOT requires boolean operand, got {operand_type.name}")
                    return None
                return Type("bool")  # Always returns bool

            # Unknown operator
            self.errors.append(f"Unknown unary operator: {expr.op}")
            return None

        elif isinstance(expr, FunctionCallNode):
            return self.check_function_call(expr)

        return None  # Should not happen

    def _types_compatible(self, expected, actual, is_declaration=False):
        # Exact match
        if expected.name == actual.name and expected.is_array == actual.is_array:
            # If arrays, check dimensions loosely if needed (e.g., for parameters)
            if expected.is_array:
                # Allow compatibility if expected dimensions are unknown (None)
                if (expected.array_dimensions and None in expected.array_dimensions) or \
                        len(expected.array_dimensions) == len(actual.array_dimensions):
                    return True
                else:
                    # Be more strict for known dimensions if necessary
                    # For now, allow if base types match and both are arrays
                    return True
            return True  # Non-arrays match

        # If expected is 'any', accept any type
        if expected.name == "any":
            return True

        # Allow float64 literal -> float32 variable during declaration/assignment
        if is_declaration and expected.name == "float32" and actual.name == "float64":
            # We might want to check if the literal value actually fits later
            return True

        # Numeric type widening conversion (implicit)
        if expected.name == "float64" and actual.name in ["int", "float32"]:
            return True
        if expected.name == "float32" and actual.name == "int":
            return True

        # Array compatibility (passing array to function expecting array)
        if expected.is_array and actual.is_array and expected.name == actual.name:
            # Allow if expected dimensions are unknown (e.g., param m[][])
            if expected.array_dimensions and None in expected.array_dimensions:
                return True
            # Or if dimensions match exactly
            if len(expected.array_dimensions) == len(actual.array_dimensions):
                # Could add check for actual dimension values if needed
                return True

        return False


# Helper class definitions (Type, FunctionType) remain the same
class Type:
    def __init__(self, name, is_array=False, array_dimensions=None):
        self.name = name
        self.is_array = is_array
        # Ensure dimensions are stored correctly, even if unknown (None)
        self.array_dimensions = array_dimensions if array_dimensions is not None else []

    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        # Basic equality check
        return (self.name == other.name and
                self.is_array == other.is_array and
                len(self.array_dimensions) == len(other.array_dimensions))  # Loose check for now

    def __str__(self):
        base = self.name
        if self.is_array:
            if self.array_dimensions and None in self.array_dimensions:
                # Represent unknown dimensions as []
                base += "[]" * len(self.array_dimensions)
            elif self.array_dimensions:
                # Could represent known dimensions like [5] or [3][3]
                base += "[]" * len(self.array_dimensions)  # Simple representation for now
            else:
                base += "[]"  # Default if dimensions list is empty but is_array is true
        return base


class FunctionType:
    def __init__(self, return_type, param_types):
        self.return_type = return_type
        self.param_types = param_types

