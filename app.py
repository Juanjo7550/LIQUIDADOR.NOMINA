from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

import sys

sys.path.append("src")

# Lógica de la nómina
from model import logica_nomina
from model.logica_nomina import liquidar_nomina

# Acceso a la base de datos
from controller.trabajadores_controller import Trabajadorescontroller


# Campos numéricos del formulario: (atributo de Empleado, etiqueta, tipo)
CAMPOS_NUMERICOS = [
    ("salario_base", "Salario base", float),
    ("dias_trabajados", "Días trabajados", int),
    ("horas_extra_diurnas", "Horas extra diurnas", float),
    ("horas_extra_nocturnas", "Horas extra nocturnas", float),
    ("horas_extra_dominicales_diurnas", "Horas extra dominicales diurnas", float),
    ("horas_extra_dominicales_nocturnas", "Horas extra dominicales nocturnas", float),
    ("horas_recargo_nocturno", "Horas recargo nocturno", float),
    ("horas_recargo_dominical_festivo", "Horas recargo dominical/festivo", float),
]

# Longitudes máximas según la tabla Empleado (sql/crear_trabajadores.sql)
MAX_CODIGO = 10
MAX_NOMBRE = 20


class PaymentApp(App):

    def build(self):
        self.controlador = Trabajadorescontroller()

        principal = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        formulario = GridLayout(
            cols=2,
            spacing=10
        )

        # -----------------------------
        # CÓDIGO Y NOMBRE
        # -----------------------------
        self.codigo = self.agregar_campo(formulario, "Código empleado")
        self.nombre = self.agregar_campo(formulario, "Nombre")

        # -----------------------------
        # SALARIO, DÍAS, HORAS
        # -----------------------------
        self.campos = {}

        for atributo, etiqueta, _ in CAMPOS_NUMERICOS:
            self.campos[atributo] = self.agregar_campo(formulario, etiqueta)

        # -----------------------------
        # RESULTADO
        # -----------------------------
        formulario.add_widget(
            Label(text="Neto a pagar")
        )

        self.resultado = Label(
            text="0",
            font_size=22
        )

        formulario.add_widget(self.resultado)

        principal.add_widget(formulario)

        # -----------------------------
        # BOTONES
        # -----------------------------
        botones = BoxLayout(
            spacing=10,
            size_hint_y=None,
            height=60
        )

        for texto, accion in [
            ("Buscar", self.buscar_empleado),
            ("Insertar", self.insertar_empleado),
            ("Calcular", self.calcular_nomina),
            ("Limpiar", self.limpiar),
        ]:
            boton = Button(
                text=texto,
                font_size=24
            )
            boton.bind(on_press=accion)
            botones.add_widget(boton)

        principal.add_widget(botones)

        # Retornamos el contenedor principal
        return principal

    def agregar_campo(self, contenedor, etiqueta):
        """
        Agrega una etiqueta y su caja de texto
        al formulario, y retorna la caja.
        """

        contenedor.add_widget(
            Label(text=etiqueta)
        )

        campo = TextInput(
            font_size=20,
            multiline=False
        )

        contenedor.add_widget(campo)

        return campo

    # -----------------------------
    # ACCIONES DE LOS BOTONES
    # -----------------------------

    def buscar_empleado(self, value):
        """
        Busca en la base de datos el empleado
        con el código ingresado y llena el formulario.
        """

        try:
            codigo = self.codigo.text.strip()

            if not codigo:
                raise Exception(
                    "Ingrese el código del empleado a buscar."
                )

            empleado = self.controlador.buscar_empleado(codigo)

            self.mostrar_empleado(empleado)
            self.calcular_nomina(value)

        except Exception as err:
            self.mostrar_error(err)

    def insertar_empleado(self, value):
        """
        Valida los datos del formulario y guarda
        el empleado en la base de datos.
        """

        try:
            empleado = self.leer_empleado()

            self.controlador.insertar(empleado)

            self.mostrar_mensaje(
                "Empleado guardado",
                f"Se insertó el empleado {empleado.codigo_empleado}."
            )

        except Exception as err:
            self.mostrar_error(err)

    def calcular_nomina(self, value):
        """
        Realiza el cálculo de la nómina
        utilizando los datos ingresados.
        """

        try:
            empleado = self.leer_empleado(
                requiere_identificacion=False
            )

            # Ejecutamos la lógica de nómina
            resultado = liquidar_nomina(empleado)

            # Mostramos el resultado
            self.resultado.text = (
                f"${resultado['neto_a_pagar']:,.2f}"
            )

        except Exception as err:
            self.mostrar_error(err)

    def limpiar(self, value):
        """
        Borra todos los campos del formulario.
        """

        self.codigo.text = ""
        self.nombre.text = ""

        for campo in self.campos.values():
            campo.text = ""

        self.resultado.text = "0"

    # -----------------------------
    # FORMULARIO <-> EMPLEADO
    # -----------------------------

    def leer_empleado(self, requiere_identificacion=True):
        """
        Valida los datos del formulario y
        retorna un objeto Empleado.
        """

        codigo = self.codigo.text.strip()
        nombre = self.nombre.text.strip()

        # --------------------------------
        # Validar código y nombre
        # --------------------------------
        if requiere_identificacion:
            if not codigo:
                raise Exception(
                    "Debe ingresar el código del empleado."
                )

            if len(codigo) > MAX_CODIGO:
                raise Exception(
                    f"El código no puede tener más de {MAX_CODIGO} caracteres."
                )

            if not nombre:
                raise Exception(
                    "Debe ingresar el nombre del empleado."
                )

            if len(nombre) > MAX_NOMBRE:
                raise Exception(
                    f"El nombre no puede tener más de {MAX_NOMBRE} caracteres."
                )

        # --------------------------------
        # Validar salario, días y horas
        # --------------------------------
        valores = {}

        for atributo, etiqueta, tipo in CAMPOS_NUMERICOS:
            texto = self.campos[atributo].text.strip()

            # Las horas son opcionales; vacío equivale a 0
            if not texto:
                if atributo in ("salario_base", "dias_trabajados"):
                    raise Exception(
                        f"Debe ingresar: {etiqueta}."
                    )
                texto = "0"

            try:
                valores[atributo] = tipo(texto)
            except ValueError:
                tipo_texto = "un número entero" if tipo is int else "un número válido"
                raise Exception(
                    f"{etiqueta} debe ser {tipo_texto}."
                )

        empleado = logica_nomina.Empleado(
            codigo_empleado=codigo,
            nombre=nombre,
            **valores
        )

        # Reutilizamos las validaciones del modelo
        logica_nomina.verificar_salario(empleado.salario_base)
        logica_nomina.verificar_dias(empleado.dias_trabajados)

        for atributo, etiqueta, _ in CAMPOS_NUMERICOS[2:]:
            logica_nomina.verificar_horas(
                getattr(empleado, atributo),
                etiqueta.lower()
            )

        return empleado

    def mostrar_empleado(self, empleado):
        """
        Llena el formulario con los datos
        de un empleado.
        """

        self.codigo.text = empleado.codigo_empleado
        self.nombre.text = empleado.nombre

        for atributo, _, tipo in CAMPOS_NUMERICOS:
            valor = getattr(empleado, atributo)
            self.campos[atributo].text = str(tipo(valor))

    # -----------------------------
    # VENTANAS EMERGENTES
    # -----------------------------

    def mostrar_error(self, err):
        """
        Abre una ventana emergente con
        el mensaje de error.
        """

        self.mostrar_mensaje("Error", str(err))

    def mostrar_mensaje(self, titulo, mensaje):
        """
        Abre una ventana emergente con
        un título y un mensaje.
        """

        contenido = GridLayout(
            cols=1,
            padding=10,
            spacing=10
        )

        texto = Label(text=mensaje)

        # Ajusta el texto largo al ancho de la ventana
        texto.bind(
            width=lambda label, ancho: setattr(label, "text_size", (ancho, None))
        )

        contenido.add_widget(texto)

        cerrar = Button(
            text="Cerrar"
        )

        contenido.add_widget(cerrar)

        popup = Popup(
            title=titulo,
            content=contenido,
            size_hint=(0.8, 0.4)
        )

        cerrar.bind(
            on_press=popup.dismiss
        )

        popup.open()


if __name__ == "__main__":
    PaymentApp().run()
