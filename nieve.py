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
import matplotlib.pyplot as plt


API_KEY = "demokey"
DATA_FILE = 'data.csv'
OUT_FILE = 'nieve.csv'


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
	return_data = []
	for row in csv_reader:
		if row[symbol_index] == '' or row[publication_index] == '' or row[still_find] == 'TRUE':
			continue
		pub_month = int(row[publication_index].split('/')[0])
		pub_day = int(row[publication_index].split('/')[1])
		pub_year = int(row[publication_index].split('/')[2])
		return_data.append({"symbol": row[symbol_index], "day": pub_day, "month" : pub_month, "year" : pub_year, 'combined_date' : row[publication_index] })
	return return_data

def read_nasdaq(fname, start_date):
	base_path = os.path.dirname(os.path.abspath(__file__))
	full_path =  base_path + "/IXIC.csv"
	nasdaq_df = pandas.read_csv(full_path)
	compliant_date = []
	for date in nasdaq_df['Date']:
		our_date = datetime.datetime.strptime(date, "%m/%d/%y")
		compliant_date.append(our_date.strftime("%Y-%m-%d"))
	nasdaq_df['compliant'] = compliant_date
	return nasdaq_df


def process_daydata(symbol_record, nasdaq_df, breach_date, stats_csv_writer):
	symbol = symbol_record['symbol']
	base_path = os.path.dirname(os.path.abspath(__file__))
	full_path =  base_path + "/data/"+ symbol + "-daydata.csv"
	stock_df = pandas.read_csv(full_path)

	stock_months = []
	stock_days = []
	stock_years = []
	for stock_date in stock_df['date']:
		stock_months.append(int(stock_date.split('-')[1]))
		stock_days.append(int(stock_date.split('-')[2]))
		stock_years.append(int(stock_date.split('-')[0]))

	# Fix the date if it falls on a weekend
	breachday = datetime.datetime.strptime(breach_date, "%Y-%m-%d")
	breachday_minusone = datetime.datetime.strptime(breach_date, "%Y-%m-%d") - datetime.timedelta(days=1)
	# check if we're on a weekend
	if breachday.weekday() == 5:
		breachday = breachday + datetime.timedelta(days=2)
		breach_date = breachday.strftime("%Y-%m-%d")
	if breachday.weekday() == 6:
		breachday = breachday + datetime.timedelta(days=1)
		breach_date = breachday.strftime("%Y-%m-%d")

	# if we end up on a sunday move us to Friday
	#if breachday_minusone.weekday() == 6:
	#	breachday_minusone = breachday_minusone + datetime.timedelta(days=2)
	#	breachday_minusone = breachday_minusone.strftime("%Y-%m-%d")

	try:
		nasdaq_breach_index = (nasdaq_df.index[nasdaq_df['compliant'] == breach_date].tolist()[0])
		stock_breach_index = (stock_df.index[stock_df['date'] == breach_date].tolist()[0])
	except:
		pdb.set_trace()
	price_on_breach_day = stock_df.iloc[stock_breach_index]['4. close']
	nasdaq_on_breach_day = nasdaq_df.iloc[nasdaq_breach_index]['Close']

	price_on_before_breach_day = stock_df.iloc[stock_breach_index-1]['4. close']
	nasdaq_on_before_breach_day = nasdaq_df.iloc[nasdaq_breach_index-1]['Close']

	print(symbol_record['symbol'])


	stock_per_chat = ((price_on_breach_day-price_on_before_breach_day)/price_on_before_breach_day)*100
	nasdaq_per_chat = ((nasdaq_on_breach_day-nasdaq_on_before_breach_day)/nasdaq_on_before_breach_day)*100
	big_calc = (((price_on_breach_day)/(price_on_before_breach_day)-1)*100) - (((nasdaq_on_breach_day)/(nasdaq_on_before_breach_day)-1)*100)
	stats_csv_writer.writerow([symbol_record['symbol'], stock_per_chat, nasdaq_per_chat, big_calc])


def main():
	csv_headers, csv_reader = get_csv_file(DATA_FILE)
	if csv_headers is None or csv_reader is None:
		print("Couldn't read CSV file")
		sys.exit()
	symbol_data = process_file(csv_headers, csv_reader)
	stats_csv = open(OUT_FILE, 'w')
	stats_csv_writer = csv.writer(stats_csv)
	symbol_stats = ["symbol", "stock per chang", "nasdaq per chang", "bigcalc" ]
	stats_csv_writer.writerow(symbol_stats)
	for symbol_record in symbol_data:
		combined_date = datetime.datetime.strptime(symbol_record['combined_date'], "%m/%d/%y")
		breach_date = combined_date.strftime("%Y-%m-%d")
		nasdaq_df = read_nasdaq('IXIC.csv', breach_date)
		process_daydata(symbol_record, nasdaq_df, breach_date, stats_csv_writer)
	stats_csv.close()
	#sys.exit()

main()
