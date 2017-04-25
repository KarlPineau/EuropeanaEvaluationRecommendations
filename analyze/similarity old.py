
# Computation for single proposal:
array = {1: [], 2: [], 3: [], 4: [], 5: [], 99: [], 100: []}
for proposal in proposals:
    if "single-id" in proposal and proposal["single-rate-value"] is not None:
        titleReference = ""
        titleSuggested = ""
        if "single-reference-item" in proposal and proposal["single-reference-item"] in entities and "dcTitle" in entities[proposal["single-reference-item"]]:
            titleArrayReference = entities[proposal["single-reference-item"]]["dcTitle"]
            if type(titleArrayReference) == list:
                if len(titleArrayReference) >= 1 and type(titleArrayReference[0]) == str and titleArrayReference[0] != "":
                    titleReference = titleArrayReference[0]
            elif type(titleArrayReference) == dict:
                if len(titleArrayReference) >= 1 and "en" in titleArrayReference and type(titleArrayReference["en"]) == str and titleArrayReference["en"] != "":
                    titleReference = titleArrayReference["en"]

        if "single-suggested-item" in proposal and proposal["single-suggested-item"] in entities and "dcTitle" in entities[proposal["single-suggested-item"]]:
            titleArraySuggested = entities[proposal["single-suggested-item"]]["dcTitle"]
            if type(titleArraySuggested) == list:
                if len(titleArraySuggested) >= 1 and type(titleArraySuggested[0]) == str and titleArraySuggested[0] != "":
                    titleSuggested = titleArraySuggested[0]
            elif type(titleArraySuggested) == dict:
                if len(titleArraySuggested) >= 1 and "en" in titleArraySuggested and type(
                        titleArraySuggested["en"]) == str and titleArraySuggested["en"] != "":
                    titleSuggested = titleArraySuggested["en"]

        vector1 = text_to_vector(titleReference)
        vector2 = text_to_vector(titleSuggested)
        cosine = get_cosine(vector1, vector2)
        array[proposal["single-rate-value"]].append(cosine)

print(array)

for line in array:
    sum = 0
    for value in array[line]:
        sum += value
    print(str(line)+": "+str(sum/len(array[line]))+" - "+str(len(array[line])))

sum = 0
lenS = 0
for line in array:
    for value in array[line]:
        sum += value
        lenS += 1
print("General similarity : "+str(sum/lenS)+" - "+str(lenS))
