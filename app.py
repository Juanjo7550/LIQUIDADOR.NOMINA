import sys
sys.path.append("src")

from flask import Flask

app = Flask(__name__)

from view import vista_empleados

app.register_blueprint(vista_empleados.vista )

if __name__ == "__main__":
    app.run(debug=True)