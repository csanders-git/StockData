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
DATA_FILE = 'MonthlyNasdaq.csv'
OUT_FILE = 'nasdaq_data/out.csv'


def get_csv_file(fname):
	csv_file = open(fname, 'r')
	try:
		csv_reader = csv.reader(csv_file, delimiter=',')
	except:
		csv_reader = None
	return csv_reader

def fetch_symbols(csv_reader):
    stats_csv = open(OUT_FILE, 'w')
    stats_csv_writer = csv.writer(stats_csv)
    init_row = []
    counter = 0
    for row in csv_reader:
        counter += 1
        symbol = row[0]
        print str(counter) + " - " + symbol
        retry = True
        retry_counter = 0
        while retry is True:
            retry_counter+=1
            if retry_counter == 3:
                print(symbol + " cannot be downloaded")
                retry = False
            payload = {'symbol': symbol, 'apikey': API_KEY, 'function': 'TIME_SERIES_MONTHLY', 'datatype' : 'csv'}
            resp = requests.get("https://www.alphavantage.co/query", params=payload)
            resp_data = resp.text.split('\r\n')
            if init_row == []:
                for date in resp_data[1:]:
                    date = date.split(',')
                    try:
                        init_row.append(date[0])
                    except:
                        init_row.append("")
                init_row = ["symbol"] + init_row
                stats_csv_writer.writerow(init_row)
            if len(resp_data) < 10:
                try:
                    print resp.json()
                except:
                    print resp.text
                print("Got an error, backing off for 60 seconds")
                time.sleep(61)
                continue
            dates = []
            for date in resp_data[1:]:
                date = date.split(',')
                try:
                    dates.append(date[4])
                except:
                    dates.append("")
            retry = False
            dates = [symbol] + dates
            stats_csv_writer.writerow(dates)

def calculate_per_change(csv_data):
    my_csv = []
    counter = 0
    # get rid of header
    next(csv_data)
    # get rid of january 19
    next(csv_data)
    for row in csv_data:
        my_csv.append(row)
    for i in range(0,len(my_csv),12):
        print my_csv[i][0].split('-')[0]
        dec = float(my_csv[i][1])
        jan = float(my_csv[i+11][1])

        per_chang = ((dec-jan)/jan)*100
        print per_chang

def main():
    csv_reader = get_csv_file(DATA_FILE)
    if csv_reader is None:
        print("Couldn't read CSV file")
        sys.exit()
    calculate_per_change(csv_reader)

main()
