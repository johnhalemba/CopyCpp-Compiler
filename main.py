#!/usr/bin/env python3
"""
CopyCpp Compiler - Main Entry Point

This is the main entry point for the CopyCpp compiler.
Usage: python main.py <input_file> [output_file]
"""

import sys
import os

# Add the current directory to Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compiler.compiler import Compiler


def main():
    """Main entry point for the CopyCpp compiler"""

    if len(sys.argv) < 2:
        print("CopyCpp Compiler")
        print("Usage: python main.py <input_file> [output_file]")
        print("       python main.py --help")
        print("       python main.py --version")
        print("       python main.py --clean <input_file>")
        print("       python main.py --run <input_file>")
        sys.exit(1)

    # Create compiler instance
    compiler = Compiler()

    # Handle different command line options
    if sys.argv[1] == "--version":
        print(compiler.get_version())

    elif sys.argv[1] == "--help":
        compiler.show_help()

    elif sys.argv[1] == "--clean":
        if len(sys.argv) < 3:
            print("Error: --clean requires input file")
            print("Usage: python main.py --clean <input_file>")
            sys.exit(1)
        compiler.cleanup(sys.argv[2])

    elif sys.argv[1] == "--run":
        if len(sys.argv) < 3:
            print("Error: --run requires input file")
            print("Usage: python main.py --run <input_file>")
            sys.exit(1)
        success = compiler.compile_and_run(sys.argv[2])
        sys.exit(0 if success else 1)

    else:
        # Regular compilation
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        # Validate input file
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            sys.exit(1)

        # Check file extension (optional warning)
        if not input_file.endswith('.ccpp'):
            print(f"Warning: Input file '{input_file}' doesn't have .cpp extension")

        # Compile
        try:
            success = compiler.compile(input_file, output_file)
            sys.exit(0 if success else 1)
        except KeyboardInterrupt:
            print("\nCompilation interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()