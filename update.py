from pathlib import Path
from ruamel.yaml import YAML
from pprint import pprint
import json
import os
import requests
import sys

def read_data():
    inp = Path('Webserver-1/helm/values.yaml')
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style=None
    with open(str(inp), "r") as yaml_file:
        values_yml = yaml.load(yaml_file)  
    return values_yml 


def update_values(values_json):
    values_json['deployment']['image'] = image_name
    yaml = YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.default_flow_style=None
    with open('values.yaml', 'w') as file:
        yaml.dump(values_json, file)



def commit_to_git():
    os.system("git add *")
    os.system('git commit -m "changing image name"')
    os.system("git push origin main")


if __name__ == '__main__':
    image_name = sys.argv[1] 
    repo = "https://github.com/arif11111/Webserver-hosting.git"
    values_json = read_data()
    print(values_json)
    update_values(values_json)
    commit_to_git()

