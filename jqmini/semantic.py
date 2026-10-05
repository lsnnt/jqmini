from .ast import BinaryExpr,UnaryExpr,Comparison,Literal
class SemanticError(Exception): pass
class SemanticAnalyzer:
    def __init__(self,fields=None): self.fields=fields
    def analyze(self,q):
        if not q.fields: raise SemanticError("SELECT requires fields")
        if self.fields is not None:
            for f in q.fields:
                if f not in self.fields: raise SemanticError(f"Unknown selected field: {f}")
            if q.sort_field and q.sort_field not in self.fields: raise SemanticError(f"Unknown sort field: {q.sort_field}")
        if q.where: self.expr(q.where)
        if q.limit is not None and q.limit<0: raise SemanticError("LIMIT cannot be negative")
    def expr(self,n):
        if isinstance(n,Comparison):
            if self.fields is not None and n.field not in self.fields: raise SemanticError(f"Unknown WHERE field: {n.field}")
        elif isinstance(n,BinaryExpr): self.expr(n.left); self.expr(n.right)
        elif isinstance(n,UnaryExpr): self.expr(n.operand)
        elif isinstance(n,Literal): pass
        else: raise SemanticError("Invalid expression")
