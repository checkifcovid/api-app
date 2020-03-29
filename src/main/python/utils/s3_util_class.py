import csv
import boto3 as bt
import pandas as pd
import json
import uuid


class Uploader:
    # not sure about initilization info yet
    # I assumed different data objects might have different bucket names/keys
    # otherwise we could initialize the class with a unique bucket_name and key
    # for all data input

    # create unique file names to minimize collisions in storage
    def create_unique_name(self, data_object):
        file_info = ''.join([key for key in data_object.keys()])
        random_id = uuid.uuid4().hex[:8]
        return ''.join(str(random_id, file_info, ".csv"))


    def dict_to_csv(self, dict_object):
        # assuming the dict object is a dict of dicts
        # create a unique id from all the first level keys
        file_name = self.create_unique_name(dict_object)

        open_csv = open(file_name, 'w')
        csv_writer = csv.writer(open_csv)

        for item in dict_object:
            csv_writer.writerow(dict_object[item])

        return file_name


    def json_to_csv(self, json_object):
        json_data = json.loads(json_object)

        # create unique id from all the keys of first json element
        file_name = self.create_unique_name(json_data[0])

        open_csv = open(file_name, 'w')
        csv_writer = csv.writer(open_csv)

        for item in json_data:
            csv_writer.writerow(json.dumps(item))

        return file_name


    def panda_df_to_csv(self, panda_df):
        # first convert panda data frame to traditional json format
        json_object = panda_df.to_json(orient='records')

        # execute json to csv routine on new json data
        file_name = self.json_to_csv(json_object)

        return file_name

    # generic function to upload any csv file to s3
    def upload_csv(self, filename, bucket_name, key):
        s3_client = bt.client('s3')

        try:
            s3_client.upload_file(filename, bucket_name, key)
        except:
            print('[ERROR]')

    # class method to upload dictionary objects to s3
    def upload_dict_object(self, dict_object, bucket_name, key):
        file_name = self.dict_to_csv(dict_object)

        self.upload_csv(file_name, bucket_name, key)

    # class method to upload json objects to s3
    def upload_json_object(self, json_object, bucket_name, key):
        file_name = self.json_to_csv(json_object)

        self.upload_csv(file_name, bucket_name, key)

    # class method to upload panda data frame objects to s3
    def upload_panda_df_object(self, panda_df, bucket_name, key):
        file_name = self.panda_df_to_csv(panda_df)

        self.upload_csv(file_name, bucket_name, key)
