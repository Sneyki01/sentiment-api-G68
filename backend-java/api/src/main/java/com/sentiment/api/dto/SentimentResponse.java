package com.sentiment.api.dto;


public record SentimentResponse(
        String prevision,
        Double probabilidad
) {
}
