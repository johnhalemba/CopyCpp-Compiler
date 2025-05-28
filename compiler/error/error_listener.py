# compiler/error/error_listener.py
from antlr4.error.ErrorListener import ErrorListener as BaseErrorListener

class ErrorListener(BaseErrorListener):
    def __init__(self):
        super().__init__()
        self.had_error = False
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """Handle syntax errors during parsing"""
        self.had_error = True
        error_msg = f"Syntax error at line {line}, column {column}: {msg}"
        if offendingSymbol:
            error_msg += f" (near '{offendingSymbol.text}')"

        self.errors.append(error_msg)
        print(f"ERROR: {error_msg}")

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        """Handle ambiguity in parsing"""
        print(f"WARNING: Ambiguity detected at positions {startIndex}-{stopIndex}")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        """Handle full context attempts"""
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        """Handle context sensitivity"""
        pass

    def get_errors(self):
        """Return all collected errors"""
        return self.errors