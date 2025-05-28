"""Generator management for CopyCpp compiler"""
import llvmlite.ir as ir
from ...ast.nodes import FunctionDeclNode, VarDeclarationNode, WhileStatementNode, ForStatementNode, BlockNode, IfStatementNode

class GeneratorManager:
    def __init__(self, module, types_manager, function_manager, debug=False):
        self.module = module
        self.types_manager = types_manager
        self.function_manager = function_manager
        self.debug = debug

        self.generators = {}
        self.generator_objects = {}
        self.current_generator_context = None

    def log(self, message):
        if self.debug:
            print(f"DEBUG GEN: {message}")

    def register_generator(self, node: FunctionDeclNode):
        """Register a generator function with full state analysis"""
        if node.name in self.generators:
            return self.generators[node.name]

        self.log(f"Registering generator: {node.name}")

        # Analyze what local variables need to persist across yields
        local_vars = self._analyze_generator_state_vars(node.body)
        self.log(f"Generator {node.name} local variables: {local_vars}")

        yield_type_llvm = self.types_manager.get_llvm_type(node.type_name)
        param_types = [
            self.types_manager.get_llvm_type(p['type'], p['dimensions'])
            for p in node.params
        ]

        # Build generator object fields:
        # [state, yield_point, last_yielded_value, ...parameters, ...local_variables]
        obj_fields = [
            ir.IntType(32),  # state (0=CREATED, 1=RUNNING, 2=SUSPENDED, 3=COMPLETED)
            ir.IntType(32),  # yield_point (which yield point to resume from)
            yield_type_llvm  # last_yielded_value
        ]

        # Add parameter fields
        obj_fields.extend(param_types)

        # Add local variable fields
        local_var_types = {}
        local_var_names = []
        for var_name, var_type in local_vars.items():
            llvm_type = self.types_manager.get_llvm_type(var_type)
            obj_fields.append(llvm_type)
            local_var_types[var_name] = llvm_type
            local_var_names.append(var_name)

        # Create the generator object type using identified struct type
        obj_type_name = f"GeneratorObj_{node.name}"
        obj_type = self.module.context.get_identified_type(f"struct.{obj_type_name}")
        obj_type.set_body(*obj_fields)

        generator_info = {
            'name': node.name,
            'node': node,
            'yield_type': yield_type_llvm,
            'param_types': param_types,
            'local_var_types': local_var_types,
            'local_var_names': local_var_names,
            'obj_type_info': {'type': obj_type, 'name': obj_type_name},
            'param_count': len(param_types),
            'local_var_offset': 3 + len(param_types),  # offset where local vars start in struct
            'yield_points': []
        }

        self.generators[node.name] = generator_info
        self.log(f"Registered generator: {node.name} with {len(local_vars)} local variables")
        return generator_info

    def _analyze_generator_state_vars(self, body_node):
        """Analyze which local variables need to persist across yields"""
        state_vars = {}

        def analyze_node(node, in_loop_or_conditional=False):
            if isinstance(node, VarDeclarationNode):
                # All variables in loops/conditionals that might contain yields need to persist
                # For simplicity, we'll save all local variables for now
                state_vars[node.var_name] = node.type_name
            elif isinstance(node, WhileStatementNode):
                analyze_node(node.body, True)
            elif isinstance(node, ForStatementNode):
                if node.init:
                    analyze_node(node.init, True)
                analyze_node(node.body, True)
            elif isinstance(node, BlockNode):
                for stmt in node.statements:
                    analyze_node(stmt, in_loop_or_conditional)
            elif isinstance(node, IfStatementNode):
                analyze_node(node.then_branch, True)
                if node.else_branch:
                    analyze_node(node.else_branch, True)
            # Add other control flow nodes as needed

        analyze_node(body_node)
        return state_vars

    def create_generator_object_type(self, generator_name, yield_type_llvm, param_types):
        """Create the LLVM structure for a generator object (legacy method)"""
        # This method is kept for compatibility but the new register_generator
        # handles object type creation internally
        type_name = f"GeneratorObj_{generator_name}"

        if type_name in self.generator_objects:
            return self.generator_objects[type_name]

        gen_obj_type = self.module.context.get_identified_type(f"struct.{type_name}")

        # Basic generator object fields: [state, yield_point, last_value, ...params]
        fields = [
            ir.IntType(32),  # state
            ir.IntType(32),  # yield_point
            yield_type_llvm  # last_yielded_value
        ]
        fields.extend(param_types)  # parameters

        gen_obj_type.set_body(*fields)

        self.generator_objects[type_name] = {
            'type': gen_obj_type,
            'yield_type': yield_type_llvm,
            'param_types': param_types,
            'generator_name': generator_name
        }

        self.log(f"Created generator object type: {type_name}")
        return self.generator_objects[type_name]

    def declare_generator_support_functions(self):
        """Declare helper functions for generator operations"""
        self.log("Declaring generator support functions")
        # These are placeholder functions - actual step functions are generated per-generator

    def is_generator(self, name):
        """Check if a function name is a generator"""
        return name in self.generators

    def get_generator_info(self, name):
        """Get generator information by name"""
        return self.generators.get(name)

    def set_current_generator_context(self, context):
        """Set the current generator context"""
        self.current_generator_context = context

    def get_current_generator_context(self):
        """Get the current generator context"""
        return self.current_generator_context

    def create_state_save_restore_helpers(self, builder, gen_obj_ptr, gen_info):
        """Create helper functions for saving/restoring local variable state"""
        def save_local_var_to_generator(var_name, var_alloca):
            """Save a local variable's value to the generator object"""
            if var_name in gen_info['local_var_names']:
                var_index = gen_info['local_var_names'].index(var_name)
                var_ptr_in_obj = builder.gep(gen_obj_ptr, [
                    ir.Constant(ir.IntType(32), 0),
                    ir.Constant(ir.IntType(32), gen_info['local_var_offset'] + var_index)
                ])
                var_value = builder.load(var_alloca)
                builder.store(var_value, var_ptr_in_obj)
                if self.debug:
                    self.log(f"Saved local var '{var_name}' to generator object at offset {gen_info['local_var_offset'] + var_index}")

        def restore_local_var_from_generator(var_name, var_alloca):
            """Restore a local variable's value from the generator object"""
            if var_name in gen_info['local_var_names']:
                var_index = gen_info['local_var_names'].index(var_name)
                var_ptr_in_obj = builder.gep(gen_obj_ptr, [
                    ir.Constant(ir.IntType(32), 0),
                    ir.Constant(ir.IntType(32), gen_info['local_var_offset'] + var_index)
                ])
                var_value = builder.load(var_ptr_in_obj)
                builder.store(var_value, var_alloca)
                if self.debug:
                    self.log(f"Restored local var '{var_name}' from generator object at offset {gen_info['local_var_offset'] + var_index}")

        def save_all_local_vars(scope_manager):
            """Save all currently visible local variables"""
            for var_name in gen_info['local_var_names']:
                var_info = scope_manager.lookup_variable(var_name)
                if var_info:
                    var_ptr, _, _, _, _ = var_info
                    save_local_var_to_generator(var_name, var_ptr)

        def restore_all_local_vars(scope_manager):
            """Restore all local variables that exist in the generator object"""
            for var_name in gen_info['local_var_names']:
                var_info = scope_manager.lookup_variable(var_name)
                if var_info:
                    var_ptr, _, _, _, _ = var_info
                    restore_local_var_from_generator(var_name, var_ptr)

        def initialize_local_vars_in_generator():
            """Initialize local variable slots in generator object to default values"""
            for i, (var_name, var_type) in enumerate(zip(gen_info['local_var_names'], gen_info['local_var_types'].values())):
                var_ptr = builder.gep(gen_obj_ptr, [
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

                builder.store(default_val, var_ptr)

        return {
            'save_local_var': save_local_var_to_generator,
            'restore_local_var': restore_local_var_from_generator,
            'save_all_local_vars': save_all_local_vars,
            'restore_all_local_vars': restore_all_local_vars,
            'initialize_local_vars': initialize_local_vars_in_generator
        }

    def get_local_var_offset_in_generator(self, gen_info, var_name):
        """Get the field offset for a local variable in the generator object"""
        if var_name not in gen_info['local_var_names']:
            return None

        var_index = gen_info['local_var_names'].index(var_name)
        return gen_info['local_var_offset'] + var_index

    def add_yield_point(self, generator_name, yield_id, resume_block):
        """Add a yield point to a generator"""
        if generator_name in self.generators:
            self.generators[generator_name]['yield_points'].append({
                'id': yield_id,
                'resume_block': resume_block
            })
