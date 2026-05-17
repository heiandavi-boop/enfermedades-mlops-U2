import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

STATS_FILE = Path(os.getenv("STATS_FILE", "predicciones.json"))
CATEGORIAS = [
    "NO ENFERMO",
    "ENFERMEDAD LEVE",
    "ENFERMEDAD AGUDA",
    "ENFERMEDAD CRÓNICA",
    "ENFERMEDAD TERMINAL",
]

HTML_FORM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Predicción de enfermedad</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f7f9fb; }
        .card { background: white; max-width: 620px; padding: 28px; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.08); }
        label { display: block; margin-top: 14px; font-weight: bold; }
        input { width: 100%; padding: 10px; margin-top: 6px; border: 1px solid #ccc; border-radius: 8px; }
        button { margin-top: 20px; padding: 12px 18px; border: 0; border-radius: 8px; cursor: pointer; }
        .primary { background: #0b5ed7; color: white; }
        .secondary { background: #e9ecef; color: #222; }
        .result { margin-top: 20px; padding: 14px; background: #eef7ee; border-radius: 8px; }
        a { display: inline-block; margin-top: 16px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Servicio de predicción médica</h1>
        <p>Ingrese los datos clínicos básicos del paciente para obtener una clasificación simulada.</p>
        <form method="POST" action="/predecir_form">
            <label>Temperatura corporal (°C)</label>
            <input type="number" step="0.1" name="temperatura" required>

            <label>Número de síntomas</label>
            <input type="number" name="sintomas" required>

            <label>Días de evolución</label>
            <input type="number" name="dias_evolucion" required>

            <label>Severidad clínica observada (1 a 10)</label>
            <input type="number" name="severidad" min="1" max="10" required>

            <button class="primary" type="submit">Predecir</button>
        </form>
        <form method="GET" action="/estadisticas">
            <button class="secondary" type="submit">Ver estadísticas</button>
        </form>
        {% if resultado %}
        <div class="result"><strong>Resultado:</strong> {{ resultado }}</div>
        {% endif %}
    </div>
</body>
</html>
"""


def predecir_estado(temperatura: float, sintomas: int, dias_evolucion: int, severidad: int) -> str:
    """Simula la predicción del estado de enfermedad de un paciente.

    La función usa reglas simples porque el objetivo académico no es entrenar
    un modelo real, sino simular el comportamiento de un modelo desplegado.
    """
    if severidad >= 9 or (temperatura >= 40 and sintomas >= 8 and dias_evolucion >= 20):
        return "ENFERMEDAD TERMINAL"

    if dias_evolucion >= 30 or (sintomas >= 6 and dias_evolucion >= 15):
        return "ENFERMEDAD CRÓNICA"

    if temperatura >= 38.0 and sintomas >= 4 and dias_evolucion <= 14:
        return "ENFERMEDAD AGUDA"

    if temperatura < 38.0 and sintomas <= 3 and dias_evolucion <= 7:
        return "ENFERMEDAD LEVE"

    return "NO ENFERMO"


def _estadisticas_vacias() -> Dict:
    return {
        "total_por_categoria": {categoria: 0 for categoria in CATEGORIAS},
        "ultimas_5_predicciones": [],
        "fecha_ultima_prediccion": None,
    }


def cargar_estadisticas() -> Dict:
    if not STATS_FILE.exists():
        return _estadisticas_vacias()

    try:
        with STATS_FILE.open("r", encoding="utf-8") as archivo:
            data = json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return _estadisticas_vacias()

    base = _estadisticas_vacias()
    base.update(data)
    for categoria in CATEGORIAS:
        base["total_por_categoria"].setdefault(categoria, 0)
    return base


def guardar_prediccion(entrada: Dict, prediccion: str) -> Dict:
    estadisticas = cargar_estadisticas()
    fecha = datetime.now().isoformat(timespec="seconds")

    registro = {
        "fecha": fecha,
        "entrada": entrada,
        "prediccion": prediccion,
    }

    estadisticas["total_por_categoria"][prediccion] += 1
    estadisticas["ultimas_5_predicciones"].append(registro)
    estadisticas["ultimas_5_predicciones"] = estadisticas["ultimas_5_predicciones"][-5:]
    estadisticas["fecha_ultima_prediccion"] = fecha

    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STATS_FILE.open("w", encoding="utf-8") as archivo:
        json.dump(estadisticas, archivo, ensure_ascii=False, indent=2)

    return estadisticas


def _leer_entrada(payload: Dict) -> Dict:
    campos = ["temperatura", "sintomas", "dias_evolucion", "severidad"]
    faltantes = [campo for campo in campos if campo not in payload]
    if faltantes:
        raise ValueError(f"Faltan campos requeridos: {', '.join(faltantes)}")

    entrada = {
        "temperatura": float(payload["temperatura"]),
        "sintomas": int(payload["sintomas"]),
        "dias_evolucion": int(payload["dias_evolucion"]),
        "severidad": int(payload["severidad"]),
    }

    if entrada["sintomas"] < 0 or entrada["dias_evolucion"] < 0:
        raise ValueError("Los síntomas y días de evolución no pueden ser negativos.")
    if not 1 <= entrada["severidad"] <= 10:
        raise ValueError("La severidad debe estar entre 1 y 10.")

    return entrada


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_FORM)


@app.route("/predecir_form", methods=["POST"])
def predecir_form():
    try:
        entrada = _leer_entrada(request.form)
        resultado = predecir_estado(**entrada)
        guardar_prediccion(entrada, resultado)
        return render_template_string(HTML_FORM, resultado=resultado)
    except ValueError as error:
        return render_template_string(HTML_FORM, resultado=f"Error: {error}"), 400


@app.route("/predecir", methods=["POST"])
def predecir_api():
    if not request.is_json:
        return jsonify({"error": "La solicitud debe enviarse en formato JSON."}), 400

    try:
        entrada = _leer_entrada(request.get_json())
        resultado = predecir_estado(**entrada)
        estadisticas = guardar_prediccion(entrada, resultado)
        return jsonify({
            "entrada": entrada,
            "prediccion": resultado,
            "fecha_ultima_prediccion": estadisticas["fecha_ultima_prediccion"],
        })
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.route("/estadisticas", methods=["GET"])
def estadisticas_api():
    return jsonify(cargar_estadisticas())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
