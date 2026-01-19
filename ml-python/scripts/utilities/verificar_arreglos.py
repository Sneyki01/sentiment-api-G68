import sys
import os

# Rutas
sys.path.append(os.path.join(os.getcwd(), 'ml-python', 'src', 'app'))
sys.path.append(os.path.join(os.getcwd(), 'ml-python', 'src'))

from motor_hibrido import enriquecer_respuesta

tests = [
    ("Excelente, el baño oliendo a cloaca y no hay agua caliente. Un aplauso.", "Positivo", 0.5),
    ("La cama es una nube, volvería mañana mismo.", "Negativo", 0.14),
    ("El hotel es normal, ni bueno ni malo.", "Negativo", 0.4)
]

for texto, pred, prob in tests:
    res = enriquecer_respuesta(texto, pred, prob)
    print(f"\nRESULTADO: {res['previsión']} ({res['probabilidad']})")
