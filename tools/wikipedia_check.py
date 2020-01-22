import csv
import requests
import re
import json

def get_company_name(row, headers):
    """
    Gets and prunes the company name from each row if needed
    """
    was_public_index = headers.index("Was_Public")
    company_name_index = headers.index("Company Name")
    # Find any element we haven't labeled yet
    if row[was_public_index] not in ["TRUE", "FALSE"]:
        # get the company name and remove any quotes
        company_name = row[company_name_index].strip('"')
        return company_name
    return False

def find_wikipedia_entry(company_name):
    """
    searches Wikipedia for company and associated info
    Returns: A Dict if found, otherwise False
    """
    # We search the top five entries to find our company
    url = [
        "https://en.wikipedia.org/w/api.php?",
        "action=opensearch",
        f"&search={company_name}",
        "&limit=5",
        "&namespace=0",
        "&format=json"
    ]
    url = "".join(url)
    resp = requests.get(url)
    # It is possible if we get an invalid char that we'll throw a JSON error
    try:
        resp_json = resp.json()
    except json.decoder.JSONDecodeError:
        print(resp.text)
        return False
    # Sometimes we don't get any responses and the page_titles will be empty
    try:
        page_titles = resp_json[1]
    except KeyError:
        return False
    # We should return up to five titles, request each articles info box
    for title in page_titles:
        url = [
            "https://en.wikipedia.org/w/api.php?",
            "action=query",
            "&prop=revisions"
            f"&titles={title}",
            "&rvprop=content",
            "&rvsection=0",
            "&format=json",
            "&redirects=1"
        ]
        url = "".join(url)
        resp = requests.get(url)
        # It is possible that there may be some error (this shouldn't happen)
        try:
            resp_json = resp.json()
        except json.decoder.JSONDecodeError:
            print(resp.text)
            continue
        info_box_pages = resp_json['query']['pages']
        output = {}
        # you'll get multiple pages depending on revision,
        # Typically this is just one key, not really sure.
        for page in info_box_pages.keys():
            try:
                info_box = info_box_pages[page]['revisions'][0]['*']
            # Account for weird responses, if it doesn't have our index, skip
            except KeyError:
                continue
            # Do a crappy but effective parse of the returned data
            info_box_split = info_box.split('| ')
            for line in info_box_split:
                split_line = line.split(' = ', 1)
                if split_line[0].strip() == "location":
                    output['location'] = split_line[1].strip()
                if split_line[0].strip() == "type":
                    output['type'] = split_line[1].strip()
                if split_line[0].strip() == "num_employees":
                    output['num_employees'] = split_line[1].strip()
                if split_line[0].strip() == "traded_as":
                    output['traded_as'] = split_line[1].strip()
                if split_line[0].strip() == "parent":
                    output['parent'] = split_line[1].strip()
        # If we got something, return it
        if output != {}:
            return output
    return False

def parse_wikipedia_entry(wikipedia_result):
    # check if it is a subsidary
    if "type" in wikipedia_result and "traded_as" not in wikipedia_result:
        if wikipedia_result['type'].find("Subsidiary") > -1:
            if "parent" not in wikipedia_result:
                print("\tThis is a problem with wikipedia")
                return False
            parent = wikipedia_result["parent"].strip(']]')
            parent = parent.strip('[[')
            wikipedia_result = find_wikipedia_entry(parent)
            if not wikipedia_result:
                print("\tWTF")
                # Something to review
                return "WTF"

    if "traded_as" in wikipedia_result.keys():
        # Extract most stock elements from the template format {{stockinfo}}
        trade_locations = re.findall(r'{{.*?}}', wikipedia_result['traded_as'])

        # Some info_boxes don't have this format (annoying)
        if trade_locations == []:
            print(f"\tUnstructured Traded as: {wikipedia_result['traded_as']}")
            return wikipedia_result['traded_as']
        # otherwise it is a normal stock
        print(f"\tTraded as: {','.join(trade_locations)}")
        return ','.join(trade_locations)
    else:
        return False

def update_stock(headers, row, replace_text):
    was_public_index = headers.index("Was_Public")
    row[was_public_index] = replace_text
    return row

def main():
    out_file = open('dataset_update.csv', 'w')
    dataset_writer = csv.writer(out_file, delimiter=',', quotechar='"')
    with open('../datasetv2.csv', 'r', encoding='cp1252') as dataset_fp:
        csv_reader = csv.reader(dataset_fp, delimiter=',')
        headers = next(csv_reader)
        dataset_writer.writerow(headers)
        for row in csv_reader:
            company_name = get_company_name(row, headers)
            if company_name:
                wikipedia_result = find_wikipedia_entry(company_name)
                print(company_name)
                # If we got a wikipedia result
                if wikipedia_result:
                    stock_result = parse_wikipedia_entry(wikipedia_result)
                    if not stock_result:
                        # Write response with False as stock isn't there
                        row = update_stock(headers, row, "FALSE")
                        dataset_writer.writerow(row)
                        continue
                    # We found a result, with a stock
                    row = update_stock(headers, row, str(stock_result))
                    dataset_writer.writerow(row)
                # Otherwise we don't know
                else:
                    dataset_writer.writerow(row)
            # If it already has been sorted
            else:
                dataset_writer.writerow(row)

main()
