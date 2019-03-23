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
OUT_FILE = 'parsed.csv'


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

def generate_data(symbol, nasdaq_breach_index, stock_breach_index, nasdaq_df, stock_df, stats_csv_writer):
	symbol_stats = ["symbol","one week NASDAQ", "one week stock", "two week NASDAQ", "two week stock", "one month NASDAQ", "one month stock", "one year NASDAQ", "one year stock",  "two years NASDAQ", "two years stock",  "three years NASDAQ", "three years stock" ]
	output_stats = []
	output_stats.append(symbol)
	# 1 week average change
	nasdaq_on_breach_day = nasdaq_df.iloc[nasdaq_breach_index]['Close']
	nasdaq_one_week= nasdaq_df.iloc[nasdaq_breach_index+5]['Close']
	stock_on_breach_day = stock_df.iloc[stock_breach_index]['4. close']
	stock_one_week= stock_df.iloc[stock_breach_index+5]['4. close']
	print("NASDAQ Gains - 1 week")
	output_stats.append((1-(nasdaq_on_breach_day/nasdaq_one_week))*100)
	print("Stock Gains - 1 week")
	output_stats.append((1-(stock_on_breach_day/stock_one_week))*100)
	print("Does it outperform he nasdaq")
	if( (1-(stock_on_breach_day/stock_one_week))*100 > (1-(nasdaq_on_breach_day/nasdaq_one_week))*100):
		output_stats.append("True")
	else:
		output_stats.append("False")
	# 2 weeks average change
	nasdaq_two_week= nasdaq_df.iloc[nasdaq_breach_index+10]['Close']
	stock_two_week= stock_df.iloc[stock_breach_index+10]['4. close']
	print()
	print("NASDAQ Gains - 2 week")
	output_stats.append((1-(nasdaq_on_breach_day/nasdaq_two_week))*100)
	print("Stock Gains - 2 week")
	output_stats.append((1-(stock_on_breach_day/stock_two_week))*100)
	print("Does it outperform he nasdaq")
	if( (1-(stock_on_breach_day/stock_two_week))*100 > (1-(nasdaq_on_breach_day/nasdaq_two_week))*100):
		output_stats.append("True")
	else:
		output_stats.append("False")
	# 1 month average Change
	nasdaq_one_month = nasdaq_df.iloc[nasdaq_breach_index+20]['Close']
	stock_one_month = stock_df.iloc[stock_breach_index+20]['4. close']
	print()
	print("NASDAQ Gains - 1 month")
	output_stats.append((1-(nasdaq_on_breach_day/nasdaq_one_month))*100)
	print("Stock Gains - 1 month")
	output_stats.append((1-(stock_on_breach_day/stock_one_month))*100)
	print("Does it outperform he nasdaq")
	if( (1-(stock_on_breach_day/stock_one_month))*100 > (1-(nasdaq_on_breach_day/nasdaq_one_month))*100):
		output_stats.append("True")
	else:
		output_stats.append("False")
	# 1 year average change
	try:
		nasdaq_one_year = nasdaq_df.iloc[nasdaq_breach_index+260]['Close']
		stock_one_year = stock_df.iloc[stock_breach_index+260]['4. close']
		print()
		print("NASDAQ Gains - 1 year")
		output_stats.append((1-(nasdaq_on_breach_day/nasdaq_one_year))*100)
		print("Stock Gains - 1 year")
		output_stats.append((1-(stock_on_breach_day/stock_one_year))*100)
		print("Does it outperform he nasdaq")
		if( (1-(stock_on_breach_day/stock_one_year))*100 > (1-(nasdaq_on_breach_day/nasdaq_one_year))*100):
			output_stats.append("True")
		else:
			output_stats.append("False")
	except IndexError:
		output_stats.append('-')
		output_stats.append('-')
	# 2 year average change
	try:
		nasdaq_two_year = nasdaq_df.iloc[nasdaq_breach_index+520]['Close']
		stock_two_year = stock_df.iloc[stock_breach_index+520]['4. close']
		print()
		print("NASDAQ Gains - 2 year")
		output_stats.append((1-(nasdaq_on_breach_day/nasdaq_two_year))*100)
		print("Stock Gains - 2 year")
		output_stats.append((1-(stock_on_breach_day/stock_two_year))*100)
		print("Does it outperform he nasdaq")
		if( (1-(stock_on_breach_day/stock_two_year))*100 > (1-(nasdaq_on_breach_day/nasdaq_two_year))*100):
			output_stats.append("True")
		else:
			output_stats.append("False")
	except IndexError:
		output_stats.append('-')
		output_stats.append('-')
	# 3 year average change
	try:
		nasdaq_three_year = nasdaq_df.iloc[nasdaq_breach_index+780]['Close']
		stock_three_year = stock_df.iloc[stock_breach_index+780]['4. close']
		print()
		print("NASDAQ Gains - 3 year")
		output_stats.append((1-(nasdaq_on_breach_day/nasdaq_three_year))*100)
		print("Stock Gains - 3 year")
		output_stats.append((1-(stock_on_breach_day/stock_three_year))*100)
		print("Does it outperform he nasdaq")
		if( (1-(stock_on_breach_day/stock_three_year))*100 > (1-(nasdaq_on_breach_day/nasdaq_three_year))*100):
			output_stats.append("True")
		else:
			output_stats.append("False")
	except IndexError:
		output_stats.append('-')
		output_stats.append('-')
	stats_csv_writer.writerow(output_stats)
	return output_stats

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
	# check if we're on a weekend
	if breachday.weekday() == 5:
		breachday = breachday + datetime.timedelta(days=2)
		breach_date = breachday.strftime("%Y-%m-%d")
	if breachday.weekday() == 6:
		breachday = breachday + datetime.timedelta(days=1)
		breach_date = breachday.strftime("%Y-%m-%d")

	try:
		nasdaq_breach_index = (nasdaq_df.index[nasdaq_df['compliant'] == breach_date].tolist()[0])
		stock_breach_index = (stock_df.index[stock_df['date'] == breach_date].tolist()[0])
	except:
		pdb.set_trace()
	price_on_breach_day = stock_df.iloc[stock_breach_index]['4. close']
	nasdaq_on_breach_day = nasdaq_df.iloc[nasdaq_breach_index]['Close']

	generate_data(symbol, nasdaq_breach_index, stock_breach_index, nasdaq_df, stock_df, stats_csv_writer)

	nasdaq_df = nasdaq_df.truncate(before=nasdaq_breach_index-5, after=nasdaq_breach_index+30)
	stock_df = stock_df.truncate(before=stock_breach_index-5, after=stock_breach_index+30)


	# Add Market Days
	market_days = []
	for ind_value in stock_df.index:
		if ind_value < stock_breach_index:
			market_days.append(-(stock_breach_index - ind_value))
		elif ind_value == stock_breach_index:
			market_days.append(stock_breach_index - ind_value)
		else:
			market_days.append(ind_value - stock_breach_index)
	stock_df['market_days'] = market_days
	#print(market_days[0:20])

	# Add NASDAQ Days
	market_days = []
	for ind_value in nasdaq_df.index:
		if ind_value < nasdaq_breach_index:
			market_days.append(-(nasdaq_breach_index - ind_value))
		elif ind_value == nasdaq_breach_index:
			market_days.append(nasdaq_breach_index - ind_value)
		else:
			market_days.append(ind_value - nasdaq_breach_index)
	nasdaq_df['market_days'] = market_days

	#for close_price in stock_df['4. close']:

	# Calculate percentage per_change for stock
	last = -1
	per_change = []
	for close_price in stock_df['4. close']:
		if last == -1:
			per_change.append(0)
		else:
			per_change.append(((close_price-price_on_breach_day)/price_on_breach_day)*100)
		last = close_price
	stock_df['Stock % Change'] = per_change

	# Calculate percentage per_change for nasdaq
	last = -1
	per_change = []
	for close_price in nasdaq_df['Close']:
		if last == -1:
			per_change.append(0)
		else:
			per_change.append(((close_price-nasdaq_on_breach_day)/nasdaq_on_breach_day)*100)
		last = close_price
	nasdaq_df['NASDAQ % Change'] = per_change

	ax = nasdaq_df.plot(x='market_days', y='NASDAQ % Change', color='olive')
	stock_df.plot(x='market_days', y='Stock % Change', ax=ax)
	ymin, ymax = ax.get_ylim()
	ax.vlines(x=0, ymin=ymin, ymax=ymax, color='r')
	plt.text(0, ymax/2.0, "Breach Day", rotation=90, verticalalignment='center')
	plt.title('Difference in % share price for ' + symbol + ' after breach  VS  NASDAQ')
	plt.ylabel('Difference in % change versus NASDAQ')
	plt.xlabel('Market Days since Breach')
	graph_save_name = "graphs/perchange-" + symbol + ".png"
	plt.savefig(graph_save_name)

def main():
	csv_headers, csv_reader = get_csv_file(DATA_FILE)
	if csv_headers is None or csv_reader is None:
		print("Couldn't read CSV file")
		sys.exit()
	symbol_data = process_file(csv_headers, csv_reader)
	stats_csv = open(OUT_FILE, 'w')
	stats_csv_writer = csv.writer(stats_csv)
	symbol_stats = ["symbol","one week NASDAQ", "one week stock", "one week outperform", "two week NASDAQ", "two week stock", "two week outperform", "one month NASDAQ", "one month stock", "one month outperform", "one year NASDAQ", "one year stock", "one year outperform", "two years NASDAQ", "two years stock", "one years outperform", "three years NASDAQ", "three years stock" "three years outperform", ]
	stats_csv_writer.writerow(symbol_stats)
	for symbol_record in symbol_data:
		combined_date = datetime.datetime.strptime(symbol_record['combined_date'], "%m/%d/%y")
		breach_date = combined_date.strftime("%Y-%m-%d")
		nasdaq_df = read_nasdaq('IXIC.csv', breach_date)
		print(breach_date)
		process_daydata(symbol_record, nasdaq_df, breach_date, stats_csv_writer)
	stats_csv.close()
	#sys.exit()

main()
