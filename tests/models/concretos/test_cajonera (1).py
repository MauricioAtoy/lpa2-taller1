"""Pruebas unitarias para Cajonera."""

import pytest

from models.concretos.cajonera import Cajonera


class TestCajoneraConstructor:
    def test_valores_por_defecto(self, cajonera):
        assert cajonera.nombre == "Cajonera Básica"
        assert cajonera.material == "Pino"
        assert cajonera.color == "Blanco"
        assert cajonera.precio_base == 500
        assert cajonera.num_cajones == 3
        assert cajonera.tiene_ruedas is False

    def test_valores_personalizados(self):
        c = Cajonera("C", "M", "Col", 300, 5, True)
        assert c.num_cajones == 5
        assert c.tiene_ruedas is True

    def test_precio_base_se_convierte_a_entero(self):
        assert Cajonera("C", "M", "Col", 99.9).precio_base == 99

    def test_precio_base_none_se_vuelve_cero(self):
        assert Cajonera("C", "M", "Col", None).precio_base == 0


class TestCajoneraCalcularPrecio:
    def test_precio_basico(self, cajonera):
        assert cajonera.calcular_precio() == 560  # 500 + 3*20

    @pytest.mark.parametrize("cajones,esperado", [(0, 500), (1, 520), (5, 600), (10, 700)])
    def test_cada_cajon_suma_20(self, cajones, esperado):
        assert Cajonera("C", "M", "Col", 500, cajones).calcular_precio() == esperado

    def test_ruedas_suman_30(self):
        assert Cajonera("C", "M", "Col", 500, 3, True).calcular_precio() == 590

    def test_retorna_entero(self, cajonera):
        assert isinstance(cajonera.calcular_precio(), int)


class TestCajoneraObtenerDescripcion:
    def test_formato_completo(self, cajonera):
        assert cajonera.obtener_descripcion() == (
            "Cajonera 'Cajonera Básica': Material=Pino, Color=Blanco, "
            "Cajones=3, Ruedas=No, Precio base=$500"
        )

    def test_con_ruedas(self):
        c = Cajonera("C", "M", "Col", 500, tiene_ruedas=True)
        assert "Ruedas=Sí" in c.obtener_descripcion()
