import java.math.BigDecimal;

public class Main {
    public static void main(String[] args) {
        Checkout checkoutCard = new Checkout(new CardPayment());
        Checkout checkoutMomo = new Checkout(new MoMoPayment());

        PaymentRequest requestCard = new PaymentRequest("123", new BigDecimal("100.00"), "USD");
        PaymentRequest requestMomo = new PaymentRequest("456", new BigDecimal("200"), "VND");

        checkoutCard.checkout(requestCard);
        checkoutMomo.checkout(requestMomo);
    }
}
