public class CardPayment implements PaymentStrategy {
    @Override
    public PaymentResponse pay(PaymentRequest request) {
        System.out.printf("Processing card payment for customer %s with amount %s %s.%n",
                request.customerId(), request.amount(), request.currency());

        return new PaymentResponse("card123", true, "Payment successful via Card.");
    }
}
