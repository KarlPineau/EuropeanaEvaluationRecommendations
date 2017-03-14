import json
import urllib.parse
import urllib.request

from algorithm.default import default_algorithm
from algorithm.europeanaPublishingFramework import europeana_publishing_framework_algorithm
from algorithm.chronological import chronological_algorithm
from algorithm.agnostic import agnostic_algorithm
from algorithm.random import random_algorithm
from algorithm.typological import typological_algorithm
from findInGraph import get_list_item
from findInGraph import pair_exist
from findInGraph import check_entity_algorithm
from findInGraph import count_deep_item


def wrap(totest):
    if type(totest) is list or type(totest) is dict:
        return map(lambda x: "\"" + x + "\"", totest)
    elif type(totest) is str:
        return "\"" + totest.replace('"', '') + "\""


def stringify(totest, delimiter, wrapBool, wrap):
    if type(totest) is dict:
        if 'def' in totest:
            if wrapBool:
                wrap = wrap(totest['def'])
            else:
                wrap = totest['def']
        elif 'en' in totest:
            if wrapBool:
                wrap = wrap(totest['en'])
            else:
                wrap = totest['en']

        if type(wrap) is list or type(wrap) is dict:
            value = delimiter.join(wrap)
        elif type(wrap) is str:
            value = wrap
        else:
            value = wrap

    elif type(totest) is list:
        if wrapBool:
            wrap = wrap(totest[0])
        else:
            wrap = totest[0]

        if type(wrap) is list or type(wrap) is dict:
            value = delimiter.join(wrap)
        elif type(wrap) is str:
            value = wrap
        else:
            value = wrap

    elif type(totest) is str:
        value = totest

    if type(value) is str:
        return value
    else:
        stringify(value, delimiter, wrapBool)


def get_reference_item(entity_computed):
    response = urllib.request.urlopen(
        'http://sol1.eanadev.org:9191/solr/search_1_shard1_replica2/select?q=europeana_id:"' + entity_computed + '"&rows=1&wt=json')
    result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    # print(result)

    # Computing reference item
    reference_item = False
    if 'response' in result and 'docs' in result['response']:
        for reference_object in result['response']['docs']:
            if reference_object["europeana_id"] == entity_computed:
                reference_item = reference_object
                break

    return reference_item


def computation(entity_computed, level, graph, row, stringify, wrap, algorithms):
    reference_item = get_reference_item(entity_computed)
    docs = []
    if reference_item is not False and reference_item['europeana_id'] == entity_computed:
        for algorithm in algorithms:
            if check_entity_algorithm(entity_computed, algorithm, graph) is False:
                if algorithm == 'default':
                    docs = default_algorithm(reference_item, stringify, wrap, row)
                    # print('default')
                elif algorithm == 'europeanaPublishingFramework':
                    docs = europeana_publishing_framework_algorithm(reference_item, stringify, wrap, row)
                    # print('EPF')
                elif algorithm == 'chronological':
                    docs = chronological_algorithm(reference_item, stringify, wrap, row)
                    # print('Chrono')
                elif algorithm == 'agnostic':
                    docs = agnostic_algorithm(reference_item, stringify, wrap, row)
                    # print('Agnostic')
                elif algorithm == 'random':
                    docs = random_algorithm(reference_item, stringify, wrap, row)
                    # print('Random')
                elif algorithm == 'typological':
                    docs = typological_algorithm(reference_item, stringify, wrap, row)
                    # print('Typological')

                print('comput: '+algorithm)
                # print(docs)
                for key, record in enumerate(docs):
                    if key+1 == row:
                        # In case of API querying, we rebuilt a Solr object
                        if 'id' in record and 'europeana_id' not in record:
                            record['europeana_id'] = record['id']

                        if record['europeana_id'] in get_list_item(record['europeana_id'], graph, []):
                            # Check if this value has been recommended previously
                            # print('re-compute')
                            computation(entity_computed, level, graph, row+1, stringify, wrap, algorithms)
                        elif pair_exist(entity_computed, record['europeana_id'], algorithm, graph) is not False:
                            # print('re-compute2')
                            computation(entity_computed, level, graph, row+1, stringify, wrap, algorithms)
                        elif record['europeana_id'] in entitiesDefault:
                            # print('re-compute3')
                            computation(entity_computed, level, graph, row+1, stringify, wrap, algorithms)
                        else:
                            # Log
                            print(algorithm + ': ' + entity_computed + ' > ' + record['europeana_id'])

                            graph["relations"].append({"algorithm": algorithm, "entity1": entity_computed, "entity2": record['europeana_id']})

                            with open('data/relations.json', 'w') as outfile:
                                json.dump(graph, outfile)

                            # if level < 4 and count_deep_item(entity_computed, graph, 0) < 4:
                                # If not at the level max, we increment
                            #    entity_computed = record['europeana_id']
                            #    computation(entity_computed, level+1, graph, 1, stringify, wrap, algorithms)

#algorithms = [
#    'default',
#    'europeanaPublishingFramework',
#    'chronological',
#    'agnostic',
#    'random',
#    'typological'
#]

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


#with open('data/relations.json') as json_data:
#    relations = json.load(json_data)

#for entity in entitiesDefault:
#     computation(entity, 0, relations, 1, stringify, wrap, algorithms)