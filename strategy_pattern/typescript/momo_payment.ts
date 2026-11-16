import { formatAmount, type PaymentRequest, type PaymentResponse, type PaymentStrategy } from "./payment";

export class MoMoPayment implements PaymentStrategy {
  pay(request: PaymentRequest): PaymentResponse {
    console.log(
      `Processing MoMo payment for customer ${request.customerId} with amount ${formatAmount(request.amountMinor, request.currency)}.`,
    );

    return { transactionId: "momo123", success: true, message: "Payment successful via MoMo." };
  }
}
