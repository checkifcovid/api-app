import csv
import boto3 as bt
import pandas as pd
import json
import uuid

class S3Connector:
    # creates unique file names to optimize performance
    def create_unique_name(self, data_object):
        file_info = ''.join([key for key in data_object.keys()])
        random_id = uuid.uuid4().hex[:8]
        return ''.join(str(random_id, file_info, ".csv"))

    # gets a file name and list of values/iterable object
    # then writes the values to the csv file
    def write_to_csv(self, file_name, data_object_values):
        open_csv = open(file_name, 'w')
        csv_writer = csv.writer(open_csv)

        for item in data_object_values:
            csv_writer.writerow(item)

        open_csv.close()

    # helper function to generate csv file from any data object
    def object_to_csv(self, data_object):

        if isinstance(data_object, dict):       # process data object as dict of dicts
            file_name = self.create_unique_name(data_object)

            self.write_to_csv(file_name, data_object.values())
            
            return file_name

        else:
            if not isinstance(data_object, str):    # if data object is not in JSON format
                try:                                # convert panda data frame to JSON
                    data_object = data_object.to_json(orient='records')

                except:             # print error message for any other format
                    print("[ERROR] unrecognized data object")

            # process data as JSON object
            json_data = json.loads(data_object)

            # create unique id from all the keys of first json element
            file_name = self.create_unique_name(json_data[0])

            self.write_to_csv(file_name, json_data)

            return file_name

    # utility to download/upload csv files to s3
    def S3Cconnect(self, filename, bucket_name, key, download=False):
        s3_client = bt.client('s3')

        if download:
            s3_client.download_file(filename, bucket_name, f'/tmp/{key}')

        else:
            try:
                s3_client.upload_file(filename, bucket_name, key)
            except:
                print('[ERROR]')

    # class method to upload data objects to s3
    def upload_file(self, data_object, bucket_name, key):
        file_name = self.object_to_csv(data_object)

        self.S3Cconnect(file_name, bucket_name, key)

    # class method to download data objects from s3
    def download_file(self, file_name, bucket_name, key):
        self.S3Cconnect(file_name, bucket_name, key, download=True)
