import csv

def write_dict_to_csv_file(filename, header_fields, data):
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header_fields)
        writer.writeheader()
        for row in data:
            writer.writerow(row)