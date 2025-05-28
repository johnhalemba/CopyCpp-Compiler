import llvmlite.ir as ir
import llvmlite.binding as llvm
from compiler.ast_builder import *

class IRGenerator:
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.module = ir.Module(name="SimpleLanguageModule")
        self.builder = None

        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        self.data_layout = target_machine.target_data
        self.module.data_layout = str(self.data_layout)
        self.module.triple = llvm.get_default_triple()

        self.variables = {}
        self.functions = {}
        self.string_constants = {}

        self.current_function = None

        self._declare_print_functions()
        self._declare_read_functions()

    def _declare_print_functions(self):
        printf_ty = ir.FunctionType(
            ir.IntType(32),
            [ir.PointerType(ir.IntType(8))],
            var_arg=True
        )
        printf = ir.Function(self.module, printf_ty, name="printf")
        self.functions["printf"] = printf

        # Create print wrappers for different types
        self._create_print_wrapper("int", ir.IntType(32))
        self._create_print_wrapper("float32", ir.FloatType())
        self._create_print_wrapper("float64", ir.DoubleType())
        self._create_print_wrapper("bool", ir.IntType(1))
        self._create_print_wrapper("string", ir.PointerType(ir.IntType(8)))

    def _create_print_wrapper(self, type_name, ir_type):
        if type_name == "int":
            fmt = "%d\n\0"
        elif type_name in ["float32", "float64"]:
            fmt = "%f\n\0"
        elif type_name == "bool":
            fmt = "%s\n\0"  # Will print "true" or "false"
        elif type_name == "string":
            fmt = "%s\n\0"
        else:
            return

        fmt_const = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf-8")))
        fmt_global = ir.GlobalVariable(self.module, fmt_const.type, name=f"fmt_str_{type_name}")
        fmt_global.global_constant = True
        fmt_global.initializer = fmt_const

        fn_type = ir.FunctionType(ir.VoidType(), [ir_type])
        fn = ir.Function(self.module, fn_type, name=f"print_{type_name}")

        block = fn.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)

        fmt_ptr = builder.bitcast(fmt_global, ir.PointerType(ir.IntType(8)))

        # Handle special case for bool
        if type_name == "bool":
            true_str = self._create_string_constant("true")
            false_str = self._create_string_constant("false")

            true_ptr = builder.bitcast(true_str, ir.PointerType(ir.IntType(8)))
            false_ptr = builder.bitcast(false_str, ir.PointerType(ir.IntType(8)))

            str_ptr = builder.select(fn.args[0], true_ptr, false_ptr)
            builder.call(self.functions["printf"], [fmt_ptr, str_ptr])
        else:
            builder.call(self.functions["printf"], [fmt_ptr, fn.args[0]])

        builder.ret_void()

        self.functions[f"print_{type_name}"] = fn

    def _declare_read_functions(self):
        # Declare scanf
        scanf_ty = ir.FunctionType(
            ir.IntType(32),
            [ir.PointerType(ir.IntType(8))],
            var_arg=True
        )
        scanf = ir.Function(self.module, scanf_ty, name="scanf")
        self.functions["scanf"] = scanf

        # Create read wrappers for different types
        self._create_read_wrapper("int", ir.IntType(32))
        self._create_read_wrapper("float32", ir.FloatType())
        self._create_read_wrapper("float64", ir.DoubleType())
        self._create_read_wrapper("string", ir.PointerType(ir.IntType(8)))

    def _create_read_wrapper(self, type_name, ir_type):
        # Create format string constant
        if type_name == "int":
            fmt = "%d\0"
        elif type_name in ["float32", "float64"]:
            fmt = "%lf\0"
        elif type_name == "string":
            fmt = "%99s\0"
        else:
            return

        fmt_const = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                                bytearray(fmt.encode("utf8")))
        fmt_global = ir.GlobalVariable(self.module, fmt_const.type, name=f"scan_fmt_{type_name}")
        fmt_global.global_constant = True
        fmt_global.initializer = fmt_const

        if type_name == "string":
            fn_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.PointerType(ir.IntType(8)))])
        else:
            fn_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir_type)])

        # Create read wrapper function
        fn = ir.Function(self.module, fn_type, name=f"read_{type_name}")

        # Create basic block
        block = fn.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)

        fmt_ptr = builder.bitcast(fmt_global, ir.PointerType(ir.IntType(8)))

        if type_name == "string":
            buffer_size = ir.Constant(ir.IntType(32), 100)
            malloc_func = self.get_or_declare_malloc()
            buffer = builder.call(malloc_func, [buffer_size])

            builder.call(self.functions["scanf"], [fmt_ptr, buffer])

            builder.store(buffer, fn.args[0])
        else:
            builder.call(self.functions["scanf"], [fmt_ptr, fn.args[0]])

        builder.ret_void()

        self.functions[f"read_{type_name}"] = fn

    def _create_string_constant(self, string_value):
        # Check if this string already exists
        if string_value in self.string_constants:
            return self.string_constants[string_value]

        # Add null terminator
        string_with_null = string_value + "\0"
        bytes_value = bytearray(string_with_null.encode("utf8"))

        # Create constant array with the string's bytes
        str_type = ir.ArrayType(ir.IntType(8), len(bytes_value))
        str_const = ir.Constant(str_type, bytes_value)

        # Create a global variable with the string
        name = f"str_{len(self.string_constants)}"
        global_str = ir.GlobalVariable(self.module, str_type, name=name)
        global_str.global_constant = True
        global_str.initializer = str_const

        # Store the global variable in cache (not the pointer)
        self.string_constants[string_value] = global_str
        return global_str

    def _get_llvm_type(self, type_name, dimensions=None):
        if type_name == "int":
            base_type = ir.IntType(32)
        elif type_name == "float32":
            base_type = ir.FloatType()
        elif type_name == "float64":
            base_type = ir.DoubleType()
        elif type_name == "bool":
            base_type = ir.IntType(1)
        elif type_name == "string":
            base_type = ir.PointerType(ir.IntType(8))
        elif type_name == "void":
            return ir.VoidType()
        else:
            raise ValueError(f"Unknown type: {type_name}")

        # Handle arrays and matrices
        if dimensions and len(dimensions) > 0:
            return ir.PointerType(base_type)

        return base_type

    def generate_ir(self, ast):
        if isinstance(ast, ProgramNode):
            # Create main function
            main_ty = ir.FunctionType(ir.IntType(32), [])
            main_fn = ir.Function(self.module, main_ty, name="main")
            entry_block = main_fn.append_basic_block(name="entry")
            self.builder = ir.IRBuilder(entry_block)

            # Generate code for each statement
            for stmt in ast.statements:
                self.generate_statement(stmt)

            # Return 0 from main
            self.builder.ret(ir.Constant(ir.IntType(32), 0))

        return self.module

    def generate_statement(self, stmt):
        if isinstance(stmt, VarDeclarationNode):
            return self.generate_var_declaration(stmt)
        elif isinstance(stmt, AssignmentNode):
            return self.generate_assignment(stmt)
        elif isinstance(stmt, IfStatementNode):
            return self.generate_if_statement(stmt)
        elif isinstance(stmt, WhileStatementNode):
            return self.generate_while_statement(stmt)
        elif isinstance(stmt, ForStatementNode):
            return self.generate_for_statement(stmt)
        elif isinstance(stmt, FunctionDeclNode):
            return self.generate_function_declaration(stmt)
        elif isinstance(stmt, FunctionCallNode):
            return self.generate_function_call(stmt)
        elif isinstance(stmt, ReturnStatementNode):
            return self.generate_return_statement(stmt)
        elif isinstance(stmt, PrintStatementNode):
            return self.generate_print_statement(stmt)
        elif isinstance(stmt, ReadStatementNode):
            return self.generate_read_statement(stmt)
        elif isinstance(stmt, BlockNode):
            return self.generate_block(stmt)

    def generate_var_declaration(self, node):
        # Determine the LLVM type
        ir_type = self._get_llvm_type(node.type_name)

        # Handle array/matrix allocation
        if node.dimensions:
            if len(node.dimensions) == 1:  # Array
                # Evaluate size expression
                size_value = self.generate_expr(node.dimensions[0])

                # Allocate array on the heap using malloc
                malloc_func = self.get_or_declare_malloc()

                # Get element size - use a different approach
                if isinstance(ir_type, ir.IntType):
                    elem_size = ir_type.width // 8  # Size in bytes
                elif isinstance(ir_type, ir.FloatType):
                    elem_size = 4  # Float is 4 bytes
                elif isinstance(ir_type, ir.DoubleType):
                    elem_size = 8  # Double is 8 bytes
                else:
                    elem_size = 4  # Default to 4 bytes

                size_bytes = self.builder.mul(size_value, ir.Constant(ir.IntType(32),
                                                                      elem_size))
                ptr = self.builder.call(malloc_func, [size_bytes])
                typed_ptr = self.builder.bitcast(ptr, ir.PointerType(ir_type))

                # Store in variables table
                self.variables[node.var_name] = (typed_ptr, node.type_name, True, node.dimensions)

            elif len(node.dimensions) == 2:  # Matrix
                # Evaluate size expressions
                rows = self.generate_expr(node.dimensions[0])
                cols = self.generate_expr(node.dimensions[1])
                total_size = self.builder.mul(rows, cols)

                # Allocate matrix on the heap
                malloc_func = self.get_or_declare_malloc()

                # Get element size - use a different approach
                if isinstance(ir_type, ir.IntType):
                    elem_size = ir_type.width // 8  # Size in bytes
                elif isinstance(ir_type, ir.FloatType):
                    elem_size = 4  # Float is 4 bytes
                elif isinstance(ir_type, ir.DoubleType):
                    elem_size = 8  # Double is 8 bytes
                else:
                    elem_size = 4  # Default to 4 bytes

                size_bytes = self.builder.mul(total_size, ir.Constant(ir.IntType(32),
                                                                      elem_size))
                ptr = self.builder.call(malloc_func, [size_bytes])
                typed_ptr = self.builder.bitcast(ptr, ir.PointerType(ir_type))

                # Store in variables table
                self.variables[node.var_name] = (typed_ptr, node.type_name, True, node.dimensions)
        else:
            # Simple variable
            ptr = self.builder.alloca(ir_type, name=node.var_name)
            self.variables[node.var_name] = (ptr, node.type_name, False, None)

            # Initialize if value provided
            if node.initial_value:
                value = self.generate_expr(node.initial_value)

                if node.type_name == "string" and isinstance(value, ir.GlobalVariable):
                    zero = ir.Constant(ir.IntType(32), 0)
                    indices = [zero, zero]
                    char_ptr = self.builder.gep(value, indices)
                    self.builder.store(char_ptr, ptr)
                else:
                    converted_value = self._convert_value_to_type(value, ir_type)
                    self.builder.store(converted_value, ptr)

    def generate_assignment(self, node):
        if node.var_name not in self.variables:
            raise ValueError(f"Undefined variable: {node.var_name}")

        ptr, type_name, is_array, dimensions = self.variables[node.var_name]
        value = self.generate_expr(node.value)

        # Handle array/matrix assignment
        if node.indices:
            if not is_array:
                raise ValueError(f"{node.var_name} is not an array or matrix")

            # Handle array access
            if len(node.indices) == 1:
                index = self.generate_expr(node.indices[0])
                element_ptr = self.builder.gep(ptr, [index])
                converted_value = self._convert_value_to_type(value, element_ptr.type.pointee)
                self.builder.store(converted_value, element_ptr)

            # Handle matrix access
            elif len(node.indices) == 2:
                row = self.generate_expr(node.indices[0])
                col = self.generate_expr(node.indices[1])

                # Calculate linear index from row and column
                # linear_index = row * num_cols + col
                cols_val = self.generate_expr(dimensions[1])
                row_offset = self.builder.mul(row, cols_val)
                linear_index = self.builder.add(row_offset, col)

                element_ptr = self.builder.gep(ptr, [linear_index])
                converted_value = self._convert_value_to_type(value, element_ptr.type.pointee)
                self.builder.store(converted_value, element_ptr)
        else:
            converted_value = self._convert_value_to_type(value, ptr.type.pointee)
            self.builder.store(converted_value, ptr)

    def generate_if_statement(self, node):
        # Evaluate condition
        condition_value = self.generate_expr(node.condition)

        # Ensure condition is a proper boolean value (i1 type)
        if not isinstance(condition_value.type, ir.IntType) or condition_value.type.width != 1:
            condition_value = self.builder.icmp_signed("!=", condition_value, ir.Constant(condition_value.type, 0))

        # Create basic blocks with unique names to avoid conflicts with nested ifs
        current_fn = self.builder.block.parent
        then_block = current_fn.append_basic_block(f"then.{id(node)}")

        if node.else_branch:
            else_block = current_fn.append_basic_block(f"else.{id(node)}")

        merge_block = current_fn.append_basic_block(f"if.end.{id(node)}")

        # Branch based on condition
        if node.else_branch:
            self.builder.cbranch(condition_value, then_block, else_block)
        else:
            self.builder.cbranch(condition_value, then_block, merge_block)

        # Generate code for then branch
        self.builder.position_at_end(then_block)
        self.generate_statement(node.then_branch)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)
        # Generate code for else branch if it exists
        if node.else_branch:
            self.builder.position_at_end(else_block)
            self.generate_statement(node.else_branch)
            # Only add branch if block isn't already terminated
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)

        # Continue with merge block
        self.builder.position_at_end(merge_block)

    def generate_while_statement(self, node):
        # Create basic blocks
        cond_block = self.builder.append_basic_block("while_cond")
        body_block = self.builder.append_basic_block("while_body")
        end_block = self.builder.append_basic_block("while_end")

        # Initial jump to condition
        self.builder.branch(cond_block)

        # Generate condition code
        self.builder.position_at_end(cond_block)
        condition_value = self.generate_expr(node.condition)
        self.builder.cbranch(condition_value, body_block, end_block)

        # Generate loop body
        self.builder.position_at_end(body_block)
        self.generate_statement(node.body)
        self.builder.branch(cond_block)

        # Continue with code after loop
        self.builder.position_at_end(end_block)

    def generate_for_statement(self, node):
        # Initialize loop variable
        self.generate_statement(node.init)

        # Create basic blocks
        cond_block = self.builder.append_basic_block("for_cond")
        body_block = self.builder.append_basic_block("for_body")
        update_block = self.builder.append_basic_block("for_update")
        end_block = self.builder.append_basic_block("for_end")

        # Initial jump to condition
        self.builder.branch(cond_block)

        # Generate condition code
        self.builder.position_at_end(cond_block)
        condition_value = self.generate_expr(node.condition)
        self.builder.cbranch(condition_value, body_block, end_block)

        # Generate loop body
        self.builder.position_at_end(body_block)
        self.generate_statement(node.body)
        self.builder.branch(update_block)

        # Generate update code
        self.builder.position_at_end(update_block)
        self.generate_expr(node.update)
        self.builder.branch(cond_block)

        # Continue with code after loop
        self.builder.position_at_end(end_block)

    def generate_function_declaration(self, node):
        # Create parameter types list
        param_types = []
        for param_type, _ in node.params:
            param_types.append(self._get_llvm_type(param_type))

        # Create function type
        return_type = self._get_llvm_type(node.type_name)
        func_type = ir.FunctionType(return_type, param_types)

        # Create function
        func = ir.Function(self.module, func_type, name=node.name)
        self.functions[node.name] = func

        # Create entry block
        entry_block = func.append_basic_block("entry")
        old_builder = self.builder
        self.builder = ir.IRBuilder(entry_block)

        # Save current function for return statements
        old_function = self.current_function
        self.current_function = func

        # Save old variables and create new scope
        old_variables = self.variables
        self.variables = {}

        # Add parameters to function scope
        for i, (param_type, param_name) in enumerate(node.params):
            # Allocate stack space for parameter
            ir_type = self._get_llvm_type(param_type)
            param_ptr = self.builder.alloca(ir_type, name=param_name)
            self.builder.store(func.args[i], param_ptr)
            self.variables[param_name] = (param_ptr, param_type, False, None)

        # Generate code for function body
        self.generate_block(node.body)

        # Add implicit return if function ends without return
        if not self.builder.block.is_terminated:
            if return_type == ir.VoidType():
                self.builder.ret_void()
            else:
                # For non-void return types, a proper return would be expected,
                # but we'll add a default return to avoid invalid IR
                zero = ir.Constant(return_type, 0)
                self.builder.ret(zero)

        # Restore old state
        self.variables = old_variables
        self.current_function = old_function
        self.builder = old_builder

    def generate_function_call(self, node):
        if node.name not in self.functions:
            raise ValueError(f"Undefined function: {node.name}")

        func = self.functions[node.name]

        # Generate arguments
        args = []
        for arg in node.args:
            args.append(self.generate_expr(arg))

        # Call function
        return self.builder.call(func, args)

    def generate_return_statement(self, node):
        if not self.current_function:
            raise ValueError("Return statement outside of function")

        # Generate return value or return void
        if node.value:
            value = self.generate_expr(node.value)
            self.builder.ret(value)
        else:
            self.builder.ret_void()

    def generate_print_statement(self, node):
        value = self.generate_expr(node.value)

        # Determine value type and call appropriate print function
        value_type = value.type

        # For global string variables, we need to convert to i8* properly
        if isinstance(value, ir.GlobalVariable) and isinstance(value.type.pointee, ir.ArrayType):
            # Get pointer to first char of string
            zero = ir.Constant(ir.IntType(32), 0)
            indices = [zero, zero]
            value = self.builder.gep(value, indices)
            value_type = value.type

        if isinstance(value_type, ir.IntType):
            if value_type.width == 1:  # Boolean
                self.builder.call(self.functions["print_bool"], [value])
            elif value_type.width == 32:  # Integer
                self.builder.call(self.functions["print_int"], [value])
        elif isinstance(value_type, ir.FloatType):
            self.builder.call(self.functions["print_float32"], [value])
        elif isinstance(value_type, ir.DoubleType):
            self.builder.call(self.functions["print_float64"], [value])
        elif value_type == ir.PointerType(ir.IntType(8)) and value_type.pointee == ir.IntType(8):  # String
            self.builder.call(self.functions["print_string"], [value])

    def generate_read_statement(self, node):
        if node.var_name not in self.variables:
            raise ValueError(f"Undefined variable: {node.var_name}")

        ptr, type_name, is_array, _ = self.variables[node.var_name]

        if is_array:
            raise ValueError(f"Cannot read directly into array variable {node.var_name}")

        # Call appropriate read function based on type
        if type_name == "int":
            self.builder.call(self.functions["read_int"], [ptr])
        elif type_name == "float32":
            self.builder.call(self.functions["read_float32"], [ptr])
        elif type_name == "float64":
            self.builder.call(self.functions["read_float64"], [ptr])
        elif type_name == "string":
            self.builder.call(self.functions["read_string"], [ptr])

    def generate_block(self, node):
        for stmt in node.statements:
            self.generate_statement(stmt)

    def generate_expr(self, expr):
        if isinstance(expr, LiteralNode):
            if expr.type_name == "int":
                return ir.Constant(ir.IntType(32), expr.value)
            elif expr.type_name == "float32":
                return ir.Constant(ir.FloatType(), expr.value)
            elif expr.type_name == "float64":
                return ir.Constant(ir.DoubleType(), expr.value)
            elif expr.type_name == "bool":
                return ir.Constant(ir.IntType(1), 1 if expr.value else 0)
            elif expr.type_name == "string":
                return self._create_string_constant(expr.value)
            return None

        elif isinstance(expr, VarReferenceNode):
            if expr.name == "true":
                return ir.Constant(ir.IntType(1), 1)
            if expr.name == "false":
                return ir.Constant(ir.IntType(1), 0)

            var_info = self._lookup_variable(expr.name)
            if not var_info:
                if expr.name in self.functions:
                    raise ValueError(f"Cannot use function '{expr.name}' as a value")
                raise ValueError(f"Undefined variable: {expr.name}")  # Error occurs here

            ptr, type_name, is_array, dimensions = var_info

            # Handle array/matrix reference
            if expr.indices:
                if not is_array:
                    raise ValueError(f"{expr.name} is not an array or matrix")

                # Handle array access
                if len(expr.indices) == 1:
                    index = self.generate_expr(expr.indices[0])
                    element_ptr = self.builder.gep(ptr, [index])
                    return self.builder.load(element_ptr)

                # Handle matrix access
                elif len(expr.indices) == 2:
                    row = self.generate_expr(expr.indices[0])
                    col = self.generate_expr(expr.indices[1])

                    # Calculate linear index from row and column
                    # linear_index = row * num_cols + col
                    cols_val = self.generate_expr(dimensions[1])
                    row_offset = self.builder.mul(row, cols_val)
                    linear_index = self.builder.add(row_offset, col)

                    element_ptr = self.builder.gep(ptr, [linear_index])
                    return self.builder.load(element_ptr)
                return None
            else:
                return self.builder.load(ptr)

        elif isinstance(expr, BinaryOpNode):
            # Implement short-circuit evaluation for logical operations
            if expr.op == "&&":
                return self.generate_short_circuit_and(expr)
            elif expr.op == "||":
                return self.generate_short_circuit_or(expr)

            # For non-short-circuit operators, evaluate both operands
            left = self.generate_expr(expr.left)
            right = self.generate_expr(expr.right)

            # Integer operations
            if isinstance(left.type, ir.IntType) and left.type.width == 32:
                if expr.op == "+":
                    return self.builder.add(left, right)
                elif expr.op == "-":
                    return self.builder.sub(left, right)
                elif expr.op == "*":
                    return self.builder.mul(left, right)
                elif expr.op == "/":
                    return self.builder.sdiv(left, right)
                elif expr.op == "%":
                    return self.builder.srem(left, right)
                elif expr.op == "<":
                    return self.builder.icmp_signed("<", left, right)
                elif expr.op == ">":
                    return self.builder.icmp_signed(">", left, right)
                elif expr.op == "<=":
                    return self.builder.icmp_signed("<=", left, right)
                elif expr.op == ">=":
                    return self.builder.icmp_signed(">=", left, right)
                elif expr.op == "==":
                    return self.builder.icmp_signed("==", left, right)
                elif expr.op == "!=":
                    return self.builder.icmp_signed("!=", left, right)
                elif expr.op == "^" and isinstance(left.type, ir.IntType) and left.type.width == 1:
                    return self.builder.xor(left, right)
                return None

            # Float operations
            elif isinstance(left.type, (ir.FloatType, ir.DoubleType)):
                if expr.op == "+":
                    return self.builder.fadd(left, right)
                elif expr.op == "-":
                    return self.builder.fsub(left, right)
                elif expr.op == "*":
                    return self.builder.fmul(left, right)
                elif expr.op == "/":
                    return self.builder.fdiv(left, right)
                elif expr.op == "<":
                    return self.builder.fcmp_ordered("<", left, right)
                elif expr.op == ">":
                    return self.builder.fcmp_ordered(">", left, right)
                elif expr.op == "<=":
                    return self.builder.fcmp_ordered("<=", left, right)
                elif expr.op == ">=":
                    return self.builder.fcmp_ordered(">=", left, right)
                elif expr.op == "==":
                    return self.builder.fcmp_ordered("==", left, right)
                elif expr.op == "!=":
                    return self.builder.fcmp_ordered("!=", left, right)
                return None

            # Boolean operations (for non-short-circuit)
            elif isinstance(left.type, ir.IntType) and left.type.width == 1:
                if expr.op == "^":  # XOR
                    return self.builder.xor(left, right)
                return None
            return None

        elif isinstance(expr, UnaryOpNode):
            operand = self.generate_expr(expr.expr)

            if expr.op == "-":
                if isinstance(operand.type, ir.IntType):
                    return self.builder.neg(operand)
                else:  # Float/Double
                    return self.builder.fneg(operand)
            elif expr.op == "!":
                return self.builder.not_(operand)
            return None

        elif isinstance(expr, FunctionCallNode):
            return self.generate_function_call(expr)
        return None

    def generate_short_circuit_and(self, expr):
        # Evaluate left operand
        left = self.generate_expr(expr.left)

        # Save the current block where 'left' was evaluated
        left_block = self.builder.block  # Get the current block

        # Create basic blocks for short-circuit
        rhs_block = self.builder.append_basic_block("and_rhs")
        end_block = self.builder.append_basic_block("and_end")

        # Convert left value to boolean if needed
        if not isinstance(left.type, ir.IntType) or left.type.width != 1:
            left = self.builder.icmp_signed("!=", left, ir.Constant(left.type, 0))

        # Branch based on left value
        self.builder.cbranch(left, rhs_block, end_block)

        # Generate right side code
        self.builder.position_at_end(rhs_block)
        right = self.generate_expr(expr.right)
        if not isinstance(right.type, ir.IntType) or right.type.width != 1:
            right = self.builder.icmp_signed("!=", right, ir.Constant(right.type, 0))
        right_block = self.builder.block  # Get the block where 'right' was evaluated
        self.builder.branch(end_block)

        # Set up phi node for result
        self.builder.position_at_end(end_block)
        phi = self.builder.phi(ir.IntType(1))
        phi.add_incoming(ir.Constant(ir.IntType(1), 0), left_block)  # Use saved left_block
        phi.add_incoming(right, right_block)  # Use right_block

        return phi

    def generate_short_circuit_or(self, expr):
        # Evaluate left operand
        left = self.generate_expr(expr.left)

        # Save the current block
        left_block = self.builder.block

        # Create basic blocks for short-circuit
        rhs_block = self.builder.append_basic_block("or_rhs")
        end_block = self.builder.append_basic_block("or_end")

        # Convert left value to boolean if needed
        if not isinstance(left.type, ir.IntType) or left.type.width != 1:
            left = self.builder.icmp_signed("!=", left, ir.Constant(left.type, 0))

        # Branch based on left value
        self.builder.cbranch(left, end_block, rhs_block)

        # Generate right side code
        self.builder.position_at_end(rhs_block)
        right = self.generate_expr(expr.right)
        if not isinstance(right.type, ir.IntType) or right.type.width != 1:
            right = self.builder.icmp_signed("!=", right, ir.Constant(right.type, 0))
        right_block = self.builder.block
        self.builder.branch(end_block)

        # Set up phi node for result
        self.builder.position_at_end(end_block)
        phi = self.builder.phi(ir.IntType(1))
        phi.add_incoming(ir.Constant(ir.IntType(1), 1), left_block)
        phi.add_incoming(right, right_block)

        return phi

    def get_or_declare_malloc(self):
        # Declare malloc if not already declared
        if "malloc" not in self.functions:
            malloc_ty = ir.FunctionType(
                ir.PointerType(ir.IntType(8)),
                [ir.IntType(32)]
            )
            malloc = ir.Function(self.module, malloc_ty, name="malloc")
            self.functions["malloc"] = malloc

        return self.functions["malloc"]

    def _convert_value_to_type(self, value, target_type):
        """Convert a value to the target LLVM type if necessary."""
        # If types already match, no conversion needed
        if value.type == target_type:
            return value

        # Handle float/double conversions
        if isinstance(value.type, (ir.FloatType, ir.DoubleType)) and isinstance(target_type,
                                                                                (ir.FloatType, ir.DoubleType)):
            if isinstance(value.type, ir.DoubleType) and isinstance(target_type, ir.FloatType):
                return self.builder.fptrunc(value, target_type)  # Double to float
            elif isinstance(value.type, ir.FloatType) and isinstance(target_type, ir.DoubleType):
                return self.builder.fpext(value, target_type)  # Float to double

        # Handle int-to-float conversions
        if isinstance(value.type, ir.IntType) and isinstance(target_type, (ir.FloatType, ir.DoubleType)):
            return self.builder.sitofp(value, target_type)

        # Handle float to int conversions
        if isinstance(value.type, (ir.FloatType, ir.DoubleType)) and isinstance(target_type, ir.IntType):
            return self.builder.fptosi(value, target_type)

        # Return unchanged if no conversion is possible
        return value

    def _lookup_variable(self, name):
        # Look up variable starting from the innermost scope (if scopes are used)
        # For now, using the simple self.variables dictionary
        if name in self.variables:
            return self.variables[name]
        return None


