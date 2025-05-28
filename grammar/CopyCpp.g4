grammar CopyCpp;

// Parser Rules
program: statement+ EOF;

statement
    : varDeclaration
    | assignment
    | ifStatement
    | whileStatement
    | forStatement
    | functionDecl
    | functionCall ';'
    | returnStatement
    | printStatement
    | readStatement
    | block
    | COMMENT
    ;

block: '{' statement* '}';

varDeclaration
    : type ID ('=' expr)? ';'
    | type ID '[' expr ']' ';'  // array declaration
    | type ID '[' expr ']' '[' expr ']' ';'  // matrix declaration
    ;

type
    : 'int'
    | 'float32'
    | 'float64'
    | 'bool'
    | 'string'
    | 'void'
    ;

assignment
    : ID '=' expr ';'
    | ID '[' expr ']' '=' expr ';'  // array assignment
    | ID '[' expr ']' '[' expr ']' '=' expr ';'  // matrix assignment
    ;

ifStatement
    : 'if' '(' expr ')' statement ('else' statement)?
    ;

whileStatement
    : 'while' '(' expr ')' statement
    ;

forStatement
    : 'for' '(' statement expr ';' expr ')' statement
    ;

functionDecl
    : type ID '(' formalParams? ')' block
    ;

formalParams
    : formalParam (',' formalParam)*
    ;

formalParam
    : type ID
    | type ID '[' ']'                 // 1D array parameter
    | type ID '[' ']' '[' ']'         // 2D array parameter
    | type ID '[' expr ']'            // 1D array with size
    | type ID '[' expr ']' '[' expr ']'  // 2D array with size
    ;

functionCall
    : ID '(' actualParams? ')'
    ;

actualParams
    : expr (',' expr)*
    ;

returnStatement
    : 'return' expr? ';'
    ;

printStatement
    : 'print' '(' expr ')' ';'
    ;

readStatement
    : 'read' '(' ID ')' ';'
    ;

expr
    : '(' expr ')'
    | '-' expr
    | '!' expr
    | expr op=('*' | '/' | '%') expr
    | expr op=('+' | '-') expr
    | expr op=('<' | '>' | '<=' | '>=') expr
    | expr op=('==' | '!=') expr
    | expr '&&' expr
    | expr '||' expr
    | expr '^' expr  // XOR
    | functionCall
    | ID '[' expr ']'  // array access
    | ID '[' expr ']' '[' expr ']'  // matrix access
    | ID
    | INT
    | FLOAT
    | BOOL
    | STRING
    ;

// Lexer Rules
ID: [a-zA-Z_][a-zA-Z0-9_]*;
INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]*;
BOOL: 'true' | 'false';
STRING: '"' (~["\r\n] | '\\"')* '"';
COMMENT: '//' ~[\r\n]* -> skip;
WS: [ \t\r\n]+ -> skip;
