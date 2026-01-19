# 🛠️ Guía para la Revisión de la Reestructuración de `ml-python`

¡Hola equipo! He reestructurado la carpeta `ml-python` para que esté más organizada y siga estándares profesionales. Para que puedan ver estos cambios en sus computadoras y darme el visto bueno, sigan estos pasos:

---

## 0. Prerrequisitos (Preparar la base)
Antes de usar el parche, asegúrense de estar en la rama correcta y con los últimos cambios comunes:

1.  **Cambiarse a la rama de la entrega:**
    ```bash
    git checkout feature/entrega-modelo-integral
    ```
2.  **Asegurarse de que esté actualizada:**
    ```bash
    git pull origin feature/entrega-modelo-integral
    ```

---

## 1. Aplicar el Parche
Ahora aplicaremos la reestructuración:

1.  **Descargar el archivo:** `mi_cambio_ml.patch`.
2.  **Ubicar el archivo:** Péguenlo en la carpeta principal del proyecto (raíz).
3.  **Ejecutar el comando:** Abran la terminal en esa carpeta y escriban:
    ```bash
    git apply mi_cambio_ml.patch
    ```

---

## 🏁 ¿Qué va a pasar?
Su carpeta `ml-python` se transformará para ser igual a la mía. Los archivos se moverán a sus nuevas ubicaciones (`src/engine`, `data`, `scripts`, etc.) y todo quedará listo para su revisión técnica.

> [!TIP]
> **¿Quieres deshacer los cambios?**
> Si después de revisarlo quieres volver al estado original de la rama, solo tienes que escribir:
> ```bash
> git checkout ml-python/
> ```

---

### ¿Por qué este método?
Este parche solo contiene las instrucciones de movimiento y edición de texto de la lógica de IA. Es ligero, seguro y no ensucia el historial de Git de nadie hasta que todos estemos de acuerdo con el cambio.
