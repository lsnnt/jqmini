from dataclasses import dataclass
@dataclass
class IR:
    source:str; fields:list; predicate:object; sort_field:str; sort_desc:bool; limit:int
class IRBuilder:
    def build(self,q): return IR(q.source,q.fields,q.where,q.sort_field,q.sort_desc,q.limit)
