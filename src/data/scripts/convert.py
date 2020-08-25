# This script converts the files from https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data 
# into a json which can be easily used by our website.

import csv
import json
from datetime import date

confirmed_cases_file_name = "time_series_covid19_confirmed_global.csv"
deaths_file_name = "time_series_covid19_deaths_global.csv"
recovered_file_name = "time_series_covid19_recovered_global.csv"
final_data_file_name = "data-global.json"

all_data = {}

def date_to_iso_format(d):
    month,day,year = (int(x) for x in d.split('/'))
    year += 2000
    date_obj = date(year=year, month=month, day=day)
    return date_obj.strftime("%Y-%m-%d")

# Make the initial data and fill with confirmed cases.
with open(confirmed_cases_file_name, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            date_list = [date_to_iso_format(x) for x in row[4:]]
        else:
            country_name = row[1].lower()
            if country_name not in all_data:
                all_data[country_name] = {}
                for cur_date in date_list:
                    all_data[country_name][cur_date] = {}
            if row[0]:
                if country_name in ['australia', 'canada', 'china']:
                    for i in range(len(date_list)):
                        if 'confirmed' in all_data[country_name][date_list[i]]:
                            all_data[country_name][date_list[i]]['confirmed'] += int(row[i+4])
                        else:
                            all_data[country_name][date_list[i]]['confirmed'] = int(row[i+4])         
            else:
                for i in range(len(date_list)):
                    all_data[country_name][date_list[i]]['confirmed'] = int(row[i+4])
        line_count += 1

# Fill the deaths.
with open(deaths_file_name,'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            date_list = [date_to_iso_format(x) for x in row[4:]]
        else:
            country_name = row[1].lower()
            if row[0]:
                if country_name in ['australia', 'canada', 'china']:
                    for i in range(len(date_list)):
                        if 'deaths' in all_data[country_name][date_list[i]]:
                            all_data[country_name][date_list[i]]['deaths'] += int(row[i+4])
                        else:
                            all_data[country_name][date_list[i]]['deaths'] = int(row[i+4])
            else:
                for i in range(len(date_list)):
                    all_data[country_name][date_list[i]]['deaths'] = int(row[i+4])
        line_count += 1

# Fill the recovered cases.
with open(recovered_file_name,'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            date_list = [date_to_iso_format(x) for x in row[4:]]
        else:
            country_name = row[1].lower()
            if row[0]:
                if country_name in ['australia', 'canada', 'china']:
                    for i in range(len(date_list)):
                        if 'recovered' in all_data[country_name][date_list[i]]:
                            all_data[country_name][date_list[i]]['recovered'] += int(row[i+4])
                        else:
                            all_data[country_name][date_list[i]]['recovered'] = int(row[i+4])
            else:
                for i in range(len(date_list)):
                    all_data[country_name][date_list[i]]['recovered'] = int(row[i+4])
        line_count += 1

with open(final_data_file_name,'w') as f:
    json.dump(all_data,f)