import sys
sys.path.append("src")

from flask import Flask
from flask import  request, render_template 
from model import logica_nomina
from controller.trabajadores_controller import  Trabajadorescontroller
from model.logica_nomina import Empleado 

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("buscar_y_guardar_empleado.html")


@app.route("/guardar_empleado")
def guardar():
    #Arma una instancia de la clase liquidadora nomina

    empleado = Empleado(
        codigo_empleado = str(request.args["codigo_empleado"]) , 
        nombre = str(request.args["nombre"]),
        salario_base = float(request.args["salario_base"]), 
        dias_trabajados = float(request.args["dias_trabajados"]),
        horas_extra_diurnas = float(request.args.get("horas_extra_diurnas") or 0),
        horas_extra_nocturnas = float(request.args.get("horas_extra_nocturnas") or 0),
        horas_extra_dominicales_diurnas = float(request.args.get("horas_extra_dominicales_diurnas") or 0), 
        horas_extra_dominicales_nocturnas = float(request.args.get("horas_extra_dominicales_nocturnas") or 0),
        horas_recargo_nocturno = float(request.args.get("horas_recargo_nocturno") or 0), 
        horas_recargo_dominical_festivo = float(request.args.get("horas_recargo_dominical_festivo") or 0), neto_a_pagar = 0
    )
    
    datos_empleado = logica_nomina.Empleado(empleado.codigo_empleado,empleado.nombre,empleado.salario_base,empleado.dias_trabajados,empleado.horas_extra_diurnas,empleado.horas_extra_nocturnas,
        empleado.horas_extra_dominicales_diurnas,empleado.horas_extra_dominicales_nocturnas,empleado.horas_recargo_dominical_festivo)
    resultado= logica_nomina.liquidar_nomina(datos_empleado)
    empleado.neto_a_pagar = resultado["neto_a_pagar"]
    
    try:
        controlador = Trabajadorescontroller()
        controlador.insertar(empleado)
        return render_template("mostrar_empleados.html", empleado = empleado)
    except Exception as error:
        print(error)
        return f"Error encontrado: {error}"


@app.route("/buscar_empleado")
def bucar_empleado():
    
    codigo_empleado = str(request.args["codigo_empleado"])
    
    try:
        controlador = Trabajadorescontroller()
        empleado_encontrado = controlador.buscar_empleado(codigo_empleado)
        return f"""
        <p> El codigo del trabajador es : {codigo_empleado} </p>
        <p> El nombre del empleado es : {empleado_encontrado.nombre} </p>
        <p> El salario base del empleado es : {empleado_encontrado.salario_base} </p>
        <p> El empleado trabajo {empleado_encontrado.dias_trabajados} dias en el mes </p>
        <p> El empleado tuvo {empleado_encontrado.horas_extra_diurnas} horas_extra_diurnas en el mes </p>
        <p> El empleado tuvo {empleado_encontrado.horas_extra_nocturnas} horas_extra_nocturnas en el mes </p>
        <p> El empleado tuvo {empleado_encontrado.horas_extra_dominicales_diurnas} horas_extra_dominicales_diurnas en el mes </p>
        <p> El empleado tuvo {empleado_encontrado.horas_extra_dominicales_nocturnas} horas_extra_dominicales_nocturnas en el mes </p>
        <p> El empleado tuvo {empleado_encontrado.horas_recargo_nocturno} horas_recargo_nocturno en el mes </p>
        <p> El empleado tuvo {empleado_encontrado.horas_recargo_dominical_festivo} horas_recargo_dominical_festivo en el mes </p>
        """
    except Exception as error:
        return "El empleado no existe"



if __name__ == "__main__":
    app.run( debug=True )