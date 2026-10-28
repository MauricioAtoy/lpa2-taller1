"""Pruebas unitarias para Silla (hereda de Asiento)."""

import pytest

from models.categorias.asientos import Asiento
from models.concretos.silla import Silla


class TestSillaConstructor:
    def test_hereda_de_asiento(self, silla):
        assert isinstance(silla, Asiento)

    def test_atributos_heredados(self, silla):
        assert silla.nombre == "Silla Básica"
        assert silla.material == "Madera"
        assert silla.color == "Café"
        assert silla.precio_base == 100.0

    def test_valores_por_defecto(self, silla):
        assert silla.tiene_respaldo is True
        assert silla.material_tapizado is None
        assert silla.altura_regulable is False
        assert silla.tiene_ruedas is False

    def test_capacidad_siempre_es_una_persona(self, silla):
        assert silla.capacidad_personas == 1

    def test_atributos_personalizados(self):
        s = Silla("S", "Metal", "Negro", 200.0, False, "cuero", True, True)
        assert s.tiene_respaldo is False
        assert s.material_tapizado == "cuero"
        assert s.altura_regulable is True
        assert s.tiene_ruedas is True


class TestSillaPropiedades:
    @pytest.mark.parametrize("valor", [True, False])
    def test_altura_regulable_setter(self, silla, valor):
        silla.altura_regulable = valor
        assert silla.altura_regulable is valor

    @pytest.mark.parametrize("valor", [True, False])
    def test_tiene_ruedas_setter(self, silla, valor):
        silla.tiene_ruedas = valor
        assert silla.tiene_ruedas is valor


class TestSillaCalcularPrecio:
    def test_precio_basico(self, silla):
        # 100 * 1.1 (respaldo)
        assert silla.calcular_precio() == pytest.approx(110.0)

    def test_sin_respaldo(self):
        s = Silla("S", "M", "C", 100.0, tiene_respaldo=False)
        assert s.calcular_precio() == pytest.approx(100.0)

    def test_con_tapizado_tela(self):
        s = Silla("S", "M", "C", 100.0, material_tapizado="tela")
        assert s.calcular_precio() == pytest.approx(120.0)

    def test_con_tapizado_cuero(self):
        s = Silla("S", "M", "C", 100.0, material_tapizado="cuero")
        assert s.calcular_precio() == pytest.approx(130.0)

    def test_altura_regulable_suma_30(self, silla):
        silla.altura_regulable = True
        assert silla.calcular_precio() == pytest.approx(140.0)

    def test_ruedas_suma_20(self, silla):
        silla.tiene_ruedas = True
        assert silla.calcular_precio() == pytest.approx(130.0)

    def test_todo_incluido(self):
        s = Silla("S", "M", "C", 100.0, True, "tela", True, True)
        assert s.calcular_precio() == pytest.approx(170.0)  # 120 + 30 + 20

    def test_precio_base_cero(self):
        s = Silla("S", "M", "C", 0.0, True, None, True, True)
        assert s.calcular_precio() == pytest.approx(50.0)

    def test_redondea_a_dos_decimales(self):
        s = Silla("S", "M", "C", 33.333, True)
        assert s.calcular_precio() == round(33.333 * 1.1, 2)


class TestSillaObtenerDescripcion:
    def test_contiene_datos_principales(self, silla):
        d = silla.obtener_descripcion()
        assert "Silla: Silla Básica" in d
        assert "Material: Madera" in d
        assert "Color: Café" in d

    def test_incluye_info_de_asiento(self, silla):
        assert "Capacidad: 1 personas" in silla.obtener_descripcion()

    def test_altura_y_ruedas_no(self, silla):
        d = silla.obtener_descripcion()
        assert "Altura regulable: No" in d
        assert "Ruedas: No" in d

    def test_altura_y_ruedas_si(self, silla):
        silla.altura_regulable = True
        silla.tiene_ruedas = True
        d = silla.obtener_descripcion()
        assert "Altura regulable: Sí" in d
        assert "Ruedas: Sí" in d

    def test_incluye_precio_final(self, silla):
        assert f"Precio final: ${silla.calcular_precio()}" in silla.obtener_descripcion()


class TestSillaRegularAltura:
    def test_sin_altura_regulable(self, silla):
        assert (
            silla.regular_altura(60) == "Esta silla no tiene altura regulable"
        )

    @pytest.mark.parametrize("altura", [40, 70, 100])
    def test_altura_valida(self, altura):
        s = Silla("S", "M", "C", 100.0, altura_regulable=True)
        assert s.regular_altura(altura) == f"Altura ajustada a {altura} cm"

    @pytest.mark.parametrize("altura", [39, 101, 0, -10, 500])
    def test_altura_fuera_de_rango(self, altura):
        s = Silla("S", "M", "C", 100.0, altura_regulable=True)
        assert s.regular_altura(altura) == "La altura debe estar entre 40 y 100 cm"


class TestSillaEsSillaOficina:
    @pytest.mark.parametrize(
        "regulable,ruedas,esperado",
        [(True, True, True), (True, False, False), (False, True, False), (False, False, False)],
    )
    def test_combinaciones(self, regulable, ruedas, esperado):
        s = Silla("S", "M", "C", 100.0, altura_regulable=regulable, tiene_ruedas=ruedas)
        assert s.es_silla_oficina() is esperado
