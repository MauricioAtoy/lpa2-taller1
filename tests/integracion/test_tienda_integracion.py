"""Pruebas de integración: Tienda + muebles reales + Comedor (sin mocks)."""

import pytest

from services.tienda import Tienda
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from models.concretos.sofa import Sofa
from models.concretos.sofacama import SofaCama
from models.concretos.armario import Armario
from models.composicion.comedor import Comedor

pytestmark = pytest.mark.integration


@pytest.fixture
def tienda_con_catalogo():
    t = Tienda()
    t.agregar_producto(Mesa("Mesa Roble", "Roble", "Natural", 1000.0))
    t.agregar_producto(Silla("Silla Roble", "Roble", "Natural", 100.0))
    t.agregar_producto(Sofa("Sofá Gris", "Madera", "Gris", 1000.0))
    t.agregar_producto(SofaCama("Sofá Cama", "Madera", "Azul", 1000.0))
    t.agregar_producto(Armario("Armario", "Pino", "Blanco", 1000))
    return t


def test_valor_del_inventario_es_la_suma_de_los_precios_reales(tienda_con_catalogo):
    esperado = 1048.0 + 110.0 + 1350.0 + 2000.0 + 1100
    assert tienda_con_catalogo.calcular_valor_inventario() == pytest.approx(esperado)


def test_vender_reduce_el_valor_del_inventario(tienda_con_catalogo, capsys):
    antes = tienda_con_catalogo.calcular_valor_inventario()
    assert tienda_con_catalogo.vender_producto("Armario") is True
    despues = tienda_con_catalogo.calcular_valor_inventario()

    assert antes - despues == pytest.approx(1100)
    assert "Vendido: Armario por $1100" in capsys.readouterr().out


def test_descuento_por_material_baja_el_valor_total(tienda_con_catalogo):
    antes = tienda_con_catalogo.calcular_valor_inventario()
    afectados = tienda_con_catalogo.aplicar_descuento_material("Roble", 0.1)
    despues = tienda_con_catalogo.calcular_valor_inventario()

    assert afectados == 2  # mesa y silla
    assert despues < antes


def test_polimorfismo_todos_los_productos_tienen_precio_y_descripcion(tienda_con_catalogo):
    for producto in tienda_con_catalogo.inventario:
        assert producto.calcular_precio() > 0
        assert producto.nombre in producto.obtener_descripcion()


def test_comedor_armado_con_productos_de_la_tienda():
    tienda = Tienda()
    tienda.agregar_producto(Mesa("Mesa", "Roble", "Natural", 1000.0))
    for i in range(4):
        tienda.agregar_producto(Silla(f"Silla {i}", "Roble", "Natural", 100.0))

    mesa = tienda.buscar_producto("Mesa")
    comedor = Comedor("Familiar", mesa)
    for i in range(4):
        comedor.agregar_silla(tienda.buscar_producto(f"Silla {i}"))

    # 4 sillas -> 5% de descuento
    assert comedor.calcular_precio_total() == pytest.approx((1048.0 + 440.0) * 0.95)


def test_sofacama_convertido_sigue_siendo_vendible(tienda_con_catalogo):
    sofacama = tienda_con_catalogo.buscar_producto("Sofá Cama")
    sofacama.convertir_a_cama()
    assert tienda_con_catalogo.vender_producto("Sofá Cama") is True
    assert tienda_con_catalogo.buscar_producto("Sofá Cama") is None
