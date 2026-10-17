import sys
import os
sys.path.append("src")
# Carpeta raíz del proyecto, donde se encuentra secret_config.py
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from model import logica_nomina
import psycopg2

import secret_config


# Datos de conexión a la base de datos, tomados de secret_config.py
DATOS_CONEXION = {
    "database": secret_config.PGDATABASE,
    "user": secret_config.PGUSER,
    "password": secret_config.PGPASSWORD,
    "host": secret_config.PGHOST,
    "port": secret_config.PGPORT,
}

COLUMNAS = (
    "codigo_empleado, nombre, salario_base, dias_trabajados, horas_extra_diurnas, horas_extra_nocturnas, "
    "horas_extra_dominicales_diurnas, horas_extra_dominicales_nocturnas, horas_recargo_nocturno, horas_recargo_dominical_festivo"
)


class EmpleadoNoEncontrado(Exception):
    """Se lanza cuando no existe un empleado con el código buscado."""
    def __init__(self, codigo_empleado):
        super().__init__(f"No existe un empleado con el código {codigo_empleado}.")


class EmpleadoDuplicado(Exception):
    """Se lanza cuando se intenta insertar un código de empleado que ya existe."""
    def __init__(self, codigo_empleado):
        super().__init__(f"Ya existe un empleado con el código {codigo_empleado}.")


SQL_CREAR_TABLA = """
CREATE TABLE IF NOT EXISTS Empleado(
    codigo_empleado VARCHAR(10) PRIMARY KEY NOT NULL,
    nombre VARCHAR(20) NOT NULL,
    salario_base DECIMAL(15,2) NOT NULL,
    dias_trabajados INT NOT NULL,
    horas_extra_diurnas DECIMAL(10,2) DEFAULT 0,
    horas_extra_nocturnas DECIMAL(10,2) DEFAULT 0,
    horas_extra_dominicales_diurnas DECIMAL(10,2) DEFAULT 0,
    horas_extra_dominicales_nocturnas DECIMAL(10,2) DEFAULT 0,
    horas_recargo_nocturno DECIMAL(10,2) DEFAULT 0,
    horas_recargo_dominical_festivo DECIMAL(10,2) DEFAULT 0
)
"""

SQL_BORRAR_TABLA = "DROP TABLE IF EXISTS Empleado"


class Trabajadorescontroller:
    """
    Realiza las operaciones de crear y borrar la tabla, e insertar, buscar y borrar
    empleados en la tabla Empleado de la base de datos

    """

    def conectar(self):
        """Abre una nueva conexión a la base de datos"""
        return psycopg2.connect(**DATOS_CONEXION)

    def ejecutar_sql(self, sql: str, valores: tuple = ()):
        """Ejecuta una instrucción SQL que no devuelve resultados y confirma los cambios"""
        connection = self.conectar()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, valores)
                    return cursor.rowcount
        finally:
            connection.close()

    def crear_tabla(self):
        """Crea la tabla Empleado si no existe"""
        self.ejecutar_sql(SQL_CREAR_TABLA)

    def borrar_tabla(self):
        """Borra la tabla Empleado con todos sus datos"""
        self.ejecutar_sql(SQL_BORRAR_TABLA)

    def insertar(self, empleado: logica_nomina.Empleado):

        """"Inserta un empleado en la base de datos"""
        sql = f"INSERT INTO Empleado({COLUMNAS}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (empleado.codigo_empleado, empleado.nombre, empleado.salario_base, empleado.dias_trabajados,
                   empleado.horas_extra_diurnas, empleado.horas_extra_nocturnas,
                   empleado.horas_extra_dominicales_diurnas, empleado.horas_extra_dominicales_nocturnas,
                   empleado.horas_recargo_nocturno, empleado.horas_recargo_dominical_festivo)

        connection = self.conectar()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, valores)
        except psycopg2.errors.UniqueViolation:
            raise EmpleadoDuplicado(empleado.codigo_empleado)
        finally:
            connection.close()

    def buscar_empleado(self, codigo_empleado: str) -> logica_nomina.Empleado:
        """Busca un empleado en la base de datos por su código de empleado y devuelve un objeto Empleado"""
        consulta = f"SELECT {COLUMNAS} FROM Empleado WHERE codigo_empleado = %s"

        connection = self.conectar()
        try:
            with connection.cursor() as cursor:
                cursor.execute(consulta, (codigo_empleado,))
                fila = cursor.fetchone()
        finally:
            connection.close()

        if fila is None:
            raise EmpleadoNoEncontrado(codigo_empleado)

        # Las columnas DECIMAL llegan como Decimal; se convierten a float para la lógica de nómina
        empleado = logica_nomina.Empleado(codigo_empleado = fila[0], nombre = fila[1], salario_base = float(fila[2]), dias_trabajados = fila[3],
                    horas_extra_diurnas = float(fila[4]), horas_extra_nocturnas = float(fila[5]), horas_extra_dominicales_diurnas = float(fila[6]), horas_extra_dominicales_nocturnas = float(fila[7]),
                    horas_recargo_nocturno = float(fila[8]), horas_recargo_dominical_festivo = float(fila[9]))
        return empleado

    def borrar(self, codigo_empleado: str):
        """Borra el empleado con el código dado"""
        filas = self.ejecutar_sql("DELETE FROM Empleado WHERE codigo_empleado = %s", (codigo_empleado,))
        if filas == 0:
            raise EmpleadoNoEncontrado(codigo_empleado)
