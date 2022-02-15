# Address Validators Testing Util
Tests the correctness of the [crypto address validators](https://github.com/null-po1nter/crypto-address-validator) of supported symbols by parsing addresses from the blockchain network and passing them to the appropriate validators.
If an invalid address is returned, the validator potentially reports a false negative result.

## Supported symbols
| Currency      | Symbol | Mainnet |
|:-------------:| ------ | ------- |
| Bitcoin       | BTC    | +       |
| Binance Coin  | BNB    | +       |


## Usage
```
poetry install
poetry run validation_tests
```

## License
The Unlicense. See the LICENSE file for details.
