"""Pruebas unitarias para Comedor (composición: una Mesa + varias Sillas)."""

import pytest
from types import SimpleNamespace

from models.composicion.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla


@pytest.fixture
def silla_a():
    return Silla("Silla A", "Roble", "Natural", 100.0)


@pytest.fixture
def comedor_vacio(mesa):
    return Comedor("Comedor Test", mesa)


@pytest.fixture
def comedor_con_dos(mesa):
    sillas = [Silla("Silla 1", "Roble", "N", 100.0), Silla("Silla 2", "Roble", "N", 100.0)]
    return Comedor("Comedor Test", mesa, sillas)


@pytest.fixture
def comedor_completo(mesa):
    sillas = [Silla(f"Silla {i}", "Roble", "N", 100.0) for i in range(4)]
    return Comedor("Comedor Completo", mesa, sillas)


class TestComedorConstructor:
    def test_guarda_nombre_y_mesa(self, comedor_vacio, mesa):
        assert comedor_vacio.nombre == "Comedor Test"
        assert comedor_vacio.mesa is mesa

    def test_sillas_por_defecto_vacio(self, comedor_vacio):
        assert comedor_vacio.sillas == []

    def test_guarda_sillas_recibidas(self, comedor_con_dos):
        assert len(comedor_con_dos.sillas) == 2

    def test_composicion_con_tipos_correctos(self, comedor_con_dos):
        assert isinstance(comedor_con_dos.mesa, Mesa)
        assert all(isinstance(s, Silla) for s in comedor_con_dos.sillas)


class TestComedorPropiedades:
    def test_nombre(self, comedor_vacio):
        assert comedor_vacio.nombre == "Comedor Test"

    def test_mesa(self, comedor_vacio, mesa):
        assert comedor_vacio.mesa is mesa

    def test_sillas_devuelve_copia(self, comedor_con_dos):
        copia = comedor_con_dos.sillas
        copia.clear()
        assert len(comedor_con_dos.sillas) == 2

    @pytest.mark.parametrize("atributo", ["nombre", "mesa", "sillas"])
    def test_son_de_solo_lectura(self, comedor_vacio, atributo):
        with pytest.raises(AttributeError):
            setattr(comedor_vacio, atributo, "x")


class TestComedorAgregarSilla:
    def test_agrega_silla(self, comedor_vacio, silla_a):
        msg = comedor_vacio.agregar_silla(silla_a)
        assert msg == "Silla Silla A agregada exitosamente al comedor"
        assert comedor_vacio.sillas == [silla_a]

    def test_agrega_hasta_la_capacidad_de_la_mesa(self, comedor_vacio):
        for i in range(4):  # mesa por defecto: capacidad 4
            comedor_vacio.agregar_silla(Silla(f"S{i}", "R", "N", 100.0))
        assert len(comedor_vacio) == 5  # mesa + 4 sillas

    def test_rechaza_si_supera_capacidad(self, comedor_completo, silla_a):
        msg = comedor_completo.agregar_silla(silla_a)
        assert msg == "No se pueden agregar más sillas. Capacidad máxima: 4"
        assert len(comedor_completo.sillas) == 4

    def test_rechaza_objeto_de_otro_tipo(self, comedor_con_dos, mesa):
        msg = comedor_con_dos.agregar_silla(mesa)
        assert msg == "Error: Solo se pueden agregar objetos de tipo Silla"
        assert len(comedor_con_dos.sillas) == 2

    def test_capacidad_respeta_mesa_personalizada(self):
        mesa_grande = Mesa("M", "R", "N", 1000.0, capacidad_personas=6)
        c = Comedor("C", mesa_grande)
        for i in range(6):
            c.agregar_silla(Silla(f"S{i}", "R", "N", 100.0))
        assert "No se pueden agregar más sillas" in c.agregar_silla(Silla("X", "R", "N", 1.0))


class TestComedorQuitarSilla:
    def test_quita_ultima_por_defecto(self, comedor_con_dos):
        msg = comedor_con_dos.quitar_silla()
        assert msg == "Silla Silla 2 removida del comedor"
        assert len(comedor_con_dos.sillas) == 1

    def test_quita_por_indice(self, comedor_con_dos):
        msg = comedor_con_dos.quitar_silla(0)
        assert msg == "Silla Silla 1 removida del comedor"
        assert comedor_con_dos.sillas[0].nombre == "Silla 2"

    def test_sin_sillas(self, comedor_vacio):
        assert comedor_vacio.quitar_silla() == "No hay sillas para quitar"

    @pytest.mark.parametrize("indice", [5, -5, 99])
    def test_indice_invalido(self, comedor_con_dos, indice):
        assert comedor_con_dos.quitar_silla(indice) == "Índice de silla inválido"
        assert len(comedor_con_dos.sillas) == 2


class TestComedorCalcularPrecioTotal:
    def test_solo_mesa(self, comedor_vacio):
        assert comedor_vacio.calcular_precio_total() == pytest.approx(1048.0)

    def test_mesa_y_dos_sillas_sin_descuento(self, comedor_con_dos):
        assert comedor_con_dos.calcular_precio_total() == pytest.approx(1048.0 + 220.0)

    def test_descuento_5_por_ciento_con_4_sillas(self, comedor_completo):
        assert comedor_completo.calcular_precio_total() == pytest.approx(
            (1048.0 + 440.0) * 0.95
        )

    def test_con_3_sillas_no_hay_descuento(self, mesa):
        c = Comedor("C", mesa, [Silla(f"S{i}", "R", "N", 100.0) for i in range(3)])
        assert c.calcular_precio_total() == pytest.approx(1048.0 + 330.0)

    def test_redondea_a_dos_decimales(self, comedor_completo):
        total = comedor_completo.calcular_precio_total()
        assert total == round(total, 2)


class TestComedorObtenerDescripcionCompleta:
    def test_encabezado_en_mayusculas(self, comedor_vacio):
        assert "=== COMEDOR COMEDOR TEST ===" in comedor_vacio.obtener_descripcion_completa()

    def test_incluye_mesa(self, comedor_vacio):
        d = comedor_vacio.obtener_descripcion_completa()
        assert "MESA:" in d
        assert "Mesa: Mesa Básica" in d

    def test_sin_sillas(self, comedor_vacio):
        assert "SILLAS: Ninguna incluida" in comedor_vacio.obtener_descripcion_completa()

    def test_con_sillas(self, comedor_con_dos):
        d = comedor_con_dos.obtener_descripcion_completa()
        assert "SILLAS (2 unidades):" in d
        assert "1. Silla: Silla 1" in d
        assert "2. Silla: Silla 2" in d

    def test_incluye_precio_total(self, comedor_con_dos):
        total = comedor_con_dos.calcular_precio_total()
        assert f"--- PRECIO TOTAL: ${total:.2f} ---" in comedor_con_dos.obtener_descripcion_completa()

    def test_nota_de_descuento_con_4_o_mas_sillas(self, comedor_completo):
        assert "Incluye 5% de descuento" in comedor_completo.obtener_descripcion_completa()

    def test_sin_nota_de_descuento_con_menos_de_4(self, comedor_con_dos):
        assert "descuento" not in comedor_con_dos.obtener_descripcion_completa()


class TestComedorObtenerResumen:
    def test_claves(self, comedor_con_dos):
        assert set(comedor_con_dos.obtener_resumen()) == {
            "nombre", "total_muebles", "precio_mesa", "precio_sillas",
            "precio_total", "capacidad_personas", "materiales_utilizados",
        }

    def test_valores(self, comedor_con_dos):
        r = comedor_con_dos.obtener_resumen()
        assert r["nombre"] == "Comedor Test"
        assert r["total_muebles"] == 3
        assert r["precio_mesa"] == pytest.approx(1048.0)
        assert r["precio_sillas"] == pytest.approx(220.0)
        assert r["precio_total"] == pytest.approx(1268.0)
        assert r["capacidad_personas"] == 2

    def test_materiales_utilizados(self, comedor_con_dos):
        assert comedor_con_dos.obtener_resumen()["materiales_utilizados"] == ["Roble"]


class TestComedorMetodosPrivados:
    def test_materiales_unicos_sin_repetir(self, comedor_con_dos):
        assert comedor_con_dos._obtener_materiales_unicos() == ["Roble"]

    def test_materiales_incluye_tapizado(self, mesa):
        s = Silla("S", "Metal", "N", 100.0, material_tapizado="cuero")
        c = Comedor("C", mesa, [s])
        assert set(c._obtener_materiales_unicos()) == {"Roble", "Metal", "cuero"}

    def test_materiales_ignora_objetos_sin_material(self):
        c = Comedor("C", SimpleNamespace(), [SimpleNamespace()])
        assert c._obtener_materiales_unicos() == []

    def test_capacidad_maxima_usa_la_de_la_mesa(self, comedor_vacio):
        assert comedor_vacio._calcular_capacidad_maxima() == 4

    def test_capacidad_maxima_por_defecto_es_6(self):
        c = Comedor("C", SimpleNamespace())
        assert c._calcular_capacidad_maxima() == 6


class TestComedorMetodosEspeciales:
    def test_str(self, comedor_con_dos):
        assert str(comedor_con_dos) == "Comedor Comedor Test: Mesa + 2 sillas"

    def test_len_solo_mesa(self, comedor_vacio):
        assert len(comedor_vacio) == 1

    def test_len_con_sillas(self, comedor_con_dos):
        assert len(comedor_con_dos) == 3
