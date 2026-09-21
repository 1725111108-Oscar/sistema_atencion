from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from fila import Fila
 
app = Flask(__name__)
app.secret_key = "cambia-esta-clave"   # necesaria para usar flash()
 
fila = Fila()            # la fila vive en memoria mientras el servidor esté encendido
ultimo_atendido = None   # texto con el último estudiante atendido
 
TRAMITES = [
    "Constancia de estudios",
    "Inscripción o reinscripción",
    "Historial académico (kardex)",
    "Credencial",
    "Baja temporal",
    "Otro",
]
 
 
def mostrar_pagina(datos=None):
    """Dibuja la página con el estado actual de la fila."""
    return render_template(
        "index.html",
        estudiantes=fila.mostrar(),          # d) mostrar todos
        total=fila.contar(),                 # e) cuántos esperan
        siguiente=fila.consultar_siguiente(),
        ultimo=ultimo_atendido,
        tramites=TRAMITES,
        datos=datos or {},                   # conserva lo escrito si hay error
    )
 
 
@app.route("/")
def inicio():
    return mostrar_pagina()
 
 
# a) Agregar estudiante
@app.route("/agregar", methods=["POST"])
def agregar():
    estudiante = {
        "matricula": request.form.get("matricula", "").strip(),
        "nombre": " ".join(request.form.get("nombre", "").split()),
        "carrera": request.form.get("carrera", "").strip(),
        "tramite": request.form.get("tramite", "").strip(),
    }
 
    if not all(estudiante.values()):
        flash("Completa todos los datos del estudiante.", "error")
        return mostrar_pagina(estudiante)
    if not estudiante["matricula"].isdigit():
        flash("La matrícula solo debe llevar números.", "error")
        return mostrar_pagina(estudiante)
    if fila.existe_matricula(estudiante["matricula"]):
        flash("Esa matrícula ya está en la fila.", "error")
        return mostrar_pagina(estudiante)
 
    fila.agregar(estudiante)
    flash(f"{estudiante['nombre']} se agregó al lugar {fila.contar()} de la fila.", "ok")
    return redirect(url_for("inicio"))
 
 
# b) Atender al estudiante del frente
@app.route("/atender", methods=["POST"])
def atender():
    global ultimo_atendido
 
    atendido = fila.atender()
    if atendido is None:
        flash("No hay a quién atender: la fila está vacía.", "alerta")
        return redirect(url_for("inicio"))
 
    hora = datetime.now().strftime("%H:%M")
    ultimo_atendido = f"{atendido['nombre']} ({atendido['tramite']}) a las {hora}"
    flash(f"Se atendió a {atendido['nombre']}.", "ok")
 
    # f) Aviso si ya no queda nadie
    if fila.esta_vacia():
        flash("Ya no hay estudiantes esperando. La fila quedó vacía.", "alerta")
    return redirect(url_for("inicio"))
 
 
# c) Consultar quién es el siguiente
@app.route("/siguiente", methods=["POST"])
def siguiente():
    sig = fila.consultar_siguiente()
    if sig is None:
        flash("No hay siguiente estudiante: la fila está vacía.", "alerta")
    else:
        flash(
            f"El siguiente es {sig['nombre']} (matrícula {sig['matricula']}), "
            f"trámite: {sig['tramite']}.",
            "info",
        )
    return redirect(url_for("inicio"))
 
 
if __name__ == "__main__":
    app.run(debug=True)
 