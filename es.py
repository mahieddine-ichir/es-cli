#!/usr/local/bin/python3.5

import configparser
import json
import sys
from os.path import expanduser
import requests
import time


def print_help():
    print("Usage: es <command> help")
    print("Usage: es <command> <sub command> help")


def print_help_index():
    print("Usage: es index help")
    print("Usage: es index create <index name> <index json file>")


# check arguments
if len(sys.argv) == 1:
    print_help()
    exit(1)

# Home directory
home = str(expanduser("~"))


def get_config_key(k):
    config = configparser.ConfigParser()
    config.read(home + "/.es/config")
    if not (config.has_section(get_default_config())):
        raise "There is not such config "+get_default_config()
    return config[get_default_config()][k]


def set_config(k, v):
    config = configparser.ConfigParser()
    config.read(home + "/.es/config")
    default_config = get_default_config()
    if not config.has_section(default_config):
        config[default_config] = {}
    config[default_config][k] = v
    with open(home+"/.es/config", 'w') as configFile:
        config.write(configFile)


def get_default_config():
    config = configparser.ConfigParser()
    config.read(home + "/.es/config")
    return config['DEFAULT']['name']


def use_default_config(sec):
    config = configparser.ConfigParser()
    config.read(home + "/.es/config")
    config['DEFAULT'] = {'name': sec}
    with open(home+"/.es/config", 'w') as configFile:
        config.write(configFile)


def check_current_config():
    config = configparser.ConfigParser()
    config.read(home + "/.es/config")
    return config.has_section('current')


def create_index(url, index, file):
    with open(file) as f:
        json_data = json.load(f)
    r = requests.put(url + "/" + index, json=json_data)
    print(r.json())


def reindex(url, old_index, new_index):
    json_data = {
        "source": {"index": old_index},
        "dest": {"index": new_index}
        }
    r = requests.post(url+"/_reindex?wait_for_completion=false", json=json_data)
    print(r.json())


def check_task(url, task_id):
    while True:
        r = requests.get(url+"/_tasks/"+task_id)
        print(r.json())
        print()
        time.sleep(3)


arg1 = sys.argv[1]

if arg1 == 'help':
    print_help()

elif arg1 == 'use':
    sec = sys.argv[2]
    use_default_config(sec)

elif arg1 == 'config':
    if sys.argv[2] == 'set':
        key = sys.argv[3]
        value = sys.argv[4]
        set_config(key, value)

elif arg1 == 'index':
    arg2 = sys.argv[2]
    if arg2 == 'help':
        print_help_index()
    elif arg2 == 'create':
        index_name = sys.argv[3]
        index_jsonFile = sys.argv[4]
        create_index(get_config_key('url'), index_name, index_jsonFile)

elif arg1 == 'reindex':
    old_index = sys.argv[2]
    new_index = sys.argv[3]
    reindex(get_config_key('url'), old_index, new_index)

elif arg1 == 'task':
    task_id = sys.argv[2]
    check_task(get_config_key('url'), task_id)
