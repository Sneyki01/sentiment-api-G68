import pandas as pd
import re
import os

def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^a-záéíóúüñ0-9.,!?\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def run_etl():
    input_file = "data/raw/Big_AHR.csv"
    output_file = "data/processed/Big_AHR_cleaned.csv"
    
    if not os.path.exists(input_file):
        print(f"Error: No se encuentra {input_file}")
        return

    print("Procesando limpieza...")
    df = pd.read_csv(input_file)
    df['review_text_clean'] = df['review_text'].apply(clean_text)
    
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Dataset limpio guardado en: {output_file}")

if __name__ == "__main__":
    run_etl()
