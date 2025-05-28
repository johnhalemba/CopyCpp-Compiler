import llvmlite.ir as ir
import llvmlite.binding as llvm
from ..ast.nodes import *
from .managers import (
    ScopeManager, TypesManager, FunctionManager, GeneratorManager,
    DynamicValueManager, StringManager, BuiltinManager
)

class IRGenerator:
    def __init__(self, debug=False):
        self.debug = debug

        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create module and setup target
        self.module = ir.Module(name="CopyCppModule")
        self.builder = None

        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        self.data_layout = target_machine.target_data
        self.module.data_layout = str(self.data_layout)
        self.module.triple = llvm.get_default_triple()

        self.scope_manager = ScopeManager(debug=debug)
        self.string_manager = StringManager(self.module, debug=debug)
        self.builtin_manager = BuiltinManager(self.module, self.string_manager, debug=debug)
        self.types_manager = TypesManager(self.module, self.data_layout, debug=debug)
        self.function_manager = FunctionManager(self.module, self.types_manager, debug=debug)
        self.generator_manager = GeneratorManager(self.module, self.types_manager, self.function_manager, debug=debug)
        self.dynamic_value_manager = DynamicValueManager(self.module, self.data_layout, self.string_manager,
                                                         debug=debug)

        self.current_class_or_struct_name = None

    def log(self, message):
        if self.debug:
            print(f"DEBUG IR: {message}")

    def generate_ir(self, ast_program_node: ProgramNode):
        """Main entry point for IR generation"""
        self.log("Starting IR generation for ProgramNode.")

        self._pass1_declare_types_and_func_sigs(ast_program_node)

        main_fn = self.function_manager.get_function("main")
        if not main_fn:
            self.log("No explicit 'main' function found, declaring default main.")
            main_ty = ir.FunctionType(ir.IntType(32), [])
            main_fn = ir.Function(self.module, main_ty, name="main")
            self.function_manager.functions["main"] = main_fn
        if not main_fn.blocks:
            main_fn.append_basic_block(name="entry")
            self.log(f"Appended entry block to '{main_fn.name}'")

        self._pass2_define_aggregate_bodies_and_method_sigs(ast_program_node)
        self._pass3_generate_bodies(ast_program_node, main_fn)

        self.log("IR generation for ProgramNode completed.")
        return self.module

    def _pass1_declare_types_and_func_sigs(self, ast_program_node: ProgramNode):
        """Pass 1: Declare opaque types and global function signatures"""
        self.log("PASS 1: Declaring opaque types and global function signatures.")

        self.generator_manager.declare_generator_support_functions()

        for stmt in ast_program_node.statements:
            if isinstance(stmt, FunctionDeclNode):
                if stmt.is_generator:
                    self.generator_manager.register_generator(stmt)
                else:
                    self.function_manager.declare_function_signature(stmt)
            elif isinstance(stmt, StructDeclNode):
                self.types_manager.declare_struct_type_opaque(stmt.name)
            elif isinstance(stmt, ClassDeclNode):
                self.types_manager.declare_class_type_opaque(stmt.name, stmt.parent_class)

    def _pass2_define_aggregate_bodies_and_method_sigs(self, ast_program_node: ProgramNode):
        """Pass 2: Define aggregate bodies and method/constructor signatures"""
        self.log("PASS 2: Defining aggregate bodies and method/ctor signatures.")

        processed_classes = set()

        for _ in range(len(ast_program_node.statements)):
            newly_processed_this_iteration = False
            for stmt in ast_program_node.statements:
                if isinstance(stmt, StructDeclNode):
                    self.types_manager.define_struct_body(stmt)
                    self._declare_struct_methods(stmt)
                elif isinstance(stmt, ClassDeclNode):
                    if stmt.name not in processed_classes:
                        parent_name = stmt.parent_class
                        if not parent_name or (parent_name in self.types_manager.classes and not self.types_manager.classes[parent_name]["type"].is_opaque):
                            self.types_manager.define_class_body(stmt)
                            self._declare_class_methods_and_constructors(stmt)
                            processed_classes.add(stmt.name)
                            newly_processed_this_iteration = True

            if not newly_processed_this_iteration:
                break

        for stmt in ast_program_node.statements:
            if isinstance(stmt, ClassDeclNode) and stmt.name not in processed_classes:
                self.log(f"Warning: Class {stmt.name} might have circular dependency, attempting final definition.")
                self.types_manager.define_class_body(stmt)
                self._declare_class_methods_and_constructors(stmt)

    def _declare_struct_methods(self, node: StructDeclNode):
        """Declare method signatures for a struct"""
        struct_info = self.types_manager.structs.get(node.name)
        if struct_info:
            for method_name, method_ast in struct_info.get("methods_ast", {}).items():
                self.function_manager.declare_method_signature(node.name, method_ast)

    def _declare_class_methods_and_constructors(self, node: ClassDeclNode):
        """Declare method and constructor signatures for a class"""
        class_info = self.types_manager.classes.get(node.name)
        if class_info:
            for method_name, method_ast in class_info.get("methods_ast", {}).items():
                self.function_manager.declare_method_signature(node.name, method_ast)
            if class_info.get("ctor_ast"):
                self.function_manager.declare_constructor_signature(node.name, class_info["ctor_ast"])

    def _pass3_generate_bodies(self, ast_program_node: ProgramNode, main_fn: ir.Function):
        """Pass 3: Generate function, method, and constructor bodies"""
        self.log("PASS 3: Generating function, method, and constructor bodies.")

        if not main_fn.blocks:
            main_fn.append_basic_block(name="entry_pass3")
            self.log(f"Appended entry block to '{main_fn.name}' in Pass 3")

        original_builder, original_function = self.builder, self.function_manager.get_current_function()

        # Generate function bodies
        for stmt in ast_program_node.statements:
            if isinstance(stmt, FunctionDeclNode):
                self.generate_function_declaration(stmt)
            elif isinstance(stmt, StructDeclNode):
                self._generate_struct_method_bodies(stmt)
            elif isinstance(stmt, ClassDeclNode):
                self._generate_class_method_and_ctor_bodies(stmt)

        # Generate main function body with global statements
        self.builder = ir.IRBuilder(main_fn.blocks[-1])
        self.function_manager.set_current_function(main_fn)

        for stmt in ast_program_node.statements:
            if not isinstance(stmt, (FunctionDeclNode, StructDeclNode, ClassDeclNode)):
                if self.builder.block.is_terminated:
                    self.log("Main's current block is terminated. Appending new block for global statements.")
                    new_block = main_fn.append_basic_block(name=f"global_cont_{len(main_fn.blocks)}")
                    self.builder.position_at_end(new_block)
                self.generate_statement(stmt)

        if self.builder and self.builder.block.parent == main_fn and not self.builder.block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))

        self.builder, original_function = original_builder, original_function
        self.function_manager.set_current_function(original_function)

    def _generate_struct_method_bodies(self, node: StructDeclNode):
        """Generate method bodies for a struct"""
        struct_info = self.types_manager.structs.get(node.name)
        if struct_info:
            for method_name, method_ast in struct_info.get("methods_ast", {}).items():
                self._generate_method_body(node.name, method_ast, is_struct=True)

    def _generate_class_method_and_ctor_bodies(self, node: ClassDeclNode):
        """Generate method and constructor bodies for a class"""
        class_info = self.types_manager.classes.get(node.name)
        if class_info:
            for method_name, method_ast in class_info.get("methods_ast", {}).items():
                self._generate_method_body(node.name, method_ast, is_struct=False)
            if class_info.get("ctor_ast"):
                self._generate_constructor_body(node.name, class_info["ctor_ast"])

    def generate_function_declaration(self, node: FunctionDeclNode):
        """Generate a function declaration"""
        if node.is_generator:
            self.log(f"Generating generator function: {node.name}")
            self._generate_complete_generator(node)
        else:
            self.log(f"Generating regular function: {node.name}")
            func = self.function_manager.get_function(node.name)
            if not func:
                self.log(f"ERROR: Function {node.name} not declared")
                return

            if func.blocks and func.entry_basic_block.instructions:
                self.log(f"Function {node.name} body already exists")
                return

            entry_block = func.append_basic_block(name="entry")
            prev_builder, prev_function = self.builder, self.function_manager.get_current_function()
            self.builder, self.function_manager.current_function = ir.IRBuilder(entry_block), func

            self.scope_manager.push_scope()

            # Add parameters to scope
            for i, param_info in enumerate(node.params):
                param_name = param_info['name']
                param_type = param_info['type']
                param_dims = param_info['dimensions']

                llvm_arg = func.args[i]
                param_alloca = self.builder.alloca(llvm_arg.type, name=param_name)
                self.builder.store(llvm_arg, param_alloca)
                self.scope_manager.add_variable(param_name, param_alloca, param_type,
                                                bool(param_dims), param_dims, True)

            # Generate function body
            self.generate_statement(node.body)

            # Add return if missing
            if not self.builder.block.is_terminated:
                if func.return_value.type == ir.VoidType():
                    self.builder.ret_void()
                else:
                    default_ret = self._get_default_return_value(func.return_value.type)
                    if default_ret is not None:
                        self.builder.ret(default_ret)

            self.scope_manager.pop_scope()
            self.builder, self.function_manager.current_function = prev_builder, prev_function

    # ===== GENERATOR IMPLEMENTATION =====

    def _generate_complete_generator(self, node: FunctionDeclNode):
        """Generate a complete generator implementation"""
        self.log(f"=== GENERATOR IMPL: Starting full implementation for '{node.name}' ===")

        gen_info = self.generator_manager.get_generator_info(node.name)
        if not gen_info:
            self.log(f"ERROR: Generator {node.name} not registered")
            return

        # Create constructor and step function
        self._create_generator_constructor(node, gen_info)
        self._create_generator_step_function(node, gen_info)

        # Make the generator function point to the constructor
        constructor_name = f"__{node.name}_create"
        if constructor_name in self.function_manager.functions:
            self.function_manager.functions[node.name] = self.function_manager.functions[constructor_name]

        self.log(f"=== GENERATOR IMPL: '{node.name}' implementation completed ===")

    def _create_generator_constructor(self, node: FunctionDeclNode, gen_info):
        """Create the function that creates and initializes a generator object"""
        constructor_name = f"__{node.name}_create"
        self.log(f"=== GENERATOR CONSTRUCTOR: Creating '{constructor_name}' ===")

        gen_obj_type = gen_info['obj_type_info']['type']
        param_types = gen_info['param_types']

        constructor_type = ir.FunctionType(ir.PointerType(gen_obj_type), param_types)
        constructor_func = ir.Function(self.module, constructor_type, name=constructor_name)
        self.function_manager.functions[constructor_name] = constructor_func

        entry_block = constructor_func.append_basic_block(name="entry")
        prev_builder, prev_function = self.builder, self.function_manager.get_current_function()
        self.builder, self.function_manager.current_function = ir.IRBuilder(entry_block), constructor_func

        # Allocate memory for generator object
        obj_size = gen_obj_type.get_abi_size(self.data_layout)
        size_const = ir.Constant(self.types_manager.size_t_type, obj_size)
        malloc_func = self.builtin_manager.get_function("malloc")
        raw_mem = self.builder.call(malloc_func, [size_const])
        gen_obj_ptr = self.builder.bitcast(raw_mem, ir.PointerType(gen_obj_type), name="gen_obj")

        # Initialize generator object fields
        # Field 0: state (CREATED = 0)
        state_ptr = self.builder.gep(gen_obj_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        self.builder.store(ir.Constant(ir.IntType(32), 0), state_ptr)

        # Field 1: yield_point (0)
        yield_point_ptr = self.builder.gep(gen_obj_ptr,
                                           [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 1)])
        self.builder.store(ir.Constant(ir.IntType(32), 0), yield_point_ptr)

        # Field 2: last_yielded_value (default)
        value_ptr = self.builder.gep(gen_obj_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 2)])
        default_val = self._get_default_return_value(gen_info['yield_type'])
        if default_val:
            self.builder.store(default_val, value_ptr)

        # Fields 3+: parameters
        for i, param_arg in enumerate(constructor_func.args):
            param_ptr = self.builder.gep(gen_obj_ptr,
                                         [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 3 + i)])
            self.builder.store(param_arg, param_ptr)

        # Initialize local variables to default values
        for i, (var_name, var_type) in enumerate(
                zip(gen_info['local_var_names'], gen_info['local_var_types'].values())):
            var_ptr = self.builder.gep(gen_obj_ptr, [
                ir.Constant(ir.IntType(32), 0),
                ir.Constant(ir.IntType(32), gen_info['local_var_offset'] + i)
            ])
            # Initialize to default value
            if isinstance(var_type, ir.IntType):
                default_val = ir.Constant(var_type, 0)
            elif isinstance(var_type, (ir.FloatType, ir.DoubleType)):
                default_val = ir.Constant(var_type, 0.0)
            elif isinstance(var_type, ir.PointerType):
                default_val = ir.Constant(var_type, None)
            else:
                continue  # Skip unsupported types

            self.builder.store(default_val, var_ptr)
            self.log(
                f"GENERATOR CONSTRUCTOR: Initialized local var '{var_name}' at offset {gen_info['local_var_offset'] + i}")

        self.builder.ret(gen_obj_ptr)
        self.builder, self.function_manager.current_function = prev_builder, prev_function

        self.log(f"=== GENERATOR CONSTRUCTOR: '{constructor_name}' completed ===")

    def _create_generator_step_function(self, node: FunctionDeclNode, gen_info):
        """Create the generator step function (state machine)"""
        step_func_name = f"__{node.name}_step"
        self.log(f"=== GENERATOR STEP: Creating state machine '{step_func_name}' ===")

        gen_obj_type = gen_info['obj_type_info']['type']
        step_func_type = ir.FunctionType(ir.IntType(1), [ir.PointerType(gen_obj_type)])
        step_func = ir.Function(self.module, step_func_type, name=step_func_name)
        self.function_manager.functions[step_func_name] = step_func

        entry_block = step_func.append_basic_block(name="entry")
        prev_builder, prev_function = self.builder, self.function_manager.get_current_function()
        prev_gen_ctx = self.generator_manager.get_current_generator_context()

        self.builder, self.function_manager.current_function = ir.IRBuilder(entry_block), step_func
        gen_obj_ptr = step_func.args[0]

        # PRE-ALLOCATE ALL VARIABLES IN ENTRY BLOCK
        param_allocas = {}
        local_var_allocas = {}

        # Allocate space for all parameters
        for i, param_info in enumerate(node.params):
            param_type = self.types_manager.get_llvm_type(param_info['type'])
            param_alloca = self.builder.alloca(param_type, name=param_info['name'])
            param_allocas[param_info['name']] = param_alloca

        # Pre-allocate space for local variables
        for var_name, var_type in gen_info['local_var_types'].items():
            var_alloca = self.builder.alloca(var_type, name=var_name)
            local_var_allocas[var_name] = var_alloca

        # ALWAYS RESTORE PARAMETERS AND LOCAL VARIABLES AT THE START
        # Restore parameters
        for i, param_info in enumerate(node.params):
            param_ptr_in_obj = self.builder.gep(gen_obj_ptr,
                                                [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 3 + i)])
            param_value = self.builder.load(param_ptr_in_obj, name=f"param_{param_info['name']}")
            param_alloca = param_allocas[param_info['name']]
            self.builder.store(param_value, param_alloca)

        # Restore local variables
        for i, var_name in enumerate(gen_info['local_var_names']):
            var_ptr_in_obj = self.builder.gep(gen_obj_ptr, [
                ir.Constant(ir.IntType(32), 0),
                ir.Constant(ir.IntType(32), gen_info['local_var_offset'] + i)
            ])
            var_value = self.builder.load(var_ptr_in_obj, name=f"restored_{var_name}")
            var_alloca = local_var_allocas[var_name]
            self.builder.store(var_value, var_alloca)

        # Get state and yield point
        state_ptr = self.builder.gep(gen_obj_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        current_state = self.builder.load(state_ptr, name="current_state")
        yield_point_ptr = self.builder.gep(gen_obj_ptr,
                                           [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 1)])
        current_yield_point = self.builder.load(yield_point_ptr, name="current_yield_point")

        check_completed_block = step_func.append_basic_block(f"{node.name}_check_completed")
        dispatch_block = step_func.append_basic_block(f"{node.name}_dispatch_yield")
        generator_completed_block = step_func.append_basic_block(f"{node.name}_completed")
        initial_run_block = step_func.append_basic_block(f"{node.name}_initial_run")

        self.builder.branch(check_completed_block)

        self.builder.position_at_end(check_completed_block)
        is_completed = self.builder.icmp_signed("==", current_state, ir.Constant(ir.IntType(32), 3))
        self.builder.cbranch(is_completed, generator_completed_block, dispatch_block)

        # DISPATCH BLOCK - Use switch instruction only
        self.builder.position_at_end(dispatch_block)
        switch_inst = self.builder.switch(current_yield_point, initial_run_block)

        # Set up scope with all variables in initial_run_block
        self.builder.position_at_end(initial_run_block)
        self.scope_manager.push_scope()

        # Add all parameters to scope
        for i, param_info in enumerate(node.params):
            param_alloca = param_allocas[param_info['name']]
            self.scope_manager.add_variable(param_info['name'], param_alloca, param_info['type'],
                                            bool(param_info['dimensions']), param_info['dimensions'], True)

        # Set generator context
        self.generator_manager.set_current_generator_context({
            'obj_ptr': gen_obj_ptr, 'obj_info': gen_info, 'node': node,
            'yield_points_blocks': [], 'step_func': step_func,
            'completed_block': generator_completed_block, 'dispatch_block': dispatch_block,
            'local_var_allocas': local_var_allocas,
            'current_yield_point': current_yield_point
        })

        # Generate the body - this will create resume points based on yields
        resume_blocks_map = self._generate_generator_body_with_yields(node.body)

        # Add cases to the switch instruction for each yield point
        for yield_idx, block_target in resume_blocks_map.items():
            if yield_idx > 0:
                switch_inst.add_case(ir.Constant(ir.IntType(32), yield_idx), block_target)

        self.scope_manager.pop_scope()

        # Completed Block
        self.builder.position_at_end(generator_completed_block)
        if not generator_completed_block.is_terminated:
            self.builder.store(ir.Constant(ir.IntType(32), 3), state_ptr)
            self.builder.ret(ir.Constant(ir.IntType(1), 0))

        self.builder, self.function_manager.current_function = prev_builder, prev_function
        self.generator_manager.set_current_generator_context(prev_gen_ctx)
        self.log(f"=== GENERATOR STEP: '{step_func_name}' completed ===")

    def _analyze_generator_locals(self, body_node):
        """Analyze the generator body to determine what local variables are needed"""
        local_vars = {}

        def analyze_node(node):
            if isinstance(node, VarDeclarationNode):
                local_vars[node.var_name] = node.type_name
            elif isinstance(node, BlockNode):
                for stmt in node.statements:
                    analyze_node(stmt)
            elif isinstance(node, IfStatementNode):
                analyze_node(node.then_branch)
                if node.else_branch:
                    analyze_node(node.else_branch)
            elif isinstance(node, WhileStatementNode):
                analyze_node(node.body)
            elif isinstance(node, ForStatementNode):
                if node.init:
                    analyze_node(node.init)
                analyze_node(node.body)
            # Add other node types as needed

        if isinstance(body_node, BlockNode):
            for stmt in body_node.statements:
                analyze_node(stmt)
        else:
            analyze_node(body_node)

        return local_vars

    def _generate_generator_body_with_yields(self, body_node):
        """Generate generator body with yield handling"""
        self.log(f"GENERATOR BODY: Generating body with yield handling")

        gen_ctx = self.generator_manager.get_current_generator_context()
        if not gen_ctx:
            raise Exception("Generator context not set for body generation")

        resume_blocks_map = {}

        current_segment_start_block = self.builder.block
        resume_blocks_map[0] = current_segment_start_block

        gen_ctx['yield_points_blocks'] = []

        def process_statements_recursively(statements_list):
            for stmt_idx, stmt_node in enumerate(statements_list):
                if self.builder.block.is_terminated:
                    self.log(f"GENERATOR BODY: Block terminated before statement {stmt_idx}")
                    return

                if isinstance(stmt_node, YieldStatementNode):
                    new_block_after_yield = self.generate_yield_statement(stmt_node)
                    stored_yield_id = len(gen_ctx['yield_points_blocks'])
                    resume_blocks_map[stored_yield_id] = new_block_after_yield

                elif isinstance(stmt_node, BlockNode):
                    self.scope_manager.push_scope()
                    process_statements_recursively(stmt_node.statements)
                    self.scope_manager.pop_scope()

                elif isinstance(stmt_node, IfStatementNode):
                    self._generate_if_in_generator(stmt_node, gen_ctx, process_statements_recursively)

                elif isinstance(stmt_node, WhileStatementNode):
                    self._generate_while_in_generator(stmt_node, gen_ctx, process_statements_recursively)

                elif isinstance(stmt_node, ForStatementNode):
                    self._generate_for_in_generator(stmt_node, gen_ctx, process_statements_recursively)

                else:
                    self.generate_statement(stmt_node)

        if isinstance(body_node, BlockNode):
            process_statements_recursively(body_node.statements)
        else:
            process_statements_recursively([body_node])

        if self.builder.block and not self.builder.block.is_terminated:
            self.builder.branch(gen_ctx['completed_block'])

        return resume_blocks_map

    def _generate_if_in_generator(self, stmt_node, gen_ctx, process_func):
        """Generate if statement in generator context"""
        condition_val = self.generate_expr(stmt_node.condition)
        if condition_val.type != ir.IntType(1):
            condition_val = self.builder.icmp_signed("!=", condition_val, ir.Constant(condition_val.type, 0))

        unique_suffix = f"{gen_ctx['node'].name}_if_{len(gen_ctx['yield_points_blocks'])}"
        then_block = gen_ctx['step_func'].append_basic_block(f"then_{unique_suffix}")
        merge_block = gen_ctx['step_func'].append_basic_block(f"merge_{unique_suffix}")

        if stmt_node.else_branch:
            else_block = gen_ctx['step_func'].append_basic_block(f"else_{unique_suffix}")
            self.builder.cbranch(condition_val, then_block, else_block)
        else:
            self.builder.cbranch(condition_val, then_block, merge_block)

        # Then branch
        self.builder.position_at_end(then_block)
        self.scope_manager.push_scope()
        process_func([stmt_node.then_branch])
        self.scope_manager.pop_scope()
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)

        # Else branch
        if stmt_node.else_branch:
            self.builder.position_at_end(else_block)
            self.scope_manager.push_scope()
            process_func([stmt_node.else_branch])
            self.scope_manager.pop_scope()
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)

        self.builder.position_at_end(merge_block)

    def _generate_while_in_generator(self, stmt_node, gen_ctx, process_func):
        """Generate while statement in generator context"""
        unique_suffix = f"{gen_ctx['node'].name}_while_{len(gen_ctx['yield_points_blocks'])}"
        loop_header = gen_ctx['step_func'].append_basic_block(f"header_{unique_suffix}")
        loop_body = gen_ctx['step_func'].append_basic_block(f"body_{unique_suffix}")
        loop_exit = gen_ctx['step_func'].append_basic_block(f"exit_{unique_suffix}")

        self.builder.branch(loop_header)

        self.builder.position_at_end(loop_header)
        condition_val = self.generate_expr(stmt_node.condition)
        if condition_val.type != ir.IntType(1):
            condition_val = self.builder.icmp_signed("!=", condition_val, ir.Constant(condition_val.type, 0))
        self.builder.cbranch(condition_val, loop_body, loop_exit)

        self.builder.position_at_end(loop_body)
        self.scope_manager.push_scope()
        process_func([stmt_node.body])
        self.scope_manager.pop_scope()
        if not self.builder.block.is_terminated:
            self.builder.branch(loop_header)

        self.builder.position_at_end(loop_exit)

    def _generate_for_in_generator(self, stmt_node, gen_ctx, process_func):
        """Generate for statement in generator context"""
        self.scope_manager.push_scope()

        if stmt_node.init:
            self.generate_statement(stmt_node.init)

        unique_suffix = f"{gen_ctx['node'].name}_for_{len(gen_ctx['yield_points_blocks'])}"
        cond_block = gen_ctx['step_func'].append_basic_block(f"cond_{unique_suffix}")
        body_block = gen_ctx['step_func'].append_basic_block(f"body_{unique_suffix}")
        update_block = gen_ctx['step_func'].append_basic_block(f"update_{unique_suffix}")
        exit_block = gen_ctx['step_func'].append_basic_block(f"exit_{unique_suffix}")

        self.builder.branch(cond_block)

        self.builder.position_at_end(cond_block)
        cond_val = self.generate_expr(stmt_node.condition)
        if cond_val.type != ir.IntType(1):
            cond_val = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))
        self.builder.cbranch(cond_val, body_block, exit_block)

        self.builder.position_at_end(body_block)
        self.scope_manager.push_scope()
        process_func([stmt_node.body])
        self.scope_manager.pop_scope()
        if not self.builder.block.is_terminated:
            self.builder.branch(update_block)

        self.builder.position_at_end(update_block)
        if stmt_node.update:
            self.generate_expr(stmt_node.update)
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_block)

        self.builder.position_at_end(exit_block)
        self.scope_manager.pop_scope()

    def generate_yield_statement(self, node: YieldStatementNode):
        """Generate yield statement in generator"""
        gen_ctx = self.generator_manager.get_current_generator_context()
        if not gen_ctx:
            self.log(f"ERROR: Yield statement outside generator context!")
            if node.value:
                self.generate_expr(node.value)
            return self.builder.block

        self.log(f"=== GENERATOR YIELD: Processing yield statement ===")

        gen_obj_ptr = gen_ctx['obj_ptr']
        step_func = gen_ctx['step_func']
        gen_info = gen_ctx['obj_info']

        # SAVE ALL LOCAL VARIABLES BEFORE YIELDING
        for i, var_name in enumerate(gen_info['local_var_names']):
            var_info = self.scope_manager.lookup_variable(var_name)
            if var_info:
                var_ptr, _, _, _, _ = var_info
                var_value = self.builder.load(var_ptr)
                var_ptr_in_obj = self.builder.gep(gen_obj_ptr, [
                    ir.Constant(ir.IntType(32), 0),
                    ir.Constant(ir.IntType(32), gen_info['local_var_offset'] + i)
                ])
                self.builder.store(var_value, var_ptr_in_obj)
                self.log(f"GENERATOR YIELD: Saved local var '{var_name}' to offset {gen_info['local_var_offset'] + i}")

        # Generate yield value
        yield_value = self.generate_expr(node.value)

        # Store yield value in generator object
        value_ptr = self.builder.gep(gen_obj_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 2)])
        converted_value = self._convert_value_to_type(yield_value, value_ptr.type.pointee)
        self.builder.store(converted_value, value_ptr)

        # Set next yield point
        next_resume_yield_point_id = len(gen_ctx['yield_points_blocks']) + 1
        yield_point_ptr = self.builder.gep(gen_obj_ptr,
                                           [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 1)])
        self.builder.store(ir.Constant(ir.IntType(32), next_resume_yield_point_id), yield_point_ptr)

        # Set state to SUSPENDED
        state_ptr = self.builder.gep(gen_obj_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        self.builder.store(ir.Constant(ir.IntType(32), 2), state_ptr)  # SUSPENDED = 2

        # Return true (has value)
        self.builder.ret(ir.Constant(ir.IntType(1), 1))

        # Create resume block
        resume_block_name = f"{gen_ctx['node'].name}_resume_at_{next_resume_yield_point_id}"
        resume_block = step_func.append_basic_block(resume_block_name)
        gen_ctx['yield_points_blocks'].append(resume_block)
        self.builder.position_at_end(resume_block)

        # RESTORE ALL LOCAL VARIABLES WHEN RESUMING
        for i, var_name in enumerate(gen_info['local_var_names']):
            var_info = self.scope_manager.lookup_variable(var_name)
            if var_info:
                var_ptr, _, _, _, _ = var_info
                var_ptr_in_obj = self.builder.gep(gen_obj_ptr, [
                    ir.Constant(ir.IntType(32), 0),
                    ir.Constant(ir.IntType(32), gen_info['local_var_offset'] + i)
                ])
                var_value = self.builder.load(var_ptr_in_obj)
                self.builder.store(var_value, var_ptr)
                self.log(
                    f"GENERATOR YIELD: Restored local var '{var_name}' from offset {gen_info['local_var_offset'] + i}")

        return resume_block

    # ===== METHOD GENERATION =====

    def _generate_method_body(self, owner_name: str, method_node: FunctionDeclNode, is_struct: bool):
        """Generate method body for struct or class"""
        mangled_name = f"{owner_name}_{method_node.name}"
        method_func = self.function_manager.get_function(mangled_name)

        if not method_func or (method_func.blocks and method_func.entry_basic_block.instructions):
            return

        entry_block = method_func.append_basic_block(name="entry")
        prev_builder, prev_function = self.builder, self.function_manager.get_current_function()
        prev_context = self.current_class_or_struct_name

        self.builder = ir.IRBuilder(entry_block)
        self.function_manager.current_function = method_func
        self.current_class_or_struct_name = owner_name

        self.scope_manager.push_scope()

        # Add 'this' parameter
        if is_struct:
            this_type = self.types_manager.structs[owner_name]["type"]
        else:
            this_type = self.types_manager.classes[owner_name]["type"]

        this_alloca = self.builder.alloca(ir.PointerType(this_type), name="this")
        self.builder.store(method_func.args[0], this_alloca)
        self.scope_manager.add_variable("this", this_alloca, owner_name, False, None, True)

        # Add method parameters
        for i, param_info in enumerate(method_node.params):
            param_name = param_info['name']
            param_type = param_info['type']
            param_dims = param_info['dimensions']

            llvm_arg = method_func.args[i + 1]
            param_alloca = self.builder.alloca(llvm_arg.type, name=param_name)
            self.builder.store(llvm_arg, param_alloca)
            self.scope_manager.add_variable(param_name, param_alloca, param_type,
                                            bool(param_dims), param_dims, True)

        # Generate method body
        self.generate_statement(method_node.body)

        # Add return if missing
        if not self.builder.block.is_terminated:
            if method_func.return_value.type == ir.VoidType():
                self.builder.ret_void()
            else:
                default_ret = self._get_default_return_value(method_func.return_value.type)
                if default_ret is not None:
                    self.builder.ret(default_ret)

        self.scope_manager.pop_scope()
        self.builder, self.function_manager.current_function = prev_builder, prev_function
        self.current_class_or_struct_name = prev_context

    def _generate_constructor_body(self, class_name: str, ctor_node: ConstructorDeclNode):
        """Generate constructor body for a class"""
        ctor_func = self.function_manager.get_constructor(class_name)

        if not ctor_func or (ctor_func.blocks and ctor_func.entry_basic_block.instructions):
            return

        entry_block = ctor_func.append_basic_block(name="entry")
        prev_builder, prev_function = self.builder, self.function_manager.get_current_function()
        prev_context = self.current_class_or_struct_name

        self.builder = ir.IRBuilder(entry_block)
        self.function_manager.current_function = ctor_func
        self.current_class_or_struct_name = class_name

        self.scope_manager.push_scope()

        # Add 'this' parameter
        class_type = self.types_manager.classes[class_name]["type"]
        this_alloca = self.builder.alloca(ir.PointerType(class_type), name="this")
        self.builder.store(ctor_func.args[0], this_alloca)
        self.scope_manager.add_variable("this", this_alloca, class_name, False, None, True)

        # Add constructor parameters
        for i, param_info in enumerate(ctor_node.params):
            param_name = param_info['name']
            param_type = param_info['type']
            param_dims = param_info['dimensions']

            llvm_arg = ctor_func.args[i + 1]
            param_alloca = self.builder.alloca(llvm_arg.type, name=param_name)
            self.builder.store(llvm_arg, param_alloca)
            self.scope_manager.add_variable(param_name, param_alloca, param_type,
                                            bool(param_dims), param_dims, True)

        # Generate constructor body
        self.generate_statement(ctor_node.body)

        if not self.builder.block.is_terminated:
            self.builder.ret_void()

        self.scope_manager.pop_scope()
        self.builder, self.function_manager.current_function = prev_builder, prev_function
        self.current_class_or_struct_name = prev_context

    # ===== STATEMENT GENERATION =====

    def generate_statement(self, stmt_node: StatementNode):
        """Generate code for a statement"""
        if not self.builder:
            self.log(f"ERROR: Builder is None for statement: {type(stmt_node).__name__}")
            return

        stmt_type_name = type(stmt_node).__name__
        self.log(f"Generating statement: {stmt_type_name}")

        if isinstance(stmt_node, VarDeclarationNode):
            self.generate_var_declaration(stmt_node)
        elif isinstance(stmt_node, AssignmentNode):
            self.generate_assignment(stmt_node)
        elif isinstance(stmt_node, IfStatementNode):
            self.generate_if_statement(stmt_node)
        elif isinstance(stmt_node, WhileStatementNode):
            self.generate_while_statement(stmt_node)
        elif isinstance(stmt_node, ForStatementNode):
            self.generate_for_statement(stmt_node)
        elif isinstance(stmt_node, ForeachStatementNode):
            self.generate_foreach_statement(stmt_node)
        elif isinstance(stmt_node, FunctionCallStatementNode):
            self.generate_expr(stmt_node.function_call)
        elif isinstance(stmt_node, ReturnStatementNode):
            self.generate_return_statement(stmt_node)
        elif isinstance(stmt_node, PrintStatementNode):
            self.generate_print_statement(stmt_node)
        elif isinstance(stmt_node, YieldStatementNode):
            self.generate_yield_statement(stmt_node)
        elif isinstance(stmt_node, ReadStatementNode):
            self.generate_read_statement(stmt_node)
        elif isinstance(stmt_node, BlockNode):
            self.scope_manager.push_scope()
            for s_in_block in stmt_node.statements:
                if self.builder.block.is_terminated:
                    break
                self.generate_statement(s_in_block)
            self.scope_manager.pop_scope()
        elif isinstance(stmt_node, ExprNode):
            self.generate_expr(stmt_node)
        else:
            self.log(f"WARNING: Unknown statement type: {stmt_type_name}")

    def generate_var_declaration(self, node: VarDeclarationNode):
        """Generate variable declaration"""
        self.log(f"Declaring var: {node.var_name} type {node.type_name}")

        if node.dimensions:
            # Array declaration
            self._generate_array_declaration(node)
        else:
            # Scalar declaration
            self._generate_scalar_declaration(node)

    def _generate_array_declaration(self, node: VarDeclarationNode):
        """Generate array declaration"""
        base_elem_type = self.types_manager.get_llvm_type(node.type_name)
        total_elements_llvm = ir.Constant(self.types_manager.size_t_type, 1)

        for dim_ast in node.dimensions:
            dim_size_llvm = self.generate_expr(dim_ast)
            dim_size_llvm = self._convert_value_to_type(dim_size_llvm, self.types_manager.size_t_type)
            total_elements_llvm = self.builder.mul(total_elements_llvm, dim_size_llvm)

        elem_size = base_elem_type.get_abi_size(self.data_layout)
        total_bytes_llvm = self.builder.mul(total_elements_llvm,
                                            ir.Constant(self.types_manager.size_t_type, elem_size))

        malloc_func = self.builtin_manager.get_function("malloc")
        raw_memory_ptr = self.builder.call(malloc_func, [total_bytes_llvm], name=f"{node.var_name}_rawmem")
        array_ptr = self.builder.bitcast(raw_memory_ptr, ir.PointerType(base_elem_type),
                                         name=f"{node.var_name}_ptr")

        self.scope_manager.add_variable(node.var_name, array_ptr, node.type_name,
                                        is_array=True, dimensions_ast=node.dimensions)

    def _generate_scalar_declaration(self, node: VarDeclarationNode):
        """Generate scalar variable declaration"""
        gen_ctx = self.generator_manager.get_current_generator_context()

        # Check if we're in a generator and have pre-allocated storage
        if gen_ctx and 'local_var_allocas' in gen_ctx and node.var_name in gen_ctx['local_var_allocas']:
            var_ptr = gen_ctx['local_var_allocas'][node.var_name]
            gen_info = gen_ctx['obj_info']

            # Check if this variable needs to be restored from generator object
            if node.var_name in gen_info['local_var_names']:
                var_index = gen_info['local_var_names'].index(node.var_name)
                var_ptr_in_obj = self.builder.gep(gen_ctx['obj_ptr'], [
                    ir.Constant(ir.IntType(32), 0),
                    ir.Constant(ir.IntType(32), gen_info['local_var_offset'] + var_index)
                ])
                restored_value = self.builder.load(var_ptr_in_obj)
                self.builder.store(restored_value, var_ptr)
                self.log(f"GENERATOR VAR DECL: Restored '{node.var_name}' from generator object")

            if node.initial_value:
                initial_llvm_val = self.generate_expr(node.initial_value)
                converted_val = self._convert_value_to_type(initial_llvm_val, var_ptr.type.pointee)
                self.builder.store(converted_val, var_ptr)
        else:
            # Normal non-generator variable declaration
            if node.type_name == "var":
                # Dynamic typing
                dyn_type = self.dynamic_value_manager.get_dynamic_value_type()
                var_ptr = self.builder.alloca(dyn_type, name=node.var_name)

                if node.initial_value:
                    malloc_func = self.builtin_manager.get_function("malloc")
                    dyn_obj = self.dynamic_value_manager.create_dynamic_value_object(
                        self.builder, node.initial_value, malloc_func)
                    self.builder.store(dyn_obj, var_ptr)
                else:
                    # Initialize to null
                    malloc_func = self.builtin_manager.get_function("malloc")
                    null_obj = self.dynamic_value_manager.create_dynamic_value_object(
                        self.builder, NullLiteralNode(), malloc_func)
                    self.builder.store(null_obj, var_ptr)
            else:
                # Static typing
                llvm_type = self.types_manager.get_llvm_type(node.type_name)
                var_ptr = self.builder.alloca(llvm_type, name=node.var_name)

                if node.initial_value:
                    initial_llvm_val = self.generate_expr(node.initial_value)
                    converted_val = self._convert_value_to_type(initial_llvm_val, llvm_type)
                    self.builder.store(converted_val, var_ptr)

        self.scope_manager.add_variable(node.var_name, var_ptr, node.type_name, is_array=False)
    def generate_assignment(self, node: AssignmentNode):
        """Generate assignment statement"""
        self.log(f"Generating assignment to {type(node.target).__name__}")

        value_llvm = self.generate_expr(node.value)

        if isinstance(node.target, VarReferenceNode):
            self._generate_var_assignment(node.target, value_llvm, node.value)
        elif isinstance(node.target, ArrayAccessNode):
            self._generate_array_assignment(node.target, value_llvm)
        elif isinstance(node.target, FieldAccessNode):
            self._generate_field_assignment(node.target, value_llvm)
        else:
            raise TypeError(f"Invalid target for assignment: {type(node.target).__name__}")

    def _generate_var_assignment(self, target, value_llvm, value_ast):
        """Generate variable assignment"""
        var_name = target.name
        var_info = self.scope_manager.lookup_variable(var_name)

        if var_info:
            var_ptr, type_name_str, _, _, _ = var_info

            if type_name_str == "var":
                # Dynamic variable assignment
                old_dyn_obj_ptr = self.builder.load(var_ptr)
                # Free old object (optional optimization)
                # TODO: Add reference counting or GC

                malloc_func = self.builtin_manager.get_function("malloc")
                new_dyn_obj_ptr = self.dynamic_value_manager.create_dynamic_value_object(
                    self.builder, value_ast, malloc_func)
                self.builder.store(new_dyn_obj_ptr, var_ptr)
            else:
                # Static variable assignment
                converted_value = self._convert_value_to_type(value_llvm, var_ptr.type.pointee)
                self.builder.store(converted_value, var_ptr)

        elif self.current_class_or_struct_name:
            # Check if it's a field of 'this'
            this_var_info = self.scope_manager.lookup_variable("this")
            if this_var_info:
                self._assign_to_this_field(var_name, value_llvm, this_var_info)
            else:
                raise NameError(f"Variable '{var_name}' not defined for assignment")
        else:
            raise NameError(f"Variable '{var_name}' not defined for assignment")

    def _assign_to_this_field(self, field_name, value_llvm, this_var_info):
        """Assign to a field of 'this'"""
        this_ptr_alloca, owner_type_name, _, _, _ = this_var_info
        actual_this_obj_ptr = self.builder.load(this_ptr_alloca, name="this_obj_ptr")

        if owner_type_name in self.types_manager.structs:
            type_info = self.types_manager.structs[owner_type_name]
        elif owner_type_name in self.types_manager.classes:
            type_info = self.types_manager.classes[owner_type_name]
        else:
            raise NameError(f"Type '{owner_type_name}' not found")

        if field_name not in type_info["field_names"]:
            raise AttributeError(f"Field '{field_name}' not found in '{owner_type_name}'")

        field_idx = type_info["field_names"].index(field_name)
        field_ptr = self.builder.gep(actual_this_obj_ptr,
                                     [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), field_idx)])
        converted_value = self._convert_value_to_type(value_llvm, field_ptr.type.pointee)
        self.builder.store(converted_value, field_ptr)

    def _generate_array_assignment(self, target, value_llvm):
        """Generate array element assignment"""
        array_name = target.array.name
        var_info = self.scope_manager.lookup_variable(array_name)

        if not var_info:
            raise NameError(f"Array '{array_name}' not defined")

        array_ptr, _, is_array, declared_dims_ast, _ = var_info
        if not is_array:
            raise TypeError(f"'{array_name}' is not an array")

        indices_llvm = [self.generate_expr(idx_ast) for idx_ast in target.indices]

        if len(indices_llvm) == 1:
            # 1D array access
            idx0 = self._convert_value_to_type(indices_llvm[0], self.types_manager.size_t_type)
            element_ptr = self.builder.gep(array_ptr, [idx0])
        elif len(indices_llvm) == 2 and declared_dims_ast and len(declared_dims_ast) >= 2:
            # 2D array access (row-major order)
            cols_llvm = self.generate_expr(declared_dims_ast[1])
            cols_llvm = self._convert_value_to_type(cols_llvm, self.types_manager.size_t_type)
            idx0 = self._convert_value_to_type(indices_llvm[0], self.types_manager.size_t_type)
            idx1 = self._convert_value_to_type(indices_llvm[1], self.types_manager.size_t_type)
            linear_idx = self.builder.add(self.builder.mul(idx0, cols_llvm), idx1)
            element_ptr = self.builder.gep(array_ptr, [linear_idx])
        else:
            raise NotImplementedError("Unsupported array dimensionality for assignment")

        converted_value = self._convert_value_to_type(value_llvm, element_ptr.type.pointee)
        self.builder.store(converted_value, element_ptr)

    def _generate_field_assignment(self, target, value_llvm):
        """Generate field assignment"""
        obj_llvm_ptr = self.generate_expr(target.object_expr)
        field_name = target.field_name

        if not isinstance(obj_llvm_ptr.type, ir.PointerType) or \
                not isinstance(obj_llvm_ptr.type.pointee, ir.IdentifiedStructType):
            raise TypeError(f"Cannot access field '{field_name}' on non-struct/class type")

        struct_qname = obj_llvm_ptr.type.pointee.name
        type_name_simple = struct_qname.split('.', 1)[1]

        if type_name_simple in self.types_manager.structs:
            type_info = self.types_manager.structs[type_name_simple]
        elif type_name_simple in self.types_manager.classes:
            type_info = self.types_manager.classes[type_name_simple]
        else:
            raise NameError(f"Type '{type_name_simple}' not found")

        if field_name not in type_info["field_names"]:
            raise AttributeError(f"Field '{field_name}' not found in '{type_name_simple}'")

        field_idx = type_info["field_names"].index(field_name)
        field_ptr = self.builder.gep(obj_llvm_ptr,
                                     [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), field_idx)])
        converted_value = self._convert_value_to_type(value_llvm, field_ptr.type.pointee)
        self.builder.store(converted_value, field_ptr)

    def generate_if_statement(self, node: IfStatementNode):
        """Generate if statement"""
        condition_val = self.generate_expr(node.condition)
        if condition_val.type != ir.IntType(1):
            condition_val = self.builder.icmp_signed("!=", condition_val, ir.Constant(condition_val.type, 0))

        then_block = self.function_manager.get_current_function().append_basic_block(name="then")
        merge_block = self.function_manager.get_current_function().append_basic_block(name="if_cont")
        else_block = self.function_manager.get_current_function().append_basic_block(
            name="else") if node.else_branch else merge_block

        self.builder.cbranch(condition_val, then_block, else_block)

        self.builder.position_at_end(then_block)
        self.scope_manager.push_scope()
        self.generate_statement(node.then_branch)
        self.scope_manager.pop_scope()
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)

        if node.else_branch:
            self.builder.position_at_end(else_block)
            self.scope_manager.push_scope()
            self.generate_statement(node.else_branch)
            self.scope_manager.pop_scope()
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)

        self.builder.position_at_end(merge_block)

    def generate_while_statement(self, node: WhileStatementNode):
        """Generate while statement"""
        current_func = self.function_manager.get_current_function()
        loop_header = current_func.append_basic_block(name="while_header")
        loop_body = current_func.append_basic_block(name="while_body")
        loop_exit = current_func.append_basic_block(name="while_exit")

        self.builder.branch(loop_header)

        self.builder.position_at_end(loop_header)
        condition_val = self.generate_expr(node.condition)
        if condition_val.type != ir.IntType(1):
            condition_val = self.builder.icmp_signed("!=", condition_val, ir.Constant(condition_val.type, 0))
        self.builder.cbranch(condition_val, loop_body, loop_exit)

        self.builder.position_at_end(loop_body)
        self.scope_manager.push_scope()
        self.generate_statement(node.body)
        self.scope_manager.pop_scope()
        if not self.builder.block.is_terminated:
            self.builder.branch(loop_header)

        self.builder.position_at_end(loop_exit)

    def generate_for_statement(self, node: ForStatementNode):
        """Generate for statement"""
        self.scope_manager.push_scope()

        if node.init:
            self.generate_statement(node.init)

        current_func = self.function_manager.get_current_function()
        cond_block = current_func.append_basic_block(name="for_cond")
        body_block = current_func.append_basic_block(name="for_body")
        update_block = current_func.append_basic_block(name="for_update")
        exit_block = current_func.append_basic_block(name="for_exit")

        self.builder.branch(cond_block)

        self.builder.position_at_end(cond_block)
        cond_val = self.generate_expr(node.condition)
        if cond_val.type != ir.IntType(1):
            cond_val = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))
        self.builder.cbranch(cond_val, body_block, exit_block)

        self.builder.position_at_end(body_block)
        self.scope_manager.push_scope()
        self.generate_statement(node.body)
        self.scope_manager.pop_scope()
        if not self.builder.block.is_terminated:
            self.builder.branch(update_block)

        self.builder.position_at_end(update_block)
        if node.update:
            self.generate_expr(node.update)
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_block)

        self.builder.position_at_end(exit_block)
        self.scope_manager.pop_scope()

    def generate_foreach_statement(self, node: ForeachStatementNode):
        """Generate foreach statement with generator support"""
        self.log(f"=== FOREACH: Starting foreach implementation ===")

        # Check if the iterable is a generator function call
        if isinstance(node.iterable, FunctionCallNode):
            func_name = node.iterable.name
            if self.generator_manager.is_generator(func_name):
                self.log(f"FOREACH: '{func_name}' is a generator - implementing iterator protocol")
                self._generate_foreach_with_generator(node)
                return

        self.log(f"FOREACH: Not a generator - basic array iteration not implemented")
        # TODO: Implement array iteration
        self.scope_manager.push_scope()
        self.scope_manager.pop_scope()

    def _generate_foreach_with_generator(self, node: ForeachStatementNode):
        """Generate foreach loop specifically for generator objects"""
        self.log(f"=== FOREACH GENERATOR: Implementing generator iteration ===")

        self.scope_manager.push_scope()

        # Create generator object
        generator_obj = self.generate_expr(node.iterable)
        gen_obj_alloca = self.builder.alloca(generator_obj.type, name="foreach_generator")
        self.builder.store(generator_obj, gen_obj_alloca)

        current_func = self.function_manager.get_current_function()
        loop_header = current_func.append_basic_block("foreach_header")
        loop_body = current_func.append_basic_block("foreach_body")
        loop_exit = current_func.append_basic_block("foreach_exit")

        self.builder.branch(loop_header)

        # Loop header: call step function
        self.builder.position_at_end(loop_header)
        func_name = node.iterable.name
        step_func_name = f"__{func_name}_step"
        step_func = self.function_manager.get_function(step_func_name)

        if not step_func:
            self.log(f"FOREACH GENERATOR: ERROR - Step function '{step_func_name}' not found!")
            self.builder.branch(loop_exit)
            self.builder.position_at_end(loop_exit)
            self.scope_manager.pop_scope()
            return

        gen_obj_loaded = self.builder.load(gen_obj_alloca)
        has_value = self.builder.call(step_func, [gen_obj_loaded], name="has_value")
        self.builder.cbranch(has_value, loop_body, loop_exit)

        # Loop body: extract value and execute body
        self.builder.position_at_end(loop_body)
        gen_obj_reloaded = self.builder.load(gen_obj_alloca)
        value_ptr = self.builder.gep(gen_obj_reloaded, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 2)])
        current_value = self.builder.load(value_ptr, name="yielded_value")

        # Create loop variable
        var_type_llvm = self.types_manager.get_llvm_type(node.var_type)
        loop_var_ptr = self.builder.alloca(var_type_llvm, name=node.var_name)
        converted_value = self._convert_value_to_type(current_value, var_type_llvm)
        self.builder.store(converted_value, loop_var_ptr)
        self.scope_manager.add_variable(node.var_name, loop_var_ptr, node.var_type, False, None, False)

        # Execute loop body
        self.scope_manager.push_scope()
        self.generate_statement(node.body)
        self.scope_manager.pop_scope()

        if not self.builder.block.is_terminated:
            self.builder.branch(loop_header)

        self.builder.position_at_end(loop_exit)
        self.scope_manager.pop_scope()

    def generate_return_statement(self, node: ReturnStatementNode):
        """Generate return statement"""
        current_func = self.function_manager.get_current_function()
        if not current_func:
            raise Exception("Return statement outside function")

        if node.value:
            ret_val_llvm = self.generate_expr(node.value)
            expected_type = current_func.return_value.type
            converted = self._convert_value_to_type(ret_val_llvm, expected_type)
            self.builder.ret(converted)
        else:
            if current_func.return_value.type != ir.VoidType():
                raise TypeError(f"Function expects return value")
            self.builder.ret_void()

    def generate_print_statement(self, node: PrintStatementNode):
        """Generate print statement"""
        value_llvm = self.generate_expr(node.value)
        val_type = value_llvm.type

        if val_type == self.dynamic_value_manager.get_dynamic_value_type():
            # Print dynamic value
            current_func = self.function_manager.get_current_function()
            print_functions = self.builtin_manager.get_all_functions()
            self.dynamic_value_manager.generate_dynamic_value_print(
                self.builder, value_llvm, current_func, print_functions)
        elif val_type == ir.IntType(32):
            print_func = self.builtin_manager.get_function("print_int")
            self.builder.call(print_func, [value_llvm])
        elif val_type == ir.FloatType():
            print_func = self.builtin_manager.get_function("print_float32")
            self.builder.call(print_func, [value_llvm])
        elif val_type == ir.DoubleType():
            print_func = self.builtin_manager.get_function("print_float64")
            self.builder.call(print_func, [value_llvm])
        elif val_type == ir.IntType(1):
            print_func = self.builtin_manager.get_function("print_bool")
            self.builder.call(print_func, [value_llvm])
        elif val_type == ir.PointerType(ir.IntType(8)):
            print_func = self.builtin_manager.get_function("print_string")
            self.builder.call(print_func, [value_llvm])
        elif isinstance(val_type, ir.PointerType) and isinstance(val_type.pointee, ir.IdentifiedStructType):
            # Print object address
            if val_type.pointee.name.startswith("struct.GeneratorObj_"):
                fmt_str = f"<GeneratorObject {val_type.pointee.name} @ %p>\n\0"
            else:
                fmt_str = f"Object({val_type.pointee.name})@%p\n\0"

            fmt_global = self.string_manager.get_or_create_global_string(fmt_str, ".fmt_obj_addr")
            fmt_ptr = self.builder.gep(fmt_global, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
            obj_i8p = self.builder.bitcast(value_llvm, ir.PointerType(ir.IntType(8)))
            printf_func = self.builtin_manager.get_function("printf")
            self.builder.call(printf_func, [fmt_ptr, obj_i8p])
        else:
            # Unknown type
            fmt_str = f"[Unprintable type: {val_type}]\n\0"
            fmt_global = self.string_manager.get_or_create_global_string(fmt_str, ".fmt_unknown")
            fmt_ptr = self.builder.gep(fmt_global, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
            printf_func = self.builtin_manager.get_function("printf")
            self.builder.call(printf_func, [fmt_ptr])

    def generate_read_statement(self, node: ReadStatementNode):
        """Generate read statement"""
        var_info = self.scope_manager.lookup_variable(node.var_name)
        if not var_info:
            raise NameError(f"Variable '{node.var_name}' not defined for read")

        var_ptr, type_name, is_array, _, _ = var_info
        if is_array:
            raise NotImplementedError(f"Reading into array '{node.var_name}' not supported")

        if type_name == "int":
            read_func = self.builtin_manager.get_function("read_int")
            self.builder.call(read_func, [var_ptr])
        elif type_name == "float32":
            read_func = self.builtin_manager.get_function("read_float32")
            self.builder.call(read_func, [var_ptr])
        elif type_name == "float64":
            read_func = self.builtin_manager.get_function("read_float64")
            self.builder.call(read_func, [var_ptr])
        else:
            raise TypeError(f"Cannot read into variable '{node.var_name}' of type '{type_name}'")

    # ===== EXPRESSION GENERATION =====

    def generate_expr(self, expr_node: ExprNode):
        """Generate code for an expression"""
        node_type_name = type(expr_node).__name__
        self.log(f"Generating expr: {node_type_name}")

        if isinstance(expr_node, LiteralNode):
            return self._generate_literal(expr_node)
        elif isinstance(expr_node, NullLiteralNode):
            return ir.Constant(ir.PointerType(ir.IntType(8)), None)
        elif isinstance(expr_node, VarReferenceNode):
            return self._generate_var_reference(expr_node)
        elif isinstance(expr_node, ArrayAccessNode):
            return self._generate_array_access(expr_node)
        elif isinstance(expr_node, BinaryOpNode):
            return self._generate_binary_op(expr_node)
        elif isinstance(expr_node, UnaryOpNode):
            return self._generate_unary_op(expr_node)
        elif isinstance(expr_node, FunctionCallNode):
            return self._generate_function_call(expr_node)
        elif isinstance(expr_node, MethodCallNode):
            return self._generate_method_call(expr_node)
        elif isinstance(expr_node, FieldAccessNode):
            return self._generate_field_access(expr_node)
        elif isinstance(expr_node, ObjectInstantiationNode):
            return self._generate_object_instantiation(expr_node)
        else:
            self.log(f"ERROR: Unhandled expression type: {node_type_name}")
            return None

    def _generate_literal(self, expr_node: LiteralNode):
        """Generate literal value"""
        if expr_node.type_name == "int":
            return ir.Constant(ir.IntType(32), expr_node.value)
        elif expr_node.type_name == "float32":
            return ir.Constant(ir.FloatType(), expr_node.value)
        elif expr_node.type_name == "float64":
            return ir.Constant(ir.DoubleType(), expr_node.value)
        elif expr_node.type_name == "bool":
            return ir.Constant(ir.IntType(1), 1 if expr_node.value else 0)
        elif expr_node.type_name == "string":
            return self.string_manager.create_string_literal(self.builder, expr_node.value)
        else:
            raise TypeError(f"Invalid literal type: {expr_node.type_name}")

    def _generate_var_reference(self, expr_node: VarReferenceNode):
        """Generate variable reference"""
        var_name = expr_node.name
        var_info = self.scope_manager.lookup_variable(var_name)

        if var_info:
            var_ptr, type_name_str, is_array, declared_dims_ast, is_param = var_info

            if type_name_str == "var":
                # Dynamic variable - return pointer to DynamicValue object
                dyn_obj_ptr_on_heap = self.builder.load(var_ptr, name=f"{var_name}_dyn_obj_ptr")
                return dyn_obj_ptr_on_heap
            elif is_array:
                # Array - return pointer
                return var_ptr
            elif type_name_str in self.types_manager.classes:
                # Class instance - load object pointer
                loaded_obj_ptr = self.builder.load(var_ptr, name=f"{var_name}_obj_ptr")
                return loaded_obj_ptr
            elif type_name_str in self.types_manager.structs:
                # Struct - return direct pointer
                return var_ptr
            else:
                # Scalar - load value
                return self.builder.load(var_ptr, name=f"{var_name}_val")

        elif self.current_class_or_struct_name:
            # Check if it's a field of 'this'
            this_var_info = self.scope_manager.lookup_variable("this")
            if this_var_info:
                return self._get_this_field_value(var_name, this_var_info)

            # Check if it's a function
        if var_name in self.function_manager.functions:
            return self.function_manager.functions[var_name]

        raise NameError(f"Undefined variable/function: '{var_name}'")

    def _get_this_field_value(self, field_name, this_var_info):
        """Get value of a field from 'this'"""
        this_ptr_alloca, owner_type_name, _, _, _ = this_var_info
        actual_this_obj_ptr = self.builder.load(this_ptr_alloca, name="this_obj_ptr")

        if owner_type_name in self.types_manager.structs:
            type_info = self.types_manager.structs[owner_type_name]
        elif owner_type_name in self.types_manager.classes:
            type_info = self.types_manager.classes[owner_type_name]
        else:
            raise NameError(f"Type '{owner_type_name}' not found")

        if field_name not in type_info["field_names"]:
            raise AttributeError(f"Field '{field_name}' not found in '{owner_type_name}'")

        field_idx = type_info["field_names"].index(field_name)
        field_ptr = self.builder.gep(actual_this_obj_ptr,
                                     [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), field_idx)])
        return self.builder.load(field_ptr, name=field_name)

    def _generate_array_access(self, expr_node: ArrayAccessNode):
        """Generate array access"""
        array_base_llvm = self.generate_expr(expr_node.array)
        if not isinstance(array_base_llvm.type, ir.PointerType):
            raise TypeError(f"Array base is not a pointer: {array_base_llvm.type}")

        indices_llvm = [self.generate_expr(idx_ast) for idx_ast in expr_node.indices]

        if len(indices_llvm) == 1:
            # 1D array access
            idx0 = self._convert_value_to_type(indices_llvm[0], self.types_manager.size_t_type)
            element_ptr = self.builder.gep(array_base_llvm, [idx0])
        elif len(indices_llvm) == 2:
            # 2D array access - need dimensions info
            array_name = expr_node.array.name
            var_info = self.scope_manager.lookup_variable(array_name)
            if not var_info or not var_info[3] or len(var_info[3]) < 2:
                raise ValueError(f"Insufficient dimension info for 2D array access on '{array_name}'")

            declared_dims_ast = var_info[3]
            cols_llvm = self.generate_expr(declared_dims_ast[1])
            cols_llvm = self._convert_value_to_type(cols_llvm, self.types_manager.size_t_type)
            idx0 = self._convert_value_to_type(indices_llvm[0], self.types_manager.size_t_type)
            idx1 = self._convert_value_to_type(indices_llvm[1], self.types_manager.size_t_type)
            linear_idx = self.builder.add(self.builder.mul(idx0, cols_llvm), idx1)
            element_ptr = self.builder.gep(array_base_llvm, [linear_idx])
        else:
            raise NotImplementedError(">2D array access not implemented")

        return self.builder.load(element_ptr)

    def _generate_binary_op(self, expr_node: BinaryOpNode):
        """Generate binary operation"""
        if expr_node.op == "&&":
            return self._generate_short_circuit_and(expr_node.left, expr_node.right)
        if expr_node.op == "||":
            return self._generate_short_circuit_or(expr_node.left, expr_node.right)

        lhs = self.generate_expr(expr_node.left)
        rhs = self.generate_expr(expr_node.right)

        # Type promotion
        if isinstance(lhs.type, (ir.FloatType, ir.DoubleType)) and isinstance(rhs.type, ir.IntType):
            rhs = self.builder.sitofp(rhs, lhs.type)
        elif isinstance(rhs.type, (ir.FloatType, ir.DoubleType)) and isinstance(lhs.type, ir.IntType):
            lhs = self.builder.sitofp(lhs, rhs.type)

        op = expr_node.op

        if isinstance(lhs.type, ir.IntType):
            if op == '+': return self.builder.add(lhs, rhs)
            if op == '-': return self.builder.sub(lhs, rhs)
            if op == '*': return self.builder.mul(lhs, rhs)
            if op == '/': return self.builder.sdiv(lhs, rhs)
            if op == '%': return self.builder.srem(lhs, rhs)
            if op == '==': return self.builder.icmp_signed('==', lhs, rhs)
            if op == '!=': return self.builder.icmp_signed('!=', lhs, rhs)
            if op == '<': return self.builder.icmp_signed('<', lhs, rhs)
            if op == '<=': return self.builder.icmp_signed('<=', lhs, rhs)
            if op == '>': return self.builder.icmp_signed('>', lhs, rhs)
            if op == '>=': return self.builder.icmp_signed('>=', lhs, rhs)
            if op == '^': return self.builder.xor(lhs, rhs)
        elif isinstance(lhs.type, (ir.FloatType, ir.DoubleType)):
            if op == '+': return self.builder.fadd(lhs, rhs)
            if op == '-': return self.builder.fsub(lhs, rhs)
            if op == '*': return self.builder.fmul(lhs, rhs)
            if op == '/': return self.builder.fdiv(lhs, rhs)
            if op == '==': return self.builder.fcmp_ordered('==', lhs, rhs)
            if op == '!=': return self.builder.fcmp_ordered('!=', lhs, rhs)
            if op == '<': return self.builder.fcmp_ordered('<', lhs, rhs)
            if op == '<=': return self.builder.fcmp_ordered('<=', lhs, rhs)
            if op == '>': return self.builder.fcmp_ordered('>', lhs, rhs)
            if op == '>=': return self.builder.fcmp_ordered('>=', lhs, rhs)

        raise ValueError(f"Unsupported binary operation '{op}' for type {lhs.type}")

    def _generate_short_circuit_and(self, lhs_ast, rhs_ast):
        """Generate short-circuit AND operation"""
        lhs_val = self.generate_expr(lhs_ast)
        if lhs_val.type != ir.IntType(1):
            lhs_val = self.builder.icmp_signed("!=", lhs_val, ir.Constant(lhs_val.type, 0))

        lhs_eval_block = self.builder.block
        current_func = self.function_manager.get_current_function()
        rhs_check_block = current_func.append_basic_block("and_rhs_check")
        merge_block = current_func.append_basic_block("and_merge")

        self.builder.cbranch(lhs_val, rhs_check_block, merge_block)

        self.builder.position_at_end(rhs_check_block)
        rhs_val = self.generate_expr(rhs_ast)
        if rhs_val.type != ir.IntType(1):
            rhs_val = self.builder.icmp_signed("!=", rhs_val, ir.Constant(rhs_val.type, 0))
        rhs_eval_block = self.builder.block
        self.builder.branch(merge_block)

        self.builder.position_at_end(merge_block)
        phi = self.builder.phi(ir.IntType(1), "and_res")
        phi.add_incoming(ir.Constant(ir.IntType(1), 0), lhs_eval_block)
        phi.add_incoming(rhs_val, rhs_eval_block)
        return phi

    def _generate_short_circuit_or(self, lhs_ast, rhs_ast):
        """Generate short-circuit OR operation"""
        lhs_val = self.generate_expr(lhs_ast)
        if lhs_val.type != ir.IntType(1):
            lhs_val = self.builder.icmp_signed("!=", lhs_val, ir.Constant(lhs_val.type, 0))

        lhs_eval_block = self.builder.block
        current_func = self.function_manager.get_current_function()
        rhs_check_block = current_func.append_basic_block("or_rhs_check")
        merge_block = current_func.append_basic_block("or_merge")

        self.builder.cbranch(lhs_val, merge_block, rhs_check_block)

        self.builder.position_at_end(rhs_check_block)
        rhs_val = self.generate_expr(rhs_ast)
        if rhs_val.type != ir.IntType(1):
            rhs_val = self.builder.icmp_signed("!=", rhs_val, ir.Constant(rhs_val.type, 0))
        rhs_eval_block = self.builder.block
        self.builder.branch(merge_block)

        self.builder.position_at_end(merge_block)
        phi = self.builder.phi(ir.IntType(1), "or_res")
        phi.add_incoming(ir.Constant(ir.IntType(1), 1), lhs_eval_block)
        phi.add_incoming(rhs_val, rhs_eval_block)
        return phi

    def _generate_unary_op(self, expr_node: UnaryOpNode):
        """Generate unary operation"""
        operand = self.generate_expr(expr_node.expr)
        op = expr_node.op

        if op == "-":
            if isinstance(operand.type, ir.IntType):
                return self.builder.neg(operand)
            elif isinstance(operand.type, (ir.FloatType, ir.DoubleType)):
                return self.builder.fneg(operand)
        elif op == "!":
            if operand.type != ir.IntType(1):
                operand = self.builder.icmp_signed("!=", operand, ir.Constant(operand.type, 0))
            return self.builder.not_(operand)

        raise ValueError(f"Unsupported unary operation '{op}' for type {operand.type}")

    def _generate_function_call(self, expr_node: FunctionCallNode):
        """Generate function call"""
        func_name = expr_node.name

        if self.generator_manager.is_generator(func_name):
            return self._generate_generator_call(expr_node)

        func = self.function_manager.get_function(func_name)
        if not func:
            raise NameError(f"Function '{func_name}' not defined")

        args_llvm = [self.generate_expr(arg_ast) for arg_ast in expr_node.args]

        # Convert arguments to expected types
        for i, (arg_llvm, expected_arg) in enumerate(zip(args_llvm, func.args)):
            args_llvm[i] = self._convert_value_to_type(arg_llvm, expected_arg.type)

        return self.builder.call(func, args_llvm, name=f"{func_name}_result")

    def _generate_generator_call(self, expr_node: FunctionCallNode):
        """Generate generator constructor call"""
        func_name = expr_node.name
        constructor_name = f"__{func_name}_create"
        constructor_func = self.function_manager.get_function(constructor_name)

        if not constructor_func:
            raise NameError(f"Generator constructor '{constructor_name}' not found")

        args_llvm = [self.generate_expr(arg_ast) for arg_ast in expr_node.args]

        # Convert arguments to expected types
        for i, (arg_llvm, expected_arg) in enumerate(zip(args_llvm, constructor_func.args)):
            args_llvm[i] = self._convert_value_to_type(arg_llvm, expected_arg.type)

        return self.builder.call(constructor_func, args_llvm, name=f"{func_name}_gen_obj")

    def _generate_method_call(self, expr_node: MethodCallNode):
        """Generate method call"""
        obj_llvm = self.generate_expr(expr_node.object_expr)
        method_name = expr_node.method_name

        if not isinstance(obj_llvm.type, ir.PointerType) or \
                not isinstance(obj_llvm.type.pointee, ir.IdentifiedStructType):
            raise TypeError(f"Cannot call method '{method_name}' on non-struct/class type")

        struct_qname = obj_llvm.type.pointee.name
        type_name_simple = struct_qname.split('.', 1)[1] if '.' in struct_qname else struct_qname

        # First try to find the method on the current type
        mangled_method_name = f"{type_name_simple}_{method_name}"
        method_func = self.function_manager.get_function(mangled_method_name)

        # If not found on current type, check parent classes
        if not method_func and type_name_simple in self.types_manager.classes:
            current_class = type_name_simple
            while current_class and not method_func:
                class_info = self.types_manager.classes.get(current_class)
                if class_info and class_info.get("parent"):
                    parent_class = class_info["parent"]
                    parent_mangled_name = f"{parent_class}_{method_name}"
                    method_func = self.function_manager.get_function(parent_mangled_name)
                    if method_func:
                        mangled_method_name = parent_mangled_name
                        break
                    current_class = parent_class
                else:
                    break

        if not method_func:
            raise AttributeError(f"Method '{method_name}' not found on type '{type_name_simple}' or its parent classes")

        args_llvm = [obj_llvm] + [self.generate_expr(arg_ast) for arg_ast in expr_node.args]

        # Convert arguments to expected types
        for i, (arg_llvm, expected_arg) in enumerate(zip(args_llvm, method_func.args)):
            args_llvm[i] = self._convert_value_to_type(arg_llvm, expected_arg.type)

        return self.builder.call(method_func, args_llvm, name=f"{method_name}_result")

    def _generate_field_access(self, expr_node: FieldAccessNode):
        """Generate field access"""
        obj_llvm_ptr = self.generate_expr(expr_node.object_expr)
        field_name = expr_node.field_name

        if not isinstance(obj_llvm_ptr.type, ir.PointerType) or \
                not isinstance(obj_llvm_ptr.type.pointee, ir.IdentifiedStructType):
            raise TypeError(f"Cannot access field '{field_name}' on non-struct/class type")

        struct_qname = obj_llvm_ptr.type.pointee.name
        type_name_simple = struct_qname.split('.', 1)[1] if '.' in struct_qname else struct_qname

        if not self.types_manager.has_field(type_name_simple, field_name):
            raise AttributeError(f"Field '{field_name}' not found in '{type_name_simple}'")

        field_idx = self.types_manager.get_field_index(type_name_simple, field_name)
        field_ptr = self.builder.gep(obj_llvm_ptr,
                                     [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), field_idx)])
        return self.builder.load(field_ptr, name=field_name)

    def _generate_object_instantiation(self, expr_node: ObjectInstantiationNode):
        """Generate object instantiation"""
        class_name = expr_node.class_name

        if class_name not in self.types_manager.classes:
            raise NameError(f"Class '{class_name}' not defined")

        class_type = self.types_manager.classes[class_name]["type"]

        # Allocate memory for object
        obj_size = class_type.get_abi_size(self.data_layout)
        size_const = ir.Constant(self.types_manager.size_t_type, obj_size)
        malloc_func = self.builtin_manager.get_function("malloc")
        raw_mem = self.builder.call(malloc_func, [size_const])
        obj_ptr = self.builder.bitcast(raw_mem, ir.PointerType(class_type), name=f"{class_name}_obj")

        # Call constructor if it exists
        ctor_func = self.function_manager.get_constructor(class_name)
        if ctor_func:
            args_llvm = [obj_ptr] + [self.generate_expr(arg_ast) for arg_ast in expr_node.args]

            # Convert arguments to expected types
            for i, (arg_llvm, expected_arg) in enumerate(zip(args_llvm, ctor_func.args)):
                args_llvm[i] = self._convert_value_to_type(arg_llvm, expected_arg.type)

            self.builder.call(ctor_func, args_llvm)

        return obj_ptr

    def _convert_value_to_type(self, value, target_type):
        """Convert a value to the target LLVM type"""
        if value.type == target_type:
            return value

        # Integer conversions
        if isinstance(value.type, ir.IntType) and isinstance(target_type, ir.IntType):
            if value.type.width < target_type.width:
                return self.builder.sext(value, target_type)
            elif value.type.width > target_type.width:
                return self.builder.trunc(value, target_type)

        # Float conversions
        if isinstance(value.type, ir.FloatType) and isinstance(target_type, ir.DoubleType):
            return self.builder.fpext(value, target_type)
        if isinstance(value.type, ir.DoubleType) and isinstance(target_type, ir.FloatType):
            return self.builder.fptrunc(value, target_type)

        # Integer to float
        if isinstance(value.type, ir.IntType) and isinstance(target_type, (ir.FloatType, ir.DoubleType)):
            return self.builder.sitofp(value, target_type)

        # Float to integer
        if isinstance(value.type, (ir.FloatType, ir.DoubleType)) and isinstance(target_type, ir.IntType):
            return self.builder.fptosi(value, target_type)

        # Pointer conversions
        if isinstance(value.type, ir.PointerType) and isinstance(target_type, ir.PointerType):
            return self.builder.bitcast(value, target_type)

        return value

    def _get_default_return_value(self, llvm_type):
        """Get default return value for a type"""
        if isinstance(llvm_type, ir.IntType):
            return ir.Constant(llvm_type, 0)
        elif isinstance(llvm_type, (ir.FloatType, ir.DoubleType)):
            return ir.Constant(llvm_type, 0.0)
        elif isinstance(llvm_type, ir.PointerType):
            return ir.Constant(llvm_type, None)
        else:
            return None




