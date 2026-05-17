# Guía de comandos Git para cumplir la entrega

> Reemplaza `enfermedades-mlops-U2` por el nombre real de tu repositorio si decides usar otro.

## 1. Crear repositorio local

```bash
git init
git branch -M main
```

Crear el repositorio en GitHub con el nombre:

```text
enfermedades-mlops-U2
```

Agregar el remoto:

```bash
git remote add origin https://github.com/TU_USUARIO/enfermedades-mlops-U2.git
```

## 2. Primer commit en main con README inicial

```bash
git add README.md
git commit -m "Agregar README inicial del repositorio"
git push -u origin main
```

Luego protege la rama `main` en GitHub:

```text
Settings -> Branches -> Add branch protection rule -> main
```

## 3. Rama solución-inicial

```bash
git checkout -b solución-inicial
```

Agregar los archivos de la solución inicial de la unidad 1, excepto el archivo del pipeline general.

```bash
git add app Dockerfile README.md
git commit -m "Agregar solución inicial dockerizada"
git push -u origin solución-inicial
```

Crear PR hacia `main`, sin reviewer, y hacer merge.

## 4. Rama para nueva categoría

```bash
git checkout main
git pull origin main
git checkout -b nueva-prediccion-terminal
```

Después de modificar `app/app.py`:

```bash
git add app/app.py README.md
git commit -m "Agregar categoria enfermedad terminal"
git push -u origin nueva-prediccion-terminal
```

Crear PR hacia `main` y hacer merge.

## 5. Rama para estadísticas

```bash
git checkout main
git pull origin main
git checkout -b estadisticas-predicciones
```

Después de agregar la funcionalidad de estadísticas:

```bash
git add app/app.py tests/test_app.py README.md
git commit -m "Agregar estadisticas de predicciones"
git push -u origin estadisticas-predicciones
```

Crear PR hacia `main` y hacer merge.

## 6. Rama añadir-github-actions

```bash
git checkout main
git pull origin main
git checkout -b añadir-github-actions
```

Agregar el workflow:

```bash
git add .github/workflows/ci-cd.yml tests/test_app.py app/requirements.txt README.md
git commit -m "Agregar pipeline de CI CD con GitHub Actions"
git push -u origin añadir-github-actions
```

Crear PR hacia `main` y hacer merge.

## 7. Agregar colaborador

En GitHub:

```text
Settings -> Collaborators & Teams -> Add people
```

Agregar:

```text
aviladavid28@gmail.com
```
