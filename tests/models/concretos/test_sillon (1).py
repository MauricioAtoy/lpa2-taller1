"""Pruebas unitarias para Sillon."""

import pytest

from models.concretos.sillon import Sillon


class TestSillonConstructor:
    def test_valores_por_defecto(self, sillon):
        assert sillon.nombre == "Sillón Básico"
        assert sillon.material == "Madera"
        assert sillon.color == "Beige"
        assert sillon.precio_base == 1000
        assert sillon.capacidad_personas == 2
        assert sillon.tiene_respaldo is True
        assert sillon.material_tapizado is None
        assert sillon.tiene_brazos is True
        assert sillon.es_reclinable is False
        assert sillon.tiene_reposapiés is False

    def test_valores_personalizados(self):
        s = Sillon("S", "M", "C", 500, 1, False, "cuero", False, True, True)
        assert s.capacidad_personas == 1
        assert s.tiene_respaldo is False
        assert s.material_tapizado == "cuero"
        assert s.tiene_brazos is False
        assert s.es_reclinable is True
        assert s.tiene_reposapiés is True

    def test_precio_base_se_convierte_a_entero(self):
        assert Sillon("S", "M", "C", 99.9).precio_base == 99

    def test_precio_base_none_se_vuelve_cero(self):
        assert Sillon("S", "M", "C", None).precio_base == 0


class TestSillonCalcularPrecio:
    def test_precio_basico(self, sillon):
        assert sillon.calcular_precio() == 1100  # 1000 + brazos 100

    def test_sin_brazos(self):
        assert Sillon("S", "M", "C", 1000, tiene_brazos=False).calcular_precio() == 1000

    def test_tapizado_suma_200(self):
        s = Sillon("S", "M", "C", 1000, tiene_brazos=False, material_tapizado="tela")
        assert s.calcular_precio() == 1200

    def test_reclinable_suma_250(self):
        s = Sillon("S", "M", "C", 1000, tiene_brazos=False, es_reclinable=True)
        assert s.calcular_precio() == 1250

    def test_reposapies_suma_80(self):
        s = Sillon("S", "M", "C", 1000, tiene_brazos=False, tiene_reposapiés=True)
        assert s.calcular_precio() == 1080

    def test_todo_incluido(self):
        s = Sillon("S", "M", "C", 1000, 2, True, "cuero", True, True, True)
        assert s.calcular_precio() == 1000 + 200 + 100 + 250 + 80

    def test_retorna_entero(self, sillon):
        assert isinstance(sillon.calcular_precio(), int)


class TestSillonObtenerDescripcion:
    def test_formato_completo(self, sillon):
        assert sillon.obtener_descripcion() == (
            "Sillón 'Sillón Básico': Material=Madera, Color=Beige, "
            "Capacidad=2 personas, Tapizado=N/A, Brazos=Sí, Reclinable=No, "
            "Reposapiés=No, Precio base=$1000"
        )

    def test_muestra_tapizado_si_existe(self):
        s = Sillon("S", "M", "C", 1000, material_tapizado="cuero")
        assert "Tapizado=cuero" in s.obtener_descripcion()

    def test_extras_activados(self):
        s = Sillon("S", "M", "C", 1000, tiene_brazos=False, es_reclinable=True, tiene_reposapiés=True)
        d = s.obtener_descripcion()
        assert "Brazos=No" in d
        assert "Reclinable=Sí" in d
        assert "Reposapiés=Sí" in d
