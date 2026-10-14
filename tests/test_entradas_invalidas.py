import pytest

from mini_interprete.cli import interpretar
from mini_interprete.errores import ErrorDeSintaxis


def test_operador_al_final():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 +")


def test_parentesis_sin_cerrar():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("(3 + 4")

        
def test_parentesis_sin_abrir():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 + 4)")


def test_operadores_seguidos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 + * 4")

        
def test_parentesis_vacios():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("()")
        

def test_caracter_no_reconocido():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 $ 4")


def test_entrada_vacia_invalida():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("")


def test_entrada_de_solo_espacios_invalidos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("   ")


def test_dos_numeros_sin_operador_invalido():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("3 4")

        
def test_menos_unario_invalido():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-3")


def test_caracter_inesperado_indica_la_posicion():
    with pytest.raises(ErrorDeSintaxis) as msg:
        interpretar("3 / - 4")

    assert msg.value.posicion == 4


def test_caracter_no_reconocido_indica_la_posicion():
    with pytest.raises(ErrorDeSintaxis) as msg:
        interpretar("3 $ 4")

    assert msg.value.posicion == 2
