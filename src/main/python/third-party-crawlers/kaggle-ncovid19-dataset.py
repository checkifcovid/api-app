import csv
import requests
import re

from resource_urls import *

commonPhrases = ['mild', 'severe', 'mild symptoms']

def fetch_data():
    try:
        response = requests.get(kaggle_ncovid19_dataset)
        if response.status_code == 200:
            return response.text
    except:
        return ''

def parse_symptoms(symptomsString):
    symptomSplit = re.sub(r'(;|and)', ', ', symptomsString).split(', ')
    symptoms = {}
    mainSymptoms = ["fever", "cough", "runny_nose"]
    if symptomsString != '':
        for symptom in symptomSplit:
            stripped = symptom.strip()
            normalized = stripped.lower()

            # this matches `asymptomatic` as well as `oligosymptomatic` so we use this regex to remove those
            if bool(re.match(r'.*symptomatic.*', normalized)) \
                or bool(re.match(r'.*℃.*', normalized)) \
                or normalized == 'no symptoms' \
                or normalized == 'between others' \
                or normalized in commonPhrases:
                # strings that match any of the above conditions are useless to us
                continue

            try:
                # some weird numbers are in the symptoms so we avoid storing those with this
                int(normalized)
                continue
            except:
                if re.match(r'.*fever.*', normalized):
                    symptoms['fever'] = True
                elif re.match(r'.*cough.*', normalized):
                    symptoms['cough'] = True
                elif re.match(r'.*runny.*', normalized) \
                    or normalized == 'rhinorrhea' \
                    or normalized == 'rhinorrhoea' \
                    or normalized == 'running nose':
                    symptoms['runny_nose'] = True
                else:
                    if normalized == 'milagia':
                        stripped = 'myalgia'
                    if 'others' in symptoms:
                        symptoms['others'].append(stripped)
                    else:
                        symptoms['others'] = [stripped]
    return symptoms

def parse_data(dataString):
    res = []
    for row in csv.DictReader(dataString.split('\n'), skipinitialspace=True):
        item = {}
        for k, v in row.items():
            if k == 'symptoms':
                item['symptoms'] = parse_symptoms(v)
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