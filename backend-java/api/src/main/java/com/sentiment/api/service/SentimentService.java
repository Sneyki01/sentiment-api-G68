package com.sentiment.api.service;

import com.sentiment.api.client.MlClient;
import com.sentiment.api.dto.SentimentResponse;
import org.springframework.stereotype.Service;

@Service
public class SentimentService {

    private final MlClient mlClient;

    public SentimentService(MlClient mlClient) {
        this.mlClient = mlClient;
    }

    /**
     Analiza el sentimiento del texto recibido
    Actualmente retorna una respuesta MOCK.
    TODO: Integrar llamada al servicio ML (Python) via HTTP.
    el servicio ML debe devolver {prevision, probabilidad}.
    */

    public SentimentResponse analyze(String text) {
        return mlClient.predict(text);
    }
}
