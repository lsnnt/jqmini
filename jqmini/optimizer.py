from dataclasses import replace
from .ast import BinaryExpr,UnaryExpr,Literal
class Optimizer:
    def optimize(self,ir): return replace(ir,predicate=self.fold(ir.predicate))
    def fold(self,n):
        if n is None:return None
        if isinstance(n,BinaryExpr):
            a,b=self.fold(n.left),self.fold(n.right)
            if isinstance(a,Literal) and isinstance(a.value,bool):
                if n.op=="AND": return b if a.value else Literal(False)
                return Literal(True) if a.value else b
            if isinstance(b,Literal) and isinstance(b.value,bool):
                if n.op=="AND": return a if b.value else Literal(False)
                return Literal(True) if b.value else a
            return BinaryExpr(n.op,a,b)
        if isinstance(n,UnaryExpr):
            a=self.fold(n.operand)
            return Literal(not a.value) if isinstance(a,Literal) and isinstance(a.value,bool) else UnaryExpr(n.op,a)
        return n
