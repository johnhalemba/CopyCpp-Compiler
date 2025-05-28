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


    # Enter a parse tree produced by CopyCppParser#VarDeclStmt.
    def enterVarDeclStmt(self, ctx:CopyCppParser.VarDeclStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#VarDeclStmt.
    def exitVarDeclStmt(self, ctx:CopyCppParser.VarDeclStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#AssignStmt.
    def enterAssignStmt(self, ctx:CopyCppParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#AssignStmt.
    def exitAssignStmt(self, ctx:CopyCppParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#IfStmt.
    def enterIfStmt(self, ctx:CopyCppParser.IfStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#IfStmt.
    def exitIfStmt(self, ctx:CopyCppParser.IfStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#WhileStmt.
    def enterWhileStmt(self, ctx:CopyCppParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#WhileStmt.
    def exitWhileStmt(self, ctx:CopyCppParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ForStmt.
    def enterForStmt(self, ctx:CopyCppParser.ForStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ForStmt.
    def exitForStmt(self, ctx:CopyCppParser.ForStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ForeachStmt.
    def enterForeachStmt(self, ctx:CopyCppParser.ForeachStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ForeachStmt.
    def exitForeachStmt(self, ctx:CopyCppParser.ForeachStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#FuncDeclStmt.
    def enterFuncDeclStmt(self, ctx:CopyCppParser.FuncDeclStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#FuncDeclStmt.
    def exitFuncDeclStmt(self, ctx:CopyCppParser.FuncDeclStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ReturnStmt.
    def enterReturnStmt(self, ctx:CopyCppParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ReturnStmt.
    def exitReturnStmt(self, ctx:CopyCppParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#YieldStmt.
    def enterYieldStmt(self, ctx:CopyCppParser.YieldStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#YieldStmt.
    def exitYieldStmt(self, ctx:CopyCppParser.YieldStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#PrintStmt.
    def enterPrintStmt(self, ctx:CopyCppParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#PrintStmt.
    def exitPrintStmt(self, ctx:CopyCppParser.PrintStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ReadStmt.
    def enterReadStmt(self, ctx:CopyCppParser.ReadStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ReadStmt.
    def exitReadStmt(self, ctx:CopyCppParser.ReadStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#BlockStmt.
    def enterBlockStmt(self, ctx:CopyCppParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#BlockStmt.
    def exitBlockStmt(self, ctx:CopyCppParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#StructDeclStmt.
    def enterStructDeclStmt(self, ctx:CopyCppParser.StructDeclStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#StructDeclStmt.
    def exitStructDeclStmt(self, ctx:CopyCppParser.StructDeclStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ClassDeclStmt.
    def enterClassDeclStmt(self, ctx:CopyCppParser.ClassDeclStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ClassDeclStmt.
    def exitClassDeclStmt(self, ctx:CopyCppParser.ClassDeclStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ExprStmt.
    def enterExprStmt(self, ctx:CopyCppParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ExprStmt.
    def exitExprStmt(self, ctx:CopyCppParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by CopyCppParser#CommentStmt.
    def enterCommentStmt(self, ctx:CopyCppParser.CommentStmtContext):
        pass

    # Exit a parse tree produced by CopyCppParser#CommentStmt.
    def exitCommentStmt(self, ctx:CopyCppParser.CommentStmtContext):
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


    # Enter a parse tree produced by CopyCppParser#foreachStatement.
    def enterForeachStatement(self, ctx:CopyCppParser.ForeachStatementContext):
        pass

    # Exit a parse tree produced by CopyCppParser#foreachStatement.
    def exitForeachStatement(self, ctx:CopyCppParser.ForeachStatementContext):
        pass


    # Enter a parse tree produced by CopyCppParser#structDecl.
    def enterStructDecl(self, ctx:CopyCppParser.StructDeclContext):
        pass

    # Exit a parse tree produced by CopyCppParser#structDecl.
    def exitStructDecl(self, ctx:CopyCppParser.StructDeclContext):
        pass


    # Enter a parse tree produced by CopyCppParser#structMember.
    def enterStructMember(self, ctx:CopyCppParser.StructMemberContext):
        pass

    # Exit a parse tree produced by CopyCppParser#structMember.
    def exitStructMember(self, ctx:CopyCppParser.StructMemberContext):
        pass


    # Enter a parse tree produced by CopyCppParser#classDecl.
    def enterClassDecl(self, ctx:CopyCppParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by CopyCppParser#classDecl.
    def exitClassDecl(self, ctx:CopyCppParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by CopyCppParser#classMember.
    def enterClassMember(self, ctx:CopyCppParser.ClassMemberContext):
        pass

    # Exit a parse tree produced by CopyCppParser#classMember.
    def exitClassMember(self, ctx:CopyCppParser.ClassMemberContext):
        pass


    # Enter a parse tree produced by CopyCppParser#constructorDecl.
    def enterConstructorDecl(self, ctx:CopyCppParser.ConstructorDeclContext):
        pass

    # Exit a parse tree produced by CopyCppParser#constructorDecl.
    def exitConstructorDecl(self, ctx:CopyCppParser.ConstructorDeclContext):
        pass


    # Enter a parse tree produced by CopyCppParser#GeneratorFuncDecl.
    def enterGeneratorFuncDecl(self, ctx:CopyCppParser.GeneratorFuncDeclContext):
        pass

    # Exit a parse tree produced by CopyCppParser#GeneratorFuncDecl.
    def exitGeneratorFuncDecl(self, ctx:CopyCppParser.GeneratorFuncDeclContext):
        pass


    # Enter a parse tree produced by CopyCppParser#NonGeneratorFuncDecl.
    def enterNonGeneratorFuncDecl(self, ctx:CopyCppParser.NonGeneratorFuncDeclContext):
        pass

    # Exit a parse tree produced by CopyCppParser#NonGeneratorFuncDecl.
    def exitNonGeneratorFuncDecl(self, ctx:CopyCppParser.NonGeneratorFuncDeclContext):
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


    # Enter a parse tree produced by CopyCppParser#yieldStatement.
    def enterYieldStatement(self, ctx:CopyCppParser.YieldStatementContext):
        pass

    # Exit a parse tree produced by CopyCppParser#yieldStatement.
    def exitYieldStatement(self, ctx:CopyCppParser.YieldStatementContext):
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


    # Enter a parse tree produced by CopyCppParser#BoolLiteralExpr.
    def enterBoolLiteralExpr(self, ctx:CopyCppParser.BoolLiteralExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#BoolLiteralExpr.
    def exitBoolLiteralExpr(self, ctx:CopyCppParser.BoolLiteralExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ArrayAccess1DExpr.
    def enterArrayAccess1DExpr(self, ctx:CopyCppParser.ArrayAccess1DExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ArrayAccess1DExpr.
    def exitArrayAccess1DExpr(self, ctx:CopyCppParser.ArrayAccess1DExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#IdExpr.
    def enterIdExpr(self, ctx:CopyCppParser.IdExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#IdExpr.
    def exitIdExpr(self, ctx:CopyCppParser.IdExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#XorExpr.
    def enterXorExpr(self, ctx:CopyCppParser.XorExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#XorExpr.
    def exitXorExpr(self, ctx:CopyCppParser.XorExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#NewObjectExpr.
    def enterNewObjectExpr(self, ctx:CopyCppParser.NewObjectExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#NewObjectExpr.
    def exitNewObjectExpr(self, ctx:CopyCppParser.NewObjectExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#StringLiteralExpr.
    def enterStringLiteralExpr(self, ctx:CopyCppParser.StringLiteralExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#StringLiteralExpr.
    def exitStringLiteralExpr(self, ctx:CopyCppParser.StringLiteralExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#RelationalExpr.
    def enterRelationalExpr(self, ctx:CopyCppParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#RelationalExpr.
    def exitRelationalExpr(self, ctx:CopyCppParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#LogicalAndExpr.
    def enterLogicalAndExpr(self, ctx:CopyCppParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#LogicalAndExpr.
    def exitLogicalAndExpr(self, ctx:CopyCppParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#NullLiteralExpr.
    def enterNullLiteralExpr(self, ctx:CopyCppParser.NullLiteralExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#NullLiteralExpr.
    def exitNullLiteralExpr(self, ctx:CopyCppParser.NullLiteralExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#MultiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:CopyCppParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#MultiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:CopyCppParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#LogicalOrExpr.
    def enterLogicalOrExpr(self, ctx:CopyCppParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#LogicalOrExpr.
    def exitLogicalOrExpr(self, ctx:CopyCppParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#IntLiteralExpr.
    def enterIntLiteralExpr(self, ctx:CopyCppParser.IntLiteralExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#IntLiteralExpr.
    def exitIntLiteralExpr(self, ctx:CopyCppParser.IntLiteralExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#FunctionCallExpr.
    def enterFunctionCallExpr(self, ctx:CopyCppParser.FunctionCallExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#FunctionCallExpr.
    def exitFunctionCallExpr(self, ctx:CopyCppParser.FunctionCallExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#EqualityExpr.
    def enterEqualityExpr(self, ctx:CopyCppParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#EqualityExpr.
    def exitEqualityExpr(self, ctx:CopyCppParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#AdditiveExpr.
    def enterAdditiveExpr(self, ctx:CopyCppParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#AdditiveExpr.
    def exitAdditiveExpr(self, ctx:CopyCppParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#FloatLiteralExpr.
    def enterFloatLiteralExpr(self, ctx:CopyCppParser.FloatLiteralExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#FloatLiteralExpr.
    def exitFloatLiteralExpr(self, ctx:CopyCppParser.FloatLiteralExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#FieldAccessExpr.
    def enterFieldAccessExpr(self, ctx:CopyCppParser.FieldAccessExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#FieldAccessExpr.
    def exitFieldAccessExpr(self, ctx:CopyCppParser.FieldAccessExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#UnaryOpExpr.
    def enterUnaryOpExpr(self, ctx:CopyCppParser.UnaryOpExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#UnaryOpExpr.
    def exitUnaryOpExpr(self, ctx:CopyCppParser.UnaryOpExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ParenExpr.
    def enterParenExpr(self, ctx:CopyCppParser.ParenExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ParenExpr.
    def exitParenExpr(self, ctx:CopyCppParser.ParenExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#ArrayAccess2DExpr.
    def enterArrayAccess2DExpr(self, ctx:CopyCppParser.ArrayAccess2DExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#ArrayAccess2DExpr.
    def exitArrayAccess2DExpr(self, ctx:CopyCppParser.ArrayAccess2DExprContext):
        pass


    # Enter a parse tree produced by CopyCppParser#MethodCallExpr.
    def enterMethodCallExpr(self, ctx:CopyCppParser.MethodCallExprContext):
        pass

    # Exit a parse tree produced by CopyCppParser#MethodCallExpr.
    def exitMethodCallExpr(self, ctx:CopyCppParser.MethodCallExprContext):
        pass



del CopyCppParser