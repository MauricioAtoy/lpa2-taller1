"""Pruebas unitarias para la clase abstracta Mueble."""

import pytest
from abc import ABC

from models.mueble import Mueble
from fixtures.dobles import MuebleFalso


class TestMuebleEstructura:
    def test_es_clase_abstracta(self):
        assert issubclass(Mueble, ABC)

    def test_no_se_puede_instanciar(self):
        with pytest.raises(TypeError):
            Mueble("Mesa", "Madera", "Café", 100.0)

    def test_metodos_abstractos(self):
        assert Mueble.__abstractmethods__ == frozenset(
            {"calcular_precio", "obtener_descripcion"}
        )

    def test_subclase_incompleta_no_se_puede_instanciar(self):
        class Incompleta(Mueble):
            def calcular_precio(self):
                return 0

        with pytest.raises(TypeError):
            Incompleta("X", "Madera", "Café", 1.0)


class TestMuebleConstructor:
    def test_asigna_atributos(self, mueble_falso):
        assert mueble_falso.nombre == "Mueble Test"
        assert mueble_falso.material == "Madera"
        assert mueble_falso.color == "Café"
        assert mueble_falso.precio_base == 100.0


class TestMuebleNombre:
    def test_getter(self, mueble_falso):
        assert mueble_falso.nombre == "Mueble Test"

    def test_setter_valido(self, mueble_falso):
        mueble_falso.nombre = "Nuevo"
        assert mueble_falso.nombre == "Nuevo"

    def test_setter_elimina_espacios(self, mueble_falso):
        mueble_falso.nombre = "  Nuevo  "
        assert mueble_falso.nombre == "Nuevo"

    @pytest.mark.parametrize("valor", ["", "   ", None])
    def test_setter_rechaza_vacio(self, mueble_falso, valor):
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            mueble_falso.nombre = valor

    def test_setter_invalido_no_modifica(self, mueble_falso):
        with pytest.raises(ValueError):
            mueble_falso.nombre = ""
        assert mueble_falso.nombre == "Mueble Test"


class TestMuebleMaterial:
    def test_getter(self, mueble_falso):
        assert mueble_falso.material == "Madera"

    def test_setter_valido(self, mueble_falso):
        mueble_falso.material = "Metal"
        assert mueble_falso.material == "Metal"

    def test_setter_elimina_espacios(self, mueble_falso):
        mueble_falso.material = " Metal "
        assert mueble_falso.material == "Metal"

    @pytest.mark.parametrize("valor", ["", "  ", None])
    def test_setter_rechaza_vacio(self, mueble_falso, valor):
        with pytest.raises(ValueError, match="El material no puede estar vacío"):
            mueble_falso.material = valor


class TestMuebleColor:
    def test_getter(self, mueble_falso):
        assert mueble_falso.color == "Café"

    def test_setter_valido(self, mueble_falso):
        mueble_falso.color = "Rojo"
        assert mueble_falso.color == "Rojo"

    def test_setter_elimina_espacios(self, mueble_falso):
        mueble_falso.color = " Rojo "
        assert mueble_falso.color == "Rojo"

    @pytest.mark.parametrize("valor", ["", "  ", None])
    def test_setter_rechaza_vacio(self, mueble_falso, valor):
        with pytest.raises(ValueError, match="El color no puede estar vacío"):
            mueble_falso.color = valor


class TestMueblePrecioBase:
    def test_getter(self, mueble_falso):
        assert mueble_falso.precio_base == 100.0

    @pytest.mark.parametrize("valor", [0, 0.0, 50.5, 1000])
    def test_setter_acepta_valores_validos(self, mueble_falso, valor):
        mueble_falso.precio_base = valor
        assert mueble_falso.precio_base == valor

    @pytest.mark.parametrize("valor", [-1, -0.01, -500])
    def test_setter_rechaza_negativos(self, mueble_falso, valor):
        with pytest.raises(ValueError, match="El precio base no puede ser negativo"):
            mueble_falso.precio_base = valor

    def test_setter_invalido_no_modifica(self, mueble_falso):
        with pytest.raises(ValueError):
            mueble_falso.precio_base = -5
        assert mueble_falso.precio_base == 100.0


class TestMuebleMetodosAbstractos:
    def test_calcular_precio_es_abstracto(self):
        assert Mueble.calcular_precio.__isabstractmethod__

    def test_obtener_descripcion_es_abstracto(self):
        assert Mueble.obtener_descripcion.__isabstractmethod__

    def test_subclase_concreta_los_implementa(self, mueble_falso):
        assert mueble_falso.calcular_precio() == 100.0
        assert mueble_falso.obtener_descripcion() == "Falso: Mueble Test"


class TestMuebleRepresentaciones:
    def test_str(self, mueble_falso):
        assert str(mueble_falso) == "Mueble Test de Madera en color Café"

    def test_repr(self, mueble_falso):
        assert repr(mueble_falso) == (
            "Mueble(nombre='Mueble Test', material='Madera', "
            "color='Café', precio_base=100.0)"
        )

    def test_str_refleja_cambios(self, mueble_falso):
        mueble_falso.color = "Azul"
        assert "Azul" in str(mueble_falso)


def test_instancia_de_mueble(mueble_falso):
    assert isinstance(mueble_falso, Mueble)
    assert isinstance(mueble_falso, MuebleFalso)
