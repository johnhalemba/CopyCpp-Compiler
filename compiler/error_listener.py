from antlr4.error import ErrorListener

class ErrorListener(ErrorListener.ErrorListener):
    def __init__(self):
        super().__init__()
        self.had_error = False
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.had_error = True
        error_msg = f"Line {line}:{column} - {msg}"
        self.errors.append(error_msg)
        print(error_msg)
