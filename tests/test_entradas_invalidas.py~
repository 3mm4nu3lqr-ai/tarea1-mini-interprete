import pytest

from mini_interprete.cli import interpretar
from mini_interprete.errores import ErrorDeSintaxis


def test_operador_al_final():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 +")


def test_parentesis_sin_cerrar():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("(3 + 4")


def test_caracter_no_reconocido():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 $ 4")
