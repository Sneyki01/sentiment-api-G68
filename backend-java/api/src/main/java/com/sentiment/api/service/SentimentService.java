package com.sentiment.api.service;

import com.sentiment.api.dto.SentimentResponse;
import org.springframework.stereotype.Service;

@Service
public class SentimentService {

    /**
     Analiza el sentimiento del texto recibido
    Actualmente retorna una respuesta MOCK.
    TODO: Integrar llamada al servicio ML (Python) via HTTP.
    el servicio ML debe devolver {prevision, probabilidad}.
    */

    public SentimentResponse analyze(String text) {
        //MOCK: mientras data entrega el servicio ML
        return new SentimentResponse("Neutro", 0.50);
    }
}
