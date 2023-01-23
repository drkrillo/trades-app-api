from celery import shared_task
from celery.utils.log import get_task_logger

import requests
from datetime import datetime, timedelta


SYMBOLS = ['ETH-USD', 'BTC-USD', 'AVAX-USD']
COINBASE_URL = 'https://api.pro.coinbase.com/'


logger = get_task_logger(__name__)


def get_data_from_api(symbol):
    """
    Generates API call to gather real-time symbol data.
    """

    data = requests.get(f'{COINBASE_URL}products/{symbol}/ticker',
        headers={"content-type": "application/json"})
    return data.json()

def get_data_from_api_lastmin(
    symbol,
    end_datetime=datetime.now(),
    granularity=60
):
    """
    Generates API call to gather symbol data from end datetime,
    x nummber of days window.
    Granularity defines if records are daily, monthly, hourly, etc.
    (default: seconds).
    """
    delta = timedelta(minutes=1)
    start_datetime = end_datetime - delta

    parameters = {
        'start': start_datetime.isoformat(),
        'end': end_datetime.isoformat(),
        'granularity': str(granularity),
    }

    data = requests.get(f'{COINBASE_URL}products/{symbol}/candles',
        params=parameters,
        headers={"content-type": "application/json"})
    return data.json()

@shared_task
def gather_intra_minute_data():
    for symbol in SYMBOLS:
        data = get_data_from_api(symbol)

        logger.info(f"symbol: {symbol} | {data['price']}")

@shared_task
def gather_minute_data():
    for symbol in SYMBOLS:
        data = get_data_from_api_lastmin(symbol)

        logger.info(f"CLOSED: {symbol} | {data[0][4]}")
