"""Del AST a un numero.

Recorre el arbol de abajo hacia arriba: para evaluar una operacion hay que
evaluar primero sus dos lados.
"""

from .ast import Numero, OperacionBinaria
from .errores import ErrorDeEvaluacion


from .ast import Nodo, Numero, OperacionBinaria
from .errores import ErrorDeEvaluacion


def _calcular_binaria(op: str, izq, der):
    if op == "+":
        return izq + der
    if op == "-":
        return izq - der
    if op == "*":
        return izq * der
    if op == "/":
        if der == 0:
            raise ErrorDeEvaluacion("Division por cero")
        resultado = izq / der
        return int(resultado) if resultado.is_integer() else resultado

    raise ErrorDeEvaluacion(f"Operador no soportado {op!r}")


def evaluar(nodo: Nodo):
    """Evalua un nodo del AST y regresa su valor numerico."""
    if isinstance(nodo, Numero):
        return nodo.valor

    if isinstance(nodo, OperacionBinaria):
        izq = evaluar(nodo.izquierda)
        der = evaluar(nodo.derecha)
        return _calcular_binaria(nodo.operador, izq, der)

    raise ErrorDeEvaluacion(f"Nodo AST no soportado: {type(nodo).__name__}")