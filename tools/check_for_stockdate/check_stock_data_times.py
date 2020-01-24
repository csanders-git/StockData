import csv
import os

DATA_FILE = '../../dataset.csv'


def get_csv_file(fname):
    """
    Fetch a CSV and return the header and reader
    """
    csv_file = open(fname, 'r', encoding='cp1252')
    try:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_headers = next(csv_reader)
    except csv.Error:
        csv_reader = None
        csv_headers = None
    return csv_headers, csv_reader

def breach_day_is_found(pub_month, pub_year, save_fname):
    """
    Check if the date of the breach is found in the stock data
    """
    _, csv_data = get_csv_file(save_fname)
    for date in csv_data:
        try:
            year = int(date[0].split('-')[0][2:])
            month = int(date[0].split('-')[1])
        except ValueError:
            print(f"Invalid format within {save_fname}:")
            print(date)
            exit()
        # don't look for specific day as it may be a weekend or holiday
        if year == pub_year and month == pub_month:
            return True
    return False

def process_file(csv_headers, csv_reader):
    """
    Read through the dataset and determine which orgs should be checked
    """
    symbol_index = csv_headers.index("Symbol")
    exchange_index = csv_headers.index("Market")
    publication_index = csv_headers.index("Publication")
    in_scope_index = csv_headers.index("In_Scope")
    was_public_index = csv_headers.index("Was_Public")
    for row in csv_reader:
        try:
            pub_month = int(row[publication_index].split('/')[0])
            pub_year = int(row[publication_index].split('/')[2])
        except ValueError:
            print(f"Error trying to process date for {row[symbol_index]}")
            print(row)
        # For this research the API can only return us info on the following two exchanges
        if(row[exchange_index] not in ["NASDAQ", "NYSE"]):
            continue
        # Some values don't fit our minimum definition of breach
        if row[in_scope_index] == "FALSE":
            continue
        # Check if we've already marked these values as not pubic during that time
        if row[was_public_index] == "FALSE":
            continue
        symbol = row[symbol_index]
        # If the file already exists, don't waste an API call
        save_fname = f"../fetch_stock_info/data/{row[symbol_index]}-daydata.csv"
        if not os.path.isfile(save_fname):
            continue
        breach_found = breach_day_is_found(pub_month, pub_year, save_fname)
        if not breach_found:
            print(f"Didn't find data for {symbol}")
        else:
            print(f"Data FOUND for {symbol}")


def main():
    """
    Kick off our reading and checking of the dataset
    """
    csv_headers, csv_reader = get_csv_file(DATA_FILE)
    if csv_headers is None or csv_reader is None:
        print("Couldn't read CSV file")
        exit()
    process_file(csv_headers, csv_reader)

if __name__ == "__main__":
    main()
