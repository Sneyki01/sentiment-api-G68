package com.sentiment.api.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record SentimentRequest(
        @NotBlank(message = "el campo text es obligatorio")
        @Size(min = 3, max = 2000, message = "El texto debe tener entre 3 y 2000 caracteres")
        String text
) {
}
