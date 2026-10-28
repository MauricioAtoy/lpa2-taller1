"""Pruebas unitarias para la clase abstracta Almacenamiento."""

import pytest
from abc import ABC

from models.mueble import Mueble
from models.categorias.almacenamiento import Almacenamiento
from fixtures.dobles import AlmacenamientoFalso


class TestAlmacenamientoEstructura:
    def test_hereda_de_mueble(self):
        assert issubclass(Almacenamiento, Mueble)

    def test_es_abstracta(self):
        assert issubclass(Almacenamiento, ABC)

    def test_no_se_puede_instanciar(self):
        with pytest.raises(TypeError):
            Almacenamiento("A", "Madera", "Negro", 100.0, 2, 50.0)

    def test_metodos_abstractos(self):
        assert Almacenamiento.__abstractmethods__ == frozenset(
            {"calcular_precio", "obtener_descripcion"}
        )

    def test_subclase_incompleta_no_se_puede_instanciar(self):
        class Incompleta(Almacenamiento):
            def calcular_precio(self):
                return 0.0

        with pytest.raises(TypeError):
            Incompleta("X", "Madera", "Negro", 10.0, 1, 10.0)


class TestAlmacenamientoConstructor:
    def test_asigna_atributos_propios(self, almacenamiento_falso):
        assert almacenamiento_falso.num_compartimentos == 3
        assert almacenamiento_falso.capacidad_litros == 200.0

    def test_inicializa_atributos_de_mueble(self, almacenamiento_falso):
        assert almacenamiento_falso.nombre == "Alm Test"
        assert almacenamiento_falso.precio_base == 100.0
        assert isinstance(almacenamiento_falso, Mueble)


class TestNumCompartimentos:
    def test_getter(self, almacenamiento_falso):
        assert almacenamiento_falso.num_compartimentos == 3

    @pytest.mark.parametrize("valor", [1, 2, 10])
    def test_setter_valido(self, almacenamiento_falso, valor):
        almacenamiento_falso.num_compartimentos = valor
        assert almacenamiento_falso.num_compartimentos == valor

    @pytest.mark.parametrize("valor", [0, -1, -10])
    def test_setter_rechaza_no_positivos(self, almacenamiento_falso, valor):
        with pytest.raises(
            ValueError, match="El número de compartimentos debe ser mayor a 0"
        ):
            almacenamiento_falso.num_compartimentos = valor

    def test_setter_invalido_no_modifica(self, almacenamiento_falso):
        with pytest.raises(ValueError):
            almacenamiento_falso.num_compartimentos = 0
        assert almacenamiento_falso.num_compartimentos == 3


class TestCapacidadLitros:
    def test_getter(self, almacenamiento_falso):
        assert almacenamiento_falso.capacidad_litros == 200.0

    @pytest.mark.parametrize("valor", [0.1, 50, 350.5])
    def test_setter_valido(self, almacenamiento_falso, valor):
        almacenamiento_falso.capacidad_litros = valor
        assert almacenamiento_falso.capacidad_litros == valor

    @pytest.mark.parametrize("valor", [0, -1, -10.5])
    def test_setter_rechaza_no_positivos(self, almacenamiento_falso, valor):
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            almacenamiento_falso.capacidad_litros = valor

    def test_setter_invalido_no_modifica(self, almacenamiento_falso):
        with pytest.raises(ValueError):
            almacenamiento_falso.capacidad_litros = -1
        assert almacenamiento_falso.capacidad_litros == 200.0


class TestCalcularFactorAlmacenamiento:
    @pytest.mark.parametrize(
        "compartimentos,capacidad,esperado",
        [
            (1, 100.0, 1.02),  # 1 + 0 + 1*0.02
            (5, 100.0, 1.22),  # 1 + 4*0.05 + 0.02
            (1, 500.0, 1.10),  # 1 + 0 + 5*0.02
            (3, 200.0, 1.14),  # 1 + 2*0.05 + 2*0.02
        ],
    )
    def test_valores_calculados(self, compartimentos, capacidad, esperado):
        alm = AlmacenamientoFalso("A", "M", "C", 100.0, compartimentos, capacidad)
        assert alm.calcular_factor_almacenamiento() == pytest.approx(esperado)

    def test_siempre_mayor_a_uno(self):
        alm = AlmacenamientoFalso("A", "M", "C", 100.0, 1, 1.0)
        assert alm.calcular_factor_almacenamiento() > 1.0

    def test_crece_con_compartimentos(self):
        pequeno = AlmacenamientoFalso("A", "M", "C", 100.0, 2, 100.0)
        grande = AlmacenamientoFalso("A", "M", "C", 100.0, 8, 100.0)
        assert (
            grande.calcular_factor_almacenamiento()
            > pequeno.calcular_factor_almacenamiento()
        )

    def test_crece_con_capacidad(self):
        pequeno = AlmacenamientoFalso("A", "M", "C", 100.0, 3, 50.0)
        grande = AlmacenamientoFalso("A", "M", "C", 100.0, 3, 400.0)
        assert (
            grande.calcular_factor_almacenamiento()
            > pequeno.calcular_factor_almacenamiento()
        )

    def test_refleja_cambios_en_setters(self, almacenamiento_falso):
        almacenamiento_falso.num_compartimentos = 4
        almacenamiento_falso.capacidad_litros = 300.0
        assert almacenamiento_falso.calcular_factor_almacenamiento() == pytest.approx(
            1.21
        )


class TestObtenerInfoAlmacenamiento:
    def test_formato_exacto(self, almacenamiento_falso):
        assert (
            almacenamiento_falso.obtener_info_almacenamiento()
            == "Compartimentos: 3, Capacidad: 200.0L"
        )

    def test_refleja_cambios(self, almacenamiento_falso):
        almacenamiento_falso.num_compartimentos = 5
        almacenamiento_falso.capacidad_litros = 250.0
        assert (
            almacenamiento_falso.obtener_info_almacenamiento()
            == "Compartimentos: 5, Capacidad: 250.0L"
        )


class TestAlmacenamientoMetodosAbstractos:
    def test_calcular_precio_es_abstracto(self):
        assert Almacenamiento.calcular_precio.__isabstractmethod__

    def test_obtener_descripcion_es_abstracto(self):
        assert Almacenamiento.obtener_descripcion.__isabstractmethod__

    def test_subclase_los_implementa(self, almacenamiento_falso):
        assert almacenamiento_falso.calcular_precio() == pytest.approx(114.0)
        assert "Compartimentos: 3" in almacenamiento_falso.obtener_descripcion()
