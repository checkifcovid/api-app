import json
import boto3
import uuid


def lambda_handler(event, context):
    # TODO implement
    try:
        dynamo_db = boto3.resource('dynamodb')
        survey_table = dynamo_db.Table('ftc-survey-app-staging')
        report_table = dynamo_db.Table('covid-user-reports')

        survey_id = event['survey_id']
        user_id = event['user_id']
        report_date = event['report_date']
        report_source = event['report_source']
        gender = event['gender']
        age = event['age']
        postalcode = event['postcode']
        symptoms = str(event['symptoms'])
        country = event['country'].rstrip()
        country_code = event['country_code'].rstrip()
        # travel = event['travel'] if event['travel'] else "No Travel"

        table.put_item(
            Item={
                'SurveyID': survey_id,
                'UserID': user_id,
                'ReportDate': report_date,
                'ReportSource': report_source,
                'Gender': gender,
                'Age': age,
                'PostalCode': postalcode,
                'Symptoms': symptoms,
                'Country': country,
                'CountryCode': country_code
                # 'Travel': travel
            }
        )
        response = {
            'user_id': str(user_id),
            'survey_id': str(survey_id),
            'message': 'Successfully submitted Survey Form'
        }
        return {
            'statusCode': 200,
            'body': response
        }
    except Exception as err:
        response = {
            'user_id': str(user_id),
            'survey_id': str(survey_id),
            'message': 'Failed to submit survey for user; ERROR MSG : ' + str(err)
        }
        return {
            'statusCode': 503,
            'body': response

        }