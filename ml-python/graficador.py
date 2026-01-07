
import pandas as pd
import matplotlib.pyplot as plt
import os

def ver_grafica():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base_dir, "data", "processed", "resultados_lote.csv")
    if not os.path.exists(ruta): return print("❌ Corre primero el procesador")
    
    df = pd.read_csv(ruta)
    conteo = df['prevision'].value_counts()
    
    # Agregamos un 4to color (naranja) para soportar la categoría de Sarcasmo
    conteo.plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99', '#ffcc99'], title='Sentimiento G68')
    plt.show()

if __name__ == "__main__":
    ver_grafica()