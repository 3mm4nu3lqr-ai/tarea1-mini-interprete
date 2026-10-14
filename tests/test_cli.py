from mini_interprete.ast import Numero, OperacionBinaria
from mini_interprete.cli import formatear_arbol


def test_dibujo_del_arbol():
    arbol = OperacionBinaria(
        "+", Numero(3), OperacionBinaria("*", Numero(4), Numero(2))
    )
    assert formatear_arbol(arbol) == [
        "+",
        "|-- 3",
        "`-- *",
        "    |-- 4",
        "    `-- 2",
    ]
