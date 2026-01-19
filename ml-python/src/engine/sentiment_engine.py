import joblib
import os
import numpy as np

class SentimentEngine:
    """
    Clase encargada de la interacción directa con los modelos de Machine Learning (Sklearn).
    Maneja la carga, predicción y extracción de importancia de características.
    """
    def __init__(self, model_dir):
        self.model_path = os.path.join(model_dir, "sentiment_model.pkl")
        self.vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.pkl")
        
        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)
        
        # Mapeo de índices para consistencia con clases del modelo (0, 1, 3)
        self.target_names = {0: "Negativo", 1: "Positivo", 3: "Neutro"}

    def predict_raw(self, text):
        """Devuelve la clase numérica y la probabilidad máxima del modelo."""
        vec = self.vectorizer.transform([text])
        prediction = self.model.predict(vec)[0]
        probabilities = self.model.predict_proba(vec)[0]
        
        # Obtenemos la probabilidad de la clase predicha para reportar confianza
        cls_list = list(self.model.classes_)
        actual_idx = cls_list.index(prediction)
        confidence = probabilities[actual_idx]
        
        return prediction, confidence

    def get_top_features_from_model(self, text, top_n=5):
        """
        Extrae las palabras del texto que más influyeron en la decisión del modelo 
        basándose en los coeficientes (coef_).
        """
        try:
            vec = self.vectorizer.transform([text])
            pred_class = self.model.predict(vec)[0]
            
            # Navegamos por el CalibratedClassifierCV si es necesario
            base_model = self.model
            if hasattr(self.model, 'calibrated_classifiers_'):
                base_model = self.model.calibrated_classifiers_[0].estimator
            
            if not hasattr(base_model, 'coef_'):
                return []

            # Mapeo de clase predicha al índice de coeficientes
            cls_list = list(self.model.classes_)
            class_idx = cls_list.index(pred_class)
            
            # Coeficientes para la clase específica
            coef = base_model.coef_[class_idx]
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Identificamos qué features del texto están activas
            vec_array = vec.toarray()[0]
            active_indices = np.where(vec_array > 0)[0]
            
            # Creamos lista de (feature, importancia)
            impacts = []
            for idx in active_indices:
                impacts.append((feature_names[idx], coef[idx] * vec_array[idx]))
            
            # Ordenamos por magnitud de impacto
            impacts.sort(key=lambda x: abs(x[1]), reverse=True)
            return impacts[:top_n]
            
        except Exception as e:
            # Fallback silencioso para no romper el flujo principal
            return []
