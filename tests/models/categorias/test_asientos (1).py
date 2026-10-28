"""Pruebas unitarias para la clase abstracta Asiento."""

import pytest
from abc import ABC

from models.mueble import Mueble
from models.categorias.asientos import Asiento
from fixtures.dobles import AsientoFalso


class TestAsientoEstructura:
    def test_hereda_de_mueble(self):
        assert issubclass(Asiento, Mueble)

    def test_es_abstracta(self):
        assert issubclass(Asiento, ABC)

    def test_no_se_puede_instanciar(self):
        with pytest.raises(TypeError):
            Asiento("A", "M", "C", 100.0, 1, True)

    def test_metodos_abstractos(self):
        assert Asiento.__abstractmethods__ == frozenset(
            {"calcular_precio", "obtener_descripcion"}
        )


class TestAsientoConstructor:
    def test_asigna_atributos_propios(self, asiento_falso):
        assert asiento_falso.capacidad_personas == 2
        assert asiento_falso.tiene_respaldo is True
        assert asiento_falso.material_tapizado == "tela"

    def test_material_tapizado_es_opcional(self):
        a = AsientoFalso("A", "M", "C", 100.0, 1, False)
        assert a.material_tapizado is None

    def test_inicializa_atributos_de_mueble(self, asiento_falso):
        assert asiento_falso.nombre == "Asiento Test"
        assert asiento_falso.material == "Madera"
        assert asiento_falso.color == "Café"
        assert asiento_falso.precio_base == 100.0


class TestCapacidadPersonas:
    def test_getter(self, asiento_falso):
        assert asiento_falso.capacidad_personas == 2

    @pytest.mark.parametrize("valor", [1, 3, 10])
    def test_setter_valido(self, asiento_falso, valor):
        asiento_falso.capacidad_personas = valor
        assert asiento_falso.capacidad_personas == valor

    @pytest.mark.parametrize("valor", [0, -1, -5])
    def test_setter_rechaza_no_positivos(self, asiento_falso, valor):
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            asiento_falso.capacidad_personas = valor

    def test_setter_invalido_no_modifica(self, asiento_falso):
        with pytest.raises(ValueError):
            asiento_falso.capacidad_personas = 0
        assert asiento_falso.capacidad_personas == 2


class TestTieneRespaldo:
    def test_getter(self, asiento_falso):
        assert asiento_falso.tiene_respaldo is True

    @pytest.mark.parametrize("valor", [True, False])
    def test_setter(self, asiento_falso, valor):
        asiento_falso.tiene_respaldo = valor
        assert asiento_falso.tiene_respaldo is valor


class TestMaterialTapizado:
    def test_getter(self, asiento_falso):
        assert asiento_falso.material_tapizado == "tela"

    def test_setter(self, asiento_falso):
        asiento_falso.material_tapizado = "cuero"
        assert asiento_falso.material_tapizado == "cuero"

    def test_setter_acepta_none(self, asiento_falso):
        asiento_falso.material_tapizado = None
        assert asiento_falso.material_tapizado is None


class TestCalcularFactorComodidad:
    @pytest.mark.parametrize(
        "capacidad,respaldo,tapizado,esperado",
        [
            (1, False, None, 1.0),  # base
            (1, True, None, 1.1),  # respaldo
            (1, False, "cuero", 1.2),  # cuero
            (1, False, "tela", 1.1),  # tela
            (1, False, "plástico", 1.0),  # tapizado sin recargo
            (3, False, None, 1.1),  # (3-1)*0.05
            (3, True, "cuero", 1.4),  # 1 + 0.1 + 0.2 + 0.1
            (2, True, "tela", 1.25),  # 1 + 0.1 + 0.1 + 0.05
        ],
    )
    def test_combinaciones(self, capacidad, respaldo, tapizado, esperado):
        a = AsientoFalso("A", "M", "C", 100.0, capacidad, respaldo, tapizado)
        assert a.calcular_factor_comodidad() == pytest.approx(esperado)

    @pytest.mark.parametrize("tapizado", ["CUERO", "Cuero", "cuero"])
    def test_tapizado_no_distingue_mayusculas(self, tapizado):
        a = AsientoFalso("A", "M", "C", 100.0, 1, False, tapizado)
        assert a.calcular_factor_comodidad() == pytest.approx(1.2)


class TestObtenerInfoAsiento:
    def test_con_respaldo_y_tapizado(self, asiento_falso):
        assert (
            asiento_falso.obtener_info_asiento()
            == "Capacidad: 2 personas, Respaldo: Sí, Tapizado: tela"
        )

    def test_sin_respaldo_ni_tapizado(self):
        a = AsientoFalso("A", "M", "C", 100.0, 1, False)
        assert a.obtener_info_asiento() == "Capacidad: 1 personas, Respaldo: No"

    def test_no_incluye_tapizado_si_es_none(self):
        a = AsientoFalso("A", "M", "C", 100.0, 1, True, None)
        assert "Tapizado" not in a.obtener_info_asiento()


class TestAsientoMetodosAbstractos:
    def test_calcular_precio_es_abstracto(self):
        assert Asiento.calcular_precio.__isabstractmethod__

    def test_obtener_descripcion_es_abstracto(self):
        assert Asiento.obtener_descripcion.__isabstractmethod__

    def test_subclase_los_implementa(self, asiento_falso):
        # factor = 1 + 0.1 + 0.1 + 0.05 = 1.25
        assert asiento_falso.calcular_precio() == pytest.approx(125.0)
        assert "Capacidad: 2" in asiento_falso.obtener_descripcion()
