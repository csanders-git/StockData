import csv
import sys
import json
import requests
import logging
import pdb
import os
import datetime
import time
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import pandas

API_KEY = "demokey"
DATA_FILE = 'data.csv'


def get_csv_file(fname):
	csv_file = open(fname, 'r', encoding='cp1252')
	try:
		csv_reader = csv.reader(csv_file, delimiter=',')
		csv_headers = next(csv_reader)
	except:
		csv_reader = None
		csv_headers = None
	return csv_headers, csv_reader

def process_file(csv_headers, csv_reader):
    symbol_index = csv_headers.index("Symbol")
    publication_index = csv_headers.index("Publication")
    still_find = csv_headers.index("Remaining")
    for row in csv_reader:
        if row[symbol_index] == '' or row[publication_index] == '' or row[still_find] == 'TRUE':
            continue
        pub_month = int(row[publication_index].split('/')[0])
        pub_day = int(row[publication_index].split('/')[1])
        pub_year = int(row[publication_index].split('/')[2])
        print(row[symbol_index])
        # If the file already exists, don't waste an API call
        save_fname = "data/" + row[symbol_index] + "-daydata.csv"
        if os.path.isfile(save_fname):
            continue
        ts = TimeSeries(key=API_KEY, output_format='pandas', indexing_type='date')
        retry = True
        retry_counter = 0
        while retry is True:
            if retry_counter == 2:
                print(row[symbol_index] + " cannot be downloaded")
            try:
                daily_df, meta_data = ts.get_daily(symbol=row[symbol_index], outputsize='full')
                retry = False
            except KeyError:
                print("Got an error, backing off for 60 seconds")
                time.sleep(60)
            retry_counter+=1

        print(daily_df)
        json_daily_df = daily_df.to_csv()

        with open(save_fname, 'w') as daydata_file:
        	daydata_file.write(json_daily_df)

def main():
    csv_headers, csv_reader = get_csv_file(DATA_FILE)
    if csv_headers is None or csv_reader is None:
        print("Couldn't read CSV file")
        sys.exit()
    process_file(csv_headers, csv_reader)

main()
