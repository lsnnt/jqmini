import argparse, json, sys
from jqmini.lexer import Lexer, LexerError
from jqmini.parser import Parser, ParserError
from jqmini.semantic import SemanticAnalyzer, SemanticError
from jqmini.ir import IRBuilder
from jqmini.optimizer import Optimizer
from jqmini.codegen import PythonCodeGenerator

def compile_query(source, schema):
    tokens = Lexer().tokenize(source)
    ast = Parser(tokens).parse()
    SemanticAnalyzer(schema).analyze(ast)
    ir = IRBuilder().build(ast)
    ir = Optimizer().optimize(ir)
    return PythonCodeGenerator().generate(ir)

def main():
    p=argparse.ArgumentParser(description="JQMini JSON Query Compiler")
    p.add_argument("query")
    p.add_argument("--data", required=True)
    p.add_argument("--emit", action="store_true")
    p.add_argument("--emit-file")
    a=p.parse_args()
    try:
        source=open(a.query,encoding="utf8").read()
        data=json.load(open(a.data,encoding="utf8"))
        if not isinstance(data,list) or any(not isinstance(x,dict) for x in data):
            raise ValueError("JSON input must be an array of objects")
        schema=set().union(*(x.keys() for x in data)) if data else set()
        code=compile_query(source,schema)
        if a.emit: print(code)
        if a.emit_file:
            open(a.emit_file,"w",encoding="utf8").write(code)
            print("Generated:",a.emit_file)
        ns={}
        exec(code,ns)
        print(json.dumps(ns["run"](data),indent=2))
    except (LexerError,ParserError,SemanticError,ValueError,FileNotFoundError,json.JSONDecodeError) as e:
        print("JQMini error:",e,file=sys.stderr); sys.exit(1)

if __name__=="__main__": main()
