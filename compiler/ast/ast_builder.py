# compiler/ast_builder.py
from grammar.CopyCppParser import CopyCppParser  # Adjust if your path is different
from grammar.CopyCppVisitor import CopyCppVisitor  # Adjust if your path is different
from .nodes import *
from antlr4.tree.Tree import TerminalNodeImpl


class ASTBuilder(CopyCppVisitor):
    def __init__(self, debug=True):
        self.debug = debug

    def log(self, message):
        if self.debug:
            print(f"DEBUG AST: {message}")

    # Top-level rule
    def visitProgram(self, ctx: CopyCppParser.ProgramContext):
        self.log("Visiting Program")
        statements = []
        for stmt_ctx in ctx.statement():
            stmt_node = self.visit(stmt_ctx)
            if stmt_node:  # Filter out None if CommentStmt is visited and returns None
                statements.append(stmt_node)
        return ProgramNode(statements)

    # Dispatcher for statements (using labels)
    # ANTLR's default visit method will call the specific visit<LabelName> methods.
    # We just need to implement them.

    def visitBlock(self, ctx: CopyCppParser.BlockContext):
        self.log(f"Visiting Block with {len(ctx.statement())} statements")
        statements = []
        for stmt_ctx in ctx.statement():
            stmt_node = self.visit(stmt_ctx)
            if stmt_node:
                statements.append(stmt_node)
        return BlockNode(statements)

    # --- Statement Visitor Methods (from labeled alternatives) ---
    def visitVarDeclStmt(self, ctx: CopyCppParser.VarDeclStmtContext):
        self.log("Visiting VarDeclStmt")
        return self.visit(ctx.varDeclaration())

    def visitAssignStmt(self, ctx: CopyCppParser.AssignStmtContext):
        self.log("Visiting AssignStmt")
        return self.visit(ctx.assignment())

    def visitIfStmt(self, ctx: CopyCppParser.IfStmtContext):
        self.log("Visiting IfStmt")
        return self.visit(ctx.ifStatement())

    def visitWhileStmt(self, ctx: CopyCppParser.WhileStmtContext):
        self.log("Visiting WhileStmt")
        return self.visit(ctx.whileStatement())

    def visitForStmt(self, ctx: CopyCppParser.ForStmtContext):
        self.log("Visiting ForStmt")
        return self.visit(ctx.forStatement())

    def visitForeachStmt(self, ctx: CopyCppParser.ForeachStmtContext):
        self.log("Visiting ForeachStmt")
        return self.visit(ctx.foreachStatement())

    def visitFuncDeclStmt(self, ctx: CopyCppParser.FuncDeclStmtContext):
        self.log("Visiting FuncDeclStmt")
        return self.visit(ctx.functionDecl())

    def visitReturnStmt(self, ctx: CopyCppParser.ReturnStmtContext):
        self.log("Visiting ReturnStmt")
        return self.visit(ctx.returnStatement())

    def visitYieldStmt(self, ctx: CopyCppParser.YieldStmtContext):
        self.log("Visiting YieldStmt")
        return self.visit(ctx.yieldStatement())

    def visitPrintStmt(self, ctx: CopyCppParser.PrintStmtContext):
        self.log("Visiting PrintStmt")
        return self.visit(ctx.printStatement())

    def visitReadStmt(self, ctx: CopyCppParser.ReadStmtContext):
        self.log("Visiting ReadStmt")
        return self.visit(ctx.readStatement())

    def visitBlockStmt(self, ctx: CopyCppParser.BlockStmtContext):  # For standalone blocks if needed
        self.log("Visiting BlockStmt")
        return self.visit(ctx.block())

    def visitStructDeclStmt(self, ctx: CopyCppParser.StructDeclStmtContext):
        self.log("Visiting StructDeclStmt")
        return self.visit(ctx.structDecl())

    def visitClassDeclStmt(self, ctx: CopyCppParser.ClassDeclStmtContext):
        self.log("Visiting ClassDeclStmt")
        return self.visit(ctx.classDecl())

    def visitExprStmt(self, ctx: CopyCppParser.ExprStmtContext):
        self.log("Visiting ExprStmt")
        expr_node = self.visit(ctx.expr())
        # If the expression itself is a function call, wrap it for statement context
        if isinstance(expr_node, FunctionCallNode):
            return FunctionCallStatementNode(expr_node)
        return expr_node  # Or a generic ExpressionStatementNode(expr_node)

    def visitCommentStmt(self, ctx: CopyCppParser.CommentStmtContext):
        self.log("Visiting CommentStmt (skipping)")
        return None  # Comments don't usually become AST nodes for execution

    # --- Implementations for specific rule contexts ---

    def visitVarDeclaration(self, ctx: CopyCppParser.VarDeclarationContext):
        type_name_str = "var"  # Default for 'var' keyword
        if ctx.type_():  # If type rule is present
            type_name_str = self.visit(ctx.type_())

        var_name = ctx.ID().getText()
        initial_value_node = None
        if ctx.expr():  # If there's an expression (either for init or array size)
            # Check if it's an array declaration first
            if ctx.LBRACK():  # type ID '[' expr ']' or type ID '[' expr ']' '[' expr ']'
                dimensions = [self.visit(e) for e in ctx.expr()]  # All exprs are dimensions here
                self.log(f"  VarDecl: Array '{var_name}', type '{type_name_str}', dims: {len(dimensions)}")
                return VarDeclarationNode(type_name_str, var_name, None, dimensions)
            else:  # Simple var with potential initializer: type ID ('=' expr)? or 'var' ID '=' expr
                initial_value_node = self.visit(ctx.expr(0))  # Only one expr for initializer
                self.log(f"  VarDecl: Scalar '{var_name}', type '{type_name_str}', with initializer")
                return VarDeclarationNode(type_name_str, var_name, initial_value_node, [])
        else:  # No expr, so no initializer and not an array decl of the form ID[expr]
            self.log(f"  VarDecl: Scalar '{var_name}', type '{type_name_str}', no initializer")
            return VarDeclarationNode(type_name_str, var_name, None, [])

    def visitType(self, ctx: CopyCppParser.TypeContext):
        return ctx.getText()  # K_INT, K_FLOAT32, ID, etc.

    def visitAssignment(self, ctx: CopyCppParser.AssignmentContext):
        target_id_token = ctx.ID(0)  # First ID is always the base target
        value_node = self.visit(ctx.expr(len(ctx.expr()) - 1))  # Value is always the last expr

        if ctx.DOT():  # Field assignment: ID '.' ID '=' expr
            obj_ref = VarReferenceNode(target_id_token.getText())
            field_name = ctx.ID(1).getText()
            target_node = FieldAccessNode(obj_ref, field_name)
            self.log(f"  Assignment to field: {target_id_token.getText()}.{field_name}")
        elif ctx.LBRACK():  # Array assignment
            array_ref = VarReferenceNode(target_id_token.getText())
            indices = [self.visit(e) for e in ctx.expr()[:-1]]  # All exprs except the last one (value)
            target_node = ArrayAccessNode(array_ref, indices)
            self.log(f"  Assignment to array: {target_id_token.getText()} with {len(indices)} indices")
        else:  # Simple variable assignment: ID '=' expr
            target_node = VarReferenceNode(target_id_token.getText())
            self.log(f"  Assignment to var: {target_id_token.getText()}")

        return AssignmentNode(target_node, value_node)

    def visitIfStatement(self, ctx: CopyCppParser.IfStatementContext):
        condition = self.visit(ctx.expr())
        then_branch = self.visit(ctx.statement(0))
        else_branch = None
        if ctx.K_ELSE():
            else_branch = self.visit(ctx.statement(1))
        return IfStatementNode(condition, then_branch, else_branch)

    def visitWhileStatement(self, ctx: CopyCppParser.WhileStatementContext):
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.statement())
        return WhileStatementNode(condition, body)

    def visitForStatement(self, ctx: CopyCppParser.ForStatementContext):
        # statement expr SEMI expr
        init_stmt = self.visit(ctx.statement(0))  # The first statement is init
        condition_expr = self.visit(ctx.expr(0))  # First expr is condition
        update_expr = self.visit(ctx.expr(1))  # Second expr is update
        body_stmt = self.visit(ctx.statement(1))  # Second statement is body
        return ForStatementNode(init_stmt, condition_expr, update_expr, body_stmt)

    def visitForeachStatement(self, ctx: CopyCppParser.ForeachStatementContext):
        var_type_str = ctx.type_().getText() if ctx.type_() else ctx.K_VAR().getText()
        var_name = ctx.ID().getText()
        iterable_expr = self.visit(ctx.expr())
        body_stmt = self.visit(ctx.statement())
        return ForeachStatementNode(var_type_str, var_name, iterable_expr, body_stmt)

    def visitStructDecl(self, ctx: CopyCppParser.StructDeclContext):
        name = ctx.ID().getText()
        members = [self.visit(sm) for sm in ctx.structMember()]
        return StructDeclNode(name, members)

    def visitStructMember(self, ctx: CopyCppParser.StructMemberContext):
        if ctx.varDeclaration():
            return self.visit(ctx.varDeclaration())
        elif ctx.functionDecl():
            return self.visit(ctx.functionDecl())
        return None

    def visitClassDecl(self, ctx: CopyCppParser.ClassDeclContext):
        name = ctx.ID(0).getText()
        parent_name = ctx.ID(1).getText() if ctx.K_EXTENDS() else None

        private_members, public_members, protected_members = [], [], []
        # This parsing of members needs to be careful due to optionality and order
        current_section = public_members  # Default if no explicit specifier first

        for child_idx in range(ctx.getChildCount()):  # Iterate all children of classDecl
            child = ctx.getChild(child_idx)
            if isinstance(child, TerminalNodeImpl):  # Check if it's a token
                token_text = child.getText()
                if token_text == 'private:':
                    current_section = private_members
                elif token_text == 'public:':
                    current_section = public_members
                elif token_text == 'protected:':
                    current_section = protected_members
            elif isinstance(child, CopyCppParser.ClassMemberContext):
                member_node = self.visit(child)
                if member_node:
                    current_section.append(member_node)

        return ClassDeclNode(name, parent_name, private_members, public_members, protected_members)

    def visitClassMember(self, ctx: CopyCppParser.ClassMemberContext):
        if ctx.varDeclaration(): return self.visit(ctx.varDeclaration())
        if ctx.functionDecl(): return self.visit(ctx.functionDecl())
        if ctx.constructorDecl(): return self.visit(ctx.constructorDecl())
        return None

    def visitConstructorDecl(self, ctx: CopyCppParser.ConstructorDeclContext):
        class_name = ctx.ID().getText()  # Should match class name
        params = self.visit(ctx.formalParams()) if ctx.formalParams() else []
        body = self.visit(ctx.block())
        return ConstructorDeclNode(class_name, params, body)

    def visitActualParams(self, ctx:CopyCppParser.ActualParamsContext):
        self.log(f"Visiting ActualParams context. It has {len(ctx.expr())} direct expr children.")
        args_nodes = []
        if ctx.expr(): # expr is a list of expression contexts for each argument
            for i, expr_child_ctx in enumerate(ctx.expr()):
                self.log(f"  ActualParams: Visiting argument expr child {i}: '{expr_child_ctx.getText()}'")
                arg_node = self.visit(expr_child_ctx) # This should return an AST node for the argument
                if arg_node:
                    args_nodes.append(arg_node)
                else:
                    self.log(f"  WARNING AST: ActualParams - argument expr '{expr_child_ctx.getText()}' resulted in None AST node.")
        self.log(f"  ActualParams returning list of {len(args_nodes)} AST argument nodes.")
        return args_nodes # Always return a list

    def visitFunctionDecl(self, ctx: CopyCppParser.FunctionDeclContext):
        type_name_str = self.visit(ctx.type_()) if ctx.type_() else ctx.K_GENERATOR().getText()
        is_generator = bool(ctx.K_GENERATOR())
        name = ctx.ID().getText()
        params = self.visit(ctx.formalParams()) if ctx.formalParams() else []
        body = self.visit(ctx.block())
        return FunctionDeclNode(type_name_str, name, params, body, is_generator)

    def visitFormalParams(self, ctx: CopyCppParser.FormalParamsContext):
        return [self.visit(fp) for fp in ctx.formalParam()]

    def visitFormalParam(self, ctx: CopyCppParser.FormalParamContext):
        param_type = self.visit(ctx.type_()) if ctx.type_() else ctx.K_VAR().getText()
        param_name = ctx.ID().getText()
        dimensions = []  # For array parameters
        # type ID LBRACK RBRACK (LBRACK RBRACK)?
        # type ID LBRACK expr RBRACK (LBRACK expr RBRACK)?
        if ctx.LBRACK(0):  # At least one LBRACK exists
            if ctx.expr(0):  # type ID [expr]
                dimensions.append(self.visit(ctx.expr(0)))
                if ctx.LBRACK(1) and ctx.expr(1):  # type ID [expr][expr]
                    dimensions.append(self.visit(ctx.expr(1)))
            else:  # type ID []
                dimensions.append(None)  # Placeholder for unsized dimension
                if ctx.LBRACK(1) and not ctx.expr(0):  # type ID [][] (assuming expr(0) would be first if present)
                    # This logic for unsized 2D needs care. If expr(0) is for first dim, expr(1) for second.
                    # If type ID [] [], then expr list is empty.
                    if not ctx.expr():  # No expressions at all
                        if ctx.LBRACK(1): dimensions.append(None)
                    # This part of grammar for formalParam array might need refinement for clarity
                    # For now, if LBRACK exists and no corresponding expr, it's unsized for that dim.

        return {'type': param_type, 'name': param_name, 'dimensions': dimensions}

    def visitReturnStatement(self, ctx: CopyCppParser.ReturnStatementContext):
        value_node = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStatementNode(value_node)

    def visitYieldStatement(self, ctx: CopyCppParser.YieldStatementContext):
        return YieldStatementNode(self.visit(ctx.expr()))

    def visitPrintStatement(self, ctx: CopyCppParser.PrintStatementContext):
        return PrintStatementNode(self.visit(ctx.expr()))

    def visitReadStatement(self, ctx: CopyCppParser.ReadStatementContext):
        return ReadStatementNode(ctx.ID().getText())

    # --- Expression Visitor Methods (from labeled alternatives) ---

    def visitParenExpr(self, ctx: CopyCppParser.ParenExprContext):
        self.log(f"  Visiting ParenExpr: {ctx.expr().getText()}")
        return self.visit(ctx.expr())

    def visitUnaryOpExpr(self, ctx: CopyCppParser.UnaryOpExprContext):
        op = ctx.getChild(0).getText()  # '-' or '!'
        operand = self.visit(ctx.expr())
        self.log(f"  Visiting UnaryOpExpr: {op}{type(operand).__name__}")
        return UnaryOpNode(op, operand)

    def visitMultiplicativeExpr(self, ctx: CopyCppParser.MultiplicativeExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text  # op is the token for '*', '/', or '%'
        self.log(f"  Visiting MultiplicativeExpr: {type(left).__name__} {op} {type(right).__name__}")
        return BinaryOpNode(left, op, right)

    def visitAdditiveExpr(self, ctx: CopyCppParser.AdditiveExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text  # '+' or '-'
        self.log(f"  Visiting AdditiveExpr: {type(left).__name__} {op} {type(right).__name__}")
        return BinaryOpNode(left, op, right)

    def visitRelationalExpr(self, ctx: CopyCppParser.RelationalExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text  # '<', '>', '<=', '>='
        self.log(f"  Visiting RelationalExpr: {type(left).__name__} {op} {type(right).__name__}")
        return BinaryOpNode(left, op, right)

    def visitEqualityExpr(self, ctx: CopyCppParser.EqualityExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text  # '==' or '!='
        self.log(f"  Visiting EqualityExpr: {type(left).__name__} {op} {type(right).__name__}")
        return BinaryOpNode(left, op, right)

    def visitLogicalAndExpr(self, ctx: CopyCppParser.LogicalAndExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.AND_OP().getText()  # '&&'
        self.log(f"  Visiting LogicalAndExpr: {type(left).__name__} {op} {type(right).__name__}")
        return BinaryOpNode(left, op, right)

    def visitLogicalOrExpr(self, ctx: CopyCppParser.LogicalOrExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.OR_OP().getText()  # '||'
        self.log(f"  Visiting LogicalOrExpr: {type(left).__name__} {op} {type(right).__name__}")
        return BinaryOpNode(left, op, right)

    def visitXorExpr(self, ctx: CopyCppParser.XorExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.XOR_OP().getText()  # '^'
        self.log(f"  Visiting XorExpr: {type(left).__name__} {op} {type(right).__name__}")
        return BinaryOpNode(left, op, right)

    def visitMethodCallExpr(self, ctx: CopyCppParser.MethodCallExprContext):
        obj_expr = self.visit(ctx.expr())  # The object is the first 'expr'
        method_name = ctx.ID().getText()
        args = self.visit(ctx.actualParams()) if ctx.actualParams() else []
        self.log(f"  Visiting MethodCallExpr: {type(obj_expr).__name__}.{method_name} with {len(args)} args")
        return MethodCallNode(obj_expr, method_name, args)

    def visitFieldAccessExpr(self, ctx: CopyCppParser.FieldAccessExprContext):
        obj_expr = self.visit(ctx.expr())  # The object is the 'expr'
        field_name = ctx.ID().getText()
        self.log(f"  Visiting FieldAccessExpr: {type(obj_expr).__name__}.{field_name}")
        return FieldAccessNode(obj_expr, field_name)

    def visitNewObjectExpr(self, ctx: CopyCppParser.NewObjectExprContext):
        class_name = ctx.ID().getText()
        args = self.visit(ctx.actualParams()) if ctx.actualParams() else []
        self.log(f"  Visiting NewObjectExpr: new {class_name} with {len(args)} args")
        return ObjectInstantiationNode(class_name, args)

    def visitFunctionCallExpr(self, ctx: CopyCppParser.FunctionCallExprContext):
        func_name = ctx.ID().getText()

        # actualParams() returns an ActualParamsContext or None
        # self.visit(ActualParamsContext) should return a list of AST nodes
        args_ast_nodes = []  # Default to an empty list
        if ctx.actualParams():
            self.log(f"  FunctionCallExpr '{func_name}': Found actualParams. Visiting it.")
            # visitActualParams is guaranteed to return a list by its implementation
            args_ast_nodes = self.visit(ctx.actualParams())
            if not isinstance(args_ast_nodes, list):
                # This case should ideally not happen if visitActualParams is correct
                self.log(
                    f"  ERROR AST: visitActualParams for '{func_name}' did not return a list! Got: {type(args_ast_nodes)}. Forcing to empty list.")
                args_ast_nodes = []
        else:
            self.log(f"  FunctionCallExpr '{func_name}': No actualParams found.")

        self.log(f"  Visiting FunctionCallExpr: {func_name} with {len(args_ast_nodes)} args")
        return FunctionCallNode(func_name, args_ast_nodes)

    def visitArrayAccess1DExpr(self, ctx: CopyCppParser.ArrayAccess1DExprContext):
        array_name = ctx.ID().getText()
        index_expr = self.visit(ctx.expr())  # The single expr is the index
        self.log(f"  Visiting ArrayAccess1DExpr: {array_name}[{type(index_expr).__name__}]")
        return ArrayAccessNode(VarReferenceNode(array_name), [index_expr])

    def visitArrayAccess2DExpr(self, ctx: CopyCppParser.ArrayAccess2DExprContext):
        array_name = ctx.ID().getText()
        # expr(0) is the first index, expr(1) is the second index
        index1_expr = self.visit(ctx.expr(0))
        index2_expr = self.visit(ctx.expr(1))
        self.log(
            f"  Visiting ArrayAccess2DExpr: {array_name}[{type(index1_expr).__name__}][{type(index2_expr).__name__}]")
        return ArrayAccessNode(VarReferenceNode(array_name), [index1_expr, index2_expr])

    def visitIdExpr(self, ctx: CopyCppParser.IdExprContext):
        name = ctx.ID().getText()
        self.log(f"  Visiting IdExpr: {name}")
        return VarReferenceNode(name)

    def visitIntLiteralExpr(self, ctx: CopyCppParser.IntLiteralExprContext):
        val = int(ctx.INT().getText())
        self.log(f"  Visiting IntLiteralExpr: {val}")
        return LiteralNode(val, "int")

    def visitFloatLiteralExpr(self, ctx: CopyCppParser.FloatLiteralExprContext):
        val = float(ctx.FLOAT().getText())
        self.log(f"  Visiting FloatLiteralExpr: {val}")
        return LiteralNode(val, "float64")  # Default to float64

    def visitBoolLiteralExpr(self, ctx: CopyCppParser.BoolLiteralExprContext):
        val = ctx.BOOL().getText() == 'true'
        self.log(f"  Visiting BoolLiteralExpr: {val}")
        return LiteralNode(val, "bool")

    def visitStringLiteralExpr(self, ctx: CopyCppParser.StringLiteralExprContext):
        val = ctx.STRING().getText()[1:-1]  # Remove quotes
        self.log(f"  Visiting StringLiteralExpr: \"{val}\"")
        return LiteralNode(val, "string")

    def visitNullLiteralExpr(self, ctx: CopyCppParser.NullLiteralExprContext):
        self.log(f"  Visiting NullLiteralExpr")
        return NullLiteralNode()

    def visitNonGeneratorFuncDecl(self, ctx:CopyCppParser.NonGeneratorFuncDeclContext):
        self.log("Visiting NonGeneratorFuncDecl")
        # ctx.type_() odnosi się do reguły 'type' w tej alternatywie
        # ctx.ID() odnosi się do tokenu ID (nazwa funkcji)
        # ctx.formalParams() odnosi się do opcjonalnej reguły 'formalParams'
        # ctx.block() odnosi się do reguły 'block'

        type_name_str = self.visit(ctx.type_())
        name = ctx.ID().getText()
        params = self.visit(ctx.formalParams()) if ctx.formalParams() else []
        body = self.visit(ctx.block())

        self.log(f"  Created Non-Generator Function: Name='{name}', Type='{type_name_str}'")
        return FunctionDeclNode(type_name_str, name, params, body, is_generator=False)

    def visitGeneratorFuncDecl(self, ctx: CopyCppParser.GeneratorFuncDeclContext):
        self.log("Visiting GeneratorFuncDecl")
        # ctx.K_GENERATOR() odnosi się do tokenu 'generator'
        # ctx.type_() odnosi się do reguły 'type' (typ wartości yield)
        # ctx.ID() odnosi się do tokenu ID (nazwa funkcji generatora)
        # ctx.formalParams() odnosi się do opcjonalnej reguły 'formalParams'
        # ctx.block() odnosi się do reguły 'block'

        # Typ zwracany przez yield
        type_name_str = self.visit(ctx.type_())
        name = ctx.ID().getText()
        params = self.visit(ctx.formalParams()) if ctx.formalParams() else []
        body = self.visit(ctx.block())

        self.log(f"  Created Generator Function: Name='{name}', YieldType='{type_name_str}'")
        # Przekazujemy typ wartości yield jako 'type_name' do FunctionDeclNode,
        # a flaga is_generator=True rozróżni go.
        return FunctionDeclNode(type_name_str, name, params, body, is_generator=True)

        # Upewnij się, że visitFuncDeclStmt nadal istnieje i deleguje:


