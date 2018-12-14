import json




def getConfig(path='config.json'):
    """reads configuration file and return a python dict"""
    with open(path) as f:
        data = f.readlines()
    conf_str = ''
    for line in data:
        conf_str += line
    return json.loads(conf_str)