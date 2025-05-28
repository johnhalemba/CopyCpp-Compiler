grammar CopyCpp;

// Parser Rules
program: statement+ EOF;

statement
    : varDeclaration                  # VarDeclStmt
    | assignment                      # AssignStmt
    | ifStatement                     # IfStmt
    | whileStatement                  # WhileStmt
    | forStatement                    # ForStmt
    | foreachStatement                # ForeachStmt
    | functionDecl                    # FuncDeclStmt
    | returnStatement                 # ReturnStmt
    | yieldStatement                  # YieldStmt
    | printStatement                  # PrintStmt
    | readStatement                   # ReadStmt
    | block                           # BlockStmt
    | structDecl                      # StructDeclStmt
    | classDecl                       # ClassDeclStmt
    | expr SEMI                       # ExprStmt // Handles function calls as statements, etc.
    | COMMENT                         # CommentStmt // (often skipped by visitor)
    ;

block: LBRACE statement* RBRACE;

varDeclaration
    : type ID (ASSIGN expr)? SEMI
    | K_VAR ID ASSIGN expr SEMI
    | type ID LBRACK expr RBRACK SEMI // 1D array declaration
    | type ID LBRACK expr RBRACK LBRACK expr RBRACK SEMI // 2D array declaration
    ;

type
    : K_INT
    | K_FLOAT32
    | K_FLOAT64
    | K_BOOL
    | K_STRING
    | K_VOID
    | ID  // For user-defined types (structs, classes)
    ;

assignment
    : ID ASSIGN expr SEMI
    | ID LBRACK expr RBRACK ASSIGN expr SEMI
    | ID LBRACK expr RBRACK LBRACK expr RBRACK ASSIGN expr SEMI
    | ID DOT ID ASSIGN expr SEMI
    ;

ifStatement
    : K_IF LPAREN expr RPAREN statement (K_ELSE statement)?
    ;

whileStatement
    : K_WHILE LPAREN expr RPAREN statement
    ;

forStatement
    // Example: for (int i = 0; i < 10; i = i + 1) { ... }
    // The first 'statement' in for is often a varDecl without SEMI or an assignment without SEMI.
    // For simplicity, let's assume the init part can be a full varDeclaration or an assignment (which includes SEMI).
    // Or, we can define a 'forInit' rule. Let's try to keep it simple:
    // For now, assume 'statement' for init is okay, but it might need refinement
    // if you want `int i = 0` without a semicolon inside the for-loop parentheses.
    // A common way is `for '(' (varDeclaration | exprList)? SEMI expr? SEMI exprList? ')' statement`
    // Let's stick to your current structure for now, but be aware of this.
    : K_FOR LPAREN statement expr SEMI expr RPAREN statement
    ;

foreachStatement
    : K_FOREACH LPAREN (type | K_VAR) ID K_IN expr RPAREN statement
    ;

structDecl
    : K_STRUCT ID LBRACE structMember* RBRACE SEMI
    ;

structMember
    : varDeclaration
    | functionDecl
    ;

classDecl
    : K_CLASS ID (K_EXTENDS ID)? LBRACE
      (K_PRIVATE COLON classMember*)?
      (K_PUBLIC COLON classMember*)?
      (K_PROTECTED COLON classMember*)?
      RBRACE SEMI
    ;

classMember
    : varDeclaration
    | functionDecl
    | constructorDecl
    ;

constructorDecl
    : ID LPAREN formalParams? RPAREN block // ID should match class name
    ;

functionDecl
    : K_GENERATOR type ID LPAREN formalParams? RPAREN block  # GeneratorFuncDecl
    | type ID LPAREN formalParams? RPAREN block             # NonGeneratorFuncDecl
    ;

formalParams
    : formalParam (COMMA formalParam)*
    ;

formalParam
    : type ID
    | K_VAR ID
    | type ID LBRACK RBRACK // Unsized array param: type id[]
    | type ID LBRACK RBRACK LBRACK RBRACK // Unsized 2D array param: type id[][]
    | type ID LBRACK expr RBRACK // Sized array param: type id[size]
    | type ID LBRACK expr RBRACK LBRACK expr RBRACK // Sized 2D array param: type id[size1][size2]
    ;

// functionCall rule is removed as it's now an alternative in 'expr' (FunctionCallExpr)
// and statements are handled by 'expr SEMI'

actualParams
    : expr (COMMA expr)*
    ;

returnStatement
    : K_RETURN expr? SEMI
    ;

yieldStatement
    : K_YIELD expr SEMI
    ;

printStatement
    : K_PRINT LPAREN expr RPAREN SEMI
    ;

readStatement
    : K_READ LPAREN ID RPAREN SEMI
    ;

// Expression rule with labeled alternatives for visitor generation
// Order implies precedence (higher precedence rules are generally matched first by ANTLR's interpretation of left-recursion)
expr
    : LPAREN expr RPAREN                  # ParenExpr
    | BOOL                                # BoolLiteralExpr
    | (MINUS | NOT) expr                  # UnaryOpExpr
    | expr op=(STAR | SLASH | MOD) expr   # MultiplicativeExpr
    | expr op=(PLUS | MINUS) expr         # AdditiveExpr
    | expr op=(LT | GT | LTE | GTE) expr  # RelationalExpr
    | expr op=(EQ | NEQ) expr             # EqualityExpr
    | expr AND_OP expr                    # LogicalAndExpr
    | expr OR_OP expr                     # LogicalOrExpr
    | expr XOR_OP expr                    # XorExpr
    | expr DOT ID LPAREN actualParams? RPAREN # MethodCallExpr
    | expr DOT ID                         # FieldAccessExpr
    | K_NEW ID LPAREN actualParams? RPAREN  # NewObjectExpr
    | ID LPAREN actualParams? RPAREN      # FunctionCallExpr
    | ID LBRACK expr RBRACK               # ArrayAccess1DExpr // Specific for 1D
    | ID LBRACK expr RBRACK LBRACK expr RBRACK # ArrayAccess2DExpr // Specific for 2D
    | ID                                  # IdExpr
    | INT                                 # IntLiteralExpr
    | FLOAT                               # FloatLiteralExpr
    | STRING                              # StringLiteralExpr
    | K_NULL                              # NullLiteralExpr
    ;

// Lexer Rules
K_VAR: 'var';
K_INT: 'int';
K_FLOAT32: 'float32';
K_FLOAT64: 'float64';
K_BOOL: 'bool';
K_STRING: 'string';
K_VOID: 'void';
K_GENERATOR: 'generator';
K_IF: 'if';
K_ELSE: 'else';
K_WHILE: 'while';
K_FOR: 'for';
K_FOREACH: 'foreach';
K_IN: 'in';
K_STRUCT: 'struct';
K_CLASS: 'class';
K_EXTENDS: 'extends';
K_PRIVATE: 'private';
K_PUBLIC: 'public';
K_PROTECTED: 'protected';
K_RETURN: 'return';
K_YIELD: 'yield';
K_PRINT: 'print';
K_READ: 'read';
K_NEW: 'new';
K_NULL: 'null';

BOOL: 'true' | 'false';

LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
SEMI: ';';
COMMA: ',';
DOT: '.';
ASSIGN: '=';
COLON: ':';

GT    : '>';
LT    : '<';
GTE   : '>=';
LTE   : '<=';
EQ    : '==';
NEQ   : '!=';
AND_OP: '&&'; // Logical AND
OR_OP : '||'; // Logical OR
XOR_OP: '^';  // Bitwise/Logical XOR
NOT   : '!';  // Logical NOT

PLUS  : '+';
MINUS : '-'; // Also used for unary minus
STAR  : '*';
SLASH : '/';
MOD   : '%';

ID: [a-zA-Z_][a-zA-Z0-9_]*;
INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]*; // Allows for .5, 5. etc.
STRING: '"' (~["\r\n] | '\\"')* '"'; // Allows escaped quotes within strings

COMMENT: '//' ~[\r\n]* -> skip;
WS: [ \t\r\n]+ -> skip;