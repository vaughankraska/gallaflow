import pandas as pd
import json
import re
import os


def load_cfs(directory, start_date='1990-01-01', end_date='2024-06-15'):
    date_range = pd.date_range(start=start_date,
                               end=end_date,
                               freq='h'
                               )
    df = pd.DataFrame(date_range, columns=['date'])
    df.set_index('date', inplace=True)

    daily_pattern = re.compile(r'cfs-\d{4}-\d{2}-\d{2}T00:00\.json')
    for filename in os.listdir(directory):
        if daily_pattern.match(filename):
            print(f'Found {filename}')
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                full = json.load(file)
                ts = full['value']['timeSeries']
                if len(ts) > 0:
                    cfs = pd.json_normalize(ts[0]['values'][0]['value'])
                    cfs.rename(columns={'dateTime': 'date', 'value': 'CFS'},
                               inplace=True)
                    cfs['date'] = pd.to_datetime(
                            cfs['date'],
                            utc=True
                            ).dt.tz_localize(None)
                    cfs.set_index('date', inplace=True)

                    # df = pd.merge_asof(df, cfs,
                    #                    left_index=True,
                    #                    right_index=True,
                    #                    )
                    df = df.combine_first(cfs)

    df['CFS'] = df['CFS'].ffill()
    return df


def load_json_files(directory, start_date='1990-01-01', end_date='2024-06-15'):
    # TODO!!! Finish this function and merge with CFS
    date_range = pd.date_range(start=start_date, end=end_date)
    df = pd.DataFrame(date_range, columns=['date'])
    df['date'] = df['date'].astype(str)
    df.set_index('date', inplace=True)

    daily_pattern = re.compile(r'sntl-\d{4}-\d{2}-\d{2}\.json')
    for filename in os.listdir(directory):
        if daily_pattern.match(filename):
            print(f'Found {filename}')
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                full = json.load(file)
                data = full[0]['data']
                for key in data:
                    col_name = key['stationElement']['elementCode']
                    column_df = pd.json_normalize(key['values'])
                    column_df['date'] = column_df['date'].astype(str)
                    column_df.set_index('date', inplace=True)
                    column_df = column_df.add_prefix(col_name+'_')

                    df = df.combine_first(column_df)
    return df


fine_grained_cfs = load_cfs('data/raw/')
fine_grained_cfs.to_csv('data/granular_cfs.csv')
fine_grained_cfs['CFS'] = pd.to_numeric(fine_grained_cfs['CFS'])

hourly_cfs = fine_grained_cfs.drop(['qualifiers'], axis=1).groupby(
        pd.Grouper(level='date', freq="h")
        ).mean()
hourly_cfs.to_csv('data/hourly_cfs.csv')

daily_cfs = fine_grained_cfs.drop(['qualifiers'], axis=1).groupby(
        pd.Grouper(level='date', freq="d")
        ).mean()
daily_cfs.to_csv('data/daily_cfs_aggregated.csv')
