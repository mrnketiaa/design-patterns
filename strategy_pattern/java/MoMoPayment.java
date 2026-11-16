public class MoMoPayment implements PaymentStrategy {
    @Override
    public PaymentResponse pay(PaymentRequest request) {
        System.out.printf("Processing MoMo payment for customer %s with amount %s %s.%n",
                request.customerId(), request.amount(), request.currency());

        return new PaymentResponse("momo123", true, "Payment successful via MoMo.");
    }
}
