import json

errors = open('Data/testing/mw_data/mw_errors.json')

data = json.load(errors)

print(len(data))