import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.model import logica_nomina


class TestsLiquidacionNomina(unittest.TestCase):
    """
    Clase utilizada para realizar las pruebas correspondientes a cada
    concepto de la liquidación de nómina (auxilio de transporte, horas
    extra, recargos, seguridad social y liquidación completa).
    Cada método deberá definir un "valor_esperado", el cual será
    comparado con el valor calculado por el archivo "logica_nomina".
    De esta manera se podrá verificar y garantizar que la nómina se
    liquide correctamente y que ambos valores coincidan.
    """

    # ------------------------------------------------------------
    # VALOR HORA ORDINARIA
    # ------------------------------------------------------------
    def test_valor_hora_ordinaria_smmlv(self):
        """
        Verifica que el valor de la hora ordinaria se calcule
        correctamente para un trabajador que devenga 1 SMMLV.
        """
        salario_base = 1_423_500
        valor_esperado = round(1_423_500 / 220, 2)

        valor_calculado = logica_nomina.calcular_valor_hora_ordinaria(salario_base)

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)

    # ------------------------------------------------------------
    # AUXILIO DE TRANSPORTE
    # ------------------------------------------------------------
    def test_auxilio_transporte_salario_minimo(self):
        """
        Verifica que un trabajador que devenga el salario mínimo SÍ
        tenga derecho al auxilio de transporte.
        """
        salario_base = 1_423_500
        valor_esperado = 200_000

        valor_calculado = logica_nomina.calcular_auxilio_transporte(salario_base)

        self.assertEqual(valor_calculado, valor_esperado)

    def test_auxilio_transporte_dos_smmlv_exacto(self):
        """
        Verifica que un trabajador que devenga exactamente 2 SMMLV
        todavía tenga derecho al auxilio de transporte (el tope es
        inclusivo).
        """
        salario_base = 2 * 1_423_500
        valor_esperado = 200_000

        valor_calculado = logica_nomina.calcular_auxilio_transporte(salario_base)

        self.assertEqual(valor_calculado, valor_esperado)

    def test_auxilio_transporte_salario_alto(self):
        """
        Verifica que un trabajador que devenga más de 2 SMMLV NO
        tenga derecho al auxilio de transporte.
        """
        salario_base = 5_000_000
        valor_esperado = 0

        valor_calculado = logica_nomina.calcular_auxilio_transporte(salario_base)

        self.assertEqual(valor_calculado, valor_esperado)

    # ------------------------------------------------------------
    # HORAS EXTRA Y RECARGOS
    # ------------------------------------------------------------
    def test_hora_extra_diurna(self):
        """
        Verifica que la hora extra diurna (HED) se calcule con un
        recargo del 25% sobre el valor de la hora ordinaria.
        """
        valor_hora = 10_000
        cantidad_horas = 2
        valor_esperado = 25_000  # 10.000 * 1.25 * 2

        valor_calculado = logica_nomina.calcular_hora_extra_diurna(valor_hora, cantidad_horas)

        self.assertEqual(valor_calculado, valor_esperado)

    def test_hora_extra_nocturna(self):
        """
        Verifica que la hora extra nocturna (HEN) se calcule con un
        recargo del 75% sobre el valor de la hora ordinaria.
        """
        valor_hora = 10_000
        cantidad_horas = 2
        valor_esperado = 35_000  # 10.000 * 1.75 * 2

        valor_calculado = logica_nomina.calcular_hora_extra_nocturna(valor_hora, cantidad_horas)

        self.assertEqual(valor_calculado, valor_esperado)

    def test_hora_extra_dominical_diurna(self):
        """
        Verifica que la hora extra dominical/festiva diurna (HEDD) se
        calcule con un recargo del 100% sobre el valor de la hora
        ordinaria.
        """
        valor_hora = 10_000
        cantidad_horas = 1
        valor_esperado = 20_000  # 10.000 * 2.00 * 1

        valor_calculado = logica_nomina.calcular_hora_extra_dominical_diurna(valor_hora, cantidad_horas)

        self.assertEqual(valor_calculado, valor_esperado)

    def test_hora_extra_dominical_nocturna(self):
        """
        Verifica que la hora extra dominical/festiva nocturna (HEDN)
        se calcule con un recargo del 150% sobre el valor de la hora
        ordinaria.
        """
        valor_hora = 10_000
        cantidad_horas = 1
        valor_esperado = 25_000  # 10.000 * 2.50 * 1

        valor_calculado = logica_nomina.calcular_hora_extra_dominical_nocturna(valor_hora, cantidad_horas)

        self.assertEqual(valor_calculado, valor_esperado)

    def test_recargo_nocturno(self):
        """
        Verifica que el recargo nocturno (RN) sobre horas ordinarias
        (no extra) se calcule correctamente al 35%.
        """
        valor_hora = 10_000
        cantidad_horas = 8
        valor_esperado = 28_000  # 10.000 * 0.35 * 8

        valor_calculado = logica_nomina.calcular_recargo_nocturno(valor_hora, cantidad_horas)

        self.assertEqual(valor_calculado, valor_esperado)

    def test_recargo_dominical_festivo(self):
        """
        Verifica que el recargo dominical/festivo (RDF) sobre horas
        ordinarias (no extra) se calcule correctamente al 75%.
        """
        valor_hora = 10_000
        cantidad_horas = 8
        valor_esperado = 60_000  # 10.000 * 0.75 * 8

        valor_calculado = logica_nomina.calcular_recargo_dominical_festivo(valor_hora, cantidad_horas)

        self.assertEqual(valor_calculado, valor_esperado)

    # ------------------------------------------------------------
    # SEGURIDAD SOCIAL
    # ------------------------------------------------------------
    def test_salud_empleado(self):
        """
        Verifica que el descuento de salud del empleado corresponda
        al 4% del IBC.
        """
        ibc = 1_500_000
        valor_esperado = 60_000

        valor_calculado = logica_nomina.calcular_salud_empleado(ibc)

        self.assertEqual(valor_calculado, valor_esperado)

    def test_pension_empleado(self):
        """
        Verifica que el descuento de pensión del empleado corresponda
        al 4% del IBC.
        """
        ibc = 1_500_000
        valor_esperado = 60_000

        valor_calculado = logica_nomina.calcular_pension_empleado(ibc)

        self.assertEqual(valor_calculado, valor_esperado)

    # ------------------------------------------------------------
    # LIQUIDACIÓN COMPLETA - CASOS REALES
    # ------------------------------------------------------------
    def test_liquidacion_completa_trabajador_salario_minimo_mes_completo(self):
        """
        Verifica la liquidación completa de un trabajador que devenga
        el salario mínimo, trabajando el mes completo sin horas
        extra ni recargos.
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=1_423_500,
            dias_trabajados=30
        )
        resultado = logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)

        self.assertEqual(resultado["salario_proporcional"], 1_423_500)
        self.assertEqual(resultado["auxilio_transporte"], 200_000)
        self.assertEqual(resultado["total_devengado"], 1_623_500)
        self.assertAlmostEqual(resultado["salud_empleado"], 1_423_500 * 0.04, 2)
        self.assertAlmostEqual(resultado["pension_empleado"], 1_423_500 * 0.04, 2)

    def test_liquidacion_completa_trabajador_con_horas_extra(self):
        """
        Verifica la liquidación completa de un trabajador con salario
        superior al mínimo que trabajó horas extra diurnas y
        recargo nocturno durante el mes completo.
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=3_500_000,
            dias_trabajados=30,
            horas_extra_diurnas=4,
            horas_recargo_nocturno=10,
        )
        resultado = logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)

        valor_hora = 3_500_000 / 220
        hed_esperado = round(valor_hora * 1.25 * 4, 2)
        rn_esperado = round(valor_hora * 0.35 * 10, 2)

        self.assertAlmostEqual(resultado["hora_extra_diurna"], hed_esperado, 2)
        self.assertAlmostEqual(resultado["recargo_nocturno"], rn_esperado, 2)
        self.assertEqual(resultado["auxilio_transporte"], 0)  # supera 2 SMMLV ($2.847.000)

    def test_liquidacion_completa_trabajador_dias_parciales(self):
        """
        Verifica la liquidación completa de un trabajador que solo
        laboró 15 días del mes, comprobando que el salario y el
        auxilio de transporte se liquiden de forma proporcional.
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=1_423_500,
            dias_trabajados=15
        )
        resultado = logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)

        salario_esperado = round((1_423_500 / 30) * 15, 2)
        auxilio_esperado = round(200_000 * (15 / 30), 2)

        self.assertAlmostEqual(resultado["salario_proporcional"], salario_esperado, 2)
        self.assertAlmostEqual(resultado["auxilio_transporte"], auxilio_esperado, 2)

    def test_liquidacion_provisiones_prestacionales(self):
        """
        Verifica que las provisiones de prestaciones sociales
        (cesantías, intereses de cesantías, prima y vacaciones) se
        calculen correctamente dentro de la liquidación completa.
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=1_423_500,
            dias_trabajados=30
        )
        resultado = logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)
        provisiones = resultado["provisiones_prestacionales"]

        ibc = resultado["ibc"]
        cesantias_esperadas = round(ibc * 0.0833, 2)

        self.assertAlmostEqual(provisiones["cesantias"], cesantias_esperadas, 2)
        self.assertAlmostEqual(
            provisiones["intereses_cesantias"], round(cesantias_esperadas * 0.12, 2), 1
        )
        self.assertAlmostEqual(provisiones["prima_servicios"], round(ibc * 0.0833, 2), 2)

    # ------------------------------------------------------------
    # CASOS DE ERROR
    # ------------------------------------------------------------

    # ERROR 1 - SALARIO BASE IGUAL A CERO
    def test_error_salario_base_cero(self):
        """
        Prueba encargada de verificar que la nómina NO sea liquidada
        debido a que el SALARIO BASE ES IGUAL A CERO.
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=0,
            dias_trabajados=30
        )
        with self.assertRaises(logica_nomina.SalarioInvalido):
            logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)

    # ERROR 2 - SALARIO BASE NEGATIVO
    def test_error_salario_base_negativo(self):
        """
        Prueba encargada de verificar que la nómina NO sea liquidada
        debido a que el SALARIO BASE ES NEGATIVO.
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=-1_423_500,
            dias_trabajados=30
        )
        with self.assertRaises(logica_nomina.SalarioInvalido):
            logica_nomina.liquidar_nomina(datos_empleado=datos_empleado )

    # ERROR 3 - HORAS EXTRA NEGATIVAS
    def test_error_horas_extra_negativas(self):
        """
        Prueba encargada de verificar que la nómina NO sea liquidada
        debido a que se ingresó una cantidad de HORAS EXTRA
        NEGATIVA.
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=1_423_500,
            dias_trabajados=30,
            horas_extra_diurnas=-2
        )
        with self.assertRaises(logica_nomina.HorasInvalidas):
            logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)
            
            
        

    # ERROR 4 - DÍAS TRABAJADOS FUERA DE RANGO
    def test_error_dias_trabajados_fuera_de_rango(self):
        """
        Prueba encargada de verificar que la nómina NO sea liquidada
        debido a que los DÍAS TRABAJADOS SUPERAN EL MÁXIMO PERMITIDO
        (30 días).
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=1_423_500,
            dias_trabajados=35
        )   
        with self.assertRaises(logica_nomina.DiasInvalidos):
            logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)

    # ------------------------------------------------------------
    # CASOS DE PRUEBA EXTRAORDINARIOS
    # ------------------------------------------------------------

    # EXTRAORDINARIO 1 - TRABAJADOR CON SALARIO MUY ALTO (SIN AUXILIO)
    def test_extraordinario_salario_alto_sin_auxilio(self):
        """
        Se verifica que un trabajador con un SALARIO MUY ALTO no
        reciba auxilio de transporte, aunque el resto de la
        liquidación se calcule con normalidad.
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=15_000_000,
            dias_trabajados=30
        )
        resultado = logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)

        self.assertEqual(resultado["auxilio_transporte"], 0)
        self.assertGreater(resultado["total_devengado"], 0)

    # EXTRAORDINARIO 2 - TRABAJADOR CON TODOS LOS TIPOS DE HORA A LA VEZ
    def test_extraordinario_todos_los_tipos_de_hora(self):
        """
        Se verifica que la función calcule correctamente la
        liquidación cuando el trabajador tiene, en el mismo periodo,
        HORAS EXTRA DIURNAS, NOCTURNAS, DOMINICALES DIURNAS,
        DOMINICALES NOCTURNAS, RECARGO NOCTURNO Y RECARGO
        DOMINICAL/FESTIVO simultáneamente.
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=1_423_500,
            dias_trabajados=30,
            horas_extra_diurnas=2,
            horas_extra_nocturnas=2,
            horas_extra_dominicales_diurnas=2,
            horas_extra_dominicales_nocturnas=2,
            horas_recargo_nocturno=5,
            horas_recargo_dominical_festivo=5,
        )
        resultado = logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)
        total_extra_y_recargos = (
            resultado["hora_extra_diurna"]
            + resultado["hora_extra_nocturna"]
            + resultado["hora_extra_dominical_diurna"]
            + resultado["hora_extra_dominical_nocturna"]
            + resultado["recargo_nocturno"]
            + resultado["recargo_dominical_festivo"]
        )

        self.assertGreater(total_extra_y_recargos, 0)
        self.assertEqual(
            resultado["total_devengado"],
            round(
                resultado["salario_proporcional"]
                + resultado["auxilio_transporte"]
                + total_extra_y_recargos,
                2,
            ),
        )

    # EXTRAORDINARIO 3 - TRABAJADOR SIN DÍAS TRABAJADOS EN EL PERIODO
    def test_extraordinario_cero_dias_trabajados(self):
        """
        Se verifica que un trabajador que registra CERO DÍAS
        TRABAJADOS en el periodo obtenga un salario proporcional y un
        auxilio de transporte iguales a cero, sin que el sistema
        genere un error, ya que 0 es un valor válido dentro del rango
        permitido (0 a 30 días).
        """
        datos_empleado = logica_nomina.Empleado(
            salario_base=1_423_500,
            dias_trabajados=0
        )
        resultado = logica_nomina.liquidar_nomina(datos_empleado=datos_empleado)

        self.assertEqual(resultado["salario_proporcional"], 0)
        self.assertEqual(resultado["auxilio_transporte"], 0)


if __name__ == '__main__':
    unittest.main()
