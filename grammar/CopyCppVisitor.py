# Generated from grammar/CopyCpp.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CopyCppParser import CopyCppParser
else:
    from CopyCppParser import CopyCppParser

# This class defines a complete generic visitor for a parse tree produced by CopyCppParser.

class CopyCppVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CopyCppParser#program.
    def visitProgram(self, ctx:CopyCppParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#statement.
    def visitStatement(self, ctx:CopyCppParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#block.
    def visitBlock(self, ctx:CopyCppParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#varDeclaration.
    def visitVarDeclaration(self, ctx:CopyCppParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#type.
    def visitType(self, ctx:CopyCppParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#assignment.
    def visitAssignment(self, ctx:CopyCppParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ifStatement.
    def visitIfStatement(self, ctx:CopyCppParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#whileStatement.
    def visitWhileStatement(self, ctx:CopyCppParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#forStatement.
    def visitForStatement(self, ctx:CopyCppParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#functionDecl.
    def visitFunctionDecl(self, ctx:CopyCppParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#formalParams.
    def visitFormalParams(self, ctx:CopyCppParser.FormalParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#formalParam.
    def visitFormalParam(self, ctx:CopyCppParser.FormalParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#functionCall.
    def visitFunctionCall(self, ctx:CopyCppParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#actualParams.
    def visitActualParams(self, ctx:CopyCppParser.ActualParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#returnStatement.
    def visitReturnStatement(self, ctx:CopyCppParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#printStatement.
    def visitPrintStatement(self, ctx:CopyCppParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#readStatement.
    def visitReadStatement(self, ctx:CopyCppParser.ReadStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#expr.
    def visitExpr(self, ctx:CopyCppParser.ExprContext):
        return self.visitChildren(ctx)



del CopyCppParser