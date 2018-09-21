"""
Main script of traveling time
"""

import configparser
import json
import os
import urllib

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

print(config['API']['KEY'])
