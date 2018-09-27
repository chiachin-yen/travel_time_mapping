import csv
import os
import json

result = [['lat', 'lng', 'duration']]

for file_path in os.listdir():
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        if data['status'] == 'OK':
            feature = [
                data['legs'][0]['end_location']['lat'],
                data['legs'][0]['end_location']['lng'],
                data['legs'][0]['duration']['value']
            ]
            result.append(feature)

with open('result.csv', 'w', newline='')as result_file:
    csv_writer = csv.writer(result_file)
    csv_writer.writelines(result)
