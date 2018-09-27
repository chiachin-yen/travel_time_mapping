"""
Main script of traveling time
"""

import configparser
import datetime
import json
import os
import time
import urllib.request

# API URL
API_url = ("https://maps.googleapis.com/maps/api/directions/json?"
           "origin={},{}"
           "&destination={},{}""&key={}")

# Load API KEY
config = configparser.ConfigParser()
if os.path.isfile('setting.ini'):
    config.read('setting.ini')
else:
    config['API'] = {
        'KEY': input("Paste your API here: ")
    }
    print("API Key Saved.")

    with open('setting.ini', 'w') as configfile:
        config.write(configfile)

    config.read('setting.ini')

KEY = config['API']['KEY']


def gen_grid(cen_X, cen_Y, step, count_X, count_Y):
    '''Generate a matrix of coordinates'''
    x = y = 0
    dx = 0
    dy = -1
    count_X = int(count_X)
    count_Y = int(count_Y)
    step = float(step)
    cen_X = float(cen_X)
    cen_Y = float(cen_Y)
    for i in range(max(count_X, count_Y)**2):
        if (-count_X/2 < x <= count_X/2) and (-count_Y/2 < y <= count_Y/2):
            yield [cen_X + x * step, cen_Y + y * step]
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x + dx, y + dy


def access_API(origin, dest):
    """Acess API and return json."""
    url = API_url.format(origin[0], origin[1], dest[0], dest[1], KEY)
    result = urllib.request.urlopen(url)
    return result


def remap_features():
    """Unpack json to feature."""
    pass


def mapping():
    """Mapping."""
    origin = [input("Origin Lat: "),
              input("Origin Long: ")
              ]
    grid_size = input("Grid size(degree): ")
    grid_x = input("Grid size x: ")
    grid_y = input("Grid size y: ")
    task_name = input("Task name: ")
    if task_name == '':
        task_name = datetime.datetime.now().strftime('%y-%m-%dT%H-%M-%S')
    os.makedirs(os.path.join('result', task_name))

    for i, pt in enumerate(
        gen_grid(origin[1], origin[0], grid_size, grid_x, grid_y)
    ):
        print('Mapping point {}, [{},{}]'.format(i, pt[1], pt[0]))
        with open(
            os.path.join('result', task_name, str(i)+'.json'), 'w'
        ) as temp_file:
            result = json.load(access_API(origin, list(reversed(pt))))
            json.dump(result, temp_file)
        time.sleep(1)


if __name__ == "__main__":
    mode = input('Mapping via API(1) or Remap results?')
    if mode == '1':
        mapping()
