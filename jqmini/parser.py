from .token import TokenType as T
from .ast import Query,BinaryExpr,UnaryExpr,Comparison

class ParserError(Exception): pass

class Parser:
    def __init__(self,tokens):
        self.t=tokens
        self.i=0

    @property
    def c(self):
        return self.t[self.i]

    def take(self,typ,msg=None):
        x=self.c
        if x.type!=typ:
            raise ParserError(msg or f"Expected {typ.name}, got {x.type.name} at {x.line}:{x.column}")
        self.i+=1
        return x

    def parse(self):
        self.take(T.QUERY)
        name=self.take(T.IDENT).value
        self.take(T.FROM)
        source=self.take(T.STRING).value

        where=None
        if self.c.type==T.WHERE:
            self.i+=1
            where=self.parse_or()

        self.take(T.SELECT)
        fields=[self.take(T.IDENT).value]
        while self.c.type==T.COMMA:
            self.i+=1
            fields.append(self.take(T.IDENT).value)

        sf=None
        desc=False
        lim=None

        if self.c.type==T.SORT:
            self.i+=1
            self.take(T.BY)
            sf=self.take(T.IDENT).value
            if self.c.type==T.DESC:
                self.i+=1
                desc=True
            elif self.c.type==T.ASC:
                self.i+=1

        if self.c.type==T.LIMIT:
            self.i+=1
            lim=self.take(T.NUMBER).value
            if not isinstance(lim,int):
                raise ParserError("LIMIT must be an integer")

        self.take(T.EOF)
        return Query(name,source,fields,where,sf,desc,lim)

    def parse_or(self):
        n=self.parse_and()
        while self.c.type==T.OR:
            self.i+=1
            n=BinaryExpr("OR",n,self.parse_and())
        return n

    def parse_and(self):
        n=self.parse_not()
        while self.c.type==T.AND:
            self.i+=1
            n=BinaryExpr("AND",n,self.parse_not())
        return n

    def parse_not(self):
        if self.c.type==T.NOT:
            self.i+=1
            return UnaryExpr("NOT",self.parse_not())
        return self.primary()

    def primary(self):
        if self.c.type==T.LPAREN:
            self.i+=1
            n=self.parse_or()
            self.take(T.RPAREN)
            return n
        return self.comparison()

    def comparison(self):
        f=self.take(T.IDENT).value
        ops={T.EQ:"=",T.NE:"!=",T.GT:">",T.GE:">=",T.LT:"<",T.LE:"<="}
        if self.c.type not in ops:
            raise ParserError("Expected comparison operator")
        op=ops[self.c.type]
        self.i+=1
        x=self.c
        if x.type in (T.STRING,T.NUMBER):
            v=x.value
        elif x.type==T.TRUE:
            v=True
        elif x.type==T.FALSE:
            v=False
        elif x.type==T.NULL:
            v=None
        else:
            raise ParserError("Expected literal")
        self.i+=1
        return Comparison(f,op,v)
