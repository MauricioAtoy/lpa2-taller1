"""Pruebas unitarias para el Comedor simple de models/concretos."""

import pytest
from unittest.mock import Mock

from models.concretos.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla


@pytest.fixture
def mesa_mock():
    m = Mock(spec=Mesa)
    m.calcular_precio.return_value = 1000.0
    m.obtener_descripcion.return_value = "Mesa Mock"
    return m


def crear_silla_mock(precio=100.0, descripcion="Silla Mock"):
    s = Mock(spec=Silla)
    s.calcular_precio.return_value = precio
    s.obtener_descripcion.return_value = descripcion
    return s


class TestComedorConstructor:
    def test_guarda_la_mesa(self, mesa_mock):
        assert Comedor(mesa_mock).mesa is mesa_mock

    def test_sillas_por_defecto_es_lista_vacia(self, mesa_mock):
        assert Comedor(mesa_mock).sillas == []

    def test_guarda_las_sillas_recibidas(self, mesa_mock):
        sillas = [crear_silla_mock(), crear_silla_mock()]
        assert Comedor(mesa_mock, sillas).sillas == sillas

    def test_instancias_no_comparten_lista_por_defecto(self, mesa_mock):
        c1, c2 = Comedor(mesa_mock), Comedor(mesa_mock)
        c1.agregar_silla(crear_silla_mock())
        assert c2.cantidad_sillas() == 0


class TestComedorAgregarSilla:
    def test_agrega_una_silla(self, mesa_mock):
        c = Comedor(mesa_mock)
        s = crear_silla_mock()
        c.agregar_silla(s)
        assert c.sillas == [s]

    def test_agrega_varias_en_orden(self, mesa_mock):
        c = Comedor(mesa_mock)
        s1, s2 = crear_silla_mock(), crear_silla_mock()
        c.agregar_silla(s1)
        c.agregar_silla(s2)
        assert c.sillas == [s1, s2]


class TestComedorQuitarSilla:
    def test_quita_silla_existente(self, mesa_mock):
        s = crear_silla_mock()
        c = Comedor(mesa_mock, [s])
        c.quitar_silla(s)
        assert c.sillas == []

    def test_silla_inexistente_no_hace_nada(self, mesa_mock):
        s = crear_silla_mock()
        c = Comedor(mesa_mock, [s])
        c.quitar_silla(crear_silla_mock())
        assert c.sillas == [s]

    def test_quita_solo_la_indicada(self, mesa_mock):
        s1, s2 = crear_silla_mock(), crear_silla_mock()
        c = Comedor(mesa_mock, [s1, s2])
        c.quitar_silla(s1)
        assert c.sillas == [s2]


class TestComedorCantidadSillas:
    def test_vacio(self, mesa_mock):
        assert Comedor(mesa_mock).cantidad_sillas() == 0

    @pytest.mark.parametrize("n", [1, 4, 8])
    def test_con_n_sillas(self, mesa_mock, n):
        c = Comedor(mesa_mock, [crear_silla_mock() for _ in range(n)])
        assert c.cantidad_sillas() == n


class TestComedorCalcularPrecioTotal:
    def test_solo_mesa(self, mesa_mock):
        assert Comedor(mesa_mock).calcular_precio_total() == 1000.0

    def test_mesa_mas_sillas(self, mesa_mock):
        c = Comedor(mesa_mock, [crear_silla_mock(100.0), crear_silla_mock(150.0)])
        assert c.calcular_precio_total() == 1250.0

    def test_no_aplica_descuento(self, mesa_mock):
        c = Comedor(mesa_mock, [crear_silla_mock(100.0) for _ in range(6)])
        assert c.calcular_precio_total() == 1600.0

    def test_con_objetos_reales(self):
        c = Comedor(Mesa("M", "Roble", "N", 1000.0), [Silla("S", "R", "N", 100.0)])
        assert c.calcular_precio_total() == pytest.approx(1048.0 + 110.0)


class TestComedorDescripcion:
    def test_incluye_la_mesa(self, mesa_mock):
        assert "Comedor con mesa: Mesa Mock" in Comedor(mesa_mock).descripcion()

    def test_cantidad_de_sillas(self, mesa_mock):
        c = Comedor(mesa_mock, [crear_silla_mock(), crear_silla_mock()])
        assert "y 2 sillas:" in c.descripcion()

    def test_enumera_las_sillas(self, mesa_mock):
        c = Comedor(
            mesa_mock,
            [crear_silla_mock(descripcion="Silla A"), crear_silla_mock(descripcion="Silla B")],
        )
        d = c.descripcion()
        assert "1. Silla A" in d
        assert "2. Silla B" in d

    def test_sin_sillas(self, mesa_mock):
        assert "y 0 sillas:" in Comedor(mesa_mock).descripcion()
