"""
Main script of traveling time
"""

import configparser
import json
import os
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
    return result.read()


def remap_features():
    """Unpack json to feature."""
    pass


def mapping(origin, grid_size, grid_x, grid_y):
    """Mapping."""
    pass


origin = [24.127682, 121.173583]
dest = [24.151994, 121.194043]

print(access_API(origin, dest))
