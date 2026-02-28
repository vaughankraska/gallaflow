import json
import time
from datetime import datetime, timedelta
from typing import Any

import requests

STATION_ID = 'USGS-06043500'
START_DATE = datetime(1990, 1, 1)
CHUNK_DAYS = 5000
BASE_URL = 'https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items'


def get_date_chunks(start: datetime, chunk_days: int = CHUNK_DAYS) -> list[tuple[str, str]]:
    now = datetime.now()
    chunks = []
    current = start
    while current < now:
        end = min(current + timedelta(days=chunk_days - 1), now)
        chunks.append((
            current.strftime('%Y-%m-%dT00:00:00Z'),
            end.strftime('%Y-%m-%dT23:00:00Z'),
        ))
        current = end + timedelta(days=1)
    return chunks


def fetch_daily_data(date_chunks: list[tuple[str, str]]) -> list[dict[str, Any]]:
    all_features = []

    for start, end in date_chunks:
        print(f'Fetching {start} to {end}')
        params = {
            'f': 'json',
            'limit': CHUNK_DAYS,
            'properties': 'time,value,unit_of_measure,approval_status',
            'skipGeometry': 'true',
            'sortby': 'time',
            'monitoring_location_id': STATION_ID,
            'time': f'{start}/{end}',
        }

        response = requests.get(BASE_URL, params=params, headers={'accept': 'application/geo+json'})
        time.sleep(1)

        if response.status_code != 200:
            print(f'Error {response.status_code}: {response.text}')
            continue

        features: list[dict[str, Any]] = response.json().get('features', [])
        if not features:
            print(f'WARN: no features returned for {start} -> {end}')
        all_features.extend(features)
        print(f'  Got {len(features)} records (total so far: {len(all_features)})')

    return all_features


if __name__ == '__main__':
    chunks = get_date_chunks(START_DATE)
    print(f'Fetching {len(chunks)} chunk(s) of up to {CHUNK_DAYS} days each')
    all_features = fetch_daily_data(chunks)
    with open('data/raw/cfs-daily.json', 'w') as f:
        json.dump({'type': 'FeatureCollection', 'features': all_features}, f, indent=4)
    print(f'Done. Saved {len(all_features)} total records to data/raw/cfs-daily.json')
