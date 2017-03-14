import json
import urllib.parse
import urllib.request
from pprint import pprint
from main import computation
from main import stringify
from main import wrap
import random

with open('data/relations.json') as json_data:
    relations = json.load(json_data)

with open('data/entities_tree.json') as json_data:
    entities = json.load(json_data)

level = 4
algorithms_missing = {}
algorithms_missing_id = []

for europeana_id in entities:
    if 'ee_level' in entities[europeana_id] and entities[europeana_id]['ee_level'] == level:
        # print(entities[europeana_id])
        algorithms = [
            'default',
            'europeanaPublishingFramework',
            'chronological',
            'agnostic',
            'random',
            'typological'
        ]
        algorithms_done = []

        for relation in relations['relations']:
            if relation['entity1'] == europeana_id:
                algorithms_done.append(relation['algorithm'])
        if len(algorithms_done) > 0 and len(set(algorithms).difference(algorithms_done)) > 0:
            algorithms_missing[europeana_id] = set(algorithms).difference(algorithms_done)
            algorithms_missing_id.append(europeana_id)
        else:
            algorithms_missing[europeana_id] = algorithms
            algorithms_missing_id.append(europeana_id)

random.shuffle(algorithms_missing_id)
print(algorithms_missing)
print(len(algorithms_missing_id))
for europeana_id in algorithms_missing_id:
    print(algorithms_missing[europeana_id])
    computation(europeana_id, level, relations, 1, stringify, wrap, algorithms_missing[europeana_id])