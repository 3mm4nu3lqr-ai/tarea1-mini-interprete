"""De los tokens al AST.

La gramatica que reconoce este parser es:

    expresion := termino  (('+' | '-') termino)*
    termino   := factor   (('*' | '/') factor)*
    factor    := NUMERO | '(' expresion ')'

Los tres niveles son lo que hace que  3 + 4 * 2  se agrupe como  3 + (4 * 2)
y no como  (3 + 4) * 2 : la multiplicacion vive un nivel mas abajo, asi que
se arma primero.
"""

from .ast import Numero, OperacionBinaria
from .errores import ErrorDeSintaxis
from .tokens import TipoToken

OPERADORES_SUMA = (TipoToken.MAS, TipoToken.MENOS)
OPERADORES_PRODUCTO = (TipoToken.POR, TipoToken.ENTRE)


class Parser:

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def parsear(self):
        """Construye el AST de la lista de tokens."""
        if not self.tokens:
            raise ErrorDeSintaxis("La entrada esta vacia", 0)

        arbol = self._expresion()

        actual = self._actual()
        if actual is not None:
            raise ErrorDeSintaxis(f"Token inesperado {actual.valor!r}", actual.posicion)
        
        return arbol

    def _actual(self):
        """El token en la posicion actual, o None si ya no quedan."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _avanzar(self):
        """Consume el token actual y lo regresa."""
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _coincidir(self, *tipos):
        """Si el token actual es de algun tipo esperado, lo consume y lo devuelve, sino, devuelve None"""
        actual = self._actual()
        if actual and actual.tipo in tipos:
            return self._avanzar()
        return None

    def _expresion(self):
        izquierda = self._termino()
        while operador := self._coincidir(*OPERADORES_SUMA):
            derecha = self._termino()
            izquierda = OperacionBinaria(operador.valor, izquierda, derecha)
        return izquierda

    def _termino(self):
        izquierda = self._factor()
        while operador := self._coincidir(*OPERADORES_PRODUCTO):
            derecha = self._factor()
            izquierda = OperacionBinaria(operador.valor, izquierda, derecha)
        return izquierda

    def _factor(self):
        actual = self._actual()
        if actual is None:
            pos = self.tokens[-1].posicion if self.tokens else 0
            raise ErrorDeSintaxis("Falta un número o '('", pos)

        if actual.tipo == TipoToken.NUMERO:
            token = self._avanzar()
            return Numero(token.valor)

        if actual.tipo == TipoToken.PAR_IZQ:
            self._avanzar()
            nodo = self._expresion()
            cierre = self._coincidir(TipoToken.PAR_DER)
            if not cierre:
                pos = self._actual().posicion if self._actual() else (self.tokens[-1].posicion if self.tokens else 0)
                raise ErrorDeSintaxis("Se esperaba ')'", pos)
            return nodo

        raise ErrorDeSintaxis(f"Token inesperado {actual.valor!r}", actual.posicion)
