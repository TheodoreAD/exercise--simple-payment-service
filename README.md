# Simple Payment Service

## Usage

To get up and running in "production" (using stock dev server):

```shell script
make install
make start
```

Replace the stock dev server with gunicorn for real production.

## Configuration

There is user-accessible configuration at this moment.
Good configuration requires loading dev / prod config files dynamically
based on environment variables.

## Development

Create a virtual environment. Always.

To get up and running in reload on code changes mode with full logging output:

```shell script
make install-dev
make start-dev
```

For the rest below, make sure you've done `make install-dev`.

To run formatter and show report only, useful for pipelines:

```shell script
make format-check
```

To run formatter and apply changes, useful before committing:

```shell script
make format
```

To run linter:

```shell script
make lint
```

To run tests:

```shell script
make test
```

## API

### `/ProcessPayment`

Methods: `POST`

Content-Type: application/json

Body:

- CreditCardNumber: Visa or Mastercard credit card number
- CardHolder: ASCII letters and spaces, between 2 and 40 characters
- ExpirationDate: mm-yyyy formatted date
- SecurityCode: three digit number
- Amount: positive decimal
