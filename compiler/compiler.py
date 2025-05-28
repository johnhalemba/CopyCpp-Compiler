import os
from antlr4 import *

from grammar.CopyCppLexer import CopyCppLexer
from grammar.CopyCppParser import CopyCppParser
from .ast.ast_builder import ASTBuilder
from .ir.ir_generator import IRGenerator
from .error.error_listener import ErrorListener
import llvmlite.binding as llvm

class Compiler:
    def __init__(self):
        pass

    def compile(self, input_file, output_file=None):
        print("=" * 50)
        print(f"Compiling: {input_file}")
        print("=" * 50)

        # 1. Parse the input file
        print("Step 1: Reading input file...")
        try:
            input_stream = FileStream(input_file, encoding="utf-8")
        except Exception as e:
            print(f"ERROR: Cannot open input file '{input_file}': {e}")
            return False

        # 2. Lexical Analysis
        print("Step 2: Lexical analysis...")
        lexer = CopyCppLexer(input_stream)

        # 3. Syntactic Analysis
        print("Step 3: Syntactic analysis...")
        token_stream = CommonTokenStream(lexer)
        parser = CopyCppParser(token_stream)

        # Set up error handling for both lexer and parser
        error_listener = ErrorListener()

        # Remove default error listeners and add our custom one
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        # Parse the program
        try:
            tree = parser.program()
        except Exception as e:
            print(f"ERROR: Parsing failed with exception: {e}")
            return False

        # Check for lexical/syntax errors
        if error_listener.had_error:
            print("\n" + "=" * 50)
            print("COMPILATION FAILED - Lexical/Syntax Errors Found:")
            print("=" * 50)
            for i, error in enumerate(error_listener.get_errors(), 1):
                print(f"{i}. {error}")
            print("=" * 50)
            return False

        print("✓ Lexical and syntactic analysis completed successfully")

        # 4. Build AST
        print("Step 4: Building Abstract Syntax Tree...")
        try:
            ast_builder = ASTBuilder(debug=True)  # Set to True for AST debug info
            ast = ast_builder.visit(tree)
            if ast is None:
                print("ERROR: Failed to build AST - root node is None")
                return False
            print("✓ AST built successfully")
        except Exception as e:
            print(f"ERROR: AST building failed: {e}")
            import traceback
            traceback.print_exc()
            return False

        # 5. IR Generation
        print("Step 5: Generating LLVM IR...")
        try:
            ir_generator = IRGenerator(debug=True)  # Set to True for IR debug info
            module = ir_generator.generate_ir(ast)
            if module is None:
                print("ERROR: IR generation failed - module is None")
                return False
            print("✓ LLVM IR generated successfully")
        except Exception as e:
            print(f"ERROR: IR generation failed: {e}")
            import traceback
            traceback.print_exc()
            return False

        # 6. Optimization and Code Generation
        print("Step 6: Optimizing and generating code...")
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

            # Create LLVM module from IR
            try:
                llvm_module = llvm.parse_assembly(str(module))
            except Exception as e:
                print(f"ERROR: Failed to parse generated IR: {e}")
                print("Generated IR content:")
                print(str(module))
                return False

            # Optimize module
            print("  - Running optimization passes...")
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = 2  # -O2 optimization level
            pass_manager = llvm.create_module_pass_manager()
            pmb.populate(pass_manager)
            pass_manager.run(llvm_module)

            # Output LLVM IR for inspection
            print(f"  - Writing LLVM IR to {output_file}.ll")
            with open(f"{output_file}.ll", "w") as f:
                f.write(str(llvm_module))

            # Output LLVM IR for inspection
            print(f"  - Writing LLVM IR to {output_file}.ll")
            with open(f"{output_file}.ll", "w") as f:
                f.write(str(llvm_module))

            # Generate object file
            print(f"  - Generating object file {output_file}.o")
            with open(f"{output_file}.o", "wb") as f:
                f.write(target_machine.emit_object(llvm_module))

            # Link the final executable
            print(f"  - Linking executable {output_file}")
            link_command = f"clang {output_file}.o -o {output_file}"
            result = os.system(link_command)

            if result != 0:
                print(f"ERROR: Linking failed. Command: {link_command}")
                return False

            print("\n" + "=" * 50)
            print("COMPILATION SUCCESSFUL!")
            print("=" * 50)
            print(f"✓ Executable: {output_file}")
            print(f"✓ LLVM IR:    {output_file}.ll")
            print(f"✓ Object:     {output_file}.o")
            print("=" * 50)
            return True
        except Exception as e:
            print(f"ERROR: Optimization and code generation failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def compile_and_run(self, input_file, args=None):
        """Compile and immediately run the program"""
        output_file = os.path.splitext(input_file)[0]

        if self.compile(input_file, output_file):
            print(f"\nRunning {output_file}...")
            print("-" * 30)

            run_command = f"./{output_file}"
            if args:
                run_command += f" {' '.join(args)}"

            result = os.system(run_command)
            print("-" * 30)

            if result == 0:
                print("Program executed successfully")
            else:
                print(f"Program exited with code {result}")

            return result == 0

        return False

    def get_version(self):
        """Get compiler version"""
        return "CopyCpp Compiler v1.0"

    def cleanup(self, input_file):
        """Clean up generated files"""
        base_name = os.path.splitext(input_file)[0]
        files_to_remove = [
            f"{base_name}",  # executable
            f"{base_name}.ll",  # LLVM IR
            f"{base_name}.o"  # object file
        ]

        removed_count = 0
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    removed_count += 1
                    print(f"Removed: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

        if removed_count > 0:
            print(f"Cleaned up {removed_count} files")
        else:
            print("No files to clean up")

    def show_help(self):
        """Show help information"""
        help_text = """
CopyCpp Compiler - Usage Information

BASIC USAGE:
    python -m compiler <input_file> [output_file]

    input_file   : Source file to compile (.cpp extension)
    output_file  : Optional output executable name (default: same as input without extension)

EXAMPLES:
    python -m compiler program.cpp
    python -m compiler program.cpp myprogram
    python -m compiler examples/hello.cpp

OPTIONS:
    --version    : Show compiler version
    --help       : Show this help message
    --clean      : Clean up generated files for a source file
    --run        : Compile and immediately run the program

ADVANCED USAGE:
    python -m compiler --clean program.cpp      # Clean generated files
    python -m compiler --run program.cpp        # Compile and run
    python -m compiler --version                # Show version

OUTPUT FILES:
    The compiler generates three files:
    - <name>     : Executable binary
    - <name>.ll  : LLVM IR (intermediate representation)
    - <name>.o   : Object file

SUPPORTED FEATURES:
    - Variables and arrays
    - Functions and generators
    - Classes and inheritance
    - Control structures (if, while, for, foreach)
    - Dynamic typing with 'var' keyword
    - Built-in types: int, float32, float64, bool, string
    - Print and read statements

For more information, visit: https://github.com/your-repo/copycpp-compiler
"""
        print(help_text)