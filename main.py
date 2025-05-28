import sys
from compiler.compiler import Compiler
def main():
    if len(sys.argv) < 2:
        print("Usage: python -m simple_language.compiler <input_file> [output_file]")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    compiler = Compiler()
    compiler.compile(input_file, output_file)

if __name__ == "__main__":
    main()

