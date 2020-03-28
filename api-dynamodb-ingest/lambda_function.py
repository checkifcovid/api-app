import json
import boto3
import uuid 

def lambda_handler(event, context):
    # TODO implement
    
    dynamo_db = boto3.resource('dynamodb')
    table = dynamo_db.Table('survey-app-dump')
    
    report_date = event['report_date']
    report_source = event['report_source']
    gender = event['gender']
    age = event['age']
    postcode = event['postcode']
    symptoms = event['symptoms']
    country = event['country'].rstrip()
    travel = event['travel']

            # Construct a unique sort key for this line item
    userID = str(uuid.uuid1())
    surveyID = str(uuid.uuid1())

    table.put_item(
        Item={
            'SurveyID': surveyID,
            'UserID': userID,
            'ReportDate': report_date,
            'ReportSource': report_source,
            'Gender': gender,
            'Age': int(age),
            'PostCode': postcode,
            'Symptoms': symptoms,
            'Country': country,
            'Travel': travel
        }
    )

    
    return {
        'statusCode': 200,
        'body': json.dumps('Data loaded succesffuly for Patient : ' + str(userID))
    }

