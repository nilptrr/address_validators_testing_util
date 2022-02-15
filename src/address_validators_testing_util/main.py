from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Process, Queue
import queue
import logging
from src.address_validators_testing_util.settings import LOGGING_CONFIG
from src.address_validators_testing_util.validator_tester import ValidatorTester


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("address_validators_testing_util")


def _run_validate(validation_testers, address_queues):
    '''
    Validates addresses from the blockchain network of the corresponding symbol.
    '''

    while True:
        for (validation_tester, address_queue) in zip(validation_testers, address_queues):
            try:
                address = address_queue.get()
                logger.debug(f'{validation_tester}: Get {address} from queue.')
                logger.debug(f'{validation_tester}: Queue size: {address_queue.qsize()}')

            except queue.Empty:
                logger.debug(f'{validation_tester}: The queue {address_queue} is empty.')

            else:
                logger.debug(f'{validation_tester}: Passing the {address} to the validator.')

                try:
                    validation_result = validation_tester.validate_address(address)
                    logger.debug(f'{validation_tester}: Validation result: {validation_result}')

                except Exception as e:
                    logger.critical(e, exc_info=True)       # unknown error

                else:
                    if not validation_result:
                        logger.critical(f'Unexpected validation result! Validation_result: {validation_result}. Address: {address}. Validation tester: {validation_tester}')


def _run_parse(validation_testers, address_queues):
    '''
    Parses addresses from the blockchain network of the corresponding symbol.
    '''

    def put_address_to_queue(validation_tester, address_queue):
        parsed_addresses = validation_tester.parse_address()
        for pa in parsed_addresses:
            address_queue.put(pa)

    with ThreadPoolExecutor(max_workers=len(validation_testers)) as pool:
        results = [pool.submit(put_address_to_queue, validation_tester, address_queue) for (validation_tester, address_queue) in zip(validation_testers, address_queues)]

        for future in as_completed(results):
            future.result()


def main():
    '''
    Tests the correctness of the validators of supported symbols by parsing addresses from the blockchain network and passing them to the appropriate validators.
    If an invalid address is returned, the validator potentially reports a false negative result.
    '''

    supported_symbols = ['bnb', 'btc']

    validation_testers = [ValidatorTester(symbol) for symbol in supported_symbols]
    logger.info(f'Run validation testers: {validation_testers}')

    # Queues are used for communication of the corresponding parsers and validators
    address_queues = [Queue() for _ in supported_symbols]
    logger.info('Run queues for validation testers.')

    # Validators run parallel to parsers
    validate_p = Process(target=_run_validate, args=(validation_testers, address_queues))
    validate_p.start()

    logger.info('Run child process for validators.')
    logger.info('Run validators.')

    logger.info('Run address parsers.')
    _run_parse(validation_testers, address_queues)

    validate_p.join()
    logger.info('Stop validators. Child process exiting.')
    logger.info('Main process exiting.')


if __name__ == '__main__':
    main()
