from antlr4 import *
from grammar.CopyCppParser import CopyCppParser
from grammar.CopyCppVisitor import CopyCppVisitor
from grammar.CopyCppLexer import CopyCppLexer

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class StatementNode(ASTNode):
    pass

class VarDeclarationNode(StatementNode):
    def __init__(self, type_name, var_name, initial_value=None, dimensions=None):
        self.type_name = type_name
        self.var_name = var_name
        self.initial_value = initial_value
        self.dimensions = dimensions or []

class AssignmentNode(StatementNode):
    def __init__(self, var_name, value, indices=None):
        self.var_name = var_name
        self.value = value
        self.indices = indices or []  # For arrays and matrices

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

class FunctionDeclNode(StatementNode):
    def __init__(self, type_name, name, params, body):
        self.type_name = type_name
        self.name = name
        self.params = params
        self.body = body

class FunctionCallNode(StatementNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ReturnStatementNode(StatementNode):
    def __init__(self, value=None):
        self.value = value

class PrintStatementNode(StatementNode):
    def __init__(self, value):
        self.value = value

class ReadStatementNode(StatementNode):
    def __init__(self, var_name):
        self.var_name = var_name

class BlockNode(StatementNode):
    def __init__(self, statements):
        self.statements = statements

class ExprNode(ASTNode):
    pass

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
    def __init__(self, name, indices=None):
        self.name = name
        self.indices = indices or []  # For arrays and matrices

class LiteralNode(ExprNode):
    def __init__(self, value, type_name):
        self.value = value
        self.type_name = type_name

class ASTBuilder(CopyCppVisitor):
    def visitProgram(self, ctx):
        statements = [self.visit(stmt) for stmt in ctx.statement()]
        return ProgramNode(statements)

    def visitStatement(self, ctx):
        if ctx.varDeclaration():
            return self.visit(ctx.varDeclaration())
        elif ctx.assignment():
            return self.visit(ctx.assignment())
        elif ctx.ifStatement():
            return self.visit(ctx.ifStatement())
        elif ctx.whileStatement():
            return self.visit(ctx.whileStatement())
        elif ctx.forStatement():
            return self.visit(ctx.forStatement())
        elif ctx.functionDecl():
            return self.visit(ctx.functionDecl())
        elif ctx.functionCall():
            return self.visit(ctx.functionCall())
        elif ctx.returnStatement():
            return self.visit(ctx.returnStatement())
        elif ctx.printStatement():
            return self.visit(ctx.printStatement())
        elif ctx.readStatement():
            return self.visit(ctx.readStatement())
        elif ctx.block():
            return self.visit(ctx.block())
        return None  # For COMMENT

    def visitBlock(self, ctx):
        statements = [self.visit(stmt) for stmt in ctx.statement()]
        return BlockNode(statements)

    def visitVarDeclaration(self, ctx):
        type_name = ctx.type_().getText()
        var_name = ctx.ID().getText()

        dimensions = []
        if len(ctx.expr()) > 1:
            dimensions = [self.visit(ctx.expr(0)), self.visit(ctx.expr(1))]
        elif len(ctx.expr()) == 1:
            if ctx.getText().count('[') > 0:
                dimensions = [self.visit(ctx.expr(0))]
            else:
                return VarDeclarationNode(type_name, var_name, self.visit(ctx.expr(0)))

        return VarDeclarationNode(type_name, var_name, None, dimensions)

    def visitType(self, ctx):
        return ctx.getText()

    def visitAssignment(self, ctx):
        var_name = ctx.ID().getText()
        indices = []

        if len(ctx.expr()) > 1:
            for i in range(len(ctx.expr()) - 1):
                indices.append(self.visit(ctx.expr(i)))
            value = self.visit(ctx.expr()[-1])
        else:
            value = self.visit(ctx.expr(0))

        return AssignmentNode(var_name, value, indices)

    def visitIfStatement(self, ctx):
        condition = self.visit(ctx.expr())
        then_branch = self.visit(ctx.statement(0))
        else_branch = None
        if len(ctx.statement()) > 1:
            else_branch = self.visit(ctx.statement(1))
        return IfStatementNode(condition, then_branch, else_branch)

    def visitWhileStatement(self, ctx):
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.statement())
        return WhileStatementNode(condition, body)

    def visitForStatement(self, ctx):
        init = self.visit(ctx.statement())
        condition = self.visit(ctx.expr(0))
        update = self.visit(ctx.expr(1))
        body = self.visit(ctx.statement(1))
        return ForStatementNode(init, condition, update, body)

    def visitFunctionDecl(self, ctx):
        type_name = ctx.type_().getText()
        name = ctx.ID().getText()

        params = []
        if ctx.formalParams():
            params = self.visit(ctx.formalParams())

        body = self.visit(ctx.block())
        return FunctionDeclNode(type_name, name, params, body)

    def visitFormalParams(self, ctx):
        return [self.visit(param) for param in ctx.formalParam()]

    def visitFormalParam(self, ctx):
        type_name = ctx.type_().getText()
        var_name = ctx.ID().getText()

        # Determine if it's an array parameter and its dimensions
        dimensions = []
        text = ctx.getText()

        # Check for array declarations with just []
        if "[][]" in text:
            dimensions = [None, None]  # 2D array/matrix
        elif "[]" in text:
            dimensions = [None]  # 1D array
        # Check for array declarations with size expressions
        elif len(ctx.expr()) > 0:
            dimensions = [self.visit(expr) for expr in ctx.expr()]

        if dimensions:
            return (type_name, var_name, dimensions)
        else:
            return (type_name, var_name)

    def visitFunctionCall(self, ctx):
        name = ctx.ID().getText()
        args = []
        if ctx.actualParams():
            args = self.visit(ctx.actualParams())
        return FunctionCallNode(name, args)

    def visitActualParams(self, ctx):
        return [self.visit(expr) for expr in ctx.expr()]

    def visitReturnStatement(self, ctx:CopyCppParser.ReturnStatementContext):
        value = None
        if ctx.expr():
            value = self.visit(ctx.expr())
        return ReturnStatementNode(value)

    def visitPrintStatement(self, ctx:CopyCppParser.PrintStatementContext):
        value = self.visit(ctx.expr())
        return PrintStatementNode(value)

    def visitReadStatement(self, ctx:CopyCppParser.ReadStatementContext):
        var_name = ctx.ID().getText()
        return ReadStatementNode(var_name)

    def visitExpr(self, ctx):
        if ctx.INT():
            return LiteralNode(int(ctx.INT().getText()), "int")
        elif ctx.FLOAT():
            return LiteralNode(float(ctx.FLOAT().getText()), "float64")
        elif ctx.BOOL():
            return LiteralNode(ctx.BOOL().getText() == "true", "bool")
        elif ctx.STRING():
            # Remove quotes
            text = ctx.STRING().getText()
            return LiteralNode(text[1:-1], "string")
        elif ctx.ID() and not ctx.expr():
            return VarReferenceNode(ctx.ID().getText())
        elif ctx.ID() and ctx.expr():
            if ctx.getText().startswith(ctx.ID().getText() + '['):
                var_name = ctx.ID().getText()
                indices = [self.visit(expr) for expr in ctx.expr()]
                return VarReferenceNode(var_name, indices)
            else: # Function call
                return self.visit(ctx.functionCall())
        elif ctx.functionCall():
            return self.visit(ctx.functionCall())
        elif len(ctx.expr()) == 1 and ctx.getChild(0).getText() == '(':
            return self.visit(ctx.expr(0))
        elif len(ctx.expr()) == 1 and ctx.getChild(0).getText() == '-':
            return UnaryOpNode('-', self.visit(ctx.expr(0)))
        elif len(ctx.expr()) == 1 and ctx.getChild(0).getText() == '!':
            return UnaryOpNode('!', self.visit(ctx.expr(0)))
        elif len(ctx.expr()) == 2:
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))

            # Determine the operator
            if ctx.op:
                op = ctx.op.text
            elif "&&" in ctx.getText():
                op = "&&"
            elif "||" in ctx.getText():
                op = "||"
            elif "^" in ctx.getText():
                op = "^"
            else:
                op = "unknown"

            return BinaryOpNode(left, op, right)

        return None


