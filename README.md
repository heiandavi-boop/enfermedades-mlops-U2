# enfermedades-mlops-U2

Este repositorio contiene una solución académica de MLOps para simular un servicio de predicción médica. El objetivo es permitir que un médico ingrese variables clínicas básicas de un paciente y obtenga una clasificación del estado de enfermedad.

## Problema

En el campo médico existen grandes volúmenes de información para enfermedades comunes, pero pocas muestras para enfermedades huérfanas. En este ejercicio no se entrena un modelo real; se implementa una función simulada que representa el comportamiento de un modelo desplegado como servicio.

## Categorías de predicción

La solución retorna una de las siguientes categorías:

- NO ENFERMO
- ENFERMEDAD LEVE
- ENFERMEDAD AGUDA
- ENFERMEDAD CRÓNICA
- ENFERMEDAD TERMINAL

## Variables de entrada

El servicio recibe al menos cuatro valores clínicos:

- `temperatura`: temperatura corporal en grados Celsius.
- `sintomas`: número de síntomas identificados.
- `dias_evolucion`: número de días desde el inicio de los síntomas.
- `severidad`: calificación clínica de severidad entre 1 y 10.

## Nuevas funcionalidades de la unidad 2

La solución incluye dos nuevos requerimientos:

1. Nueva categoría de predicción: `ENFERMEDAD TERMINAL`.
2. Reporte de estadísticas de uso:
   - Número total de predicciones por categoría.
   - Últimas 5 predicciones realizadas.
   - Fecha de la última predicción.

Las estadísticas se almacenan en el archivo `predicciones.json`, generado automáticamente cuando se realizan predicciones.

## Estructura del repositorio

```text
.
├── app/
│   ├── __init__.py
│   ├── app.py
│   └── requirements.txt
├── tests/
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
└── README.md
```

## Ejecución local

Instalar dependencias:

```bash
pip install -r app/requirements.txt
```

Ejecutar la aplicación:

```bash
python app/app.py
```

Abrir en el navegador:

```text
http://localhost:5000
```

## Uso por API

Realizar una predicción:

```bash
curl -X POST http://localhost:5000/predecir \
  -H "Content-Type: application/json" \
  -d '{"temperatura":40.1,"sintomas":9,"dias_evolucion":25,"severidad":9}'
```

Consultar estadísticas:

```bash
curl http://localhost:5000/estadisticas
```

## Ejecución con Docker

Construir la imagen:

```bash
docker build -t mlops-enfermedades .
```

Ejecutar el contenedor:

```bash
docker run -p 5000:5000 mlops-enfermedades
```

Luego abrir:

```text
http://localhost:5000
```

## Pruebas unitarias

Ejecutar pruebas:

```bash
pytest -q
```

Las pruebas verifican que el modelo simulado pueda retornar las cinco categorías y que el endpoint de estadísticas registre correctamente una predicción.

## CI/CD con GitHub Actions

El repositorio incluye un workflow en `.github/workflows/ci-cd.yml` con dos eventos:

1. Pull request hacia `main`:
   - Comenta en el PR que el pipeline inició.
   - Instala dependencias.
   - Ejecuta pruebas unitarias.
   - Comenta en el PR que el pipeline terminó con éxito.

2. Commit o merge en `main`:
   - Ejecuta nuevamente las pruebas unitarias.
   - Construye la imagen Docker.
   - Publica la imagen en GitHub Container Registry.

## Flujo de ramas recomendado

- `main`: rama principal protegida.
- `solución-inicial`: primera versión con los archivos de la unidad 1, excepto el documento del pipeline general.
- `segunda-versión`: rama opcional para ajustes solicitados por el profesor.
- `nueva-prediccion-terminal`: rama para agregar `ENFERMEDAD TERMINAL`.
- `estadisticas-predicciones`: rama para agregar el reporte de estadísticas.
- `añadir-github-actions`: rama para agregar el pipeline de CI/CD.
