"""Tools to convert json result from API to GeoJson"""

import json
import os

result = [['end_lat', 'end_lng', 'start_lat', 'start_lng', 'weight']]
target = 'THSR_Tainan'


def simplify_wgs(geo_num):
    'Simplify WGS float to integer'
    return int(round(geo_num*100000))


def rev_wgs(geo_num):
    'Simplify WGS float to integer'
    return geo_num/100000


for file_path in os.listdir(target):
    with open(os.path.join(target, file_path), 'r') as json_file:
        print(file_path)
        data = json.load(json_file)
        if data['status'] == 'OK':
            for step in data['routes'][0]['legs'][0]['steps']:
                line = [
                    simplify_wgs(step['end_location']['lat']),
                    simplify_wgs(step['end_location']['lng']),
                    simplify_wgs(step['start_location']['lat']),
                    simplify_wgs(step['start_location']['lng']),
                ]


with open('result.csv', 'w', newline='')as result_file:
    csv_writer = csv.writer(result_file)
    csv_writer.writerows(result)
