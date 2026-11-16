public class Checkout {
    private final PaymentStrategy paymentStrategy;

    public Checkout(PaymentStrategy paymentStrategy) {
        this.paymentStrategy = paymentStrategy;
    }

    public PaymentResponse checkout(PaymentRequest request) {
        System.out.println("Validating Order...");

        PaymentResponse result = paymentStrategy.pay(request);

        if (result.success()) {
            System.out.println("Payment successful: Transaction ID " + result.transactionId());
        } else {
            System.out.println("Payment failed: " + result.message());
        }

        return result;
    }
}
