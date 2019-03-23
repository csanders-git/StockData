import csv
import datetime

csv_name = "Breachdates.csv"

def get_csv_file(fname):
	csv_file = open(fname, 'r')
	try:
		csv_reader = csv.reader(csv_file, delimiter=',')
		csv_headers = next(csv_reader)
	except:
		csv_reader = None
	return csv_reader

csv_reader = get_csv_file("Breachdates.csv")

day_of_week = ['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']
week_dict = { 'Monday': 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday":0, "Sunday": 0}


for row in csv_reader:
    our_date = datetime.datetime.strptime(row[0], "%m/%d/%y")
    week_dict[day_of_week[our_date.weekday()-1]] += 1

print week_dict


#compliant_date.append(our_date.strftime("%Y-%m-%d"))
