import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import importlib


def test_modelo_retorna_las_cinco_categorias(tmp_path, monkeypatch):
    monkeypatch.setenv("STATS_FILE", str(tmp_path / "predicciones.json"))
    app_module = importlib.import_module("app.app")

    casos = [
        ((36.5, 0, 1, 1), "ENFERMEDAD LEVE"),
        ((37.6, 2, 3, 3), "ENFERMEDAD LEVE"),
        ((38.8, 5, 6, 6), "ENFERMEDAD AGUDA"),
        ((37.9, 7, 20, 7), "ENFERMEDAD CRÓNICA"),
        ((40.1, 9, 25, 9), "ENFERMEDAD TERMINAL"),
    ]

    for parametros, esperado in casos:
        assert app_module.predecir_estado(*parametros) == esperado


def test_estadisticas_despues_de_prediccion_api(tmp_path, monkeypatch):
    monkeypatch.setenv("STATS_FILE", str(tmp_path / "predicciones.json"))
    app_module = importlib.reload(importlib.import_module("app.app"))
    cliente = app_module.app.test_client()

    estadisticas_iniciales = cliente.get("/estadisticas")
    assert estadisticas_iniciales.status_code == 200
    assert estadisticas_iniciales.get_json()["fecha_ultima_prediccion"] is None

    respuesta = cliente.post(
        "/predecir",
        json={
            "temperatura": 40.1,
            "sintomas": 9,
            "dias_evolucion": 25,
            "severidad": 9,
        },
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["prediccion"] == "ENFERMEDAD TERMINAL"

    estadisticas = cliente.get("/estadisticas").get_json()
    assert estadisticas["total_por_categoria"]["ENFERMEDAD TERMINAL"] == 1
    assert estadisticas["ultimas_5_predicciones"][-1]["prediccion"] == "ENFERMEDAD TERMINAL"
    assert estadisticas["fecha_ultima_prediccion"] is not None
