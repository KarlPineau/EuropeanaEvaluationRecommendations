import json
import operator
import collections

with open('export-europeana-eval.json') as json_data:
    proposals = json.load(json_data)

sessions = {}

entitiesDefault = [
    '/2032004/2778',
    '/2021664/search_identifier_umg_items_2d688f4872f6db25b852ad5f6f35663b',
    '/9200365/BibliographicResource_1000055664026',
    '/2021641/publiek_detail_aspx_xmldescid_55194153',
    '/92062/BibliographicResource_1000126129416',
    '/15801/eDipRouteurBML_eDipRouteurBML_aspx_Application_AFFL_26Action_RechercherDirectement_NUID___53__AFFL_3BAfficherVueSurEnregistrement_Vue_Fiche_Principal_3BAfficherFrameset',
    '/2059209/data_sounds_C0023X0047XX_0600',
    '/9200365/BibliographicResource_2000081578901',
    '/9200365/BibliographicResource_2000081569228',
    '/08629/0105'
]

for proposal in proposals:
    if "session-id" in proposal and proposal["session-type"] == "browseEvaluation":
        if proposal["session-id"] not in sessions:
            sessions[proposal["session-id"]] = {}
        sessions[proposal["session-id"]][proposal["browse-id"]] = proposal

print(sessions)

algorithms = []
for id in sessions:
    session = sessions[id]
    algorithmSession = {}
    for proposalId in session:
        proposal = session[proposalId]
        if proposal["browse-choose-item"] is not None:
            for item in proposal["browse-items"]:
                if item["item-item"] == proposal["browse-choose-item"]:
                    algorithmSession[proposal["browse-id"]] = item["item-algorithm"]
        else:
            algorithmSession[proposal["browse-id"]] = "NotInteresting"

    od = collections.OrderedDict(sorted(algorithmSession.items()))
    algorithms.append(od)

countSame = 0
countNotSame = 0
countEntranceDefault = 0
countEntranceEPF = 0
countEntranceChrono = 0
countEntranceTypo = 0
countEntranceAgno = 0
countEntranceRandom = 0
countOutDefault = 0
countOutEPF = 0
countOutChrono = 0
countOutTypo = 0
countOutAgno = 0
countOutRandom = 0
countOutNI = 0
countPairDefault = 0
countPairEPF = 0
countPairChrono = 0
countPairTypo = 0
countPairAgno = 0
countPairRandom = 0


for algo in algorithms:
    if len(algo) > 1:
        prev = None
        for item in algo:
            if prev is None:
                prev = algo[item]
            else:
                if prev == algo[item]:
                    countSame += 1
                    if prev == "default":
                        countPairDefault += 1
                    elif prev == "europeanaPublishingFramework":
                        countPairEPF += 1
                    elif prev == "chronological":
                        countPairChrono += 1
                    elif prev == "typological":
                        countPairTypo += 1
                    elif prev == "agnostic":
                        countPairAgno += 1
                    elif prev == "random":
                        countPairRandom += 1
                else:
                    countNotSame += 1

                if prev == "default":
                    countEntranceDefault += 1
                elif prev == "europeanaPublishingFramework":
                    countEntranceEPF += 1
                elif prev == "chronological":
                    countEntranceChrono += 1
                elif prev == "typological":
                    countEntranceTypo += 1
                elif prev == "agnostic":
                    countEntranceAgno += 1
                elif prev == "random":
                    countEntranceRandom += 1

                if algo[item] == "default":
                    countOutDefault += 1
                elif algo[item] == "europeanaPublishingFramework":
                    countOutEPF += 1
                elif algo[item] == "chronological":
                    countOutChrono += 1
                elif algo[item] == "typological":
                    countOutTypo += 1
                elif algo[item] == "agnostic":
                    countOutAgno += 1
                elif algo[item] == "random":
                    countOutRandom += 1
                elif algo[item] == "NotInteresting":
                    countOutNI += 1
                # print(str(prev)+", "+algo[item])
                prev = algo[item]
print("Same: "+str(countSame))
print("NotSame: "+str(countNotSame))

print("IN Default: "+str(countEntranceDefault))
print("IN EPF: "+str(countEntranceEPF))
print("IN Chrono: "+str(countEntranceChrono))
print("IN Typo: "+str(countEntranceTypo))
print("IN Agno: "+str(countEntranceAgno))
print("IN Random: "+str(countEntranceRandom))

print("OUT Default: "+str(countOutDefault))
print("OUT EPF: "+str(countOutEPF))
print("OUT Chrono: "+str(countOutChrono))
print("OUT Typo: "+str(countOutTypo))
print("OUT Agno: "+str(countOutAgno))
print("OUT Random: "+str(countOutRandom))
print("OUT NI: "+str(countOutNI))

print("PAIR Default: "+str(countPairDefault))
print("PAIR EPF: "+str(countPairEPF))
print("PAIR Chrono: "+str(countPairChrono))
print("PAIR Typo: "+str(countPairTypo))
print("PAIR Agno: "+str(countPairAgno))
print("PAIR Random: "+str(countPairRandom))


