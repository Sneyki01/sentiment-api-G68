import pandas as pd

def show_clean_results():
    try:
        df = pd.read_csv("data/processed/Big_AHR_with_scores.csv")
        # Solo nos interesan las quejas reales (Score menor a -5)
        findings = df[df['sentiment_score'] < -5].sort_values(by='sentiment_score').head(10)

        print("\n" + "RAZÓN DEL ALERTA".ljust(60) + " | " + "SCORE".ljust(10) + " | " + "ÁREAS AFECTADAS")
        print("-" * 110)

        for _, row in findings.iterrows():
            # 1. Limpiamos el texto para que sea legible
            text = row['review_text_clean'][:57] + "..."
            
            # 2. Score formateado
            score = f"{row['sentiment_score']:.1f}"
            
            # 3. Limpiamos las áreas (Quitamos los paréntesis y Modificadores)
            raw_areas = str(row['areas_detectadas']).split(", ")
            # Solo dejamos nombres de áreas únicos y quitamos "Modificadores" que no sirve al gerente
            clean_areas = set([a.split("(")[1].replace(")", "") for a in raw_areas if "(" in a and "Modificadores" not in a])
            areas_str = ", ".join(list(clean_areas)[:3]) # Máximo 3 áreas para no saturar

            print(f"{text.ljust(60)} | {score.ljust(10)} | {areas_str}")
        
        print("-" * 110)
        print(f"RESUMEN: Se encontraron {len(df[df['sentiment_score'] < 0])} quejas que requieren atención inmediata.")

    except Exception as e:
        print(f"Error al leer resultados: {e}")

if __name__ == "__main__":
    show_clean_results()