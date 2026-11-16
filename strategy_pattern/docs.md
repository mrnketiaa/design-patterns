# Strategy Pattern — Payment Example

The **Strategy pattern** lets you define a family of interchangeable algorithms, put each one in its own class, and pick which one to use at runtime. The code that *uses* the algorithm never needs to know which one it got.

This example uses payments: a `Checkout` needs to take a payment, but it shouldn't care whether the customer pays by **card** or by **mobile money (MoMo)**. Each payment method is a strategy, and the checkout is handed one when it's created.

The same example is implemented in three languages:

| Folder | Language |
|---|---|
| [`python/`](python/) | Python 3 |
| [`typescript/`](typescript/) | TypeScript |
| [`java/`](java/) | Java 21 |

## Structure

```
              ┌──────────────────────┐
              │  «interface»         │
 Checkout ───▶│  PaymentStrategy     │
 (context)    │  pay(request)        │
              └──────────▲───────────┘
                         │ implements
              ┌──────────┴───────────┐
              │                      │
         CardPayment            MoMoPayment
     (concrete strategy)    (concrete strategy)
```

| Role in the pattern | Class |
|---|---|
| Strategy (interface) | `PaymentStrategy` |
| Concrete strategies | `CardPayment`, `MoMoPayment` |
| Context | `Checkout` |
| Client | `main` |
| Data passed in / out | `PaymentRequest`, `PaymentResponse` |

## Components

### `PaymentRequest`

The input to every payment. It is immutable, so it can't be changed after it's created.

| Field | Type | Description |
|---|---|---|
| `customer_id` | string | Who is paying |
| `amount` | decimal | How much to charge |
| `currency` | string | ISO currency code, e.g. `USD`, `GHS`, `VND` |

### `PaymentResponse`

The result returned by every payment strategy. Also immutable.

| Field | Type | Description |
|---|---|---|
| `transaction_id` | string | ID of the transaction from the payment provider |
| `success` | bool | Whether the payment went through |
| `message` | string | Human-readable outcome, e.g. a failure reason |

### `PaymentStrategy`

The strategy interface. It declares a single method that every payment method must implement:

```python
def pay(self, request: PaymentRequest) -> PaymentResponse
```

`Checkout` depends only on this interface, never on a concrete payment class.

### `Checkout`

The **context**. It receives a `PaymentStrategy` in its constructor and uses it to process the order:

1. Validates the order.
2. Calls `pay()` on whichever strategy it was given.
3. Prints whether the payment succeeded or failed.
4. Returns the `PaymentResponse`.

Because `Checkout` only talks to the interface, the same checkout code works for every payment method.

### `CardPayment`

A concrete strategy that processes a card payment. In this example it prints what it's doing and returns a successful response with transaction ID `card123`.

### `MoMoPayment`

A concrete strategy that processes a mobile money payment. It returns a successful response with transaction ID `momo123`.


### `main`

The **client**. It decides which strategy to use and hands it to a `Checkout`:

```python
checkout_card = Checkout(CardPayment())
checkout_momo = Checkout(MoMoPaymnent())

checkout_card.checkout(PaymentRequest(customer_id="123", amount=Decimal("100.0"), currency="USD"))
checkout_momo.checkout(PaymentRequest(customer_id="456", amount=Decimal("200.0"), currency="VND"))
```

## Running the examples

All three versions print the same flow (Python formats the card amount as `100` rather than `100.00`):

```
Validating Order...
Processing card payment for customer 123 with amount 100.00 USD.
Payment successful: Transaction ID card123
Validating Order...
Processing MoMo payment for customer 456 with amount 200 VND.
Payment successful: Transaction ID momo123
```

**Python**: run from the `design-patterns` folder, because the imports start with `strategy_pattern.python`:

```
python -m strategy_pattern.python.main
```

**TypeScript**: run from `strategy_pattern/typescript`:

```
npx tsx main.ts
```

**Java**: run from `strategy_pattern/java`:

```
javac -d out *.java
java -cp out Main
```

## Adding a new payment method

This is where the pattern pays off. To support, say, bank transfer:

1. Create a `BankTransferPayment` class that implements `PaymentStrategy` and its `pay()` method.
2. Pass it to a checkout: `Checkout(BankTransferPayment())`.

You don't need to change `Checkout`, `CardPayment` or `MoMoPayment`. New behaviour is added by writing new code, not by editing working code (the *open/closed principle*).

Without the pattern, `Checkout` would end up with a growing `if method == "card" ... elif method == "momo" ...` chain that has to be edited for every new payment method.

## Language differences

| Concept | Python | TypeScript | Java |
|---|---|---|---|
| Strategy interface | `ABC` + `@abstractmethod` | `interface` | `interface` |
| Immutable data | `@dataclass(frozen=True)` | `interface` with `readonly` fields | `record` |
| Money | `Decimal` | `number` in minor units (`amountMinor`, e.g. `10000` = 100.00 USD) | `BigDecimal` |
| Field naming | `snake_case` | `camelCase` | `camelCase` |

**Why not use a float for money?** Floating-point numbers can't represent most decimal fractions exactly (`0.1 + 0.2` gives `0.30000000000000004`), so amounts drift. Build decimals from strings, too: `Decimal("100.0")`, not `Decimal(100.0)`, so no float error is copied in.
