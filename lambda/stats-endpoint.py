import json
import random


def lambda_handler(event, context):
    # TODO implement
    try:
        probability = random.random()

        if probability > 0.75:
            diagnosis = 'Positive'
        else:
            diagnosis = 'Negative'

        response = {
            'diagnosis': diagnosis,
            'probability': probability,
            'message': 'Successfully Calculated Probability'
        }
        return {
            'statusCode': 200,
            'body': response
        }
    except Exception as err:
        response['Message'] = "ERROR : " + str(err)
        return {
            'statusCode': 503,
            'body': response
        }