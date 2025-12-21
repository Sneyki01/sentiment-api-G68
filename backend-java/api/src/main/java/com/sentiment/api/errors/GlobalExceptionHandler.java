package com.sentiment.api.errors;

import com.sentiment.api.dto.ErrorResponse;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    //Error texto vacio
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationErrors(MethodArgumentNotValidException ex) {

        String message = ex.getBindingResult()
                .getFieldErrors()
                .stream()
                .findFirst()
                .map(err -> err.getDefaultMessage())
                .orElse("Solicitud invalida");

        return ResponseEntity.badRequest().body(new ErrorResponse(message));
    }

    //JSON mal formado
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleWrongJsonFormat(HttpMessageNotReadableException ex) {
        return ResponseEntity.badRequest().body(new ErrorResponse("JSON invalido"));
    }

    // TODO [Backend-Health]: Agregar manejo de excepción para ML no disponible (503)

}
