# CopyCpp Compiler Project

A comprehensive compiler implementation for a custom programming language called **CopyCpp**, built from scratch using Python, ANTLR4, and LLVM. This project demonstrates advanced compiler construction techniques including lexical analysis, parsing, AST generation, type checking, and LLVM IR code generation.

## 🌟 Project Overview

This repository contains two major implementations of the CopyCpp compiler, each showcasing different levels of language features and complexity:

### Part 1: Basic Compiler (Branch: `part1-basic`)
A foundational compiler implementation covering essential programming language features.

### Part 2: Advanced Compiler (Branch: `part2-advanced`) 
An extended compiler with advanced features including object-oriented programming, dynamic typing, and generators.

## 🏗️ Repository Structure

main branch (this README)
├── part1-basic branch
│   ├── grammar/          # ANTLR4 grammar files
│   ├── compiler/         # Compiler implementation
│   │   ├── ast_builder.py
│   │   ├── type_checker.py
│   │   ├── ir_generator.py
│   │   └── error_listener.py
│   └── examples/         # Test programs
└── part2-advanced branch
├── grammar/          # Extended grammar
├── compiler/
│   ├── ast/          # AST node definitions
│   ├── ir/           # IR generation with managers
│   │   ├── managers/ # Specialized managers
│   │   └── ir_generator.py
└── examples/         # Advanced test programs


## 🚀 Features Comparison

### Part 1: Basic Compiler Features
- ✅ **Data Types**: Integers, floats (float32/float64), booleans, strings
- ✅ **I/O Operations**: `print()` and `read()` statements
- ✅ **Arithmetic Operations**: +, -, *, /, %
- ✅ **Arrays & Matrices**: 1D and 2D array support
- ✅ **Boolean Logic**: AND, OR, XOR, NOT with short-circuit evaluation
- ✅ **Control Flow**: if/else, while, for loops
- ✅ **Functions**: Function definitions and calls
- ✅ **Variable Scoping**: Local and global variables
- ✅ **Error Handling**: Lexical and syntax error reporting

### Part 2: Advanced Compiler Features
**All Part 1 features plus:**
- ✅ **Object-Oriented Programming**: Classes with inheritance
- ✅ **Structures**: User-defined data structures
- ✅ **Dynamic Typing**: Runtime type resolution with `var` keyword
- ✅ **Generators**: Python-style generator functions with `yield`
- ✅ **Advanced Memory Management**: Sophisticated object allocation
- ✅ **Method Inheritance**: Parent class method resolution
- ✅ **Iterator Protocol**: `foreach` loops with generator support
- ✅ **Complex Type System**: Advanced type checking and inference

## 📋 Requirements

- Python 3.8+
- ANTLR4 Python runtime (`antlr4-python3-runtime`)
- LLVM Python bindings (`llvmlite`)
- C compiler (GCC/Clang) for final executable generation

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/johnhalemba/copycpp-compiler.git
cd copycpp-compiler

# Install dependencies
pip install antlr4-python3-runtime llvmlite

# Switch to desired branch
git checkout part1-basic    # For basic compiler
# OR
git checkout part2-advanced # For advanced compiler
```

