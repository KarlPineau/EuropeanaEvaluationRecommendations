import re
import math
import json
import operator
from collections import Counter
import collections

WORD = re.compile(r'\w+')


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

##

with open('export-europeana-eval.json') as json_data:
    proposals = json.load(json_data)

with open('../data/entities_tree.json') as json_data:
    entities = json.load(json_data)

# Computation for browse proposal:
arrayBrowse = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
for proposal in proposals:
    if "browse-id" in proposal and proposal["browse-choose-item"] is not None:
        arrayInternalProposal = []
        titleReference = ""
        if "browse-reference-item" in proposal and proposal["browse-reference-item"] in entities and "dcTitle" in entities[proposal["browse-reference-item"]]:
            titleArrayReference = entities[proposal["browse-reference-item"]]["dcTitle"]
            if type(titleArrayReference) == list:
                if len(titleArrayReference) >= 1 and type(titleArrayReference[0]) == str and titleArrayReference[0] != "":
                    titleReference = titleArrayReference[0]
            elif type(titleArrayReference) == dict:
                if len(titleArrayReference) >= 1 and "en" in titleArrayReference and type(titleArrayReference["en"]) == str and titleArrayReference["en"] != "":
                    titleReference = titleArrayReference["en"]

        for item in proposal["browse-items"]:
            titleItem = ""
            if "item-item" in item and item["item-item"] in entities and "dcTitle" in entities[item["item-item"]]:
                titleArrayItem = entities[item["item-item"]]["dcTitle"]
                if type(titleArrayItem) == list:
                    if len(titleArrayItem) >= 1 and type(titleArrayItem[0]) == str and titleArrayItem[0] != "":
                        titleItem = titleArrayItem[0]
                elif type(titleArrayItem) == dict:
                    if len(titleArrayItem) >= 1 and "en" in titleArrayItem and type(titleArrayItem["en"]) == str and titleArrayItem["en"] != "":
                        titleItem = titleArrayItem["en"]
            vector1 = text_to_vector(titleReference)
            vector2 = text_to_vector(titleItem)
            cosine = get_cosine(vector1, vector2)
            arrayInternalProposal.append({"cosine": cosine, "item": item["item-item"], "algorithm": item["item-algorithm"]})

        newOrder = sorted(arrayInternalProposal, key=lambda k: k['cosine'])
        #print(newOrder)
        countOrder = 1
        for item in newOrder:
            if item["item"] == proposal["browse-choose-item"] and item["algorithm"] == "default":
                arrayBrowse[countOrder].append(item["cosine"])
            countOrder += 1

for value in arrayBrowse:
    sum = 0
    for cosine in arrayBrowse[value]:
        sum += cosine
    if len(arrayBrowse[value]) > 0:
        print(str(value) + ": " + str(sum / len(arrayBrowse[value])) + " - " + str(len(arrayBrowse[value])))
    else:
        print(str(value) + ": 0" )

sum = 0
lenS = 0
for value in arrayBrowse:
    for cosine in arrayBrowse[value]:
        sum += cosine
        lenS += 1
print("Total: " + str(sum / lenS) + " - " + str(lenS))
