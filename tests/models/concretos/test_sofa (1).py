"""Pruebas unitarias para Sofa (hereda de Asiento)."""

import pytest

from models.categorias.asientos import Asiento
from models.concretos.sofa import Sofa


class TestSofaConstructor:
    def test_hereda_de_asiento(self, sofa):
        assert isinstance(sofa, Asiento)

    def test_atributos_heredados(self, sofa):
        assert sofa.nombre == "Sofá Básico"
        assert sofa.material == "Madera"
        assert sofa.color == "Gris"
        assert sofa.precio_base == 1000.0

    def test_valores_por_defecto(self, sofa):
        assert sofa.capacidad_personas == 3
        assert sofa.tiene_respaldo is True
        assert sofa.material_tapizado is None
        assert sofa.tiene_brazos is True
        assert sofa.es_modular is False
        assert sofa.incluye_cojines is False

    def test_valores_personalizados(self):
        s = Sofa("S", "M", "C", 500.0, 4, False, "cuero", False, True, True)
        assert s.capacidad_personas == 4
        assert s.tiene_respaldo is False
        assert s.material_tapizado == "cuero"
        assert s.tiene_brazos is False
        assert s.es_modular is True
        assert s.incluye_cojines is True


class TestSofaPropiedadesSoloLectura:
    @pytest.mark.parametrize("atributo", ["tiene_brazos", "es_modular", "incluye_cojines"])
    def test_no_tienen_setter(self, sofa, atributo):
        with pytest.raises(AttributeError):
            setattr(sofa, atributo, True)


class TestSofaCalcularPrecio:
    def test_precio_basico(self, sofa):
        # factor = 1 + 0.1 (respaldo) + 0.1 (cap 3) = 1.2 -> 1200 + 150 (brazos)
        assert sofa.calcular_precio() == pytest.approx(1350.0)

    def test_sin_brazos(self):
        s = Sofa("S", "M", "C", 1000.0, tiene_brazos=False)
        assert s.calcular_precio() == pytest.approx(1200.0)

    def test_modular_suma_200(self):
        s = Sofa("S", "M", "C", 1000.0, tiene_brazos=False, es_modular=True)
        assert s.calcular_precio() == pytest.approx(1400.0)

    def test_cojines_suman_50(self):
        s = Sofa("S", "M", "C", 1000.0, tiene_brazos=False, incluye_cojines=True)
        assert s.calcular_precio() == pytest.approx(1250.0)

    def test_todo_incluido(self):
        s = Sofa("S", "M", "C", 1000.0, 3, True, "cuero", True, True, True)
        # factor = 1 + 0.1 + 0.2 + 0.1 = 1.4 -> 1400 + 150 + 200 + 50
        assert s.calcular_precio() == pytest.approx(1800.0)

    def test_tapizado_aumenta_el_precio(self):
        sin = Sofa("S", "M", "C", 1000.0)
        con = Sofa("S", "M", "C", 1000.0, material_tapizado="cuero")
        assert con.calcular_precio() > sin.calcular_precio()


class TestSofaObtenerDescripcion:
    def test_datos_principales(self, sofa):
        d = sofa.obtener_descripcion()
        assert "Sofá: Sofá Básico" in d
        assert "Material: Madera" in d
        assert "Color: Gris" in d

    def test_incluye_info_asiento(self, sofa):
        assert "Capacidad: 3 personas" in sofa.obtener_descripcion()

    def test_extras_por_defecto(self, sofa):
        d = sofa.obtener_descripcion()
        assert "Brazos: Sí" in d
        assert "Modular: No" in d
        assert "Incluye cojines: No" in d

    def test_extras_activados(self):
        s = Sofa("S", "M", "C", 1000.0, tiene_brazos=False, es_modular=True, incluye_cojines=True)
        d = s.obtener_descripcion()
        assert "Brazos: No" in d
        assert "Modular: Sí" in d
        assert "Incluye cojines: Sí" in d

    def test_incluye_precio_final(self, sofa):
        assert f"Precio final: ${sofa.calcular_precio()}" in sofa.obtener_descripcion()
