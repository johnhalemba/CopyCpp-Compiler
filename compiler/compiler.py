import os
from antlr4 import *

from grammar.CopyCppLexer import CopyCppLexer
from grammar.CopyCppParser import CopyCppParser
from compiler.ast_builder import ASTBuilder
from compiler.type_checker import TypeChecker
from compiler.ir_generator import IRGenerator
from compiler.error_listener import ErrorListener
import llvmlite.binding as llvm


class Compiler:
    def __init__(self):
        pass

    def compile(self, input_file, output_file=None):
        print("Parsing input file...")
        # 1. Parse the input file
        try:
            input_stream = FileStream(input_file, encoding="utf-8")
        except Exception as e:
            print(f"Error opening input file: {e}")
            return False

        lexer = CopyCppLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = CopyCppParser(token_stream)

        error_listener = ErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        print("Building AST...")
        # 2. Build the AST
        try:
            tree = parser.program()
            if error_listener.had_error:
                print("Compilation failed due to syntax errors")
                return False

            ast_builder = ASTBuilder()
            ast = ast_builder.visit(tree)
        except Exception as e:
            print(f"Error during parsing: {e}")
            return False

        print("Type checking...")
        # 3. Type checking
        try:
            type_checker = TypeChecker()
            errors = type_checker.check(ast)

            if errors:
                print("Type checking errors:")
                for error in errors:
                    print(f"  {error}")
                return False
        except Exception as e:
            print(f"Error during type checking: {e}")
            return False

        print("Generating IR...")
        # 4. IR Generation
        try:
            ir_generator = IRGenerator()
            module = ir_generator.generate_ir(ast)
        except Exception as e:
            print(f"Error during IR generation: {e}")
            return False

        print("Optimizing and generating code...")
        # 5. LLVM optimization and code generation
        if not output_file:
            output_file = os.path.splitext(input_file)[0]

        try:
            # Initialize LLVM components
            llvm.initialize()
            llvm.initialize_native_target()
            llvm.initialize_native_asmprinter()

            # Create target machine
            target = llvm.Target.from_default_triple()
            target_machine = target.create_target_machine()

            # Optimize module
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = 2
            pass_manager = llvm.create_module_pass_manager()
            pmb.populate(pass_manager)

            # Create LLVM module from IR
            llvm_module = llvm.parse_assembly(str(module))
            pass_manager.run(llvm_module)

            # Output LLVM IR for inspection
            with open(f"{output_file}.ll", "w") as f:
                f.write(str(llvm_module))

            # Generate object file
            with open(f"{output_file}.o", "wb") as f:
                f.write(target_machine.emit_object(llvm_module))

            # Link the final executable
            os.system(f"clang {output_file}.o -o {output_file}")

            print(f"Successfully compiled to {output_file}")
            return True
        except Exception as e:
            print(f"Error during optimization and code generation: {e}")
            return False