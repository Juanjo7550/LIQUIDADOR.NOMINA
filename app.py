from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

import sys

sys.path.append("src")

# Lógica de la nómina
from model.logica_nomina import liquidar_nomina


class PaymentApp(App):

    def build(self):
        contenedor = GridLayout(
            cols=2,
            padding=20,
            spacing=20
        )

        # -----------------------------
        # SALARIO BASE
        # -----------------------------
        contenedor.add_widget(
            Label(text="Salario base")
        )

        self.salario = TextInput(
            font_size=30,
            multiline=False
        )

        contenedor.add_widget(self.salario)

        # -----------------------------
        # DÍAS TRABAJADOS
        # -----------------------------
        contenedor.add_widget(
            Label(text="Días trabajados")
        )

        self.dias = TextInput(
            font_size=30,
            multiline=False
        )

        contenedor.add_widget(self.dias)

        # -----------------------------
        # HORAS EXTRA DIURNAS
        # -----------------------------
        contenedor.add_widget(
            Label(text="Horas extra diurnas")
        )

        self.horas_extra_diurnas = TextInput(
            font_size=30,
            multiline=False
        )

        contenedor.add_widget(
            self.horas_extra_diurnas
        )

        # -----------------------------
        # RESULTADO
        # -----------------------------
        contenedor.add_widget(
            Label(text="Neto a pagar")
        )

        self.resultado = Label(
            text="0",
            font_size=25
        )

        contenedor.add_widget(self.resultado)

        # -----------------------------
        # BOTÓN CALCULAR
        # -----------------------------
        calcular = Button(
            text="Calcular",
            font_size=40
        )

        contenedor.add_widget(calcular)

        # Conectar el botón con el método
        calcular.bind(
            on_press=self.calcular_nomina
        )

        # Retornamos el contenedor principal
        return contenedor

    def calcular_nomina(self, value):
        """
        Realiza el cálculo de la nómina
        utilizando los datos ingresados.
        """

        try:
            # Validamos los datos
            self.validar()

            # Convertimos los valores
            salario = float(self.salario.text)
            dias = int(self.dias.text)
            horas_extra = float(
                self.horas_extra_diurnas.text
            )

            # Ejecutamos la lógica de nómina
            resultado = liquidar_nomina(
                salario_base=salario,
                dias_trabajados=dias,
                horas_extra_diurnas=horas_extra
            )

            # Mostramos el resultado
            self.resultado.text = (
                f"${resultado['neto_a_pagar']:,.2f}"
            )

        except ValueError:
            self.resultado.text = (
                "Error: ingrese valores numéricos válidos."
            )

        except Exception as err:
            self.mostrar_error(err)

    def validar(self):
        """
        Verifica que los datos ingresados
        sean correctos.
        """

        salario = self.salario.text.strip()
        dias = self.dias.text.strip()
        horas_extra = self.horas_extra_diurnas.text.strip()

        # --------------------------------
        # Validar salario
        # --------------------------------
        if not salario:
            raise Exception(
                "Debe ingresar el salario base."
            )

        try:
            salario_numero = float(salario)
        except ValueError:
            raise Exception(
                "El salario debe ser un número válido."
            )

        if salario_numero <= 0:
            raise Exception(
                "El salario debe ser mayor que cero."
            )

        # --------------------------------
        # Validar días
        # --------------------------------
        if not dias:
            raise Exception(
                "Debe ingresar los días trabajados."
            )

        try:
            dias_numero = int(dias)
        except ValueError:
            raise Exception(
                "Los días trabajados deben ser un número entero."
            )

        if dias_numero < 0 or dias_numero > 30:
            raise Exception(
                "Los días trabajados deben estar entre 0 y 30."
            )

        # --------------------------------
        # Validar horas extra
        # --------------------------------
        if not horas_extra:
            raise Exception(
                "Debe ingresar las horas extra diurnas."
            )

        try:
            horas_numero = float(horas_extra)
        except ValueError:
            raise Exception(
                "Las horas extra deben ser un número válido."
            )

        if horas_numero < 0:
            raise Exception(
                "Las horas extra no pueden ser negativas."
            )

    def mostrar_error(self, err):
        """
        Abre una ventana emergente con
        el mensaje de error.
        """

        contenido = GridLayout(
            cols=1,
            padding=10,
            spacing=10
        )

        contenido.add_widget(
            Label(text=str(err))
        )

        cerrar = Button(
            text="Cerrar"
        )

        contenido.add_widget(cerrar)

        popup = Popup(
            title="Error",
            content=contenido,
            size_hint=(0.8, 0.4)
        )

        cerrar.bind(
            on_press=popup.dismiss
        )

        popup.open()


if __name__ == "__main__":
    PaymentApp().run()
