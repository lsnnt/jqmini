# JQMini

A complete small compiler for an SQL-like JSON query language.

Pipeline:
Lexer -> Parser/AST -> Semantic Analysis -> IR -> Optimizer -> Python Code Generator

Run:
python main.py examples/query.jq --data examples/students.json

Show generated code:
python main.py examples/query.jq --data examples/students.json --emit

Tests:
python -m unittest discover -s tests -v
