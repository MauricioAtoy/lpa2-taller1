"""Pruebas unitarias para Cama (hereda de Mueble)."""

import pytest

from models.mueble import Mueble
from models.concretos.cama import Cama


class TestCamaConstructor:
    def test_hereda_de_mueble(self, cama):
        assert isinstance(cama, Mueble)

    def test_valores_por_defecto(self, cama):
        assert cama.tamaño == "individual"
        assert cama.incluye_colchon is False
        assert cama.tiene_cabecera is False

    def test_valores_personalizados(self):
        c = Cama("C", "M", "Col", 100.0, "king", True, True)
        assert c.tamaño == "king"
        assert c.incluye_colchon is True
        assert c.tiene_cabecera is True


class TestCamaTamaño:
    def test_getter(self, cama):
        assert cama.tamaño == "individual"

    @pytest.mark.parametrize("valor", ["individual", "matrimonial", "queen", "king"])
    def test_setter_valido(self, cama, valor):
        cama.tamaño = valor
        assert cama.tamaño == valor

    @pytest.mark.parametrize("valor", ["gigante", "", "King", None])
    def test_setter_rechaza_invalidos(self, cama, valor):
        with pytest.raises(ValueError, match="Tamaño debe ser uno de"):
            cama.tamaño = valor

    def test_setter_invalido_no_modifica(self, cama):
        with pytest.raises(ValueError):
            cama.tamaño = "xl"
        assert cama.tamaño == "individual"


class TestCamaPropiedadesSoloLectura:
    @pytest.mark.parametrize("atributo", ["incluye_colchon", "tiene_cabecera"])
    def test_no_tienen_setter(self, cama, atributo):
        with pytest.raises(AttributeError):
            setattr(cama, atributo, True)


class TestCamaCalcularPrecio:
    @pytest.mark.parametrize(
        "tamaño,esperado",
        [("individual", 500.0), ("matrimonial", 700.0), ("queen", 900.0), ("king", 1100.0)],
    )
    def test_ajuste_por_tamaño(self, tamaño, esperado):
        c = Cama("C", "M", "Col", 500.0, tamaño)
        assert c.calcular_precio() == pytest.approx(esperado)

    def test_colchon_suma_300(self):
        c = Cama("C", "M", "Col", 500.0, incluye_colchon=True)
        assert c.calcular_precio() == pytest.approx(800.0)

    def test_cabecera_suma_100(self):
        c = Cama("C", "M", "Col", 500.0, tiene_cabecera=True)
        assert c.calcular_precio() == pytest.approx(600.0)

    def test_todo_incluido(self):
        c = Cama("C", "M", "Col", 500.0, "king", True, True)
        assert c.calcular_precio() == pytest.approx(1500.0)

    def test_cambiar_tamaño_cambia_precio(self, cama):
        antes = cama.calcular_precio()
        cama.tamaño = "queen"
        assert cama.calcular_precio() == antes + 400

    def test_redondea_a_dos_decimales(self):
        c = Cama("C", "M", "Col", 100.456)
        assert c.calcular_precio() == 100.46


class TestCamaObtenerDescripcion:
    def test_datos_principales(self, cama):
        d = cama.obtener_descripcion()
        assert "Cama: Cama Básica" in d
        assert "Material: Madera" in d
        assert "Color: Blanco" in d
        assert "Tamaño: individual" in d

    def test_extras_no(self, cama):
        d = cama.obtener_descripcion()
        assert "Incluye colchón: No" in d
        assert "Cabecera: No" in d

    def test_extras_si(self):
        c = Cama("C", "M", "Col", 500.0, "queen", True, True)
        d = c.obtener_descripcion()
        assert "Incluye colchón: Sí" in d
        assert "Cabecera: Sí" in d

    def test_incluye_precio_final(self, cama):
        assert f"Precio final: ${cama.calcular_precio()}" in cama.obtener_descripcion()
