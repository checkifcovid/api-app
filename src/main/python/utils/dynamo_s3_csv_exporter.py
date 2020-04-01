## Job to extract information from DynamoDB, write it into a CSV file and add it to S3.
import csv
import json
import decimal
import boto3
import os
from botocore.exceptions import NoCredentialsError

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            return int(o)
        return super(DecimalEncoder, self).default(o)

def extract_and_transform():
    dynamo_db = boto3.resource('dynamodb')
    table = dynamodb.Table('survey-app-dump')

    response = table.scan()

    raw_data = response['Items']
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        raw_data.extend(response['Items'])
    
    json_data = map(lambda item: json.dumps(item, cls=DecimalEncoder), raw_data)

    return json_data

def batch_write_to_csv(json_data):
    file_number = 1
    csv_file = open('data' + str(file_number) + '.csv', 'w') # Open the CSV file to write into

    csv_writer = csv.writer(csv_file)

    #Write the first line as the header row
    keys = json_data[0].keys()
    csv_writer.writerow(keys)

    # Write the data row by row
    # If the filesize is ~128MB, switch to a new file
    for row in json_data:
        csv_writer.writerow(row.values())
        if os.path.getsize('data'+ str(file_number) + '.csv') > 127 * 1024 * 1024
            file_number += 1
            csv_file = open('data' + str(file_number) + '.csv', 'w')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(keys)
    
    return file_number
        
    
def write_to_s3(csv_filename, bucket_name, target_filename):
    s3_bucket = boto3.resource('s3')
    try:
        s3_bucket.meta.client.upload_file(csv_filename, bucket_name, target_filename) 
    except NoCredentialsError:
        print('[ERROR]: Invalid AWS credentials')
    except FileNotFoundError:
        pass



if __name__ == '__main__':
    json_data = extract_and_transform()
    file_number = batch_write_to_csv(json_data)
    for i in range(1, file_number+1):
        # TODO: Push the CSV file(s) into S3
        filename = 'data'+ str(i) + '.csv'
        write_to_s3(filename, 'bucket-name', filename)# TODO: Configure name of bucket 
    # TODO: Establish context to make this a job
    pass

