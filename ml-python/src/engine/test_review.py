import json
import math
import os
from nltk.stem import SnowballStemmer

class SentimentLabG68:
    def __init__(self, lexicon_path, alpha=0.15):
        # 1. El "Cerebro" de raíces
        self.stemmer = SnowballStemmer('spanish')
        self.alpha = alpha
        
        # 2. Diccionarios de contexto
        self.negations = {'no', 'sin', 'nunca', 'jamas', 'nada', 'tampoco'}
        self.intensifiers = {'muy', 'super', 'bastante', 'extremadamente', 'totalmente'}
        self.sustantivos = {'comida', 'habitacion', 'atencion', 'servicio', 'hotel', 'precio'}
        
        # 3. Cargar el JSON parchado y convertir sus llaves a raíces
        self.lexicon = self._load_and_stem_lexicon(lexicon_path)

    def _load_and_stem_lexicon(self, path):
        if not os.path.exists(path):
            print("❌ Error: Lexicón no encontrado.")
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Convertimos las llaves a raíces para que coincidan con el input del usuario
            return {self.stemmer.stem(k): v for k, v in data.items()}

    def analyze(self, text):
        # Limpieza y tokenización
        tokens = text.lower().replace(",", "").replace(".", "").split()
        score_acumulado = 0
        
        print(f"\n{'TOKEN':<12} | {'RAÍZ':<10} | {'PESO FINAL':<12} | {'REGLA'}")
        print("-" * 75)

        for i, word in enumerate(tokens):
            root = self.stemmer.stem(word)
            # Buscamos en el lexicón por raíz
            base = self.lexicon.get(root, [0.0])[0]
            
            # Neutralizar sustantivos (para que no sesguen el resultado)
            if word in self.sustantivos or root in [self.stemmer.stem(s) for s in self.sustantivos]:
                base = 0.0
                regla = "Sustantivo"
            else:
                regla = "Unigrama"

            # Aplicar Bigramas (Negación o Intensidad)
            modifier = 1.0
            if i > 0:
                if tokens[i-1] in self.negations:
                    modifier = -1.2
                    regla = f"NEG ({tokens[i-1]})"
                elif tokens[i-1] in self.intensifiers:
                    modifier = 1.6
                    regla = f"INT ({tokens[i-1]})"

            # TU MÉTRICA DE BALANCE (Contrato G68)
            intermedio = base * modifier
            if intermedio > 0:
                peso_final = intermedio * 0.7  # Castigo positivos
                regla += " | Pos x0.7"
            elif intermedio < 0:
                peso_final = intermedio * 1.4  # Amplificación negativos
                regla += " | Neg x1.4"
            else:
                peso_final = 0.0

            score_acumulado += peso_final
            if peso_final != 0 or word in self.sustantivos:
                print(f"{word:<12} | {root:<10} | {peso_final:<12.2f} | {regla}")

        # Score Final con el Valor ALFA
        total = score_acumulado + self.alpha
        
        # Probabilidad Logística
        prob = 1 / (1 + math.exp(-abs(total) * 1.8))
        prevision = "POSITIVO" if total > 0.05 else "NEGATIVO" if total < -0.05 else "NEUTRAL"

        print("-" * 75)
        print(f"SCORE FINAL: {total:.2f} (Suma: {score_acumulado:.2f} + Alfa: {self.alpha})")
        print(f"PREVISIBILIDAD: {prevision} | PROBABILIDAD: {prob:.2%}")

if __name__ == "__main__":
    path = "data/lexicon/lexicon_final_optimizado.json"
    engine = SentimentLabG68(path)
    
    print("--- MOTOR DE SENTIMIENTO G68 ACTIVO ---")
    while True:
        review = input("\n📝 Reseña: ")
        if review.lower() == 'salir': break
        engine.analyze(review)