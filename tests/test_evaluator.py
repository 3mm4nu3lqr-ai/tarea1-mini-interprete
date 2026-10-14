"""Pruebas del evaluador: del AST a un numero."""

import pytest

from mini_interprete.cli import interpretar
from mini_interprete.errores import ErrorDeEvaluacion

def test_suma():
    assert interpretar("3 + 4") == 7


def test_resta():
    assert interpretar("10 - 3") == 7


def test_multiplicacion():
    assert interpretar("6 * 7") == 42


def test_division():
    assert interpretar("10 / 2") == 5


def test_precedencia_sin_parentesis():
    assert interpretar("3 + 4 * 2") == 11


def test_precedencia_con_parentes():
    assert interpretar("(3 + 4) * 2") == 14

    
# Pruebas añadidas por el equipo
def test_division_entre_cero():
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("5 / 0")

        
def test_division_se_asocia_a_la_izquierda():
    assert interpretar("8 / 4 / 2") == 1

    
def test_resta_se_asocia_a_la_izquierda():
    assert interpretar("10 - 3 - 2") == 5

    
def test_resta_con_resultado_negativo():
    assert interpretar("3 - 5") == -2

    
def test_division_no_exacta():
    assert interpretar("10 / 4") == 2.5


def test_ceros_a_la_izquierda():
    assert interpretar("007") == 7


def test_parentesis_redundantes():
    assert interpretar("((3))") == 3
