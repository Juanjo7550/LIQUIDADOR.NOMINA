# 🧾 Liquidador de Nómina - Colombia

## 📌 Descripción del proyecto

Este proyecto consiste en el desarrollo de un sistema para **liquidar la nómina mensual de un trabajador en Colombia**, teniendo en cuenta las principales reglas de la legislación laboral vigente: auxilio de transporte, horas extra (diurnas, nocturnas, dominicales/festivas diurnas y dominicales/festivas nocturnas), recargos (nocturno y dominical/festivo), aportes a seguridad social (salud y pensión) y la provisión de prestaciones sociales a cargo del empleador (cesantías, intereses de cesantías, prima de servicios y vacaciones).

El proyecto fue desarrollado siguiendo la misma arquitectura y metodología de pruebas de un sistema de facturación previo (basado en el patrón **Model - View**, con pruebas unitarias en `unittest`), adaptando toda la lógica al dominio de **nómina colombiana**.

---

## 🎯 Objetivo

El objetivo principal es desarrollar y probar un conjunto de funciones que permitan calcular correctamente el valor devengado, deducido y neto a pagar de un trabajador, teniendo en cuenta el salario base, los días trabajados, el auxilio de transporte, las horas extra y los recargos legales.

También se busca comprobar el funcionamiento del programa mediante **pruebas unitarias**, incluyendo pruebas de casos reales, casos de error y casos extraordinarios.

---

## ⚙️ Funcionamiento

El programa recibe como datos de entrada:

* 💰 **Salario base mensual:** salario fijo mensual pactado con el trabajador.
* 📅 **Días trabajados:** cantidad de días efectivamente laborados en el mes (0 a 30).
* ⏱️ **Horas extra y recargos (opcional):** cantidad de horas de cada tipo (diurnas, nocturnas, dominicales/festivas diurnas, dominicales/festivas nocturnas, recargo nocturno, recargo dominical/festivo).

El sistema calcula automáticamente el auxilio de transporte, el valor de cada tipo de hora extra y recargo, los aportes a seguridad social del empleado y el neto a pagar, además de la provisión de prestaciones sociales a cargo del empleador.

### 🧮 Reglas laborales implementadas

#### 🚌 Auxilio de transporte
Aplica únicamente a trabajadores que devenguen **hasta 2 SMMLV** (Salarios Mínimos Mensuales Legales Vigentes). Si el salario base supera este tope, el trabajador no tiene derecho al auxilio.

#### ⏱️ Horas extra
| Tipo | Sigla | Horario | Recargo |
| --- | --- | --- | --- |
| Hora extra diurna | HED | 6:00 a.m. - 9:00 p.m. | 25% |
| Hora extra nocturna | HEN | 9:00 p.m. - 6:00 a.m. | 75% |
| Hora extra dominical/festiva diurna | HEDD | Domingo/festivo, horario diurno | 100% |
| Hora extra dominical/festiva nocturna | HEDN | Domingo/festivo, horario nocturno | 150% |

#### 🌙 Recargos (trabajo ordinario, sin ser hora extra)
| Tipo | Sigla | Recargo |
| --- | --- | --- |
| Recargo nocturno | RN | 35% |
| Recargo dominical/festivo | RDF | 75% |

#### 🏥 Seguridad social (a cargo del empleado)
* **Salud:** 4% del Ingreso Base de Cotización (IBC).
* **Pensión:** 4% del Ingreso Base de Cotización (IBC).

> El **auxilio de transporte no hace parte del IBC**, ya que no constituye salario para efectos de seguridad social.

#### 📦 Provisión de prestaciones sociales (a cargo del empleador, informativo)
* **Cesantías:** 8.33% del IBC.
* **Intereses de cesantías:** 12% del valor de las cesantías.
* **Prima de servicios:** 8.33% del IBC.
* **Vacaciones:** 4.17% del salario proporcional.

---

## 📥 Valores de entrada

| Entrada | Descripción |
| --- | --- |
| 💰 **Salario base** | Salario mensual fijo pactado con el trabajador |
| 📅 **Días trabajados** | Días efectivamente laborados en el mes (0 a 30) |
| ⏱️ **Horas extra diurnas / nocturnas / dominicales diurnas / dominicales nocturnas** | Cantidad de horas de cada tipo trabajadas en el periodo |
| 🌙 **Horas de recargo nocturno / dominical-festivo** | Cantidad de horas ordinarias trabajadas en horario nocturno o en domingo/festivo |

---

## 📤 Valores de salida

| Salida | Descripción |
| --- | --- |
| 💵 **Total devengado** | Suma de salario proporcional, auxilio de transporte, horas extra y recargos |
| 📉 **Total deducciones** | Suma de los aportes a salud y pensión del empleado |
| 💸 **Neto a pagar** | Total devengado menos total de deducciones |
| 📦 **Provisiones prestacionales** | Cesantías, intereses de cesantías, prima de servicios y vacaciones (informativo) |

---

## ⚠️ Constantes legales

Los valores de **SMMLV** y **Auxilio de Transporte** son fijados cada año por el Gobierno Nacional mediante decreto, por lo cual **deben actualizarse cada año** en el archivo `logica_nomina.py` antes de liquidar nómina de un periodo distinto al de referencia. Actualmente el programa usa valores de referencia configurables como constantes al inicio del módulo (`SMMLV`, `AUXILIO_TRANSPORTE`, `HORAS_MES_LEGAL`).

---

## 🧪 Pruebas unitarias

Las pruebas fueron desarrolladas utilizando **Python y la librería `unittest`**.

Las pruebas cubren:

* Cálculo del valor de la hora ordinaria.
* Auxilio de transporte (con y sin derecho).
* Cada tipo de hora extra y de recargo.
* Aportes a seguridad social (salud y pensión).
* Liquidación completa de nómina en distintos escenarios (salario mínimo, con horas extra, con días parciales).
* Provisión de prestaciones sociales.

---

## ❌ Casos de error

Se desarrollaron **4 casos de error** para comprobar el comportamiento del sistema cuando se ingresan datos inválidos:

### 🔴 Error 1 — Salario base igual a cero
Se comprueba que el sistema no permita liquidar la nómina cuando el salario base es igual a `0`.

### 🔴 Error 2 — Salario base negativo
Se comprueba que el sistema rechace un salario base negativo.

### 🔴 Error 3 — Horas extra negativas
Se comprueba que el sistema rechace una cantidad negativa de horas extra.

### 🔴 Error 4 — Días trabajados fuera de rango
Se comprueba que el sistema rechace una cantidad de días trabajados superior a 30 (o negativa).

---

## 🟣 Casos de prueba extraordinarios

También se realizaron **3 casos de prueba extraordinarios**:

### 🟣 Extraordinario 1 — Salario muy alto (sin auxilio de transporte)
Se prueba el sistema con un salario considerablemente superior a 2 SMMLV, verificando que el auxilio de transporte sea igual a `0`.

### 🟣 Extraordinario 2 — Todos los tipos de hora extra y recargo a la vez
Se prueba el sistema liquidando, en el mismo periodo, horas extra diurnas, nocturnas, dominicales diurnas, dominicales nocturnas, recargo nocturno y recargo dominical/festivo simultáneamente.

### 🟣 Extraordinario 3 — Cero días trabajados
Se prueba el sistema con un trabajador que no laboró ningún día del periodo, verificando que el salario proporcional y el auxilio de transporte sean iguales a `0` sin generar errores.

### 📊 Resumen de pruebas especiales

| Tipo | Caso | Objetivo |
| --- | --- | --- |
| 🔴 Error | Salario base = `0` | Validar el salario base |
| 🔴 Error | Salario base negativo | Rechazar salarios inválidos |
| 🔴 Error | Horas extra negativas | Rechazar cantidades de horas inválidas |
| 🔴 Error | Días trabajados fuera de rango (0-30) | Validar los días trabajados |
| 🟣 Extraordinario | Salario > 2 SMMLV | Verificar ausencia de auxilio de transporte |
| 🟣 Extraordinario | Todos los tipos de hora a la vez | Probar la liquidación completa combinada |
| 🟣 Extraordinario | Cero días trabajados | Probar un periodo sin días laborados |

---

# 📂 Estructura del repositorio

El proyecto está organizado dentro de la carpeta principal `NOMINA_COL`, donde se encuentra el código fuente del sistema, siguiendo el patrón **Model - View** con pruebas unitarias separadas.

```
NOMINA_COL/
│
├── 📄 README.md
│   └── Documentación general del proyecto
│
└── 📁 src/
    │
    ├── 🧠 model/
    │   ├── __init__.py
    │   └── logica_nomina.py
    │
    ├── 🧪 test/
    │   ├── __init__.py
    │   └── test_nomina.py
    │
    └── 🖥️ view/
        ├── __init__.py
        └── consola_nomina.py
```

## 📄 README.md

Contiene la documentación general del proyecto, incluyendo:

Descripción del sistema. Objetivo. Funcionamiento. Reglas laborales implementadas. Valores de entrada y salida. Constantes legales. Pruebas realizadas. Casos de error. Casos extraordinarios. Estructura del proyecto. Futuras implementaciones. Información de los autores.

## 🧠 model

Contiene la lógica principal del sistema.

`__init__.py` → Permite identificar la carpeta como un paquete de Python.

`logica_nomina.py` → Contiene todas las funciones de cálculo (hora ordinaria, auxilio de transporte, horas extra, recargos, IBC, seguridad social, prestaciones sociales y liquidación completa), así como las validaciones y excepciones personalizadas.

## 🧪 test

Contiene las pruebas unitarias del proyecto.

`__init__.py` → Permite identificar la carpeta como un paquete de Python.

`test_nomina.py` → Contiene las pruebas de cada concepto de nómina, los 4 casos de error y los 3 casos extraordinarios.

## 🖥️ view

Contiene la parte encargada de la interacción con el usuario.

`__init__.py` → Permite identificar la carpeta como un paquete de Python.

`consola_nomina.py` → Contiene la interfaz de consola para interactuar con el sistema de liquidación de nómina.

## 🔗 Organización general

La estructura del proyecto permite separar claramente cada responsabilidad:

🧠 Model → 🖥️ View → 🧪 Test

De esta manera:

🧠 Model: realiza los cálculos y validaciones de nómina.

🖥️ View: permite la interacción mediante consola.

🧪 Test: comprueba que el sistema funcione correctamente.

📄 README: documenta todo el proyecto.

---

## 🚀 Futuras implementaciones

Como futuras mejoras del proyecto, se busca:

* 📅 Actualizar automáticamente las constantes de SMMLV y auxilio de transporte según el año vigente (por ejemplo, consultando una fuente externa).
* 🧮 Incluir el **Fondo de Solidaridad Pensional** para salarios superiores a 4 SMMLV.
* 📉 Incluir la **retención en la fuente** cuando aplique según el ingreso del trabajador.
* 🖨️ Generar el desprendible de nómina en PDF o Excel.
* 📊 Permitir la liquidación de nómina para varios trabajadores a la vez (nómina masiva).
* ⚙️ Representar de una manera más completa las novedades de nómina (incapacidades, licencias, embargos, etc.).

---

## 💻 Tecnologías utilizadas

| Tecnología | Uso |
| --- | --- |
| 🐍 **Python** | Desarrollo del programa |
| 🧪 **unittest** | Creación y ejecución de pruebas unitarias |
| 🐙 **GitHub** | Almacenamiento y gestión del proyecto |

---

## 📚 Metodología

El proyecto se desarrolló siguiendo el siguiente proceso:

**Normatividad laboral colombiana → Identificación de reglas de nómina → Desarrollo de las funciones de cálculo → Pruebas de casos reales → Casos de error → Casos extraordinarios → Análisis de resultados**

---

# ▶️ Ejecución del proyecto y pruebas

Para ejecutar el proyecto y comprobar el funcionamiento de las pruebas, otra persona puede descargar o clonar el repositorio y seguir los siguientes pasos.

## 1️⃣ Clonar el repositorio

Desde una terminal se debe ejecutar:

```
git clone URL_DEL_REPOSITORIO
```

Luego ingresar a la carpeta raíz del proyecto (la que contiene la carpeta `NOMINA_COL`).

## 2️⃣ Verificar la estructura del proyecto

Dentro de la carpeta raíz se encontrará la carpeta `NOMINA_COL`, que contiene las diferentes partes del sistema:

```
NOMINA_COL/
│
├── README.md
│
└── src/
    ├── model/
    ├── test/
    └── view/
```

## 3️⃣ Ejecutar las pruebas

Las pruebas unitarias se encuentran dentro de:

```
NOMINA_COL/src/test/test_nomina.py
```

Para ejecutarlas desde la terminal, ubicándose en la **carpeta raíz del proyecto** (la que contiene `NOMINA_COL`), se puede utilizar:

```
python -m unittest discover -s NOMINA_COL/src/test
```

Este comando busca automáticamente las pruebas dentro de la carpeta `NOMINA_COL/src/test` y las ejecuta.

## 4️⃣ Resultado esperado

Al ejecutar las pruebas, el programa mostrará en la terminal el resultado de las 23 pruebas realizadas (casos reales, casos de error y casos extraordinarios). Si todas las pruebas funcionan correctamente, se mostrará `OK` al final de la ejecución.

## 🖥️ Ejecución de la aplicación

Además de las pruebas unitarias, el proyecto cuenta con una interfaz de consola ubicada en:

```
NOMINA_COL/src/view/consola_nomina.py
```

Para ejecutarla, ubicándose en la **carpeta raíz del proyecto**, se puede utilizar:

```
python NOMINA_COL/src/view/consola_nomina.py
```

Esta parte permite interactuar con el sistema mediante la consola, ingresar el salario base, los días trabajados y las horas extra/recargos, y obtener el detalle completo de la liquidación de nómina.

---

## 👥 Autores

**[David Rios Arias ,	Juan José García]**

## 👥 Editor

**[Simon Yepes Cano]**

---

## 📌 Conclusión

El proyecto permite representar de manera clara y modular el proceso de **liquidación de nómina de un trabajador en Colombia**, teniendo en cuenta el auxilio de transporte, las horas extra, los recargos legales, los aportes a seguridad social y la provisión de prestaciones sociales.

Las pruebas unitarias permiten comprobar que los cálculos realizados por el programa sean correctos, mientras que los **4 casos de error** permiten validar el comportamiento del sistema frente a datos inválidos.

Por otra parte, los **3 casos extraordinarios** permiten comprobar que el programa también pueda trabajar correctamente con situaciones diferentes a las más comunes, como salarios altos, combinaciones de todos los tipos de hora extra o periodos sin días laborados.

Como futura mejora, se plantea incorporar el Fondo de Solidaridad Pensional, la retención en la fuente y la generación de desprendibles de nómina en PDF, haciendo que el sistema sea más completo y cercano a un liquidador de nómina real.
