"""Tools to convert json result from API to GeoJson"""

import json
import os

target = os.path.join('result', 'THSR_Tainan')


def simplify_wgs(geo_num):
    'Simplify WGS float to integer'
    return str(round(geo_num*100000))


def decode_polyline(polyline_str):
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dict to apply them later
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append([lng / 100000.0, lat / 100000.0])

    return coordinates


result = {}

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
                geo_key = 'x'.join(line)
                try:
                    result[geo_key]['properties']['weight'] += 1
                except KeyError:
                    result[geo_key] = {
                        'type': 'Feature',
                        'properties': {
                            'weight': 1
                        },
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': decode_polyline(
                                step['polyline']['points']
                            )
                        }
                    }

features = []
for key, value in result.items():
    features.append(value)

gj_result = {
    "type": "FeatureCollection",
    "name": "Path_Analysis",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    'features': features
}

with open(os.path.join('result', 're.geojson'), 'w') as file_path:
    json.dump(gj_result, file_path)
