import sys 
sys.path.append("src")

from model import logica_nomina
import psycopg2

#connection = psycopg2.connect(database="banco_97bh", user="estudiante", password="lZDYHHDJlRc7VSJaVOQvFsNB3l5MrFmm", host="dpg-daq7qoojo6nc73dekb3g-a.virginia-postgres.render.com", port=5432)


class Trabajadorescontroller:
    """
    Realiza las operaciones de insertar, buscar, borrar en la tabla trabajadores de la base de datos

    """

    def insertar(self, empleado: logica_nomina.Empleado):

        """"Inserta un empleado en la base de datos"""
        connection = psycopg2.connect(database="banco_97bh", user="estudiante", password="lZDYHHDJlRc7VSJaVOQvFsNB3l5MrFmm", host="dpg-daq7qoojo6nc73dekb3g-a.virginia-postgres.render.com", port=5432)
        
        cursor = connection.cursor()

        sql = f"""INSERT INTO Empleado(codigo_empleado, nombre, salario_base, dias_trabajados, horas_extra_diurnas, horas_extra_nocturnas, horas_extra_dominicales_diurnas, horas_extra_dominicales_nocturnas, horas_recargo_nocturno, horas_recargo_dominical_festivo)
            VALUES ('{empleado.codigo_empleado}','{empleado.nombre}',{empleado.salario_base},{empleado.dias_trabajados},{empleado.horas_extra_diurnas},{empleado.horas_extra_nocturnas},{empleado.horas_extra_dominicales_diurnas},{empleado.horas_extra_dominicales_nocturnas},{empleado.horas_recargo_nocturno},{empleado.horas_recargo_dominical_festivo})"""

        cursor.execute(sql)
        connection.commit()
        

    def buscar_empleado(self, codigo_empleado: str) -> logica_nomina.Empleado:
        """Busca un empleado en la base de datos por su código de empleado y devuelve un objeto Empleado"""
        connection = psycopg2.connect(database="banco_97bh", user="estudiante", password="lZDYHHDJlRc7VSJaVOQvFsNB3l5MrFmm", host="dpg-daq7qoojo6nc73dekb3g-a.virginia-postgres.render.com", port=5432)
        cursor = connection.cursor()
        consulta = f"""SELECT codigo_empleado,nombre,salario_base,dias_trabajados,horas_extra_diurnas,horas_extra_nocturnas,horas_extra_dominicales_diurnas,horas_extra_dominicales_nocturnas,horas_recargo_nocturno,horas_recargo_dominical_festivo FROM Empleado WHERE codigo_empleado = '{codigo_empleado}'"""

        cursor.execute(consulta)
        fila = cursor.fetchone()
        empleado = logica_nomina.Empleado(codigo_empleado = fila[0],nombre = fila[1], salario_base = fila[2], dias_trabajados = fila[3],
                    horas_extra_diurnas = fila(4), horas_extra_nocturnas = fila(5), horas_extra_dominicales_diurnas = fila(6), horas_extra_dominicales_nocturnas = fila(7),
                    horas_recargo_nocturno = fila(8), horas_recargo_dominical_festivo = fila(9))
        return empleado
    
    def borrar(self, codigo_empleado: str):
        pass