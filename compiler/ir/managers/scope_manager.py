"""Variable scope management for CopyCpp compiler"""

class ScopeManager:
    def __init__(self, debug=False):
        self.debug = debug
        self.scope_stack = [{}]

    def log(self, message):
        if self.debug:
            print(f"DEBUG SCOPE: {message}")

    def push_scope(self):
        """Push new scope onto stack"""
        self.scope_stack.append({})
        self.log(f"Pushed scope. Depth: {len(self.scope_stack)}")

    def pop_scope(self):
        """Pop scope from stack"""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.log(f"Popped scope. Depth: {len(self.scope_stack)}")

    def add_variable(self, name, ptr, type_name_str, is_array=False, dimensions_ast=None, is_param=False):
        """Add variable to current scope"""
        self.scope_stack[-1][name] = (ptr, type_name_str, is_array, dimensions_ast or [], is_param)
        self.log(f"Added var '{name}' (type: {type_name_str}, array: {is_array}) to scope {len(self.scope_stack) - 1}")

    def lookup_variable(self, name):
        """Look up variable in the scope stack"""
        for i in range(len(self.scope_stack) - 1, -1, -1):
            if name in self.scope_stack[i]:
                return self.scope_stack[i][name]
        self.log(f"Var '{name}' not found in scopes.")
        return None

    def clear_all_scopes(self):
        """Clear all scopes except global"""
        self.scope_stack = [{}]
        self.log("Cleared all scopes except global")