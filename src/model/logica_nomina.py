



SMMLV = 1_423_500                       # Salario mínimo mensual de referencia
AUXILIO_TRANSPORTE = 200_000            # Auxilio de transporte mensual de referencia
TOPE_AUXILIO_TRANSPORTE = 2 * SMMLV     # El auxilio solo aplica hasta 2 SMMLV
HORAS_MES_LEGAL = 220                   # Divisor de horas según la jornada laboral legal vigente

# Aportes a seguridad social
PORC_SALUD_EMPLEADO = 0.04
PORC_PENSION_EMPLEADO = 0.04
PORC_SALUD_EMPLEADOR = 0.085
PORC_PENSION_EMPLEADOR = 0.12

# Provisión de prestaciones sociales (a cargo del empleador)
PORC_CESANTIAS = 0.0833
PORC_INTERESES_CESANTIAS = 0.12
PORC_PRIMA_SERVICIOS = 0.0833
PORC_VACACIONES = 0.0417

# Recargos y horas extra según el Código Sustantivo del Trabajo
PORC_RECARGO_HORA_EXTRA_DIURNA = 0.25              # HED
PORC_RECARGO_HORA_EXTRA_NOCTURNA = 0.75            # HEN
PORC_RECARGO_HORA_EXTRA_DOMINICAL_DIURNA = 1.00    # HEDD
PORC_RECARGO_HORA_EXTRA_DOMINICAL_NOCTURNA = 1.50  # HEDN
PORC_RECARGO_NOCTURNO = 0.35                       # RN (trabajo ordinario nocturno)
PORC_RECARGO_DOMINICAL_FESTIVO = 0.75              # RDF (trabajo ordinario dominical/festivo)


# ------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
# ------------------------------------------------------------------

class SalarioInvalido(Exception):
    """Se lanza cuando el salario base ingresado es 0 o menor. Indica que
    no se puede liquidar la nómina sin un salario base válido."""
    def __init__(self):
        super().__init__(
            "LIQUIDAR NOMINA: Valor Nómina. No es posible liquidar la nómina. "
            "Ingrese un salario base mayor que cero."
        )


class HorasInvalidas(Exception):
    """Se lanza cuando alguna cantidad de horas ingresada es negativa.
    Indica que no se puede liquidar la nómina con horas inválidas."""
    def __init__(self, tipo_hora="horas"):
        super().__init__(
            f"LIQUIDAR NOMINA: Valor Nómina. No es posible liquidar la nómina. "
            f"La cantidad de {tipo_hora} no puede ser negativa."
        )


class DiasInvalidos(Exception):
    """Se lanza cuando los días trabajados están fuera del rango permitido
    (0 a 30, ya que en Colombia el mes laboral comercial tiene 30 días)."""
    def __init__(self):
        super().__init__(
            "LIQUIDAR NOMINA: Valor Nómina. No es posible liquidar la nómina. "
            "Los días trabajados deben estar entre 0 y 30."
        )


# ------------------------------------------------------------------
# VALIDACIONES
# ------------------------------------------------------------------

def verificar_salario(salario_base):
    if salario_base <= 0:
        raise SalarioInvalido()


def verificar_horas(horas, tipo_hora="horas"):
    if horas < 0:
        raise HorasInvalidas(tipo_hora)


def verificar_dias(dias_trabajados):
    if dias_trabajados < 0 or dias_trabajados > 30:
        raise DiasInvalidos()


def verificar_valor_no_negativo(valor, tipo_valor="valor"):
    """Verifica que un valor monetario (IBC, base de aportes, etc.) no
    sea negativo. A diferencia de "verificar_salario", sí permite que
    el valor sea 0 (por ejemplo, un trabajador con 0 días trabajados
    en el periodo)."""
    if valor < 0:
        raise SalarioInvalido()


# ------------------------------------------------------------------
# VALOR DE LA HORA ORDINARIA
# ------------------------------------------------------------------

def calcular_valor_hora_ordinaria(salario_base: float, horas_mes: int = HORAS_MES_LEGAL) -> float:
    """Devuelve un float con el valor de una hora ordinaria de trabajo,
    resultado de dividir el "salario_base" mensual entre las
    "horas_mes" legales vigentes de la jornada laboral.
    "salario_base": Salario mensual fijo del trabajador.
    "horas_mes": Cantidad de horas mensuales que se toman como divisor
    según la jornada laboral legal vigente."""
    verificar_salario(salario_base)
    verificar_horas(horas_mes, "horas mensuales")
    return salario_base / horas_mes


# ------------------------------------------------------------------
# AUXILIO DE TRANSPORTE
# ------------------------------------------------------------------

def calcular_auxilio_transporte(salario_base: float) -> float:
    """Devuelve un float con el valor del auxilio de transporte al que
    tiene derecho el trabajador. Según la legislación laboral
    colombiana, este auxilio solo aplica cuando el "salario_base" es
    menor o igual a 2 SMMLV. Si el trabajador supera ese tope, no
    tiene derecho al auxilio y la función retorna 0."""
    verificar_salario(salario_base)
    if salario_base <= TOPE_AUXILIO_TRANSPORTE:
        return float(AUXILIO_TRANSPORTE)
    return 0.0


# ------------------------------------------------------------------
# HORAS EXTRA
# ------------------------------------------------------------------

def calcular_hora_extra_diurna(valor_hora: float, cantidad_horas: float) -> float:
    """HED - Hora extra diurna: se causa entre las 6:00 a.m. y las
    9:00 p.m. y tiene un recargo del 25% sobre el valor de la hora
    ordinaria."""
    verificar_horas(cantidad_horas, "horas extra diurnas")
    return valor_hora * (1 + PORC_RECARGO_HORA_EXTRA_DIURNA) * cantidad_horas


def calcular_hora_extra_nocturna(valor_hora: float, cantidad_horas: float) -> float:
    """HEN - Hora extra nocturna: se causa entre las 9:00 p.m. y las
    6:00 a.m. y tiene un recargo del 75% sobre el valor de la hora
    ordinaria."""
    verificar_horas(cantidad_horas, "horas extra nocturnas")
    return valor_hora * (1 + PORC_RECARGO_HORA_EXTRA_NOCTURNA) * cantidad_horas


def calcular_hora_extra_dominical_diurna(valor_hora: float, cantidad_horas: float) -> float:
    """HEDD - Hora extra dominical o festiva diurna: recargo del 100%
    sobre el valor de la hora ordinaria."""
    verificar_horas(cantidad_horas, "horas extra dominicales diurnas")
    return valor_hora * (1 + PORC_RECARGO_HORA_EXTRA_DOMINICAL_DIURNA) * cantidad_horas


def calcular_hora_extra_dominical_nocturna(valor_hora: float, cantidad_horas: float) -> float:
    """HEDN - Hora extra dominical o festiva nocturna: recargo del
    150% sobre el valor de la hora ordinaria."""
    verificar_horas(cantidad_horas, "horas extra dominicales nocturnas")
    return valor_hora * (1 + PORC_RECARGO_HORA_EXTRA_DOMINICAL_NOCTURNA) * cantidad_horas


# ------------------------------------------------------------------
# RECARGOS (TRABAJO ORDINARIO, NO EXTRA)
# ------------------------------------------------------------------

def calcular_recargo_nocturno(valor_hora: float, cantidad_horas: float) -> float:
    """RN - Recargo nocturno: se paga cuando el trabajador labora su
    jornada ordinaria (sin exceder el horario pactado) en horario
    nocturno (9:00 p.m. - 6:00 a.m.). Corresponde a un 35% adicional
    sobre el valor de la hora ordinaria."""
    verificar_horas(cantidad_horas, "horas de recargo nocturno")
    return valor_hora * PORC_RECARGO_NOCTURNO * cantidad_horas


def calcular_recargo_dominical_festivo(valor_hora: float, cantidad_horas: float) -> float:
    """RDF - Recargo dominical/festivo: se paga cuando el trabajador
    labora su jornada ordinaria en domingo o festivo, sin que dicha
    hora sea considerada hora extra. Corresponde a un 75% adicional
    sobre el valor de la hora ordinaria."""
    verificar_horas(cantidad_horas, "horas de recargo dominical/festivo")
    return valor_hora * PORC_RECARGO_DOMINICAL_FESTIVO * cantidad_horas


# ------------------------------------------------------------------
# SALARIO PROPORCIONAL, IBC Y DEDUCCIONES
# ------------------------------------------------------------------

def calcular_salario_proporcional(salario_base: float, dias_trabajados: int) -> float:
    """Devuelve un float con el salario proporcional a los
    "dias_trabajados" efectivamente laborados dentro del mes, tomando
    como base un mes comercial de 30 días."""
    verificar_salario(salario_base)
    verificar_dias(dias_trabajados)
    return (salario_base / 30) * dias_trabajados


def calcular_ibc(salario_devengado: float) -> float:
    """Devuelve el Ingreso Base de Cotización (IBC) utilizado para
    calcular los aportes a seguridad social. El auxilio de transporte
    NO hace parte del IBC porque no constituye salario para efectos
    de seguridad social ni de prestaciones sociales."""
    verificar_valor_no_negativo(salario_devengado, "salario devengado")
    return salario_devengado


def calcular_salud_empleado(ibc: float) -> float:
    """Devuelve el valor a descontar por concepto de salud a cargo del
    empleado, correspondiente al 4% del IBC."""
    verificar_valor_no_negativo(ibc, "IBC")
    return ibc * PORC_SALUD_EMPLEADO


def calcular_pension_empleado(ibc: float) -> float:
    """Devuelve el valor a descontar por concepto de pensión a cargo
    del empleado, correspondiente al 4% del IBC."""
    verificar_valor_no_negativo(ibc, "IBC")
    return ibc * PORC_PENSION_EMPLEADO


# ------------------------------------------------------------------
# PROVISIÓN DE PRESTACIONES SOCIALES (A CARGO DEL EMPLEADOR)
# ------------------------------------------------------------------

def calcular_provisiones_prestacionales(ibc: float, salario_proporcional: float) -> dict:
    """Devuelve un diccionario con la provisión mensual de las
    prestaciones sociales a cargo del empleador:
      - cesantías (8.33% del IBC)
      - intereses de cesantías (12% de las cesantías)
      - prima de servicios (8.33% del IBC)
      - vacaciones (4.17% del salario proporcional)
    Estos valores son informativos: no se descuentan del trabajador,
    se provisionan y se pagan en las fechas establecidas por la ley."""
    verificar_valor_no_negativo(ibc, "IBC")
    verificar_valor_no_negativo(salario_proporcional, "salario proporcional")

    cesantias = ibc * PORC_CESANTIAS
    intereses_cesantias = cesantias * PORC_INTERESES_CESANTIAS
    prima_servicios = ibc * PORC_PRIMA_SERVICIOS
    vacaciones = salario_proporcional * PORC_VACACIONES

    return {
        "cesantias": cesantias,
        "intereses_cesantias": intereses_cesantias,
        "prima_servicios": prima_servicios,
        "vacaciones": vacaciones,
    }


# ------------------------------------------------------------------
# LIQUIDACIÓN COMPLETA DE NÓMINA
# ------------------------------------------------------------------
class Empleado:
    def __init__(self, codigo_empleado: str="", nombre: str = "", salario_base: float = 0, dias_trabajados: int = 0,
                 horas_extra_diurnas: float = 0, horas_extra_nocturnas: float = 0,
                 horas_extra_dominicales_diurnas: float = 0, horas_extra_dominicales_nocturnas: float = 0,
                 horas_recargo_nocturno: float = 0, horas_recargo_dominical_festivo: float = 0,horas_mes: int = HORAS_MES_LEGAL):
        self.nombre = nombre
        self.codigo_empleado = codigo_empleado
        self.salario_base = salario_base
        self.dias_trabajados = dias_trabajados
        self.horas_extra_diurnas = horas_extra_diurnas
        self.horas_extra_nocturnas = horas_extra_nocturnas
        self.horas_extra_dominicales_diurnas = horas_extra_dominicales_diurnas
        self.horas_extra_dominicales_nocturnas = horas_extra_dominicales_nocturnas
        self.horas_recargo_nocturno = horas_recargo_nocturno
        self.horas_recargo_dominical_festivo = horas_recargo_dominical_festivo
        self.horas_mes = horas_mes

def liquidar_nomina(
    datos_empleado: Empleado

) -> dict:
    """Realiza la liquidación completa de la nómina mensual de un
    trabajador y devuelve un diccionario con el detalle de:
      - valor de la hora ordinaria,
      - salario proporcional a los días trabajados,
      - auxilio de transporte,
      - horas e xtra (diurnas, nocturnas, dominicales diurnas y
        dominicales nocturnas),
      - recargos (nocturno y dominical/festivo),
      - IBC,
      - deducciones de salud y pensión,
      - total devengado, total deducido y neto a pagar,
      - provisión de prestaciones sociales a cargo del empleador."""

    verificar_salario(datos_empleado.salario_base)
    verificar_dias(datos_empleado.dias_trabajados)
    verificar_horas(datos_empleado.horas_extra_diurnas, "horas extra diurnas")
    verificar_horas(datos_empleado.horas_extra_nocturnas, "horas extra nocturnas")
    verificar_horas(datos_empleado.horas_extra_dominicales_diurnas, "horas extra dominicales diurnas")
    verificar_horas(datos_empleado.horas_extra_dominicales_nocturnas, "horas extra dominicales nocturnas")
    verificar_horas(datos_empleado.horas_recargo_nocturno, "horas de recargo nocturno")
    verificar_horas(datos_empleado.horas_recargo_dominical_festivo, "horas de recargo dominical/festivo")

    valor_hora = calcular_valor_hora_ordinaria(datos_empleado.salario_base, datos_empleado.horas_mes)
    salario_proporcional = calcular_salario_proporcional(datos_empleado.salario_base, datos_empleado.dias_trabajados)
    auxilio_transporte = calcular_auxilio_transporte(datos_empleado.salario_base) * (datos_empleado.dias_trabajados / 30)

    hed = calcular_hora_extra_diurna(valor_hora, datos_empleado.horas_extra_diurnas)
    hen = calcular_hora_extra_nocturna(valor_hora, datos_empleado.horas_extra_nocturnas)
    hedd = calcular_hora_extra_dominical_diurna(valor_hora, datos_empleado.horas_extra_dominicales_diurnas)
    hedn = calcular_hora_extra_dominical_nocturna(valor_hora, datos_empleado.horas_extra_dominicales_nocturnas)
    rn = calcular_recargo_nocturno(valor_hora, datos_empleado.horas_recargo_nocturno)
    rdf = calcular_recargo_dominical_festivo(valor_hora, datos_empleado.horas_recargo_dominical_festivo)

    total_horas_extra_y_recargos = hed + hen + hedd + hedn + rn + rdf

    ibc = calcular_ibc(salario_proporcional + total_horas_extra_y_recargos)

    salud_empleado = calcular_salud_empleado(ibc)
    pension_empleado = calcular_pension_empleado(ibc)
    total_deducciones = salud_empleado + pension_empleado

    total_devengado = salario_proporcional + auxilio_transporte + total_horas_extra_y_recargos
    neto_a_pagar = total_devengado - total_deducciones

    provisiones = calcular_provisiones_prestacionales(ibc, salario_proporcional)

    return {
        "valor_hora_ordinaria": round(valor_hora, 2),
        "salario_proporcional": round(salario_proporcional, 2),
        "auxilio_transporte": round(auxilio_transporte, 2),
        "hora_extra_diurna": round(hed, 2),
        "hora_extra_nocturna": round(hen, 2),
        "hora_extra_dominical_diurna": round(hedd, 2),
        "hora_extra_dominical_nocturna": round(hedn, 2),
        "recargo_nocturno": round(rn, 2),
        "recargo_dominical_festivo": round(rdf, 2),
        "ibc": round(ibc, 2),
        "salud_empleado": round(salud_empleado, 2),
        "pension_empleado": round(pension_empleado, 2),
        "total_devengado": round(total_devengado, 2),
        "total_deducciones": round(total_deducciones, 2),
        "neto_a_pagar": round(neto_a_pagar, 2),
        "provisiones_prestacionales": {k: round(v, 2) for k, v in provisiones.items()},
    }
