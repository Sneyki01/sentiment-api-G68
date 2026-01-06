import json
import pandas as pd
import os

class SentimentEngine:
    def __init__(self, lexicon_path):
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            self.lexicon = json.load(f)
        # Reglas del Informe Ejecutivo Final
        self.negations = {'no', 'sin', 'nunca', 'jamas', 'tampoco', 'ni', 'nada'}
        self.intensifiers = {'muy', 'sumamente', 'totalmente', 'extremadamente', 'super', 'bastante'}

    def analyze(self, text):
        if not isinstance(text, str): return 0.0, ""
        tokens = text.split()
        score = 0
        details = []
        
        for i, word in enumerate(tokens):
            if word in self.lexicon:
                # El lexicon tiene: [score, categoria, importancia, subcategoria, area]
                base_score = self.lexicon[word][0]
                area = self.lexicon[word][4]
                modifier = 1.0
                
                # REGLA: Bigrama de Negación
                if i > 0 and tokens[i-1] in self.negations:
                    modifier = -0.8
                # REGLA: Bigrama de Intensidad
                elif i > 0 and tokens[i-1] in self.intensifiers:
                    modifier = 1.5
                
                word_score = base_score * modifier
                
                # DETECCIÓN DE NEGATIVAS FUERTES (Tu requerimiento)
                if word_score < 0:
                    word_score *= 2.0  # Amplificamos la queja
                elif word_score > 0:
                    word_score *= 0.5  # Minimizamos el elogio
                
                score += word_score
                details.append(f"{word}({area})")
        
        return round(score, 2), ", ".join(details)

def run_engine():
    input_file = "data/processed/Big_AHR_cleaned.csv"
    lexicon_file = "data/lexicon/lexicon_final_optimizado.json"
    output_file = "data/processed/Big_AHR_with_scores.csv"

    if not os.path.exists(input_file) or not os.path.exists(lexicon_file):
        print("❌ Error: Verifica que los archivos existan en data/processed y data/lexicon")
        return

    print("🚀 Ejecutando Motor de Sentimiento...")
    engine = SentimentEngine(lexicon_file)
    df = pd.read_csv(input_file)
    
    # Aplicamos el análisis a toda la columna limpia
    results = df['review_text_clean'].apply(lambda x: engine.analyze(x))
    df['sentiment_score'] = [r[0] for r in results]
    df['areas_detectadas'] = [r[1] for r in results]
    
    df.to_csv(output_file, index=False)
    print(f"✅ Proceso terminado. Archivo generado: {output_file}")

if __name__ == "__main__":
    run_engine()