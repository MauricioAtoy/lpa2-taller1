"""Pruebas unitarias para SofaCama (herencia múltiple: Sofa + Cama)."""

import pytest

from models.mueble import Mueble
from models.categorias.asientos import Asiento
from models.concretos.cama import Cama
from models.concretos.sofa import Sofa
from models.concretos.sofacama import SofaCama


class TestSofaCamaHerenciaMultiple:
    def test_es_instancia_de_ambos_padres(self, sofacama):
        assert isinstance(sofacama, Sofa)
        assert isinstance(sofacama, Cama)

    def test_es_instancia_de_asiento_y_mueble(self, sofacama):
        assert isinstance(sofacama, Asiento)
        assert isinstance(sofacama, Mueble)

    def test_orden_de_resolucion_de_metodos(self):
        mro = SofaCama.__mro__
        assert mro.index(Sofa) < mro.index(Cama)
        assert mro[0] is SofaCama

    def test_hereda_atributos_de_sofa(self, sofacama):
        assert sofacama.capacidad_personas == 3
        assert sofacama.tiene_respaldo is True
        assert sofacama.tiene_brazos is True

    def test_hereda_atributos_de_cama(self, sofacama):
        assert sofacama.incluye_colchon is True
        assert sofacama.tiene_cabecera is False


class TestSofaCamaConstructor:
    def test_valores_por_defecto(self, sofacama):
        assert sofacama.nombre == "Sofá Cama"
        assert sofacama.material_tapizado == "tela"
        assert sofacama.tamaño_cama == "matrimonial"
        assert sofacama.mecanismo_conversion == "plegable"
        assert sofacama.modo_actual == "sofa"

    def test_valores_personalizados(self):
        sc = SofaCama("SC", "M", "C", 800, 2, "cuero", "king", False, "electrico")
        assert sc.capacidad_personas == 2
        assert sc.material_tapizado == "cuero"
        assert sc.tamaño_cama == "king"
        assert sc.incluye_colchon is False
        assert sc.mecanismo_conversion == "electrico"


class TestSofaCamaPropiedades:
    def test_tamaño_y_tamaño_cama_son_equivalentes(self, sofacama):
        assert sofacama.tamaño == sofacama.tamaño_cama == "matrimonial"

    @pytest.mark.parametrize(
        "atributo", ["tamaño", "tamaño_cama", "mecanismo_conversion", "modo_actual"]
    )
    def test_son_de_solo_lectura(self, sofacama, atributo):
        with pytest.raises(AttributeError):
            setattr(sofacama, atributo, "x")


class TestSofaCamaCalcularPrecio:
    def test_precio_por_defecto(self, sofacama):
        # sofá: 1000*1.3 + 150 = 1450 ; +300 matrimonial ; +250 colchón
        assert sofacama.calcular_precio() == pytest.approx(2000.0)

    @pytest.mark.parametrize(
        "tamaño,recargo", [("individual", 0), ("matrimonial", 300), ("queen", 500), ("king", 700)]
    )
    def test_recargo_por_tamaño(self, tamaño, recargo):
        sc = SofaCama("SC", "M", "C", 1000, tamaño_cama=tamaño, incluye_colchon=False)
        assert sc.calcular_precio() == pytest.approx(1450.0 + recargo)

    def test_colchon_suma_250(self):
        sin = SofaCama("SC", "M", "C", 1000, incluye_colchon=False)
        con = SofaCama("SC", "M", "C", 1000, incluye_colchon=True)
        assert con.calcular_precio() - sin.calcular_precio() == pytest.approx(250.0)

    @pytest.mark.parametrize(
        "mecanismo,recargo", [("plegable", 0), ("hidraulico", 150), ("electrico", 300)]
    )
    def test_recargo_por_mecanismo(self, mecanismo, recargo):
        sc = SofaCama("SC", "M", "C", 1000, mecanismo_conversion=mecanismo)
        assert sc.calcular_precio() == pytest.approx(2000.0 + recargo)

    def test_es_mayor_que_el_precio_del_sofa_solo(self, sofacama):
        sofa = Sofa("S", "M", "C", 1000, 3, True, "tela")
        assert sofacama.calcular_precio() > sofa.calcular_precio()


class TestSofaCamaConvertirACama:
    def test_desde_modo_sofa(self, sofacama):
        msg = sofacama.convertir_a_cama()
        assert msg == "Sofá convertido a cama usando mecanismo plegable"
        assert sofacama.modo_actual == "cama"

    def test_si_ya_esta_en_cama(self, sofacama):
        sofacama.convertir_a_cama()
        assert sofacama.convertir_a_cama() == "El sofá-cama ya está en modo cama"
        assert sofacama.modo_actual == "cama"

    def test_usa_el_mecanismo_configurado(self):
        sc = SofaCama("SC", "M", "C", 1000, mecanismo_conversion="electrico")
        assert "electrico" in sc.convertir_a_cama()


class TestSofaCamaConvertirASofa:
    def test_desde_modo_cama(self, sofacama):
        sofacama.convertir_a_cama()
        msg = sofacama.convertir_a_sofa()
        assert msg == "Cama convertida a sofá usando mecanismo plegable"
        assert sofacama.modo_actual == "sofa"

    def test_si_ya_esta_en_sofa(self, sofacama):
        assert sofacama.convertir_a_sofa() == "El sofá-cama ya está en modo sofá"
        assert sofacama.modo_actual == "sofa"

    def test_ciclo_completo(self, sofacama):
        sofacama.convertir_a_cama()
        sofacama.convertir_a_sofa()
        sofacama.convertir_a_cama()
        assert sofacama.modo_actual == "cama"


class TestSofaCamaObtenerDescripcion:
    def test_datos_principales(self, sofacama):
        d = sofacama.obtener_descripcion()
        assert "Sofá-Cama: Sofá Cama" in d
        assert "Material: Madera" in d
        assert "Color: Azul" in d

    def test_combina_ambas_funcionalidades(self, sofacama):
        d = sofacama.obtener_descripcion()
        assert "Capacidad: 3 personas" in d  # parte sofá
        assert "Tamaño como cama: matrimonial" in d  # parte cama
        assert "Incluye colchón: Sí" in d
        assert "Mecanismo: plegable" in d
        assert "Modo actual: sofa" in d

    def test_refleja_cambio_de_modo(self, sofacama):
        sofacama.convertir_a_cama()
        assert "Modo actual: cama" in sofacama.obtener_descripcion()

    def test_incluye_precio_final(self, sofacama):
        assert f"Precio final: ${sofacama.calcular_precio()}" in sofacama.obtener_descripcion()


class TestSofaCamaObtenerCapacidadTotal:
    def test_por_defecto(self, sofacama):
        assert sofacama.obtener_capacidad_total() == {"como_sofa": 3, "como_cama": 2}

    @pytest.mark.parametrize(
        "tamaño,personas", [("individual", 1), ("matrimonial", 2), ("queen", 2), ("king", 2)]
    )
    def test_capacidad_como_cama(self, tamaño, personas):
        sc = SofaCama("SC", "M", "C", 1000, tamaño_cama=tamaño)
        assert sc.obtener_capacidad_total()["como_cama"] == personas

    def test_capacidad_como_sofa_sigue_a_capacidad_personas(self):
        sc = SofaCama("SC", "M", "C", 1000, capacidad_personas=5)
        assert sc.obtener_capacidad_total()["como_sofa"] == 5


class TestSofaCamaStr:
    def test_modo_sofa(self, sofacama):
        assert str(sofacama) == "Sofá-cama Sofá Cama (modo: sofa)"

    def test_modo_cama(self, sofacama):
        sofacama.convertir_a_cama()
        assert str(sofacama) == "Sofá-cama Sofá Cama (modo: cama)"
