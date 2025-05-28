# Generated from grammar/CopyCpp.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CopyCppParser import CopyCppParser
else:
    from CopyCppParser import CopyCppParser

# This class defines a complete listener for a parse tree produced by CopyCppParser.
class CopyCppListener(ParseTreeListener):

    # Enter a parse tree produced by CopyCppParser#program.
    def enterProgram(self, ctx:CopyCppParser.ProgramContext):
        pass

    # Exit a parse tree produced by CopyCppParser#program.
    def exitProgram(self, ctx:CopyCppParser.ProgramContext):
        pass


    # Enter a parse tree produced by CopyCppParser#statement.
    def enterStatement(self, ctx:CopyCppParser.StatementContext):
        pass

    # Exit a parse tree produced by CopyCppParser#statement.
    def exitStatement(self, ctx:CopyCppParser.StatementContext):
        pass


    # Enter a parse tree produced by CopyCppParser#block.
    def enterBlock(self, ctx:CopyCppParser.BlockContext):
        pass

    # Exit a parse tree produced by CopyCppParser#block.
    def exitBlock(self, ctx:CopyCppParser.BlockContext):
        pass


    # Enter a parse tree produced by CopyCppParser#varDeclaration.
    def enterVarDeclaration(self, ctx:CopyCppParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by CopyCppParser#varDeclaration.
    def exitVarDeclaration(self, ctx:CopyCppParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by CopyCppParser#type.
    def enterType(self, ctx:CopyCppParser.TypeContext):
        pass

    # Exit a parse tree produced by CopyCppParser#type.
    def exitType(self, ctx:CopyCppParser.TypeContext):
        pass


    # Enter a parse tree produced by CopyCppParser#assignment.
    def enterAssignment(self, ctx:CopyCppParser.AssignmentContext):
        pass

    # Exit a parse tree produced by CopyCppParser#assignment.
    def exitAssignment(self, ctx:CopyCppParser.AssignmentContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ifStatement.
    def enterIfStatement(self, ctx:CopyCppParser.IfStatementContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ifStatement.
    def exitIfStatement(self, ctx:CopyCppParser.IfStatementContext):
        pass


    # Enter a parse tree produced by CopyCppParser#whileStatement.
    def enterWhileStatement(self, ctx:CopyCppParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by CopyCppParser#whileStatement.
    def exitWhileStatement(self, ctx:CopyCppParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by CopyCppParser#forStatement.
    def enterForStatement(self, ctx:CopyCppParser.ForStatementContext):
        pass

    # Exit a parse tree produced by CopyCppParser#forStatement.
    def exitForStatement(self, ctx:CopyCppParser.ForStatementContext):
        pass


    # Enter a parse tree produced by CopyCppParser#functionDecl.
    def enterFunctionDecl(self, ctx:CopyCppParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by CopyCppParser#functionDecl.
    def exitFunctionDecl(self, ctx:CopyCppParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by CopyCppParser#formalParams.
    def enterFormalParams(self, ctx:CopyCppParser.FormalParamsContext):
        pass

    # Exit a parse tree produced by CopyCppParser#formalParams.
    def exitFormalParams(self, ctx:CopyCppParser.FormalParamsContext):
        pass


    # Enter a parse tree produced by CopyCppParser#formalParam.
    def enterFormalParam(self, ctx:CopyCppParser.FormalParamContext):
        pass

    # Exit a parse tree produced by CopyCppParser#formalParam.
    def exitFormalParam(self, ctx:CopyCppParser.FormalParamContext):
        pass


    # Enter a parse tree produced by CopyCppParser#functionCall.
    def enterFunctionCall(self, ctx:CopyCppParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by CopyCppParser#functionCall.
    def exitFunctionCall(self, ctx:CopyCppParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by CopyCppParser#actualParams.
    def enterActualParams(self, ctx:CopyCppParser.ActualParamsContext):
        pass

    # Exit a parse tree produced by CopyCppParser#actualParams.
    def exitActualParams(self, ctx:CopyCppParser.ActualParamsContext):
        pass


    # Enter a parse tree produced by CopyCppParser#returnStatement.
    def enterReturnStatement(self, ctx:CopyCppParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by CopyCppParser#returnStatement.
    def exitReturnStatement(self, ctx:CopyCppParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by CopyCppParser#printStatement.
    def enterPrintStatement(self, ctx:CopyCppParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by CopyCppParser#printStatement.
    def exitPrintStatement(self, ctx:CopyCppParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by CopyCppParser#readStatement.
    def enterReadStatement(self, ctx:CopyCppParser.ReadStatementContext):
        pass

    # Exit a parse tree produced by CopyCppParser#readStatement.
    def exitReadStatement(self, ctx:CopyCppParser.ReadStatementContext):
        pass


    # Enter a parse tree produced by CopyCppParser#expr.
    def enterExpr(self, ctx:CopyCppParser.ExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#expr.
    def exitExpr(self, ctx:CopyCppParser.ExprContext):
        pass



del CopyCppParser