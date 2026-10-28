"""Pruebas unitarias para la clase abstracta Superficie."""

import pytest
from abc import ABC

from models.mueble import Mueble
from models.categorias.superficies import Superficie
from fixtures.dobles import SuperficieFalsa


class TestSuperficieEstructura:
    def test_hereda_de_mueble(self):
        assert issubclass(Superficie, Mueble)

    def test_es_abstracta(self):
        assert issubclass(Superficie, ABC)

    def test_no_se_puede_instanciar(self):
        with pytest.raises(TypeError):
            Superficie("S", "M", "C", 100.0, 100.0, 50.0, 75.0)

    def test_metodos_abstractos(self):
        assert Superficie.__abstractmethods__ == frozenset(
            {"calcular_precio", "obtener_descripcion"}
        )


class TestSuperficieConstructor:
    def test_asigna_dimensiones(self, superficie_falsa):
        assert superficie_falsa.largo == 100.0
        assert superficie_falsa.ancho == 50.0
        assert superficie_falsa.altura == 75.0

    def test_inicializa_atributos_de_mueble(self, superficie_falsa):
        assert superficie_falsa.nombre == "Sup Test"
        assert superficie_falsa.precio_base == 100.0


@pytest.mark.parametrize(
    "atributo,mensaje",
    [
        ("largo", "El largo debe ser mayor a 0"),
        ("ancho", "El ancho debe ser mayor a 0"),
        ("altura", "La altura debe ser mayor a 0"),
    ],
)
class TestDimensiones:
    """Largo, ancho y altura comparten la misma validación."""

    def test_getter(self, superficie_falsa, atributo, mensaje):
        esperado = {"largo": 100.0, "ancho": 50.0, "altura": 75.0}[atributo]
        assert getattr(superficie_falsa, atributo) == esperado

    @pytest.mark.parametrize("valor", [0.5, 1, 200.0])
    def test_setter_valido(self, superficie_falsa, atributo, mensaje, valor):
        setattr(superficie_falsa, atributo, valor)
        assert getattr(superficie_falsa, atributo) == valor

    @pytest.mark.parametrize("valor", [0, -1, -50.5])
    def test_setter_rechaza_no_positivos(
        self, superficie_falsa, atributo, mensaje, valor
    ):
        with pytest.raises(ValueError, match=mensaje):
            setattr(superficie_falsa, atributo, valor)

    def test_setter_invalido_no_modifica(self, superficie_falsa, atributo, mensaje):
        antes = getattr(superficie_falsa, atributo)
        with pytest.raises(ValueError):
            setattr(superficie_falsa, atributo, 0)
        assert getattr(superficie_falsa, atributo) == antes


class TestCalcularArea:
    def test_area_basica(self, superficie_falsa):
        assert superficie_falsa.calcular_area() == 5000.0

    def test_area_no_depende_de_altura(self, superficie_falsa):
        superficie_falsa.altura = 200.0
        assert superficie_falsa.calcular_area() == 5000.0

    def test_area_refleja_cambios(self, superficie_falsa):
        superficie_falsa.largo = 200.0
        superficie_falsa.ancho = 100.0
        assert superficie_falsa.calcular_area() == 20000.0


class TestCalcularFactorTamaño:
    @pytest.mark.parametrize(
        "largo,ancho,esperado",
        [
            (100.0, 100.0, 1.05),  # 10000 cm² -> +5%
            (100.0, 50.0, 1.025),  # 5000 cm²
            (200.0, 100.0, 1.10),  # 20000 cm²
            (10.0, 10.0, 1.0005),  # 100 cm²
        ],
    )
    def test_valores(self, largo, ancho, esperado):
        s = SuperficieFalsa("S", "M", "C", 100.0, largo, ancho, 75.0)
        assert s.calcular_factor_tamaño() == pytest.approx(esperado)

    def test_siempre_mayor_a_uno(self, superficie_falsa):
        assert superficie_falsa.calcular_factor_tamaño() > 1.0


class TestObtenerInfoSuperficie:
    def test_formato_exacto(self, superficie_falsa):
        assert (
            superficie_falsa.obtener_info_superficie()
            == "Dimensiones: 100.0x50.0x75.0cm (Área: 5000.0cm²)"
        )


class TestSuperficieMetodosAbstractos:
    def test_calcular_precio_es_abstracto(self):
        assert Superficie.calcular_precio.__isabstractmethod__

    def test_obtener_descripcion_es_abstracto(self):
        assert Superficie.obtener_descripcion.__isabstractmethod__

    def test_subclase_los_implementa(self, superficie_falsa):
        assert superficie_falsa.calcular_precio() == pytest.approx(102.5)
        assert "Dimensiones" in superficie_falsa.obtener_descripcion()
