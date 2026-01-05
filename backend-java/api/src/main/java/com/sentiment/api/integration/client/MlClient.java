package com.sentiment.api.integration.client;

import com.sentiment.api.errors.GlobalExceptionHandler.MlServiceException;
import com.sentiment.api.integration.client.dto.MlSentimentRequest;
import com.sentiment.api.integration.client.dto.MlSentimentResponse;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;


import java.util.Map;

@Component
public class MlClient {
    private final RestTemplate restTemplate;
    private final Environment env;

    public MlClient(RestTemplate restTemplate, Environment env) {
        this.restTemplate = restTemplate;
        this.env = env;
    }

    public MlSentimentResponse predict(String text) {
        String baseUrl = env.getProperty("ml.base-url");
        String path = env.getProperty("ml.predict-path");

        if (baseUrl == null || path == null){
            throw new MlServiceException("Configuración del servicio ML inválida");
        }
        String url = baseUrl + path;
        MlSentimentRequest request = new MlSentimentRequest(text);

        try {
            return restTemplate.postForObject(
                    url,
                    request,
                    MlSentimentResponse.class
            );
        } catch (ResourceAccessException ex) {
            throw new MlServiceException(
                    "El servicio de ML no está disponible por el momento."
            );
        }
    }
}
