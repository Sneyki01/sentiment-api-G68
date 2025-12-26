package com.sentiment.api.client;

import com.sentiment.api.dto.SentimentResponse;
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

    public SentimentResponse predict(String text) {
        String url = env.getProperty("ml.base-url")
                + env.getProperty("ml.predict-path");
        Map<String, String> request = Map.of("text", text);

        try {
            return restTemplate.postForObject(
                    url,
                    request,
                    SentimentResponse.class
            );
        } catch (ResourceAccessException ex) {
            throw new MlServiceException(
                    "El servicio de ML no está disponible por el momento."
            );
        }
    }
}
