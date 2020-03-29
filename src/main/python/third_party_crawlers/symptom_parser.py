import re

# these are too vague, generally useless or actually a diagnosis and not a symptom so not useful for us
invalidSymptoms = [
    'pain', 'discomfort', 'between others', 
    'no symptoms', 'mild', 'severe', 
    'mild symptoms', 'yes', 'no', 'unwellness', 
    'dry mouth', 'physical discomfort', 'toothache' 
    'respiratory problems', 'inappetence', 
    'poor physical condition', 'kidney failure', 'general pain',
    'other symptoms', 'acute respiratory viral infection', 'dry throat',
    'acute coronary syndrome', 'flu-like symptoms', 'muscle', 'pleural effusion',
    'esophageal reflux', 'afebrile', 'pulmonary inflammation', 'primary myelofibrosis', 
    'pharynx', 'influenza', 'discharge', 'anorexia', 'feeling ill'
]

class SymptomParser():

    def __init__(self):
        self.others = []

    def is_fatigue_or_weakness(self, symptom):
        return bool(
            re.match(r'.*fatigue.*', symptom) 
            or re.match(r'.*tired.*', symptom) 
            or re.match(r'.*weak.*', symptom) 
            or re.match(r'.*malaise.*', symptom) 
            or symptom == 'lack of energy' 
            or symptom == 'lethargy'
            or symptom == 'difficulty walking'
        )

    def is_body_ache(self, symptom):
        return bool(
            # aching muscles and bone pain
            re.match(r'.*(body|joint|muscle|muscular|bone|limb?s).*(ache|pain).*', symptom) 
            or re.match(r'.*sore.*(body|muscle|limb?s).*', symptom) 
            or re.match(r'.*(muscular|muscle) (soreness|stiffness).*', symptom) 
            or re.match(r'.*(ache|aching).*', symptom) 
            or re.match(r'.*myalg.*', symptom)
        )

    def is_sore_throat(self, symptom):
        return bool(
            symptom == 'sore throat' 
            or symptom == 'pharyngalgia'
            or re.match(r'.*throat (discomfort|distress)', symptom)
            or re.match(r'.*pharyngitis.*', symptom)
            or re.match(r'.*pharyngeal.*', symptom)
        )

    def is_chills_or_sweat(self, symptom):
        return bool(
            re.match(r'.*sweat.*', symptom) 
            or re.match(r'.*chill.*', symptom) 
            or re.match(r'.*rigor.*', symptom)
            or symptom == 'cold'
        )

    def is_nausea_or_vomiting(self, symptom):
        return bool(
            re.match(r'.*nausea.*', symptom) 
            or re.match(r'.*vomiting.*', symptom)
            or re.match(r'.*emesis.*', symptom)
        )

    def is_runny_nose(self, symptom):
        return bool(
            re.match(r'.*runn.*nose', symptom) 
            or symptom == 'rhinorrhea' 
            or symptom == 'coryza'
            or symptom == 'nasal discharge'
        )

    def is_shortness_of_breath(self, symptom):
        return bool(
            re.match(r'.*breath.*', symptom) 
            or re.match(r'.*dyspnea.*', symptom) 
            or re.match(r'.*gasp.*', symptom) 
            or re.match(r'.*respiratory (stress|complaints|problems|distress).*', symptom) 
            or symptom == 'aggressive pulmonary symptomatology'
            or symptom == 'anhelation'
            or symptom == 'wheezing'
        )

    def get_normalized_key_value(self, symptom):
        if re.match(r'.*fever.*', symptom):
            return 'fever', True
        elif symptom == 'dizziness' \
            or re.match(r'.*obnubila.*', symptom):
            return 'light_headedness', True
        elif self.is_chills_or_sweat(symptom): 
            return 'chills_sweating', True
        elif re.match(r'.*chest.*(pain|tightness|distress|discomfort).*', symptom): 
            return 'chest_pain', True
        elif re.match(r'.*diarrh.*', symptom): 
            return 'diarrhea', True
        # match for 'sneez' is enough to make up for different spellings/wordings
        elif re.match(r'.*sneez.*', symptom): 
            return 'sneezing', True
        elif re.match(r'.*headache.*', symptom): 
            return 'headache', True
        elif self.is_sore_throat(symptom): 
            return 'sore_throat', True
        elif symptom == 'rash': 
            return 'rash', True
        elif self.is_nausea_or_vomiting(symptom): 
            return 'nausea_vomiting', True
        elif symptom == 'abdominal pain': 
            return 'abdominal_pain', True
        elif re.match(r'.*cough.*', symptom) or symptom == 'expectoration':
            return 'cough', True
        elif self.is_shortness_of_breath(symptom):
            return 'breathing_difficulty', True
        elif self.is_runny_nose(symptom):
            return 'runny_nose', True
        elif self.is_fatigue_or_weakness(symptom): 
            return 'fatigue_weakness', True
        elif self.is_body_ache(symptom):
            return 'body_ache', True
        else:
            return 'others', symptom

    def parse_symptoms(self, symptomsString):
        symptomSplit = re.sub(r'(;|and)', ', ', symptomsString).split(', ')
        symptoms = {}
        if symptomsString != '':
            for symptom in symptomSplit:
                stripped = symptom.strip()
                normalized = stripped.lower()

                # this matches `asymptomatic` as well as `oligosymptomatic` so we use this regex to remove those
                if bool(re.match(r'.*symptomatic.*', normalized)) \
                    or bool(re.match(r'.*\d+°*', normalized)) \
                    or bool(re.match(r'.*(no|respiratory).*symptoms', normalized)) \
                    or bool(re.match(r'.*pneumonia.*', normalized)) \
                    or bool(re.match(r'.*pneumonitis.*', normalized)) \
                    or normalized in invalidSymptoms \
                    or len(normalized.split(' ')) >= 5:
                    # strings that match any of the above conditions 
                    # are not useful to us or are actually diagnosis not symptoms
                    # also we ignore "symptom" with 5 or more words as it's usually too general information
                    # e.g. symptoms associated with a respiratory condition
                    continue

                try:
                    # some weird numbers are in the symptoms so we avoid storing those with this
                    int(normalized)
                    continue
                except:
                    key, value = self.get_normalized_key_value(normalized)
                    if key == 'others' and value != '':
                        if 'others' in symptoms:
                            symptoms['others'].append(value)
                        else:
                            symptoms['others'] = [value]
                    elif value != '':
                        symptoms[key] = value
        
        if 'others' in symptoms:
            self.others.extend(symptoms['others'])

        return symptoms

    def get_unique_other_conditions(self):
        return set(self.others)