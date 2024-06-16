import pandas as pd
import json
import re
import os


def load_cfs(path):
    df = pd.read_csv(path, delimiter='\t', skiprows=28)
    df = df.drop(0)
    df.rename(columns={
        'datetime': 'date',
        '80830_00060_00003': 'CFS',
        '80830_00060_00003_cd': 'status',
        },
              inplace=True)
    df.set_index('date', inplace=True)

    return df


def load_json_files(directory, start_date='1990-01-01', end_date='2024-06-15'):
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


daily_sntl = load_json_files('data/raw/')
daily_sntl.to_csv('data/daily_sntl.csv')

daily_cfs = load_cfs('data/raw/cfs-daily.txt')
daily_cfs.to_csv('data/daily_cfs.csv')

merged_df = pd.merge(daily_sntl, daily_cfs,
                     how='left',
                     left_index=True,
                     right_index=True
                     )
merged_df.to_csv('data/daily.csv')
