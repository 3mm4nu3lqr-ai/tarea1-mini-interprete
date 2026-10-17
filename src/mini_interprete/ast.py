"""Los nodos del arbol de sintaxis abstracta.

Para  3 + 4 * 2  el arbol es:

              OperacionBinaria('+')
              /                   \\
        Numero(3)          OperacionBinaria('*')
                            /                  \\
                      Numero(4)            Numero(2)

Un Numero no contiene nada. Una OperacionBinaria contiene otros nodos, que a
su vez pueden ser numeros u otras operaciones.
"""


class Nodo:
    """Cualquier cosa que pueda aparecer en el arbol."""
    def __init__(self, valor):
        pass

    def __repr__(self):
        pass

    def __eq__(self, otro):
        if not isinstance(otro, type(self)):
            return NotImplemented


class Numero(Nodo):
    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"Numero({self.valor})"

    def __eq__(self, otro):
        return self.valor == otro.valor


class OperacionBinaria(Nodo):
    def __init__(self, operador: str, izquierda: Nodo, derecha: Nodo):
        self.operador = operador
        self.izquierda = izquierda
        self.derecha = derecha

    def __repr__(self):
        return (f"OperacionBinaria({self.operador!r}, "
                f"{self.izquierda!r}, {self.derecha!r})")

    def __eq__(self, otro):
        return (self.operador == otro.operador
                and self.izquierda == otro.izquierda
                and self.derecha == otro.derecha)
