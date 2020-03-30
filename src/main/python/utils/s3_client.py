
import boto3

class S3Client():

    def __init__(self):
        self.client = boto3.client('s3')
    
    def upload_csv_from_dict(self, data, bucket, key):
        self.client.upload_file()