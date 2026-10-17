import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import psycopg2
import src.controller.trabajadores_controller as Trabajadores_controller
from src.model import logica_nomina


def crear_empleado(codigo_empleado='EMP001', nombre='Manuel Gomez', **valores):
    """Crea un Empleado de prueba; los valores no indicados toman un valor por defecto"""
    datos = dict(salario_base=2000000, dias_trabajados=30, horas_extra_diurnas=2, horas_extra_nocturnas=2,
                 horas_extra_dominicales_diurnas=3, horas_extra_dominicales_nocturnas=4,
                 horas_recargo_nocturno=5, horas_recargo_dominical_festivo=4)
    datos.update(valores)
    return logica_nomina.Empleado(codigo_empleado=codigo_empleado, nombre=nombre, **datos)


class Test_trabajadores_Controller(unittest.TestCase):

    # ------------------------------------------------------------
    # FIXTURES
    # ------------------------------------------------------------
    def setUp(self):
        """Antes de cada prueba se borra y se crea de nuevo la tabla, para partir de una tabla vacía"""
        self.controlador = Trabajadores_controller.Trabajadorescontroller()
        self.controlador.borrar_tabla()
        self.controlador.crear_tabla()

    def tearDown(self):
        """Al terminar cada prueba se deja la tabla creada y vacía"""
        self.controlador.borrar_tabla()
        self.controlador.crear_tabla()

    def assertEmpleadoIgual(self, esperado, obtenido):
        """Compara todos los campos de dos empleados"""
        self.assertEqual(esperado.codigo_empleado, obtenido.codigo_empleado)
        self.assertEqual(esperado.nombre, obtenido.nombre)
        for atributo in ('salario_base', 'dias_trabajados', 'horas_extra_diurnas', 'horas_extra_nocturnas',
                         'horas_extra_dominicales_diurnas', 'horas_extra_dominicales_nocturnas',
                         'horas_recargo_nocturno', 'horas_recargo_dominical_festivo'):
            self.assertAlmostEqual(getattr(esperado, atributo), getattr(obtenido, atributo), places=2)

    # ------------------------------------------------------------
    # CASOS NORMALES
    # ------------------------------------------------------------
    def test_insertar_y_buscar(self):
        """CASO NORMAL 1: Insertar un empleado y buscarlo por su código"""
        empleado_prueba = crear_empleado('EMP002', 'Manuel Gomez')
        self.controlador.insertar(empleado_prueba)

        empleado_buscado = self.controlador.buscar_empleado('EMP002')

        self.assertEmpleadoIgual(empleado_prueba, empleado_buscado)

    def test_insertar_horas_decimales_y_cero(self):
        """CASO NORMAL 2: Insertar un empleado con horas en decimales y en cero"""
        empleado_prueba = crear_empleado('EMP003', 'Laura Rios', salario_base=1750905.50, dias_trabajados=15,
                                         horas_extra_diurnas=1.5, horas_extra_nocturnas=0,
                                         horas_extra_dominicales_diurnas=0, horas_extra_dominicales_nocturnas=0,
                                         horas_recargo_nocturno=2.25, horas_recargo_dominical_festivo=0)
        self.controlador.insertar(empleado_prueba)

        empleado_buscado = self.controlador.buscar_empleado('EMP003')

        self.assertEmpleadoIgual(empleado_prueba, empleado_buscado)

    def test_insertar_varios_y_buscar_cada_uno(self):
        """CASO NORMAL 3: Insertar varios empleados y buscar cada uno sin confundirlos"""
        empleados = [crear_empleado('EMP004', 'Ana Torres', salario_base=3000000),
                     crear_empleado('EMP005', 'Pedro Diaz', salario_base=1500000),
                     crear_empleado('EMP006', 'Sofia Mejia', salario_base=5000000)]
        for empleado in empleados:
            self.controlador.insertar(empleado)

        for empleado in empleados:
            self.assertEmpleadoIgual(empleado, self.controlador.buscar_empleado(empleado.codigo_empleado))

    def test_buscar_y_liquidar_nomina(self):
        """CASO NORMAL 4: El empleado leído de la BD liquida la misma nómina que el original"""
        empleado_prueba = crear_empleado('EMP007', 'Carlos Ruiz')
        self.controlador.insertar(empleado_prueba)

        empleado_buscado = self.controlador.buscar_empleado('EMP007')

        self.assertAlmostEqual(logica_nomina.liquidar_nomina(empleado_prueba)['neto_a_pagar'],
                               logica_nomina.liquidar_nomina(empleado_buscado)['neto_a_pagar'], places=2)

    def test_borrar_empleado(self):
        """CASO NORMAL 5: Borrar un empleado insertado, después ya no se encuentra"""
        self.controlador.insertar(crear_empleado('EMP008', 'Diana Lopez'))

        self.controlador.borrar('EMP008')

        with self.assertRaises(Trabajadores_controller.EmpleadoNoEncontrado):
            self.controlador.buscar_empleado('EMP008')

    # ------------------------------------------------------------
    # CASOS DE ERROR
    # ------------------------------------------------------------
    def test_error_insertar_codigo_duplicado(self):
        """CASO DE ERROR 1 (INSERTAR): Insertar dos veces el mismo código de empleado"""
        self.controlador.insertar(crear_empleado('EMP009', 'Miguel Garcia'))

        with self.assertRaises(Trabajadores_controller.EmpleadoDuplicado):
            self.controlador.insertar(crear_empleado('EMP009', 'Otro Nombre'))

    def test_error_insertar_nombre_muy_largo(self):
        """CASO DE ERROR 2 (INSERTAR): El nombre supera los 20 caracteres de la columna"""
        empleado_prueba = crear_empleado('EMP010', 'Nombre Demasiado Largo Para La Tabla')

        with self.assertRaises(psycopg2.errors.StringDataRightTruncation):
            self.controlador.insertar(empleado_prueba)

    def test_error_buscar_empleado_inexistente(self):
        """CASO DE ERROR 3 (BUSCAR): Buscar un código que no existe en la tabla"""
        with self.assertRaises(Trabajadores_controller.EmpleadoNoEncontrado):
            self.controlador.buscar_empleado('NOEXISTE')

    def test_error_buscar_despues_de_borrar_tabla(self):
        """CASO DE ERROR 4 (BORRAR TABLA): Después de borrar la tabla, buscar falla"""
        self.controlador.insertar(crear_empleado('EMP011', 'Jorge Castro'))
        self.controlador.borrar_tabla()

        with self.assertRaises(psycopg2.errors.UndefinedTable):
            self.controlador.buscar_empleado('EMP011')

    def test_error_borrar_empleado_inexistente(self):
        """CASO DE ERROR 5 (BORRAR): Borrar un código que no existe"""
        with self.assertRaises(Trabajadores_controller.EmpleadoNoEncontrado):
            self.controlador.borrar('NOEXISTE')


if __name__ == '__main__':
    unittest.main()
