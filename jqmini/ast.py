from dataclasses import dataclass
@dataclass
class Query:
    name:str; source:str; fields:list; where:object=None
    sort_field:str=None; sort_desc:bool=False; limit:int=None
@dataclass
class BinaryExpr: op:str; left:object; right:object
@dataclass
class UnaryExpr: op:str; operand:object
@dataclass
class Comparison: field:str; op:str; value:object
@dataclass
class Literal: value:object
