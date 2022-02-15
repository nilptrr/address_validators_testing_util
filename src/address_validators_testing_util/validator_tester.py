from src.address_validators_testing_util.parsers import btc_address_parser, bnb_address_parser
from crypto_address_validator.validators import default_validator, bnb_validator


class ValidatorTester:
    '''
    Creates a validation tester object with the passed symbol.
    '''

    def __init__(self, symbol):
        '''
        Initialize self. The symbol parameter defines the cryptocurrency symbol.
        '''
        self.symbol = symbol

    def __repr__(self) -> str:
        return f'{self.symbol.upper()} validation tester'

    def parse_address(self):
        '''
        Parses addresses from the blockchain network.
        '''

        supported_parsers = {
            'btc': btc_address_parser,
            'bnb': bnb_address_parser
        }

        parsed_addresses = supported_parsers[self.symbol].parse_address()

        for pa in parsed_addresses:
            yield pa

    def validate_address(self, address):
        '''
        Returns True if the address is successfully validated, otherwise False.
        '''

        supported_validators = {
            'btc': default_validator,
            'bnb': bnb_validator
        }

        try:
            validation_result = supported_validators[self.symbol].is_valid_address(address)

        except Exception:
            raise

        else:
            return validation_result
