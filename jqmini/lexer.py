import re, ast
from .token import Token,TokenType,KEYWORDS

class LexerError(Exception): pass

class Lexer:
    pat=re.compile(r'''(?P<WS>[ \t\r]+)|(?P<NL>\n)|(?P<CMT>\#[^\n]*)|
(?P<STRING>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|
(?P<NUMBER>-?(?:0|[1-9]\d*)(?:\.\d+)?)|
(?P<GE>>=)|(?P<LE><=)|(?P<NE>!=)|(?P<EQ>=)|(?P<GT>>)|(?P<LT><)|
(?P<COMMA>,)|(?P<LPAREN>\()|(?P<RPAREN>\))|
(?P<IDENT>[A-Za-z_][A-Za-z0-9_]*)''',re.X)

    def tokenize(self,s):
        out=[]; pos=0; line=1; col=1
        while pos<len(s):
            m=self.pat.match(s,pos)
            if not m: raise LexerError(f"Unexpected character {s[pos]!r} at {line}:{col}")
            k=m.lastgroup; text=m.group(); sl,sc=line,col
            pos=m.end()
            if k=="NL": line+=1; col=1; continue
            if k in ("WS","CMT"): col+=len(text); continue
            if k=="STRING": val=ast.literal_eval(text); typ=TokenType.STRING
            elif k=="NUMBER": val=float(text) if "." in text else int(text); typ=TokenType.NUMBER
            elif k=="IDENT": val=text; typ=KEYWORDS.get(text.upper(),TokenType.IDENT)
            else: val=text; typ=TokenType[k]
            out.append(Token(typ,val,sl,sc)); col+=len(text)
        out.append(Token(TokenType.EOF,None,line,col)); return out
