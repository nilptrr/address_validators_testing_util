import time
import requests
import logging
from logging import config as logging_config
from src.address_validators_testing_util.settings import LOGGING_CONFIG


logging_config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("address_validators_testing_util")


def _get_latest_block():
    '''
    Gets the latest block from the blockchain explorer.
    '''
    try:
        url = 'https://blockchain.info/latestblock'
        res = requests.get(url, timeout=1)
        res.raise_for_status()

    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as errht:
        logger.exception(errht)
        latest_block = None             # the latest block was not recieved

    except requests.exceptions.RequestException as re:
        logger.exception(re)

    else:
        latest_block = res.json()
        return latest_block


def _get_address_in_transaction(transaction_id):
    '''
    Gets a list of addresses of the transaction.
    '''

    try:
        url = f'https://blockchain.info/rawtx/{transaction_id}'
        res = requests.get(url, timeout=1)
        res.raise_for_status()

    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as errht:
        logger.exception(errht)
        return None

    except requests.exceptions.RequestException as re:
        logger.exception(re)

    else:
        transaction = res.json()

        for transation_out in transaction['out']:
            if 'addr' in transation_out:
                address = transation_out['addr']

                yield address

        for transation_input in transaction['inputs']:
            if 'addr' in transation_input['prev_out']:
                address = transation_input['prev_out']['addr']

                yield address


def parse_address():
    '''
    Returns the address of the latest block from the blockchain network.
    '''
    timeout = 60 * 10                       # 10 min

    current_block = {
        'height': -1,
        'txIndexes': []
    }

    while True:
        latest_block = _get_latest_block()
        logger.debug('Trying get the latest block.')

        if latest_block is None:                                        # if the latest block was not received
            time.sleep(5)
            logger.warning('The latest block was not received. Waiting 5 mins.')
            continue

        if latest_block['height'] == current_block['height']:           # if the current block is not the latest
            time.sleep(timeout)                                         # waiting for a new block
            logger.info('The current block is not the latest. Waiting next block.')
            continue

        elif latest_block['height'] < current_block['height']:          # something went wrong with the block explorer API
            time.sleep(timeout)
            logger.error(f'Incorrect API response, {latest_block}')
            continue

        current_block = latest_block

        transaction_ids = current_block['txIndexes']                    # transaction list of the current block

        for transaction_id in transaction_ids:
            logger.debug(f'Get addresses in the {transaction_id} transaction.')
            address_in_transaction = _get_address_in_transaction(transaction_id)

            if address_in_transaction is None:                          # if the address was not recieved
                logger.error('The address was not recieved.')
                time.sleep(5)
                continue

            yield next(address_in_transaction)                          # yield the address from the current transaction
