# Git Workflow del proyecto SentimentAPI (Guia practica)

Este documento define **como vamos a trabajar con git** en el proyecto para evitar:

- conflictos eternos
- ramas zombie
- PRs imposibles de revisar
- el clasico "En mi maquina si funciona"

> Regla base: **Nadie trabaja directo en 'dev' o en 'main'**

**Recuerda**: > Git no te odia. Solo es estricto. Cuando entiendes el flujo, deja de pelear contigo.

---

## 1) Estructura de ramas

### Ramas principales

- 'main': **Produccion** (solo entra por PR)
- 'dev': **integracion**. Aqui se juntan las features y fixes. (Solo entra por PR)

### Ramas de trabajo (Por persona o tarea)

crear **SIEMPRE** desde 'dev':

- feature/(descripcion)

```yaml
Ejemplo: 

Feature/BackendAPI
Feature/DataScienceNotebook
Feature/DevOps
```

---

## 2) Rutina diara (Cada que abres el editor)

### A) Sincroniza tu repo local con el remoto
```yaml
git fetch origin
```

### B) Si vas a crear una nueva rama
```yaml
git checkout dev
git pull origin dev
git checkout -b feature/(nombre de la nueva rama)
```

### C) Si ya tienes una rama en progreso (Minimo 1 vez al dia)

Actualiza tu rama trayendo cambios de 'dev' con:

```yaml
git checkout feature/(TuRama)
git fetch origin 
git merge origin/dev
```

---

## 3) Commits

**Reglas**

- Commits pequeños pero con intencion
- no usar mensajes tipo: ```fix, cambio, ya quedo, aaaa, final```

**Formato sugerido**

- ```feat: ```
- ```fix:```
- ```test:```
- ```refactor:```
- ```chore:```

**Ejemplos**

```yaml
git commit -m "feat Agrega validacion de texto"
git commit -m "fix corrige error en request largo"
git commit -m "test agrega casos para login"
```

---

## 4) PUSH (sube tu trabajo)

Sube tu rama cuando:

- Ya tengas algo estable
- Necesitas respaldar
- Necesitas compartir avances

```yaml
git push -u origin feature/(TuRama)
```

---

## 5) Antes de abrir PR (Obligatorio)

### 1) Actualiza tu rama con lo ultimo de ```dev```

```yaml
git checkout feature/TuRama
git fetch origin
git merge origin/dev
```

### 2) Push final

```yaml
git push
```

---

## 6) Pull request (PR)

### Reglas

- Todo entra a ```dev``` por PR
- PRs pequeños: idealmente menos de 100 lineas netas.
- Describe que cambiaste y como probarlo.

### Checklist Minimo para el PR 

-[ ] Rama actualizada con ```dev``` (merge aplicado)

-[ ] Compila / Build OK

-[ ] Test OK (si existen)

-[ ] Describe como probar

-[ ] Riesgos conocidos (si aplica)

---

## 7) Conflictos (Que hacer si Git se pone intenso)

Si al hacer ```merge``` aparecen conflictos: 

1. Abre los archivos
2. Verifica donde aparece el conflicto
3. Valida con el colaborador y resuelvan Manual
4. Marcar como resuelto
5. Commit del merge
```yaml
git status
git add .
git commit
```
**Regla importante:** No resuelvas conflictos "a ojo" sin probar
o validar con colaborador.

---

## 8) Que **NO** hacer (cosas que cuasan incendios)

- Commit directo a ```dev``` o ```main```
- PR gigante de 3,000 lineas
- No actualizar tu rama por dias y luego sorprenderse por conflictos
- ```rebase``` de una rama compartida sin avisar
- subir codigo roto "porque luego lo arreglo"

---

## 9) Flujo rapido (Resumen)

### Nueva tarea (Crear rama)
```yaml
git fetch origin
git checkout dev
git pull origin dev
git checkout -b feature/(nombre de la rama nueva)
```

### Dia a Dia en tu rama
```yaml
git fetch origin
git checkout feature/TuRama
git merge origin/dev

#Trabajas lo que necesitas en tu rama

git add .
git commit -m "feat ..."
git push
```

### Antes de PR
```yaml
git fetch origin
git checkout feature/TuRama
git merge origin/dev
git push
```

## 10) Regla de oro final

Tu rama debe estar al dia con ```dev``` antes de pedir entrar a ```dev```

**RECUERDA**: Aprender Git es como aprender a manejar estándar: al inicio se te apaga, luego ya ni lo piensas.

---

## Nota final

Este flujo no existe para complicarte la vida, existe para que el equipo pueda avanzar sin pisarse los pies.

Si algo no queda claro, se pregunta.  
Si algo se rompe, se arregla.  
Este proyecto prioriza procesos claros para que el talento crezca sin miedo.

— Equipo 68 SentimentAPI