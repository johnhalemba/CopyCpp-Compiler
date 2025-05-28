# Generated from grammar/CopyCpp.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,44,286,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,1,0,4,0,38,8,0,11,0,12,0,
        39,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,3,1,58,8,1,1,2,1,2,5,2,62,8,2,10,2,12,2,65,9,2,1,2,1,2,1,3,1,3,
        1,3,1,3,3,3,73,8,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,
        3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,94,8,3,1,4,1,4,1,5,1,5,1,5,1,5,
        1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,
        1,5,1,5,1,5,1,5,3,5,122,8,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,131,
        8,6,1,7,1,7,1,7,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,
        1,9,1,9,1,9,1,9,3,9,152,8,9,1,9,1,9,1,9,1,10,1,10,1,10,5,10,160,
        8,10,10,10,12,10,163,9,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
        1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
        1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,3,11,195,8,11,1,12,
        1,12,1,12,3,12,200,8,12,1,12,1,12,1,13,1,13,1,13,5,13,207,8,13,10,
        13,12,13,210,9,13,1,14,1,14,3,14,214,8,14,1,14,1,14,1,15,1,15,1,
        15,1,15,1,15,1,15,1,16,1,16,1,16,1,16,1,16,1,16,1,17,1,17,1,17,1,
        17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,
        17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,3,17,258,
        8,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,5,17,281,8,17,10,17,
        12,17,284,9,17,1,17,0,1,34,18,0,2,4,6,8,10,12,14,16,18,20,22,24,
        26,28,30,32,34,0,5,1,0,7,12,1,0,25,27,2,0,23,23,28,28,1,0,29,32,
        1,0,33,34,312,0,37,1,0,0,0,2,57,1,0,0,0,4,59,1,0,0,0,6,93,1,0,0,
        0,8,95,1,0,0,0,10,121,1,0,0,0,12,123,1,0,0,0,14,132,1,0,0,0,16,138,
        1,0,0,0,18,147,1,0,0,0,20,156,1,0,0,0,22,194,1,0,0,0,24,196,1,0,
        0,0,26,203,1,0,0,0,28,211,1,0,0,0,30,217,1,0,0,0,32,223,1,0,0,0,
        34,257,1,0,0,0,36,38,3,2,1,0,37,36,1,0,0,0,38,39,1,0,0,0,39,37,1,
        0,0,0,39,40,1,0,0,0,40,41,1,0,0,0,41,42,5,0,0,1,42,1,1,0,0,0,43,
        58,3,6,3,0,44,58,3,10,5,0,45,58,3,12,6,0,46,58,3,14,7,0,47,58,3,
        16,8,0,48,58,3,18,9,0,49,50,3,24,12,0,50,51,5,1,0,0,51,58,1,0,0,
        0,52,58,3,28,14,0,53,58,3,30,15,0,54,58,3,32,16,0,55,58,3,4,2,0,
        56,58,5,43,0,0,57,43,1,0,0,0,57,44,1,0,0,0,57,45,1,0,0,0,57,46,1,
        0,0,0,57,47,1,0,0,0,57,48,1,0,0,0,57,49,1,0,0,0,57,52,1,0,0,0,57,
        53,1,0,0,0,57,54,1,0,0,0,57,55,1,0,0,0,57,56,1,0,0,0,58,3,1,0,0,
        0,59,63,5,2,0,0,60,62,3,2,1,0,61,60,1,0,0,0,62,65,1,0,0,0,63,61,
        1,0,0,0,63,64,1,0,0,0,64,66,1,0,0,0,65,63,1,0,0,0,66,67,5,3,0,0,
        67,5,1,0,0,0,68,69,3,8,4,0,69,72,5,38,0,0,70,71,5,4,0,0,71,73,3,
        34,17,0,72,70,1,0,0,0,72,73,1,0,0,0,73,74,1,0,0,0,74,75,5,1,0,0,
        75,94,1,0,0,0,76,77,3,8,4,0,77,78,5,38,0,0,78,79,5,5,0,0,79,80,3,
        34,17,0,80,81,5,6,0,0,81,82,5,1,0,0,82,94,1,0,0,0,83,84,3,8,4,0,
        84,85,5,38,0,0,85,86,5,5,0,0,86,87,3,34,17,0,87,88,5,6,0,0,88,89,
        5,5,0,0,89,90,3,34,17,0,90,91,5,6,0,0,91,92,5,1,0,0,92,94,1,0,0,
        0,93,68,1,0,0,0,93,76,1,0,0,0,93,83,1,0,0,0,94,7,1,0,0,0,95,96,7,
        0,0,0,96,9,1,0,0,0,97,98,5,38,0,0,98,99,5,4,0,0,99,100,3,34,17,0,
        100,101,5,1,0,0,101,122,1,0,0,0,102,103,5,38,0,0,103,104,5,5,0,0,
        104,105,3,34,17,0,105,106,5,6,0,0,106,107,5,4,0,0,107,108,3,34,17,
        0,108,109,5,1,0,0,109,122,1,0,0,0,110,111,5,38,0,0,111,112,5,5,0,
        0,112,113,3,34,17,0,113,114,5,6,0,0,114,115,5,5,0,0,115,116,3,34,
        17,0,116,117,5,6,0,0,117,118,5,4,0,0,118,119,3,34,17,0,119,120,5,
        1,0,0,120,122,1,0,0,0,121,97,1,0,0,0,121,102,1,0,0,0,121,110,1,0,
        0,0,122,11,1,0,0,0,123,124,5,13,0,0,124,125,5,14,0,0,125,126,3,34,
        17,0,126,127,5,15,0,0,127,130,3,2,1,0,128,129,5,16,0,0,129,131,3,
        2,1,0,130,128,1,0,0,0,130,131,1,0,0,0,131,13,1,0,0,0,132,133,5,17,
        0,0,133,134,5,14,0,0,134,135,3,34,17,0,135,136,5,15,0,0,136,137,
        3,2,1,0,137,15,1,0,0,0,138,139,5,18,0,0,139,140,5,14,0,0,140,141,
        3,2,1,0,141,142,3,34,17,0,142,143,5,1,0,0,143,144,3,34,17,0,144,
        145,5,15,0,0,145,146,3,2,1,0,146,17,1,0,0,0,147,148,3,8,4,0,148,
        149,5,38,0,0,149,151,5,14,0,0,150,152,3,20,10,0,151,150,1,0,0,0,
        151,152,1,0,0,0,152,153,1,0,0,0,153,154,5,15,0,0,154,155,3,4,2,0,
        155,19,1,0,0,0,156,161,3,22,11,0,157,158,5,19,0,0,158,160,3,22,11,
        0,159,157,1,0,0,0,160,163,1,0,0,0,161,159,1,0,0,0,161,162,1,0,0,
        0,162,21,1,0,0,0,163,161,1,0,0,0,164,165,3,8,4,0,165,166,5,38,0,
        0,166,195,1,0,0,0,167,168,3,8,4,0,168,169,5,38,0,0,169,170,5,5,0,
        0,170,171,5,6,0,0,171,195,1,0,0,0,172,173,3,8,4,0,173,174,5,38,0,
        0,174,175,5,5,0,0,175,176,5,6,0,0,176,177,5,5,0,0,177,178,5,6,0,
        0,178,195,1,0,0,0,179,180,3,8,4,0,180,181,5,38,0,0,181,182,5,5,0,
        0,182,183,3,34,17,0,183,184,5,6,0,0,184,195,1,0,0,0,185,186,3,8,
        4,0,186,187,5,38,0,0,187,188,5,5,0,0,188,189,3,34,17,0,189,190,5,
        6,0,0,190,191,5,5,0,0,191,192,3,34,17,0,192,193,5,6,0,0,193,195,
        1,0,0,0,194,164,1,0,0,0,194,167,1,0,0,0,194,172,1,0,0,0,194,179,
        1,0,0,0,194,185,1,0,0,0,195,23,1,0,0,0,196,197,5,38,0,0,197,199,
        5,14,0,0,198,200,3,26,13,0,199,198,1,0,0,0,199,200,1,0,0,0,200,201,
        1,0,0,0,201,202,5,15,0,0,202,25,1,0,0,0,203,208,3,34,17,0,204,205,
        5,19,0,0,205,207,3,34,17,0,206,204,1,0,0,0,207,210,1,0,0,0,208,206,
        1,0,0,0,208,209,1,0,0,0,209,27,1,0,0,0,210,208,1,0,0,0,211,213,5,
        20,0,0,212,214,3,34,17,0,213,212,1,0,0,0,213,214,1,0,0,0,214,215,
        1,0,0,0,215,216,5,1,0,0,216,29,1,0,0,0,217,218,5,21,0,0,218,219,
        5,14,0,0,219,220,3,34,17,0,220,221,5,15,0,0,221,222,5,1,0,0,222,
        31,1,0,0,0,223,224,5,22,0,0,224,225,5,14,0,0,225,226,5,38,0,0,226,
        227,5,15,0,0,227,228,5,1,0,0,228,33,1,0,0,0,229,230,6,17,-1,0,230,
        231,5,14,0,0,231,232,3,34,17,0,232,233,5,15,0,0,233,258,1,0,0,0,
        234,235,5,23,0,0,235,258,3,34,17,17,236,237,5,24,0,0,237,258,3,34,
        17,16,238,258,3,24,12,0,239,240,5,38,0,0,240,241,5,5,0,0,241,242,
        3,34,17,0,242,243,5,6,0,0,243,258,1,0,0,0,244,245,5,38,0,0,245,246,
        5,5,0,0,246,247,3,34,17,0,247,248,5,6,0,0,248,249,5,5,0,0,249,250,
        3,34,17,0,250,251,5,6,0,0,251,258,1,0,0,0,252,258,5,38,0,0,253,258,
        5,39,0,0,254,258,5,40,0,0,255,258,5,41,0,0,256,258,5,42,0,0,257,
        229,1,0,0,0,257,234,1,0,0,0,257,236,1,0,0,0,257,238,1,0,0,0,257,
        239,1,0,0,0,257,244,1,0,0,0,257,252,1,0,0,0,257,253,1,0,0,0,257,
        254,1,0,0,0,257,255,1,0,0,0,257,256,1,0,0,0,258,282,1,0,0,0,259,
        260,10,15,0,0,260,261,7,1,0,0,261,281,3,34,17,16,262,263,10,14,0,
        0,263,264,7,2,0,0,264,281,3,34,17,15,265,266,10,13,0,0,266,267,7,
        3,0,0,267,281,3,34,17,14,268,269,10,12,0,0,269,270,7,4,0,0,270,281,
        3,34,17,13,271,272,10,11,0,0,272,273,5,35,0,0,273,281,3,34,17,12,
        274,275,10,10,0,0,275,276,5,36,0,0,276,281,3,34,17,11,277,278,10,
        9,0,0,278,279,5,37,0,0,279,281,3,34,17,10,280,259,1,0,0,0,280,262,
        1,0,0,0,280,265,1,0,0,0,280,268,1,0,0,0,280,271,1,0,0,0,280,274,
        1,0,0,0,280,277,1,0,0,0,281,284,1,0,0,0,282,280,1,0,0,0,282,283,
        1,0,0,0,283,35,1,0,0,0,284,282,1,0,0,0,16,39,57,63,72,93,121,130,
        151,161,194,199,208,213,257,280,282
    ]

class CopyCppParser ( Parser ):

    grammarFileName = "CopyCpp.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'{'", "'}'", "'='", "'['", "']'", 
                     "'int'", "'float32'", "'float64'", "'bool'", "'string'", 
                     "'void'", "'if'", "'('", "')'", "'else'", "'while'", 
                     "'for'", "','", "'return'", "'print'", "'read'", "'-'", 
                     "'!'", "'*'", "'/'", "'%'", "'+'", "'<'", "'>'", "'<='", 
                     "'>='", "'=='", "'!='", "'&&'", "'||'", "'^'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "ID", "INT", "FLOAT", "BOOL", 
                      "STRING", "COMMENT", "WS" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_block = 2
    RULE_varDeclaration = 3
    RULE_type = 4
    RULE_assignment = 5
    RULE_ifStatement = 6
    RULE_whileStatement = 7
    RULE_forStatement = 8
    RULE_functionDecl = 9
    RULE_formalParams = 10
    RULE_formalParam = 11
    RULE_functionCall = 12
    RULE_actualParams = 13
    RULE_returnStatement = 14
    RULE_printStatement = 15
    RULE_readStatement = 16
    RULE_expr = 17

    ruleNames =  [ "program", "statement", "block", "varDeclaration", "type", 
                   "assignment", "ifStatement", "whileStatement", "forStatement", 
                   "functionDecl", "formalParams", "formalParam", "functionCall", 
                   "actualParams", "returnStatement", "printStatement", 
                   "readStatement", "expr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    ID=38
    INT=39
    FLOAT=40
    BOOL=41
    STRING=42
    COMMENT=43
    WS=44

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(CopyCppParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.StatementContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.StatementContext,i)


        def getRuleIndex(self):
            return CopyCppParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = CopyCppParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 36
                self.statement()
                self.state = 39 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 9070978678660) != 0)):
                    break

            self.state = 41
            self.match(CopyCppParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varDeclaration(self):
            return self.getTypedRuleContext(CopyCppParser.VarDeclarationContext,0)


        def assignment(self):
            return self.getTypedRuleContext(CopyCppParser.AssignmentContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(CopyCppParser.IfStatementContext,0)


        def whileStatement(self):
            return self.getTypedRuleContext(CopyCppParser.WhileStatementContext,0)


        def forStatement(self):
            return self.getTypedRuleContext(CopyCppParser.ForStatementContext,0)


        def functionDecl(self):
            return self.getTypedRuleContext(CopyCppParser.FunctionDeclContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(CopyCppParser.FunctionCallContext,0)


        def returnStatement(self):
            return self.getTypedRuleContext(CopyCppParser.ReturnStatementContext,0)


        def printStatement(self):
            return self.getTypedRuleContext(CopyCppParser.PrintStatementContext,0)


        def readStatement(self):
            return self.getTypedRuleContext(CopyCppParser.ReadStatementContext,0)


        def block(self):
            return self.getTypedRuleContext(CopyCppParser.BlockContext,0)


        def COMMENT(self):
            return self.getToken(CopyCppParser.COMMENT, 0)

        def getRuleIndex(self):
            return CopyCppParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = CopyCppParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 57
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 43
                self.varDeclaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 44
                self.assignment()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 45
                self.ifStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 46
                self.whileStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 47
                self.forStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 48
                self.functionDecl()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 49
                self.functionCall()
                self.state = 50
                self.match(CopyCppParser.T__0)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 52
                self.returnStatement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 53
                self.printStatement()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 54
                self.readStatement()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 55
                self.block()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 56
                self.match(CopyCppParser.COMMENT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.StatementContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.StatementContext,i)


        def getRuleIndex(self):
            return CopyCppParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = CopyCppParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(CopyCppParser.T__1)
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 9070978678660) != 0):
                self.state = 60
                self.statement()
                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 66
            self.match(CopyCppParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(CopyCppParser.TypeContext,0)


        def ID(self):
            return self.getToken(CopyCppParser.ID, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.ExprContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.ExprContext,i)


        def getRuleIndex(self):
            return CopyCppParser.RULE_varDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDeclaration" ):
                listener.enterVarDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDeclaration" ):
                listener.exitVarDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDeclaration" ):
                return visitor.visitVarDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def varDeclaration(self):

        localctx = CopyCppParser.VarDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_varDeclaration)
        self._la = 0 # Token type
        try:
            self.state = 93
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 68
                self.type_()
                self.state = 69
                self.match(CopyCppParser.ID)
                self.state = 72
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4:
                    self.state = 70
                    self.match(CopyCppParser.T__3)
                    self.state = 71
                    self.expr(0)


                self.state = 74
                self.match(CopyCppParser.T__0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 76
                self.type_()
                self.state = 77
                self.match(CopyCppParser.ID)
                self.state = 78
                self.match(CopyCppParser.T__4)
                self.state = 79
                self.expr(0)
                self.state = 80
                self.match(CopyCppParser.T__5)
                self.state = 81
                self.match(CopyCppParser.T__0)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 83
                self.type_()
                self.state = 84
                self.match(CopyCppParser.ID)
                self.state = 85
                self.match(CopyCppParser.T__4)
                self.state = 86
                self.expr(0)
                self.state = 87
                self.match(CopyCppParser.T__5)
                self.state = 88
                self.match(CopyCppParser.T__4)
                self.state = 89
                self.expr(0)
                self.state = 90
                self.match(CopyCppParser.T__5)
                self.state = 91
                self.match(CopyCppParser.T__0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CopyCppParser.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)




    def type_(self):

        localctx = CopyCppParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8064) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CopyCppParser.ID, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.ExprContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.ExprContext,i)


        def getRuleIndex(self):
            return CopyCppParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = CopyCppParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_assignment)
        try:
            self.state = 121
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 97
                self.match(CopyCppParser.ID)
                self.state = 98
                self.match(CopyCppParser.T__3)
                self.state = 99
                self.expr(0)
                self.state = 100
                self.match(CopyCppParser.T__0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 102
                self.match(CopyCppParser.ID)
                self.state = 103
                self.match(CopyCppParser.T__4)
                self.state = 104
                self.expr(0)
                self.state = 105
                self.match(CopyCppParser.T__5)
                self.state = 106
                self.match(CopyCppParser.T__3)
                self.state = 107
                self.expr(0)
                self.state = 108
                self.match(CopyCppParser.T__0)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 110
                self.match(CopyCppParser.ID)
                self.state = 111
                self.match(CopyCppParser.T__4)
                self.state = 112
                self.expr(0)
                self.state = 113
                self.match(CopyCppParser.T__5)
                self.state = 114
                self.match(CopyCppParser.T__4)
                self.state = 115
                self.expr(0)
                self.state = 116
                self.match(CopyCppParser.T__5)
                self.state = 117
                self.match(CopyCppParser.T__3)
                self.state = 118
                self.expr(0)
                self.state = 119
                self.match(CopyCppParser.T__0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(CopyCppParser.ExprContext,0)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.StatementContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.StatementContext,i)


        def getRuleIndex(self):
            return CopyCppParser.RULE_ifStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = CopyCppParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 123
            self.match(CopyCppParser.T__12)
            self.state = 124
            self.match(CopyCppParser.T__13)
            self.state = 125
            self.expr(0)
            self.state = 126
            self.match(CopyCppParser.T__14)
            self.state = 127
            self.statement()
            self.state = 130
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 128
                self.match(CopyCppParser.T__15)
                self.state = 129
                self.statement()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(CopyCppParser.ExprContext,0)


        def statement(self):
            return self.getTypedRuleContext(CopyCppParser.StatementContext,0)


        def getRuleIndex(self):
            return CopyCppParser.RULE_whileStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStatement" ):
                listener.enterWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStatement" ):
                listener.exitWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStatement" ):
                return visitor.visitWhileStatement(self)
            else:
                return visitor.visitChildren(self)




    def whileStatement(self):

        localctx = CopyCppParser.WhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 132
            self.match(CopyCppParser.T__16)
            self.state = 133
            self.match(CopyCppParser.T__13)
            self.state = 134
            self.expr(0)
            self.state = 135
            self.match(CopyCppParser.T__14)
            self.state = 136
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.StatementContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.StatementContext,i)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.ExprContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.ExprContext,i)


        def getRuleIndex(self):
            return CopyCppParser.RULE_forStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStatement" ):
                listener.enterForStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStatement" ):
                listener.exitForStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStatement" ):
                return visitor.visitForStatement(self)
            else:
                return visitor.visitChildren(self)




    def forStatement(self):

        localctx = CopyCppParser.ForStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_forStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.match(CopyCppParser.T__17)
            self.state = 139
            self.match(CopyCppParser.T__13)
            self.state = 140
            self.statement()
            self.state = 141
            self.expr(0)
            self.state = 142
            self.match(CopyCppParser.T__0)
            self.state = 143
            self.expr(0)
            self.state = 144
            self.match(CopyCppParser.T__14)
            self.state = 145
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(CopyCppParser.TypeContext,0)


        def ID(self):
            return self.getToken(CopyCppParser.ID, 0)

        def block(self):
            return self.getTypedRuleContext(CopyCppParser.BlockContext,0)


        def formalParams(self):
            return self.getTypedRuleContext(CopyCppParser.FormalParamsContext,0)


        def getRuleIndex(self):
            return CopyCppParser.RULE_functionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionDecl" ):
                listener.enterFunctionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionDecl" ):
                listener.exitFunctionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDecl" ):
                return visitor.visitFunctionDecl(self)
            else:
                return visitor.visitChildren(self)




    def functionDecl(self):

        localctx = CopyCppParser.FunctionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_functionDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.type_()
            self.state = 148
            self.match(CopyCppParser.ID)
            self.state = 149
            self.match(CopyCppParser.T__13)
            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8064) != 0):
                self.state = 150
                self.formalParams()


            self.state = 153
            self.match(CopyCppParser.T__14)
            self.state = 154
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormalParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def formalParam(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.FormalParamContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.FormalParamContext,i)


        def getRuleIndex(self):
            return CopyCppParser.RULE_formalParams

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFormalParams" ):
                listener.enterFormalParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFormalParams" ):
                listener.exitFormalParams(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFormalParams" ):
                return visitor.visitFormalParams(self)
            else:
                return visitor.visitChildren(self)




    def formalParams(self):

        localctx = CopyCppParser.FormalParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_formalParams)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            self.formalParam()
            self.state = 161
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 157
                self.match(CopyCppParser.T__18)
                self.state = 158
                self.formalParam()
                self.state = 163
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormalParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(CopyCppParser.TypeContext,0)


        def ID(self):
            return self.getToken(CopyCppParser.ID, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.ExprContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.ExprContext,i)


        def getRuleIndex(self):
            return CopyCppParser.RULE_formalParam

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFormalParam" ):
                listener.enterFormalParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFormalParam" ):
                listener.exitFormalParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFormalParam" ):
                return visitor.visitFormalParam(self)
            else:
                return visitor.visitChildren(self)




    def formalParam(self):

        localctx = CopyCppParser.FormalParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_formalParam)
        try:
            self.state = 194
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 164
                self.type_()
                self.state = 165
                self.match(CopyCppParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 167
                self.type_()
                self.state = 168
                self.match(CopyCppParser.ID)
                self.state = 169
                self.match(CopyCppParser.T__4)
                self.state = 170
                self.match(CopyCppParser.T__5)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 172
                self.type_()
                self.state = 173
                self.match(CopyCppParser.ID)
                self.state = 174
                self.match(CopyCppParser.T__4)
                self.state = 175
                self.match(CopyCppParser.T__5)
                self.state = 176
                self.match(CopyCppParser.T__4)
                self.state = 177
                self.match(CopyCppParser.T__5)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 179
                self.type_()
                self.state = 180
                self.match(CopyCppParser.ID)
                self.state = 181
                self.match(CopyCppParser.T__4)
                self.state = 182
                self.expr(0)
                self.state = 183
                self.match(CopyCppParser.T__5)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 185
                self.type_()
                self.state = 186
                self.match(CopyCppParser.ID)
                self.state = 187
                self.match(CopyCppParser.T__4)
                self.state = 188
                self.expr(0)
                self.state = 189
                self.match(CopyCppParser.T__5)
                self.state = 190
                self.match(CopyCppParser.T__4)
                self.state = 191
                self.expr(0)
                self.state = 192
                self.match(CopyCppParser.T__5)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CopyCppParser.ID, 0)

        def actualParams(self):
            return self.getTypedRuleContext(CopyCppParser.ActualParamsContext,0)


        def getRuleIndex(self):
            return CopyCppParser.RULE_functionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def functionCall(self):

        localctx = CopyCppParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            self.match(CopyCppParser.ID)
            self.state = 197
            self.match(CopyCppParser.T__13)
            self.state = 199
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8521240297472) != 0):
                self.state = 198
                self.actualParams()


            self.state = 201
            self.match(CopyCppParser.T__14)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ActualParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.ExprContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.ExprContext,i)


        def getRuleIndex(self):
            return CopyCppParser.RULE_actualParams

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterActualParams" ):
                listener.enterActualParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitActualParams" ):
                listener.exitActualParams(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitActualParams" ):
                return visitor.visitActualParams(self)
            else:
                return visitor.visitChildren(self)




    def actualParams(self):

        localctx = CopyCppParser.ActualParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_actualParams)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 203
            self.expr(0)
            self.state = 208
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 204
                self.match(CopyCppParser.T__18)
                self.state = 205
                self.expr(0)
                self.state = 210
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(CopyCppParser.ExprContext,0)


        def getRuleIndex(self):
            return CopyCppParser.RULE_returnStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStatement" ):
                listener.enterReturnStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStatement" ):
                listener.exitReturnStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStatement" ):
                return visitor.visitReturnStatement(self)
            else:
                return visitor.visitChildren(self)




    def returnStatement(self):

        localctx = CopyCppParser.ReturnStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_returnStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 211
            self.match(CopyCppParser.T__19)
            self.state = 213
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8521240297472) != 0):
                self.state = 212
                self.expr(0)


            self.state = 215
            self.match(CopyCppParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(CopyCppParser.ExprContext,0)


        def getRuleIndex(self):
            return CopyCppParser.RULE_printStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintStatement" ):
                listener.enterPrintStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintStatement" ):
                listener.exitPrintStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStatement" ):
                return visitor.visitPrintStatement(self)
            else:
                return visitor.visitChildren(self)




    def printStatement(self):

        localctx = CopyCppParser.PrintStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_printStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 217
            self.match(CopyCppParser.T__20)
            self.state = 218
            self.match(CopyCppParser.T__13)
            self.state = 219
            self.expr(0)
            self.state = 220
            self.match(CopyCppParser.T__14)
            self.state = 221
            self.match(CopyCppParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReadStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CopyCppParser.ID, 0)

        def getRuleIndex(self):
            return CopyCppParser.RULE_readStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReadStatement" ):
                listener.enterReadStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReadStatement" ):
                listener.exitReadStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReadStatement" ):
                return visitor.visitReadStatement(self)
            else:
                return visitor.visitChildren(self)




    def readStatement(self):

        localctx = CopyCppParser.ReadStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_readStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 223
            self.match(CopyCppParser.T__21)
            self.state = 224
            self.match(CopyCppParser.T__13)
            self.state = 225
            self.match(CopyCppParser.ID)
            self.state = 226
            self.match(CopyCppParser.T__14)
            self.state = 227
            self.match(CopyCppParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CopyCppParser.ExprContext)
            else:
                return self.getTypedRuleContext(CopyCppParser.ExprContext,i)


        def functionCall(self):
            return self.getTypedRuleContext(CopyCppParser.FunctionCallContext,0)


        def ID(self):
            return self.getToken(CopyCppParser.ID, 0)

        def INT(self):
            return self.getToken(CopyCppParser.INT, 0)

        def FLOAT(self):
            return self.getToken(CopyCppParser.FLOAT, 0)

        def BOOL(self):
            return self.getToken(CopyCppParser.BOOL, 0)

        def STRING(self):
            return self.getToken(CopyCppParser.STRING, 0)

        def getRuleIndex(self):
            return CopyCppParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CopyCppParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 34
        self.enterRecursionRule(localctx, 34, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.state = 230
                self.match(CopyCppParser.T__13)
                self.state = 231
                self.expr(0)
                self.state = 232
                self.match(CopyCppParser.T__14)
                pass

            elif la_ == 2:
                self.state = 234
                self.match(CopyCppParser.T__22)
                self.state = 235
                self.expr(17)
                pass

            elif la_ == 3:
                self.state = 236
                self.match(CopyCppParser.T__23)
                self.state = 237
                self.expr(16)
                pass

            elif la_ == 4:
                self.state = 238
                self.functionCall()
                pass

            elif la_ == 5:
                self.state = 239
                self.match(CopyCppParser.ID)
                self.state = 240
                self.match(CopyCppParser.T__4)
                self.state = 241
                self.expr(0)
                self.state = 242
                self.match(CopyCppParser.T__5)
                pass

            elif la_ == 6:
                self.state = 244
                self.match(CopyCppParser.ID)
                self.state = 245
                self.match(CopyCppParser.T__4)
                self.state = 246
                self.expr(0)
                self.state = 247
                self.match(CopyCppParser.T__5)
                self.state = 248
                self.match(CopyCppParser.T__4)
                self.state = 249
                self.expr(0)
                self.state = 250
                self.match(CopyCppParser.T__5)
                pass

            elif la_ == 7:
                self.state = 252
                self.match(CopyCppParser.ID)
                pass

            elif la_ == 8:
                self.state = 253
                self.match(CopyCppParser.INT)
                pass

            elif la_ == 9:
                self.state = 254
                self.match(CopyCppParser.FLOAT)
                pass

            elif la_ == 10:
                self.state = 255
                self.match(CopyCppParser.BOOL)
                pass

            elif la_ == 11:
                self.state = 256
                self.match(CopyCppParser.STRING)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 282
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,15,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 280
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
                    if la_ == 1:
                        localctx = CopyCppParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 259
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 260
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 234881024) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 261
                        self.expr(16)
                        pass

                    elif la_ == 2:
                        localctx = CopyCppParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 262
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 263
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==23 or _la==28):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 264
                        self.expr(15)
                        pass

                    elif la_ == 3:
                        localctx = CopyCppParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 265
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 266
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8053063680) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 267
                        self.expr(14)
                        pass

                    elif la_ == 4:
                        localctx = CopyCppParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 268
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 269
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==33 or _la==34):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 270
                        self.expr(13)
                        pass

                    elif la_ == 5:
                        localctx = CopyCppParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 271
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 272
                        self.match(CopyCppParser.T__34)
                        self.state = 273
                        self.expr(12)
                        pass

                    elif la_ == 6:
                        localctx = CopyCppParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 274
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 275
                        self.match(CopyCppParser.T__35)
                        self.state = 276
                        self.expr(11)
                        pass

                    elif la_ == 7:
                        localctx = CopyCppParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 277
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 278
                        self.match(CopyCppParser.T__36)
                        self.state = 279
                        self.expr(10)
                        pass

             
                self.state = 284
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[17] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 9)
         




