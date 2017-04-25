import json
import urllib.parse
import urllib.request


def get_reference_item(entity_computed):
    response = urllib.request.urlopen(
        'http://sol13.eanadev.org:9191/solr/search_2/select?q=europeana_id:"' + entity_computed + '"&rows=1&wt=json')
    result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    # print(result)

    # Computing reference item
    reference_item = None
    if 'response' in result and 'docs' in result['response']:
        for reference_object in result['response']['docs']:
            if reference_object["europeana_id"] == entity_computed:
                reference_item = reference_object
                break
    return reference_item


def get_property(item, item_property):
    value = None
    if type(item) is dict or type(item) is list:
        if item_property in item:
            value = item[item_property]
    return value


def computation(entity_computed, list_entities):
    reference_item = get_reference_item(entity_computed)
    if reference_item is not None and reference_item['europeana_id'] == entity_computed and reference_item['europeana_id'] not in list_entities:
        print(reference_item['europeana_id'])

        generated_object = {}
        generated_object['europeana_id'] = get_property(reference_item, "europeana_id")
        generated_object['edmDatasetName'] = get_property(reference_item, "edm_datasetName")
        generated_object['language'] = get_property(reference_item, "europeana_aggregation_edm_language")
        generated_object['edmDataProvider'] = get_property(reference_item, "provider_aggregation_edm_dataProvider")
        generated_object['edmIsShownAt'] = get_property(reference_item, "provider_aggregation_edm_isShownAt")
        generated_object['edmIsShownBy'] = get_property(reference_item, "provider_aggregation_edm_isShownBy")
        generated_object['edmProvider'] = get_property(reference_item, "provider_aggregation_edm_provider")
        generated_object['edmRights'] = get_property(reference_item, "provider_aggregation_edm_rights")
        generated_object['edmObject'] = get_property(reference_item, "provider_aggregation_edm_object")
        generated_object['dcDescription'] = get_property(reference_item, "proxy_dc_description")
        generated_object['dcContributor'] = get_property(reference_item, "proxy_dc_contributor")
        generated_object['dcCreator'] = get_property(reference_item, "proxy_dc_creator")
        generated_object['dcDate'] = get_property(reference_item, "proxy_dc_date")
        generated_object['dcFormat'] = get_property(reference_item, "proxy_dc_format")
        generated_object['dcLanguage'] = get_property(reference_item, "proxy_dc_language")
        generated_object['dcPublisher'] = get_property(reference_item, "proxy_dc_publisher")
        generated_object['dcSubject'] = get_property(reference_item, "proxy_dc_subject")
        generated_object['dcTitle'] = get_property(reference_item, "proxy_dc_title")
        generated_object['dcType'] = get_property(reference_item, "proxy_dc_type")
        generated_object['dctermsMedium'] = get_property(reference_item, "proxy_dcterms_medium")
        generated_object['dctermsTemporal'] = get_property(reference_item, "proxy_dcterms_temporal")
        generated_object['dctermsCreated'] = get_property(reference_item, "proxy_dcterms_created")
        generated_object['dctermsProvenance'] = get_property(reference_item, "proxy_dcterms_provenance")
        generated_object['dctermsSpatial'] = get_property(reference_item, "proxy_dcterms_spatial")
        generated_object['edmType'] = get_property(reference_item, "proxy_edm_type")
        generated_object['edmPreview'] = get_property(reference_item, "europeana_aggregation_edm_preview")
        list_entities[generated_object['europeana_id']] = generated_object

with open('data/relations.json') as json_data:
    relations = json.load(json_data)

with open('data/entities_tree.json') as json_data:
    list_entities = json.load(json_data)

for relation in relations['relations']:
    if relation['entity1'] not in list_entities:
        computation(relation['entity1'], list_entities)
    if relation['entity2'] not in list_entities:
        computation(relation['entity2'], list_entities)

with open('data/entities_tree.json', 'w') as outfile:
    json.dump(list_entities, outfile)
