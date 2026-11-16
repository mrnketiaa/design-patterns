public record PaymentResponse(
    String transactionId, 
    boolean success, 
    String message) {}
