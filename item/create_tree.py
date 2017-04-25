import json
import urllib.parse
import urllib.request
from pprint import pprint

with open('data/relations.json') as json_data:
    relations = json.load(json_data)['relations']

with open('data/entities_tree.json') as json_data:
    entities = json.load(json_data)

level = 0
count_level = {}
nb_entities_computed = 0
while nb_entities_computed < len(entities):
    count_level[level] = 0
    if level == 0:
        for europeana_id in entities:
            level_zero = True
            for relation in relations:
                if relation['entity2'] == europeana_id:
                    level_zero = False

            if level_zero is True:
                entities[europeana_id]['ee_level'] = 0
                nb_entities_computed += 1
                print('0: '+str(nb_entities_computed)+' > '+europeana_id)
                count_level[level] += 1
    else:
        for europeana_id in entities:
            for relation in relations:
                if relation['entity2'] == europeana_id:
                    parent = relation['entity1']
                    if parent in entities and 'ee_level' in entities[parent]:
                        entities[europeana_id]['ee_level'] = entities[parent]['ee_level']+1
                        entities[europeana_id]['ee_parent'] = parent
                        nb_entities_computed += 1
                        print(str(level)+': '+str(nb_entities_computed)+' > '+europeana_id)
                        count_level[level] += 1
    level += 1

pprint(count_level)

with open('data/entities_tree.json', 'w') as outfile:
    json.dump(entities, outfile)
