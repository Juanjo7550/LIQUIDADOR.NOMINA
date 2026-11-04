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

El proyecto sigue el patrón **Model - View - Controller**, con pruebas unitarias separadas.

```
LIQUIDADOR.NOMINA/
│
├── 📄 README.md
├── 🌐 app.py                     → Aplicación web (Flask): menú de inicio, crear tabla, insertar y buscar
├── 🖥️ app_kivy.py                → Interfaz gráfica de escritorio (Kivy), versión anterior
├── 📦 requirements.txt           → Dependencias de la aplicación web
├── 🔑 secret_config_sample.py    → Plantilla de los datos de conexión (copiar como secret_config.py)
│
├── 🗄️ sql/                       → Scripts SQL de referencia (crear, borrar, insertar, buscar)
│
├── 🧩 templates/                 → Plantillas HTML de la aplicación web
│   ├── buscar_y_guardar_empleado.html → Página de inicio (menú): buscar, liquidar/insertar y crear tabla
│   ├── mostrar_empleados.html    → Resultado de insertar un empleado
│   ├── empleado_encontrado.html  → Resultado de una búsqueda exitosa
│   ├── empleado_no_encontrado.html → Mensaje cuando el empleado no existe
│   └── resultado_tabla.html      → Resultado de crear la tabla
│
├── 🎨 static/
│   └── estilos.css               → Estilos de la aplicación web
│
├── 📁 src/
│   ├── 🧠 model/
│   │   └── logica_nomina.py      → Clase Empleado y lógica de nómina
│   ├── 🔌 controller/
│   │   └── trabajadores_controller.py → Crear/borrar tabla, insertar, buscar y borrar en la BD
│   └── 🖥️ view/
│       └── consola_nomina.py     → Interfaz de consola del cálculo de nómina
│
└── 🧪 test/
    ├── test_nomina.py            → Pruebas de la lógica de nómina
    └── test_trabajadores_controller.py → Pruebas del controlador con la base de datos
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

Las vistas de la aplicación web son las plantillas HTML de la carpeta `templates/`, con sus estilos en `static/`.

## 🔌 controller

`trabajadores_controller.py` → Crea y borra la tabla `Empleado`, e inserta, busca y borra empleados en la base de datos PostgreSQL.

Las rutas web (`/`, `/crear_tabla`, `/guardar_empleado`, `/buscar_empleado`) están definidas en `app.py`.

## 🔗 Organización general

La estructura del proyecto permite separar claramente cada responsabilidad:

🧠 Model → 🔌 Controller → 🖥️ View → 🧪 Test

De esta manera:

🧠 Model: realiza los cálculos y validaciones de nómina.

🔌 Controller: guarda y consulta los empleados en la base de datos.

🖥️ View: permite la interacción mediante la página web (y también por consola).

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
| 🌐 **Flask** | Aplicación web |
| 🐘 **PostgreSQL + psycopg2** | Base de datos de empleados |
| 🧪 **unittest** | Creación y ejecución de pruebas unitarias |
| 🐙 **GitHub** | Almacenamiento y gestión del proyecto |

---

## 📚 Metodología

El proyecto se desarrolló siguiendo el siguiente proceso:

**Normatividad laboral colombiana → Identificación de reglas de nómina → Desarrollo de las funciones de cálculo → Pruebas de casos reales → Casos de error → Casos extraordinarios → Análisis de resultados**

---

# ▶️ Ejecución del proyecto y pruebas

La aplicación es una **aplicación web hecha con Flask** que guarda los empleados en una base de datos **PostgreSQL** (por ejemplo, una base de datos gratuita en [Render](https://render.com)) usando `psycopg2`.

## 1️⃣ Requisitos

* Python 3.10 o superior.
* Una base de datos PostgreSQL (local o en la nube, por ejemplo en Render).
* Git.

## 2️⃣ Clonar el repositorio e instalar dependencias

```
git clone https://github.com/Juanjo7550/LIQUIDADOR.NOMINA.git
cd LIQUIDADOR.NOMINA
python -m venv .venv
.venv\Scripts\activate        (en Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

> Si la instalación de `psycopg2` falla (es común en Windows), instale la versión precompilada: `pip install psycopg2-binary`.

## 3️⃣ Crear una base de datos en blanco

La aplicación puede arrancar con una base de datos **completamente vacía**: la tabla se crea desde la propia página web (paso 6).

* **En Render:** *New → PostgreSQL*. Cuando esté lista, copie los datos de la sección *Connections*: host, puerto, nombre de la base de datos, usuario y contraseña.
* **En local:** con PostgreSQL instalado, cree una base de datos vacía, por ejemplo:

```
psql -U postgres -c "CREATE DATABASE nomina;"
```

## 4️⃣ Configurar la conexión

Los datos de conexión **no** se guardan en el código. Se leen del archivo `secret_config.py`, que está en `.gitignore` y no se sube al repositorio.

1. Copie `secret_config_sample.py` y renombre la copia como `secret_config.py` (en la carpeta raíz del proyecto).
2. Reemplace en `secret_config.py` los valores de ejemplo por los datos reales de su base de datos:

```python
PGDATABASE = "nomina"
PGUSER = "postgres"
PGPASSWORD = "su_contraseña"
PGHOST = "localhost"          # o el host que entrega Render
PGPORT = 5432
```

## 5️⃣ Ejecutar la aplicación web

Desde la carpeta raíz del proyecto, con el entorno virtual activado:

```
python app.py
```

Luego abra en el navegador: **http://127.0.0.1:5000**

## 6️⃣ Usar la aplicación

La página de inicio funciona como **menú** con acceso a todas las funcionalidades:

* 🗄️ **Crear tabla Empleado**: crea la tabla en la base de datos. Es lo **primero que se debe hacer con una base de datos en blanco**. Si la tabla ya existe, la aplicación lo informa y no cambia nada.
* 🧾 **Liquidar nómina (insertar)**: se ingresan el código, el nombre, el salario base, los días trabajados y las horas extra/recargos; la aplicación calcula el neto a pagar y guarda el empleado en la base de datos.
* 🔍 **Buscar empleado**: busca un empleado por su código y muestra sus datos guardados. Si no existe, muestra un mensaje indicándolo.

También existen, como versiones alternativas, una interfaz de escritorio con Kivy (`python app_kivy.py`, requiere `pip install kivy`) y una versión de consola del cálculo de nómina sin base de datos:

```
python src/view/consola_nomina.py
```

## 7️⃣ Ejecutar las pruebas

Desde la carpeta raíz del proyecto:

```
python -m unittest discover -s test -t .
```

* `test/test_nomina.py`: 23 pruebas de la lógica de nómina (no requieren base de datos).
* `test/test_trabajadores_controller.py`: 10 pruebas del controlador contra la base de datos (insertar, buscar, borrar y crear/borrar la tabla, con casos normales y de error). Requieren tener configurado `secret_config.py`. Antes de cada prueba se borra y se vuelve a crear la tabla `Empleado` (fixtures `setUp` / `tearDown`), así que **las pruebas borran los datos de esa tabla**; se recomienda usar una base de datos de pruebas.

Si todo funciona correctamente, se mostrará `OK` al final de la ejecución.

---

## 👥 Autores

**[Pedro José Hernandez ,	Juan José García]**

## 👥 Editor

**[Simon Yepes Cano]**

---

## 📌 Conclusión

El proyecto permite representar de manera clara y modular el proceso de **liquidación de nómina de un trabajador en Colombia**, teniendo en cuenta el auxilio de transporte, las horas extra, los recargos legales, los aportes a seguridad social y la provisión de prestaciones sociales.

Las pruebas unitarias permiten comprobar que los cálculos realizados por el programa sean correctos, mientras que los **4 casos de error** permiten validar el comportamiento del sistema frente a datos inválidos.

Por otra parte, los **3 casos extraordinarios** permiten comprobar que el programa también pueda trabajar correctamente con situaciones diferentes a las más comunes, como salarios altos, combinaciones de todos los tipos de hora extra o periodos sin días laborados.

Como futura mejora, se plantea incorporar el Fondo de Solidaridad Pensional, la retención en la fuente y la generación de desprendibles de nómina en PDF, haciendo que el sistema sea más completo y cercano a un liquidador de nómina real.
