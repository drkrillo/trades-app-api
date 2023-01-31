from celery import shared_task
from celery.utils.log import get_task_logger

import requests
from datetime import datetime, timedelta


SYMBOLS = ['ETH-USD', 'BTC-USD', 'AVAX-USD']
COINBASE_URL = 'https://api.pro.coinbase.com/'


logger = get_task_logger(__name__)


def get_data_from_api(symbols=SYMBOLS):
    """
    Generates API call to gather real-time symbol data.
    """
    for symbol in symbols:
        data = requests.get(
            f'{COINBASE_URL}products/{symbol}/ticker',
            headers={"content-type": "application/json"}
        )
        logger.info(f"symbol: {symbol} | {data.json()}")

        return data.json(), data.status_code


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

    data = requests.get(
        f'{COINBASE_URL}products/{symbol}/candles',
        params=parameters,
        headers={"content-type": "application/json"}
    )
    return data.json()


@shared_task
def get_intra_minute_data(symbols=SYMBOLS):
    get_data_from_api(symbols)


@shared_task
def get_minute_data():
    for symbol in SYMBOLS:
        data = get_data_from_api_lastmin(symbol)

        logger.info(f"CLOSED: {symbol} | {data[0][4]}")
