"""AST Node definitions for CopyCpp compiler"""

class ASTNode:
    """AST Node definitions for CopyCpp compiler"""
    pass

class StatementNode(ASTNode):
    """Base class for statement nodes"""
    pass

class ExprNode(ASTNode):
    """Base class for expression nodes"""
    pass

class BlockNode(StatementNode):
    def __init__(self, statements):
        super().__init__()
        self.statements = list(statements) if statements else []
        print(f"BlockNode created with {len(self.statements)} statements")

        # Check first few statements to verify content
        for i, stmt in enumerate(self.statements[:3]):  # Show up to 3 statements
            print(f"  - Statement {i}: {type(stmt).__name__}")

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDeclarationNode(StatementNode):
    def __init__(self, type_name, var_name, initial_value=None, dimensions=None):
        self.type_name = type_name
        self.var_name = var_name
        self.initial_value = initial_value
        self.dimensions = dimensions or []

        # Add debug logging
        print(f"Created VarDeclarationNode: {var_name}, type={type_name}, "
              f"has dimensions: {len(self.dimensions) > 0}")

class AssignmentNode(StatementNode):
    def __init__(self, target, value):
        self.target = target  # Can be VarReferenceNode, ArrayAccessNode, or FieldAccessNode
        self.value = value

class IfStatementNode(StatementNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStatementNode(StatementNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForStatementNode(StatementNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class ForeachStatementNode(StatementNode):
    def __init__(self, var_type, var_name, iterable, body):
        self.var_type = var_type  # Can be a specific type or 'var' for dynamic typing
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

class FunctionDeclNode(StatementNode):
    def __init__(self, type_name, name, params, body, is_generator=False):
        self.type_name = type_name
        self.name = name
        self.params = params
        self.body = body
        self.is_generator = is_generator

        print(f"Created FunctionDeclNode: Name='{name}', Type/YieldType='{type_name}', IsGenerator={is_generator}")

class FunctionCallNode(ExprNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class FunctionCallStatementNode(StatementNode):
    def __init__(self, function_call):
        self.function_call = function_call

class MethodCallNode(ExprNode):
    def __init__(self, object_expr, method_name, args):
        self.object_expr = object_expr
        self.method_name = method_name
        self.args = args

class ReturnStatementNode(StatementNode):
    def __init__(self, value=None):
        self.value = value

class YieldStatementNode(StatementNode):
    def __init__(self, value):
        self.value = value

class PrintStatementNode(StatementNode):
    def __init__(self, value):
        self.value = value

class ReadStatementNode(StatementNode):
    def __init__(self, var_name):
        self.var_name = var_name

class StructDeclNode(StatementNode):
    def __init__(self, name, members):
        self.name = name
        self.members = members  # List of VarDeclarationNode and FunctionDeclNode

class ClassDeclNode(StatementNode):
    def __init__(self, name, parent_class, private_members, public_members, protected_members):
        self.name = name
        self.parent_class = parent_class
        self.private_members = private_members or []
        self.public_members = public_members or []
        self.protected_members = protected_members or []

class ConstructorDeclNode(StatementNode):
    def __init__(self, class_name, params, body):
        self.class_name = class_name
        self.params = params
        self.body = body

class BinaryOpNode(ExprNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOpNode(ExprNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class VarReferenceNode(ExprNode):
    def __init__(self, name):
        self.name = name

class ArrayAccessNode(ExprNode):
    def __init__(self, array, indices):
        self.array = array  # Can be a variable name or another expression
        self.indices = indices  # List of expressions for the indices

class FieldAccessNode(ExprNode):
    def __init__(self, object_expr, field_name):
        self.object_expr = object_expr
        self.field_name = field_name

class ObjectInstantiationNode(ExprNode):
    def __init__(self, class_name, args):
        self.class_name = class_name
        self.args = args

class LiteralNode(ExprNode):
    def __init__(self, value, type_name):
        self.value = value
        self.type_name = type_name

class NullLiteralNode(ExprNode):
    pass

class GeneratorObjectNode(ExprNode):
    """Represents a generator object created from calling a generator function"""

    def __init__(self, generator_func_name, args):
        self.generator_func_name = generator_func_name
        self.args = args

class GeneratorState:
    CREATED = 0
    RUNNING = 1
    SUSPENDED = 2
    COMPLETED = 3
