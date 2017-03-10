def pair_exist(entity, recommendation, algorithm, graph):
    result = False;
    for pair in graph:
        if ((pair['entity1'] == entity and pair['entity2'] == recommendation) or
                (pair['entity2'] == entity and pair['entity1'] == recommendation)) and pair['algorithm'] == algorithm:
            result = True
            break
    return result


def get_list_item(entity, graph, list_entities):
    for pair in graph:
        if pair['entity2'] == entity:
            list_entities.append(pair['entity1'])
            return get_list_item(pair['entity1'], graph, list_entities)
    return []


def count_deep_item(entity, graph, count):
    for pair in graph:
        if pair['entity2'] == entity:
            count += 1
            if getParent(pair['entity1'], graph) is not False:
                return count_deep_item(pair['entity1'], graph, count)
            else:
                break
    return count


def getParent(entity, graph):
    for pair in graph:
        if pair['entity2'] == entity:
            return pair['entity1']
    return False


def check_entity_algorithm(entity, algorithm, graph):
    result = False
    for pair in graph:
        if pair['entity1'] == entity and pair['algorithm'] == algorithm:
            result = True
            break
    return result
