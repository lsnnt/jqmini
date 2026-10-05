from dataclasses import dataclass
from enum import Enum,auto

class TokenType(Enum):
    QUERY=auto(); FROM=auto(); WHERE=auto(); SELECT=auto(); SORT=auto(); BY=auto()
    ASC=auto(); DESC=auto(); LIMIT=auto(); AND=auto(); OR=auto(); NOT=auto()
    TRUE=auto(); FALSE=auto(); NULL=auto()
    IDENT=auto(); STRING=auto(); NUMBER=auto()
    EQ=auto(); NE=auto(); GT=auto(); GE=auto(); LT=auto(); LE=auto()
    COMMA=auto(); LPAREN=auto(); RPAREN=auto(); EOF=auto()

KEYWORDS={x.name:x for x in TokenType if x.name in {
    "QUERY","FROM","WHERE","SELECT","SORT","BY","ASC","DESC","LIMIT",
    "AND","OR","NOT","TRUE","FALSE","NULL"
}}

@dataclass
class Token:
    type: TokenType
    value: object
    line: int
    column: int
