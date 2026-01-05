package com.sentiment.api.service;

import com.sentiment.api.integration.client.MlClient;
import com.sentiment.api.dto.SentimentResponse;
import com.sentiment.api.integration.client.dto.MlSentimentResponse;
import org.springframework.stereotype.Service;

@Service
public class SentimentService {

    private final MlClient mlClient;

    public SentimentService(MlClient mlClient) {
        this.mlClient = mlClient;
    }

    public SentimentResponse analyze(String text) {
        MlSentimentResponse mlResponse = mlClient.predict(text);
        return new SentimentResponse(
                mlResponse.prevision(),
                mlResponse.probabilidad()
        );
    }
}
