import csv
import os
import sys
import requests

DATA_FILE = '../../dataset.csv'

def get_csv_file(fname):
    """
    Fetches the CSV dataset file
    """
    csv_file = open(fname, 'r', encoding='cp1252')
    try:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_headers = next(csv_reader)
    except csv.Error:
        csv_reader = None
        csv_headers = None
    return csv_headers, csv_reader

def write_day_data(day_data, save_name):
    """
    Write the JSON daily market results to a CSV
    """
    # Check if the 'data' directory exists
    if not os.path.isdir('data'):
        os.mkdir('data')
    csv_writer = csv.writer(open(save_name, "w"))
    # write our headers - extracted from the first result
    csv_writer.writerow(day_data['historical'][0].keys())

    for day_values in day_data['historical']:
        csv_writer.writerow(day_values.values())

def process_file(csv_headers, csv_reader):
    """
    Extract the needed symbol and market data to fetch stock info
    """
    indexes = ["^NYA", "^IXIC"]
    for index_name in indexes:
        save_fname = f"data/{index_name}-daydata.csv"
        if os.path.isfile(save_fname):
            continue
        base_url = "https://financialmodelingprep.com"
        start_date = "1998-01-01"
        end_date = "2020-01-01"
        resp = requests.get(
            f"{base_url}/api/v3/historical-price-full/index/{index_name}?from={start_date}&to={end_date}"
        )
        if resp.status_code != 200:
            print(resp.text)
            exit()
        day_data = resp.json()
        if not day_data:
            print(f"Couldn't find {index_name}")
            continue
        write_day_data(day_data, save_fname)


def main():
    """
    Kick off the process by specifying the needed data
    """
    csv_headers, csv_reader = get_csv_file(DATA_FILE)
    if csv_headers is None or csv_reader is None:
        print("Couldn't read CSV file")
        sys.exit()
    process_file(csv_headers, csv_reader)

if __name__ == "__main__":
    main()
