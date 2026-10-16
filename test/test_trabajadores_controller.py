import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import src.controller.trabajadores_controller as Trabajadores_controller
from src.model import logica_nomina


class Test_trabajadores_Controller(unittest.TestCase):

    def test_insertar_1(self):
        """CASO NORMAL 1"""
        controlador = Trabajadores_controller.Trabajadorescontroller()
        empleado_prueba = logica_nomina.Empleado(
            codigo_empleado = 'EMP002',
            nombre = 'Manuel Gomez',
            salario_base=2000000,
            dias_trabajados= 30,
            horas_extra_diurnas = 2,
            horas_extra_nocturnas = 2,
            horas_extra_dominicales_diurnas = 3,
            horas_extra_dominicales_nocturnas = 4,
            horas_recargo_nocturno = 5,
            horas_recargo_dominical_festivo = 4,
        )
        controlador.insertar(empleado_prueba) 

        controlador.buscar_empleado(empleado_prueba.codigo_empleado)
              

    def test_error_dias_trabajados_fuera_de_rango(self):
            """CASO DE ERROR 1(INSERTAR): Días trabajados fuera de rango"""
            controlador = Trabajadores_controller.Trabajadorescontroller()
            empleado_prueba = logica_nomina.Empleado(
                codigo_empleado = 'EMP003',
                nombre = 'Miguel Garcia',
                salario_base=2000000,
                dias_trabajados= 35,
                horas_extra_diurnas = 2,
                horas_extra_nocturnas = 2,
                horas_extra_dominicales_diurnas = 3,
                horas_extra_dominicales_nocturnas = 4,
                horas_recargo_nocturno = 5,
                horas_recargo_dominical_festivo = 4,
            )
            controlador.insertar(empleado_prueba) 
            with self.assertRaises(logica_nomina.DiasInvalidos):
                logica_nomina.liquidar_nomina(datos_empleado=empleado_prueba) 

    


if __name__ == '__main__':
    unittest.main()
