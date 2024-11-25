import json

with open('expeditions.json') as file:
    expeditions = json.load(file)

print(expeditions)    