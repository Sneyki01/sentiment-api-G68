# INSTRUCCIONES PARA EJECUTAR EL NOTEBOOK 03_test_inferencia.ipynb

## Si el notebook da resultados diferentes al script:

### Opción 1: Reiniciar el Kernel
1. Abre el notebook en Jupyter
2. Ve al menú: Kernel → Restart & Run All
3. Espera a que todas las celdas se ejecuten

### Opción 2: Verificar el entorno Python
Ejecuta esta celda en el notebook para verificar qué Python está usando:

```python
import sys
print(f"Python: {sys.executable}")
print(f"Versión: {sys.version}")
print(f"Rutas: {sys.path[:3]}")
```

### Opción 3: Forzar recarga de módulos
Agrega esto al inicio de la primera celda del notebook:

```python
import sys
import importlib

# Limpiar módulos cargados
if 'motor_hibrido' in sys.modules:
    importlib.reload(sys.modules['motor_hibrido'])
if 'config_g68' in sys.modules:
    importlib.reload(sys.modules['config_g68'])
```

### Opción 4: Usar el script de verificación
Si el notebook sigue dando problemas, usa el script:
```bash
python verificar_arreglos.py
```

Este script garantiza usar siempre el código más reciente.
