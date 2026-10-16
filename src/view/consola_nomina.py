from datetime import date
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import src.model.logica_nomina as logica_nomina


class Trabajador:
    """
    Clase que representa a un trabajador y almacena la información
    necesaria para realizar la liquidación de su nómina mensual.
    "codigo_empleado": Es una cadena de texto con el código único del trabajador.
    "nombre": Es una cadena de texto con el nombre del trabajador.
    "salario_base": Es un flotante con el salario mensual fijo pactado.
    "dias_trabajados": Es un entero con los días efectivamente
    trabajados dentro del mes (0 a 30).
    """
    def __init__(self,codigo_empleado: str, nombre: str, salario_base: float, dias_trabajados: int,
                 horas_extra_diurnas: float = 0, horas_extra_nocturnas: float = 0,
                 horas_extra_dominicales_diurnas: float = 0, horas_extra_dominicales_nocturnas: float = 0,
                 horas_recargo_nocturno: float = 0, horas_recargo_dominical_festivo: float = 0):
        self.codigo_empleado = codigo_empleado
        self.nombre = nombre
        self.salario_base = salario_base
        self.dias_trabajados = dias_trabajados
        self.horas_extra_diurnas = horas_extra_diurnas
        self.horas_extra_nocturnas = horas_extra_nocturnas
        self.horas_extra_dominicales_diurnas = horas_extra_dominicales_diurnas
        self.horas_extra_dominicales_nocturnas = horas_extra_dominicales_nocturnas
        self.horas_recargo_nocturno = horas_recargo_nocturno
        self.horas_recargo_dominical_festivo = horas_recargo_dominical_festivo

    def resumen_liquidacion(self, resultado: dict) -> str:
        """
        Devuelve una cadena de texto con el resumen completo de la
        liquidación de nómina del trabajador, mostrando devengados,
        deducciones, neto a pagar y provisiones de prestaciones
        sociales.
        """
        provisiones = resultado["provisiones_prestacionales"]
        return (
            f"Trabajador: {self.nombre}\n"
            f"Código: {self.codigo_empleado}\n"
            f"Salario base: ${self.salario_base:,.2f}\n"
            f"Días trabajados: {self.dias_trabajados}\n"
            f"----------------------------\n"
            f"Value hora ordinaria: ${resultado['valor_hora_ordinaria']:,.2f}\n"
            f"Salario proporcional: ${resultado['salario_proporcional']:,.2f}\n"
            f"Auxilio de transporte: ${resultado['auxilio_transporte']:,.2f}\n"
            f"Hora extra diurna (HED): ${resultado['hora_extra_diurna']:,.2f}\n"
            f"Hora extra nocturna (HEN): ${resultado['hora_extra_nocturna']:,.2f}\n"
            f"Hora extra dominical diurna (HEDD): ${resultado['hora_extra_dominical_diurna']:,.2f}\n"
            f"Hora extra dominical nocturna (HEDN): ${resultado['hora_extra_dominical_nocturna']:,.2f}\n"
            f"Recargo nocturno (RN): ${resultado['recargo_nocturno']:,.2f}\n"
            f"Recargo dominical/festivo (RDF): ${resultado['recargo_dominical_festivo']:,.2f}\n"
            f"----------------------------\n"
            f"Total devengado: ${resultado['total_devengado']:,.2f}\n"
            f"IBC (seguridad social): ${resultado['ibc']:,.2f}\n"
            f"Salud empleado (4%): ${resultado['salud_empleado']:,.2f}\n"
            f"Pensión empleado (4%): ${resultado['pension_empleado']:,.2f}\n"
            f"Total deducciones: ${resultado['total_deducciones']:,.2f}\n"
            f"----------------------------\n"
            f"NETO A PAGAR: ${resultado['neto_a_pagar']:,.2f}\n"
            f"----------------------------\n"
            f"Provisión cesantías: ${provisiones['cesantias']:,.2f}\n"
            f"Provisión intereses de cesantías: ${provisiones['intereses_cesantias']:,.2f}\n"
            f"Provisión prima de servicios: ${provisiones['prima_servicios']:,.2f}\n"
            f"Provisión vacaciones: ${provisiones['vacaciones']:,.2f}"
        )



def pedir_horas(mensaje: str) -> float:
    """Pide un número de horas por consola y lo retorna como float."""
    valor = input(mensaje)
    return float(valor) if valor.strip() != "" else 0


print("\n")
print("============================================")
print("   LIQUIDADOR DE NÓMINA - COLOMBIA")
print("============================================")
print("\n")


codigo_empleado = input("Ingrese el código del empleado: ")
nombre = input("Ingrese el nombre del empleado: ")
salario_base = float(input("Ingrese el salario base mensual del empleado: "))
dias_trabajados = int(input("Ingrese los días trabajados en el mes (0 a 30): "))

print("\n")
print("-----------------------")
print("MENU")
print("-----------------------")
print("1. Calcular valor de la nómina (sin horas extra ni recargos)")
print("2. Liquidar nómina completa (horas extra y recargos)")
print("3. Salir")
print("-----------------------")
print("\n")

opcion_calcular = int(input("Ingrese la opción a realizar: "))
print("--------------------------------------------")

while opcion_calcular != 3:
    if opcion_calcular == 1:
        resultado = logica_nomina.LiquidadorNomina(
            salario_base=salario_base, dias_trabajados=dias_trabajados
        )
        trabajador_actual = Trabajador(codigo_empleado, nombre, salario_base, dias_trabajados,horas_extra_diurnas=0, horas_extra_nocturnas=0, horas_extra_dominicales_diurnas=0, horas_extra_dominicales_nocturnas=0, horas_recargo_nocturno=0, horas_recargo_dominical_festivo=0)
        print(trabajador_actual.resumen_liquidacion(resultado))
        print("--------------------------------------------")
        print("\n")

    elif opcion_calcular == 2:
        print("Ingrese la cantidad de horas por cada concepto (deje vacío = 0):")
        horas_extra_diurnas = pedir_horas("Horas extra diurnas (HED): ")
        horas_extra_nocturnas = pedir_horas("Horas extra nocturnas (HEN): ")
        horas_extra_dominicales_diurnas = pedir_horas("Horas extra dominicales diurnas (HEDD): ")
        horas_extra_dominicales_nocturnas = pedir_horas("Horas extra dominicales nocturnas (HEDN): ")
        horas_recargo_nocturno = pedir_horas("Horas de recargo nocturno (RN): ")
        horas_recargo_dominical_festivo = pedir_horas("Horas de recargo dominical/festivo (RDF): ")

        hoy = date.today()
        resultado = logica_nomina.liquidar_nomina(datos_empleado=logica_nomina.Empleado(
            salario_base=salario_base, 
            dias_trabajados=dias_trabajados, 
            horas_extra_diurnas=horas_extra_diurnas, 
            horas_extra_nocturnas=horas_extra_nocturnas, 
            horas_extra_dominicales_diurnas=horas_extra_dominicales_diurnas, 
            horas_extra_dominicales_nocturnas=horas_extra_dominicales_nocturnas, 
            horas_recargo_nocturno=horas_recargo_nocturno, 
            horas_recargo_dominical_festivo=horas_recargo_dominical_festivo))

        print(f"Nómina liquidada el {hoy}")
        trabajador_actual = Trabajador(codigo_empleado, nombre, salario_base, dias_trabajados,horas_extra_diurnas, horas_extra_nocturnas, horas_extra_dominicales_diurnas, horas_extra_dominicales_nocturnas, horas_recargo_nocturno, horas_recargo_dominical_festivo)
        print(trabajador_actual.resumen_liquidacion(resultado))
        print("--------------------------------------------")
        print("\n")

    opcion_calcular = int(input("Ingrese otra opción a realizar: "))
    print("---------------------------------------------")

print("Hasta luego")
print("\n")
