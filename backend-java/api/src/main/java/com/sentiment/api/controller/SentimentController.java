package com.sentiment.api.controller;


import com.sentiment.api.service.SentimentService;
import com.sentiment.api.dto.SentimentRequest;
import com.sentiment.api.dto.SentimentResponse;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SentimentController    {

    private final SentimentService sentimentService;

    public SentimentController(SentimentService sentimentService) {
        this.sentimentService = sentimentService;
    }

    /**
     Endpoint público para análisis de sentimiento.
     Valida input y delega la lógica al servicio.
     */
    @PostMapping("/sentiment")
    public SentimentResponse sentiment(@Valid @RequestBody SentimentRequest request) {
        return sentimentService.analyze(request.text());
    }
}
