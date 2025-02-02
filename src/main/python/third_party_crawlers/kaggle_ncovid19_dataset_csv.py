from sys import path
path.append('../')
path.append('../../../../')

import csv

from resource_urls import *
from utils.csv_utils import write_dict_to_csv_file
from symptom_parser import SymptomParser

header_fields = ['id', 'report_date', 'age', 'gender', 'city', 'country', 'latitude', 'longitude', 'symptoms', 'report_source', 'travel_history']
csv_output_filename = './clean_data.csv'
input_filename = '../../../../data-sets/kaggle_ncovid19-dataset.csv'


def parse_field(key, value):
    symptom_parser = SymptomParser()
    if key == 'symptoms':
        return 'symptoms', symptom_parser.parse_symptoms(value)
    elif key == 'travel_history_location':
        if value != '':
            return 'travel_history', value.split(', ')
        else:
            return 'travel_history', []
    elif key == 'country' or key == 'country_new':
        if value != '':
            return 'country', value
    elif key == 'ID':
        return 'id', value
    elif key == 'sex':
        return 'gender', value
    elif key == 'source':
        return 'report_source', value
    elif key == 'date_confirmation':
        return 'report_date', value
    elif key in header_fields:
        return key, value
    return None, None


def parse_data(f):
    res = []
    symptom_parser = SymptomParser()

    for row in csv.DictReader(f, skipinitialspace=True):
        item = {}
        for k, v in row.items():
            new_key, new_value = parse_field(k, v)
            if new_key is None:
                continue
            item[new_key] = new_value
        res.append(item)

    return res

def process_csv_data():
    with open(input_filename, encoding='utf-8-sig') as f:
        parsed_data = parse_data(f)

    write_dict_to_csv_file(csv_output_filename, header_fields, parsed_data)

process_csv_data()

