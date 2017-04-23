import json
import operator

with open('export-europeana-eval.json') as json_data:
    proposals = json.load(json_data)

countItem = 0
items = []
sessions = []

for proposal in proposals:
    if "browse-id" in proposal and proposal["session-is-contextualized"] is True:
        if proposal["session-id"] not in proposal:
            items.append(proposal["browse-id"])
            sessions.append(proposal["session-id"])

print(len(items))
