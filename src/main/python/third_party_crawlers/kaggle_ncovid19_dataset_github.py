import csv
import requests

from resource_urls import *
from symptom_parser import SymptomParser

def fetch_data():
    try:
        response = requests.get(kaggle_ncovid19_dataset)
        if response.status_code == 200:
            return response.text
    except:
        return ''

def parse_data(dataString):
    res = []
    symptom_parser = SymptomParser()

    for row in csv.DictReader(dataString.split('\n'), skipinitialspace=True):
        item = {}
        for k, v in row.items():
            if k == 'symptoms':
                item['symptoms'] = symptom_parser.parse_symptoms(v)
            elif k == 'travel_history_location':
                if v != '':
                    item['travel_history'] = v.split(', ')
                else:
                    item['travel_history'] = []
            else:
                try:
                    item[k] = float(v)
                except ValueError:
                    item[k] = v
        res.append(item)

if __name__ == "__main__":
    rawData = fetch_data()
    parse_data(rawData)