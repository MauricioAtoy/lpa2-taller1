"""Pruebas unitarias para Escritorio."""

import pytest

from models.concretos.escritorio import Escritorio


class TestEscritorioConstructor:
    def test_valores_por_defecto(self, escritorio):
        assert escritorio.nombre == "Escritorio Básico"
        assert escritorio.material == "Madera"
        assert escritorio.color == "Negro"
        assert escritorio.precio_base == 800
        assert escritorio.forma == "rectangular"
        assert escritorio.tiene_cajones is False
        assert escritorio.num_cajones == 0
        assert escritorio.largo == 1.2
        assert escritorio.tiene_iluminacion is False

    def test_valores_personalizados(self):
        e = Escritorio("E", "M", "C", 500, "en L", True, 3, 1.8, True)
        assert e.forma == "en L"
        assert e.tiene_cajones is True
        assert e.num_cajones == 3
        assert e.largo == 1.8
        assert e.tiene_iluminacion is True

    def test_precio_base_se_convierte_a_entero(self):
        assert Escritorio("E", "M", "C", 99.9).precio_base == 99

    def test_precio_base_none_se_vuelve_cero(self):
        assert Escritorio("E", "M", "C", None).precio_base == 0


class TestEscritorioCalcularPrecio:
    def test_precio_basico(self, escritorio):
        assert escritorio.calcular_precio() == 800

    def test_cajones_suman_25_cada_uno(self):
        e = Escritorio("E", "M", "C", 800, tiene_cajones=True, num_cajones=4)
        assert e.calcular_precio() == 900

    def test_cajones_no_cuentan_si_tiene_cajones_es_false(self):
        e = Escritorio("E", "M", "C", 800, tiene_cajones=False, num_cajones=4)
        assert e.calcular_precio() == 800

    @pytest.mark.parametrize("largo,esperado", [(1.2, 800), (1.5, 800), (1.51, 850), (2.0, 850)])
    def test_largo_mayor_a_1_5_suma_50(self, largo, esperado):
        assert Escritorio("E", "M", "C", 800, largo=largo).calcular_precio() == esperado

    def test_iluminacion_suma_40(self):
        assert Escritorio("E", "M", "C", 800, tiene_iluminacion=True).calcular_precio() == 840

    def test_forma_no_rectangular_suma_30(self):
        assert Escritorio("E", "M", "C", 800, forma="en L").calcular_precio() == 830

    def test_todo_incluido(self):
        e = Escritorio("E", "M", "C", 800, "en L", True, 2, 2.0, True)
        assert e.calcular_precio() == 800 + 50 + 50 + 40 + 30

    def test_retorna_entero(self, escritorio):
        assert isinstance(escritorio.calcular_precio(), int)


class TestEscritorioObtenerDescripcion:
    def test_formato_completo(self, escritorio):
        assert escritorio.obtener_descripcion() == (
            "Escritorio 'Escritorio Básico': Material=Madera, Color=Negro, "
            "Forma=rectangular, Cajones=0, Largo=1.2m, Iluminación=No, Precio base=$800"
        )

    def test_muestra_cajones_si_tiene(self):
        e = Escritorio("E", "M", "C", 800, tiene_cajones=True, num_cajones=3)
        assert "Cajones=3" in e.obtener_descripcion()

    def test_muestra_cero_cajones_si_no_tiene(self):
        e = Escritorio("E", "M", "C", 800, tiene_cajones=False, num_cajones=3)
        assert "Cajones=0" in e.obtener_descripcion()

    def test_con_iluminacion(self):
        e = Escritorio("E", "M", "C", 800, tiene_iluminacion=True)
        assert "Iluminación=Sí" in e.obtener_descripcion()
