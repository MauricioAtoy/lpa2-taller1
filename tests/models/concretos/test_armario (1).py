"""Pruebas unitarias para Armario."""

import pytest

from models.concretos.armario import Armario


class TestArmarioConstructor:
    def test_valores_por_defecto(self, armario):
        assert armario.nombre == "Armario Básico"
        assert armario.material == "Madera"
        assert armario.color == "Café"
        assert armario.precio_base == 1000
        assert armario.num_puertas == 2
        assert armario.num_cajones == 0
        assert armario.tiene_espejos is False

    def test_valores_personalizados(self):
        a = Armario("A", "Metal", "Gris", 500, 4, 3, True)
        assert (a.num_puertas, a.num_cajones, a.tiene_espejos) == (4, 3, True)

    def test_precio_base_se_convierte_a_entero(self):
        assert Armario("A", "M", "C", 99.9).precio_base == 99

    def test_precio_base_none_se_vuelve_cero(self):
        assert Armario("A", "M", "C", None).precio_base == 0


class TestArmarioCalcularPrecio:
    def test_precio_basico(self, armario):
        assert armario.calcular_precio() == 1100  # 1000 + 2*50

    def test_cada_puerta_suma_50(self):
        assert Armario("A", "M", "C", 1000, num_puertas=4).calcular_precio() == 1200

    def test_sin_puertas(self):
        assert Armario("A", "M", "C", 1000, num_puertas=0).calcular_precio() == 1000

    def test_cada_cajon_suma_30(self):
        assert Armario("A", "M", "C", 1000, num_cajones=3).calcular_precio() == 1190

    def test_espejos_suman_100(self):
        assert Armario("A", "M", "C", 1000, tiene_espejos=True).calcular_precio() == 1200

    def test_todo_incluido(self):
        a = Armario("A", "M", "C", 1000, 3, 2, True)
        assert a.calcular_precio() == 1000 + 150 + 60 + 100

    def test_retorna_entero(self, armario):
        assert isinstance(armario.calcular_precio(), int)


class TestArmarioObtenerDescripcion:
    def test_formato_completo(self, armario):
        assert armario.obtener_descripcion() == (
            "Armario 'Armario Básico': Material=Madera, Color=Café, "
            "Puertas=2, Cajones=0, Espejos=No, Precio base=$1000"
        )

    def test_con_espejos(self):
        a = Armario("A", "M", "C", 1000, tiene_espejos=True)
        assert "Espejos=Sí" in a.obtener_descripcion()

    def test_refleja_cambios(self, armario):
        armario.num_cajones = 5
        assert "Cajones=5" in armario.obtener_descripcion()
