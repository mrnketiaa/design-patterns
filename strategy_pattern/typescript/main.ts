import { CardPayment } from "./card_payment";
import { Checkout } from "./checkout";
import { MoMoPayment } from "./momo_payment";
import type { PaymentRequest } from "./payment";

const checkoutCard = new Checkout(new CardPayment());
const checkoutMomo = new Checkout(new MoMoPayment());

const requestCard: PaymentRequest = { customerId: "123", amountMinor: 10000, currency: "USD" }; // 100.00 USD
const requestMomo: PaymentRequest = { customerId: "456", amountMinor: 200, currency: "VND" }; // 200 VND (no minor unit)

checkoutCard.checkout(requestCard);
checkoutMomo.checkout(requestMomo);
