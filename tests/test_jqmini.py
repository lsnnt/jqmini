import unittest
from jqmini.lexer import Lexer
from jqmini.parser import Parser
from jqmini.semantic import SemanticAnalyzer
from jqmini.ir import IRBuilder
from jqmini.optimizer import Optimizer
from jqmini.codegen import PythonCodeGenerator

DATA=[{"name":"A","age":20,"cgpa":8.1},{"name":"B","age":22,"cgpa":9.2},{"name":"C","age":19,"cgpa":9.9}]

def run(q):
    ast=Parser(Lexer().tokenize(q)).parse()
    SemanticAnalyzer(set(DATA[0])).analyze(ast)
    ir=Optimizer().optimize(IRBuilder().build(ast))
    ns={}; exec(PythonCodeGenerator().generate(ir),ns)
    return ns["run"](DATA)

class TestJQMini(unittest.TestCase):
    def test_where(self):
        self.assertEqual(run('QUERY x FROM "x" WHERE age >= 20 SELECT name'),
                         [{"name":"A"},{"name":"B"}])
    def test_sort_limit(self):
        self.assertEqual(run('QUERY x FROM "x" WHERE age >= 19 SELECT name, cgpa SORT BY cgpa DESC LIMIT 2'),
                         [{"name":"C","cgpa":9.9},{"name":"B","cgpa":9.2}])
    def test_and(self):
        self.assertEqual(run('QUERY x FROM "x" WHERE age >= 20 AND cgpa > 8.5 SELECT name'),
                         [{"name":"B"}])

if __name__=="__main__": unittest.main()
