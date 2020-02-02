# pip install pytrends

from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

def read_nasdaq_and_nyse():
    base_path = "data/^IXIC-daydata.csv"
    nasdaq_df = pd.read_csv(base_path)
    base_path = "data/^NYA-daydata.csv"
    nyse_composite_df = pd.read_csv(base_path)
    return nasdaq_df, nyse_composite_df

def get_csv_file(fname):
    csv_file = open(fname, 'r', encoding='cp1252')
    try:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_headers = next(csv_reader)
    except:
        csv_reader = None
        csv_headers = None
    if csv_headers is None or csv_reader is None:
        raise IOError("Couldn't read CSV file")
    return csv_headers, csv_reader

def fix_weekend_date(breachday):
    # Set to monday if we're on Sat
    if breachday.weekday() == 5:
        breachday = breachday + datetime.timedelta(days=2)
    # Set to monday if we're on Sunday
    if breachday.weekday() == 6:
        breachday = breachday + datetime.timedelta(days=1)
    return breachday
    #return breachday.strftime("%Y-%m-%d")

def fix_closed_market_data(adjusted_breach_date, nasdaq_df):
    adjusted_breach_date_str = adjusted_breach_date.strftime("%Y-%m-%d")
    # The market may have been closed for whatever reason on our breach date so lets check
    nasdaq_breach_index = nasdaq_df.index[nasdaq_df['date'] == adjusted_breach_date_str].tolist()
    while nasdaq_breach_index == []:
        # Keep adding one day each time till we get to the next trading day
        adjusted_breach_date = adjusted_breach_date + datetime.timedelta(days=1)
        # we're gonna need the right format here to search our dataframe
        adjusted_breach_date_str = adjusted_breach_date.strftime("%Y-%m-%d")
        # give us the index where the date equals the adjusted_breach_date
        nasdaq_breach_index = nasdaq_df.index[nasdaq_df['date'] == adjusted_breach_date_str].tolist()
    return adjusted_breach_date

def generate_stock_data(df, nyse_df, nasdaq_df, dates, test_data=False):
    stock_info = pd.DataFrame()
    for time in dates:
        one_day_stock_holder = []
        for _, row in df.iterrows():
            # Import our stock data
            if test_data:
                full_path = "test-data/"+ row["Symbol"] + "-daydata.csv"
            else:
                full_path = "data/"+ row["Symbol"] + "-daydata.csv"
            stock_df = pd.read_csv(full_path)
            # Fix the date if it falls on a weekend
            breachday = datetime.datetime.strptime(row["Publication"], "%m/%d/%y")
            adjusted_breach_date = fix_weekend_date(breachday)
            adjusted_breach_date = fix_closed_market_data(adjusted_breach_date, nasdaq_df)
            # convert the datetime to a string, we no longer need the datetime fmt
            adjusted_breach_date = adjusted_breach_date.strftime("%Y-%m-%d")
            # since we're index on dates, these should be unique, get the first (and only element)
            nasdaq_breach_index = nasdaq_df.index[nasdaq_df['date'] == adjusted_breach_date].tolist()[0]
            stock_breach_index = (stock_df.index[stock_df['date'] == adjusted_breach_date].tolist()[0])

            # if either the NASDAQ or the stock don't have information for the future date
            # we need to return and ignore that stock.
            if stock_breach_index+time > len(stock_df):
                one_day_stock_holder.append(np.nan)
                continue
            if nasdaq_breach_index+time > len(nasdaq_df):
                one_day_stock_holder.append(np.nan)
                continue

            # get the close on breach day
            price_on_breach_day_and_time = stock_df.iloc[stock_breach_index+time]['close']
            nasdaq_on_breach_day_and_time = nasdaq_df.iloc[nasdaq_breach_index+time]['close']

            # We have the index and all data is chronological therefore subtracting one gets us the day before
            price_on_before_breach_day = stock_df.iloc[stock_breach_index-1]['close']
            nasdaq_on_before_breach_day = nasdaq_df.iloc[nasdaq_breach_index-1]['close']

            stock_per_change = ((price_on_breach_day_and_time-price_on_before_breach_day)/price_on_before_breach_day)*100
            nasdaq_per_change = ((nasdaq_on_breach_day_and_time-nasdaq_on_before_breach_day)/nasdaq_on_before_breach_day)*100
            adjusted_per_change = (((price_on_breach_day_and_time)/(price_on_before_breach_day)-1)*100) - (((nasdaq_on_breach_day_and_time)/(nasdaq_on_before_breach_day)-1)*100)
            one_day_stock_holder.append(adjusted_per_change)
        stock_info[f"stock_{time}_days"] = one_day_stock_holder
    return stock_info

def get_two_week_range(date):
    breachday = datetime.datetime.strptime(date, "%m/%d/%y")
    breachday_two_weeeks = breachday + datetime.timedelta(days=14)
    breachday = breachday.strftime("%Y-%m-%d")
    breachday_two_weeeks = breachday_two_weeeks.strftime("%Y-%m-%d")
    return breachday, breachday_two_weeeks

def main():
    nasdaq_df, nyse_composite_df = read_nasdaq_and_nyse()
    df = pd.read_csv('../../dataset-samples.csv')
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_data = []
    for index, entry in df.iterrows():
        trending_total = 0
        comp_name = entry["Company Name"].strip('\"')
        breachday, breachday_two_weeeks = get_two_week_range(entry["Publication"])

        kw_list = [f"{comp_name} Breach"]
        pytrends.build_payload(kw_list, cat=0, timeframe=f'{breachday} {breachday_two_weeeks}', geo='', gprop='')
        trends_data = pytrends.interest_over_time()

        if trends_data.empty:
            trending_data.append(trending_total)
            continue
        for day in trends_data[kw_list[0]]:
            trending_total+=day
        print(f"Found Total for {comp_name} - {trending_total}")
        trending_data.append(trending_total)
    df["Trending_amount"] = trending_data

    df.to_csv("../../dataset-samples.csv")


main()
