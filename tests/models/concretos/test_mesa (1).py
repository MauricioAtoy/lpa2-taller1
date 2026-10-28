"""Pruebas unitarias para Mesa (hereda de Superficie)."""

import pytest

from models.categorias.superficies import Superficie
from models.concretos.mesa import Mesa


class TestMesaConstructor:
    def test_hereda_de_superficie(self, mesa):
        assert isinstance(mesa, Superficie)

    def test_valores_por_defecto(self, mesa):
        assert mesa.forma == "rectangular"
        assert mesa.largo == 120.0
        assert mesa.ancho == 80.0
        assert mesa.altura == 75.0
        assert mesa.capacidad_personas == 4

    def test_atributos_heredados(self, mesa):
        assert mesa.nombre == "Mesa Básica"
        assert mesa.material == "Roble"
        assert mesa.color == "Natural"
        assert mesa.precio_base == 1000.0

    def test_valores_personalizados(self):
        m = Mesa("M", "Pino", "Blanco", 500.0, "redonda", 100.0, 100.0, 70.0, 6)
        assert m.forma == "redonda"
        assert m.largo == 100.0
        assert m.capacidad_personas == 6


class TestMesaForma:
    def test_getter(self, mesa):
        assert mesa.forma == "rectangular"

    @pytest.mark.parametrize("forma", ["rectangular", "redonda", "cuadrada", "ovalada"])
    def test_setter_formas_validas(self, mesa, forma):
        mesa.forma = forma
        assert mesa.forma == forma

    @pytest.mark.parametrize("forma", ["triangular", "", "Redonda", None])
    def test_setter_rechaza_formas_invalidas(self, mesa, forma):
        with pytest.raises(ValueError, match="Forma debe ser una de"):
            mesa.forma = forma

    def test_setter_invalido_no_modifica(self, mesa):
        with pytest.raises(ValueError):
            mesa.forma = "hexagonal"
        assert mesa.forma == "rectangular"


class TestMesaCapacidadPersonas:
    def test_getter(self, mesa):
        assert mesa.capacidad_personas == 4

    @pytest.mark.parametrize("valor", [1, 6, 12])
    def test_setter_valido(self, mesa, valor):
        mesa.capacidad_personas = valor
        assert mesa.capacidad_personas == valor

    @pytest.mark.parametrize("valor", [0, -1, -4])
    def test_setter_rechaza_no_positivos(self, mesa, valor):
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            mesa.capacidad_personas = valor

    def test_setter_invalido_no_modifica(self, mesa):
        with pytest.raises(ValueError):
            mesa.capacidad_personas = 0
        assert mesa.capacidad_personas == 4


class TestMesaCalcularPrecio:
    def test_precio_basico(self, mesa):
        # área 9600 -> factor 1.048 -> 1048
        assert mesa.calcular_precio() == pytest.approx(1048.0)

    def test_forma_no_rectangular_suma_50(self):
        m = Mesa("M", "M", "C", 1000.0, forma="redonda")
        assert m.calcular_precio() == pytest.approx(1098.0)

    @pytest.mark.parametrize(
        "capacidad,recargo",
        [(1, 0), (4, 0), (5, 50), (6, 50), (7, 100), (12, 100)],
    )
    def test_recargo_por_capacidad(self, capacidad, recargo):
        m = Mesa("M", "M", "C", 1000.0, capacidad_personas=capacidad)
        assert m.calcular_precio() == pytest.approx(1048.0 + recargo)

    def test_forma_y_capacidad_combinados(self):
        m = Mesa("M", "M", "C", 1000.0, forma="ovalada", capacidad_personas=8)
        assert m.calcular_precio() == pytest.approx(1048.0 + 50 + 100)

    def test_mesa_mas_grande_cuesta_mas(self):
        chica = Mesa("M", "M", "C", 1000.0, largo=100.0, ancho=60.0)
        grande = Mesa("M", "M", "C", 1000.0, largo=200.0, ancho=100.0)
        assert grande.calcular_precio() > chica.calcular_precio()

    def test_redondea_a_dos_decimales(self):
        m = Mesa("M", "M", "C", 33.33)
        assert m.calcular_precio() == round(33.33 * 1.048, 2)


class TestMesaObtenerDescripcion:
    def test_datos_principales(self, mesa):
        d = mesa.obtener_descripcion()
        assert "Mesa: Mesa Básica" in d
        assert "Material: Roble" in d
        assert "Color: Natural" in d
        assert "Forma: rectangular" in d

    def test_incluye_info_de_superficie(self, mesa):
        assert "Dimensiones: 120.0x80.0x75.0cm" in mesa.obtener_descripcion()

    def test_incluye_capacidad(self, mesa):
        assert "Capacidad: 4 personas" in mesa.obtener_descripcion()

    def test_incluye_precio_final(self, mesa):
        assert f"Precio final: ${mesa.calcular_precio()}" in mesa.obtener_descripcion()
