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


    # Visit a parse tree produced by CopyCppParser#VarDeclStmt.
    def visitVarDeclStmt(self, ctx:CopyCppParser.VarDeclStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#AssignStmt.
    def visitAssignStmt(self, ctx:CopyCppParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#IfStmt.
    def visitIfStmt(self, ctx:CopyCppParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#WhileStmt.
    def visitWhileStmt(self, ctx:CopyCppParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ForStmt.
    def visitForStmt(self, ctx:CopyCppParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ForeachStmt.
    def visitForeachStmt(self, ctx:CopyCppParser.ForeachStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#FuncDeclStmt.
    def visitFuncDeclStmt(self, ctx:CopyCppParser.FuncDeclStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ReturnStmt.
    def visitReturnStmt(self, ctx:CopyCppParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#YieldStmt.
    def visitYieldStmt(self, ctx:CopyCppParser.YieldStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#PrintStmt.
    def visitPrintStmt(self, ctx:CopyCppParser.PrintStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ReadStmt.
    def visitReadStmt(self, ctx:CopyCppParser.ReadStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#BlockStmt.
    def visitBlockStmt(self, ctx:CopyCppParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#StructDeclStmt.
    def visitStructDeclStmt(self, ctx:CopyCppParser.StructDeclStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ClassDeclStmt.
    def visitClassDeclStmt(self, ctx:CopyCppParser.ClassDeclStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ExprStmt.
    def visitExprStmt(self, ctx:CopyCppParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#CommentStmt.
    def visitCommentStmt(self, ctx:CopyCppParser.CommentStmtContext):
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


    # Visit a parse tree produced by CopyCppParser#foreachStatement.
    def visitForeachStatement(self, ctx:CopyCppParser.ForeachStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#structDecl.
    def visitStructDecl(self, ctx:CopyCppParser.StructDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#structMember.
    def visitStructMember(self, ctx:CopyCppParser.StructMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#classDecl.
    def visitClassDecl(self, ctx:CopyCppParser.ClassDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#classMember.
    def visitClassMember(self, ctx:CopyCppParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#constructorDecl.
    def visitConstructorDecl(self, ctx:CopyCppParser.ConstructorDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#GeneratorFuncDecl.
    def visitGeneratorFuncDecl(self, ctx:CopyCppParser.GeneratorFuncDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#NonGeneratorFuncDecl.
    def visitNonGeneratorFuncDecl(self, ctx:CopyCppParser.NonGeneratorFuncDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#formalParams.
    def visitFormalParams(self, ctx:CopyCppParser.FormalParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#formalParam.
    def visitFormalParam(self, ctx:CopyCppParser.FormalParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#actualParams.
    def visitActualParams(self, ctx:CopyCppParser.ActualParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#returnStatement.
    def visitReturnStatement(self, ctx:CopyCppParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#yieldStatement.
    def visitYieldStatement(self, ctx:CopyCppParser.YieldStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#printStatement.
    def visitPrintStatement(self, ctx:CopyCppParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#readStatement.
    def visitReadStatement(self, ctx:CopyCppParser.ReadStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#BoolLiteralExpr.
    def visitBoolLiteralExpr(self, ctx:CopyCppParser.BoolLiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ArrayAccess1DExpr.
    def visitArrayAccess1DExpr(self, ctx:CopyCppParser.ArrayAccess1DExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#IdExpr.
    def visitIdExpr(self, ctx:CopyCppParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#XorExpr.
    def visitXorExpr(self, ctx:CopyCppParser.XorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#NewObjectExpr.
    def visitNewObjectExpr(self, ctx:CopyCppParser.NewObjectExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#StringLiteralExpr.
    def visitStringLiteralExpr(self, ctx:CopyCppParser.StringLiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#RelationalExpr.
    def visitRelationalExpr(self, ctx:CopyCppParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#LogicalAndExpr.
    def visitLogicalAndExpr(self, ctx:CopyCppParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#NullLiteralExpr.
    def visitNullLiteralExpr(self, ctx:CopyCppParser.NullLiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#MultiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:CopyCppParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#LogicalOrExpr.
    def visitLogicalOrExpr(self, ctx:CopyCppParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#IntLiteralExpr.
    def visitIntLiteralExpr(self, ctx:CopyCppParser.IntLiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#FunctionCallExpr.
    def visitFunctionCallExpr(self, ctx:CopyCppParser.FunctionCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#EqualityExpr.
    def visitEqualityExpr(self, ctx:CopyCppParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#AdditiveExpr.
    def visitAdditiveExpr(self, ctx:CopyCppParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#FloatLiteralExpr.
    def visitFloatLiteralExpr(self, ctx:CopyCppParser.FloatLiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#FieldAccessExpr.
    def visitFieldAccessExpr(self, ctx:CopyCppParser.FieldAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#UnaryOpExpr.
    def visitUnaryOpExpr(self, ctx:CopyCppParser.UnaryOpExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ParenExpr.
    def visitParenExpr(self, ctx:CopyCppParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#ArrayAccess2DExpr.
    def visitArrayAccess2DExpr(self, ctx:CopyCppParser.ArrayAccess2DExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CopyCppParser#MethodCallExpr.
    def visitMethodCallExpr(self, ctx:CopyCppParser.MethodCallExprContext):
        return self.visitChildren(ctx)



del CopyCppParser