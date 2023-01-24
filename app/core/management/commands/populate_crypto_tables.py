"""
Django command to populate Crypto Tables with external API data.
"""
from django.core.management.base import BaseCommand

from core.models import Crypto

import requests
from datetime import datetime, timedelta
import pytz


SYMBOLS = ['ETH-USD', 'BTC-USD', 'AVAX-USD']
COINBASE_URL = 'https://api.pro.coinbase.com/'


def get_data_from_api(
    symbol,
    end_datetime=datetime.now(),
    window_days=30,
    granularity=60
):
    """
    Generates API call to gather symbol data from end datetime,
    x nummber of days window.
    Granularity defines if records are daily, monthly, hourly, etc.
    (default: seconds).
    """
    delta = timedelta(minutes=1)
    start_datetime = end_datetime - (300*delta)

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


class Command(BaseCommand):
    """Command to populate database tables with external API."""

    def handle(self, *args, **options):
        """Loop through symbols to get data and upidate to db table."""
        tz = pytz.timezone('America/Los_Angeles')
        self.stdout.write('Starting to populate Crypto table...')

        self.stdout.write('Deleting old rows...')
        Crypto.objects.all().delete()

        for symbol in SYMBOLS:
            data = get_data_from_api(symbol)
            for row in data:
                Crypto.objects.create(
                    date_and_time=datetime.fromtimestamp(
                        row[0],
                        tz
                    ).isoformat(),
                    low=row[1],
                    high=row[2],
                    open=row[3],
                    close=row[4],
                    volume=row[5],
                    symbol=symbol,
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f'{symbol} populated successfully.'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                'All Symbol data populated successfully.'
            )
        )
