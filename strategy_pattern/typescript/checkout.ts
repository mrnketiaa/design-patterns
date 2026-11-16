import type { PaymentRequest, PaymentResponse, PaymentStrategy } from "./payment";

export class Checkout {
  constructor(private readonly paymentStrategy: PaymentStrategy) {}

  checkout(request: PaymentRequest): PaymentResponse {
    console.log("Validating Order...");

    const result = this.paymentStrategy.pay(request);

    if (result.success) {
      console.log(`Payment successful: Transaction ID ${result.transactionId}`);
    } else {
      console.log(`Payment failed: ${result.message}`);
    }

    return result;
  }
}
