import requests
import time
import logging
from src.address_validators_testing_util.settings import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("address_validators_testing_util")


def __get_latest_block_height():
    '''
    Gets the height of latest block from the blockchain explorer.
    '''

    try:
        url = 'https://dex.binance.org/api/v1/node-info'
        res = requests.get(url)
        res.raise_for_status()

    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as errht:
        logger.exception(errht)
        latest_block = None             # the latest block was not recieved

    except requests.exceptions.RequestException as re:
        logger.exception(re)

    else:
        latest_block = res.json()
        return latest_block['sync_info']['latest_block_height']


def __get_address_in_block(block_height):
    '''
    Gets a list of addresses in the block.
    '''

    try:
        url = f"https://dex.binance.org/api/v2/transactions-in-block/{block_height}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()

    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as errht:
        logger.exception(errht)
        return None

    except requests.exceptions.RequestException as re:
        logger.exception(re)

    else:
        transactions = res.json()
        for transaction in transactions['tx']:
            yield transaction['fromAddr']
            yield transaction['toAddr']


def parse_address():
    '''
    Returns the address of the latest block from the blockchain network.
    '''

    timeout = 90        # 90 sec

    current_block_height = -1

    while True:
        latest_block_height = __get_latest_block_height()
        logger.debug('Trying get the latest block.')

        if latest_block_height is None or latest_block_height == current_block_height:          # if the latest block was not received
            logger.warning('The latest block was not received.')
            time.sleep(timeout)
            continue

        elif latest_block_height < current_block_height:            # something went wrong with the block explorer API
            logger.error(f'Incorrect API response, {latest_block_height}')
            time.sleep(timeout)
            continue

        current_block_height = latest_block_height

        logger.debug(f'Get addresses in the {current_block_height} block height.')
        addresses_in_block = __get_address_in_block(current_block_height)

        for address in addresses_in_block:
            if address is None:
                continue
            else:
                yield address
