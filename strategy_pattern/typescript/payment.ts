export interface PaymentRequest {
  readonly customerId: string;
  readonly amountMinor: number;
  readonly currency: string;
}

export interface PaymentResponse {
  readonly transactionId: string;
  readonly success: boolean;
  readonly message: string;
}

/** (Strategy) - pay method to be implemented by concrete payment strategies. */
export interface PaymentStrategy {
  pay(request: PaymentRequest): PaymentResponse;
}



export function formatAmount(amountMinor: number, currency: string): string {
  const digits = new Intl.NumberFormat("en", { style: "currency", currency })
    .resolvedOptions().maximumFractionDigits ?? 2;
  return `${(amountMinor / 10 ** digits).toFixed(digits)} ${currency}`;
}
