import json
import urllib.request
import urllib.parse


def agnostic_algorithm(object, stringify, wrap, row):
    #print(object)
    q = ''

    if "proxy_dcterms_medium" in object:
        q += "(" + stringify(object["proxy_dcterms_medium"], ' AND ', True, wrap) + ")"
    if "proxy_dc_title" in object:
        if q != "":
            q += ' OR '
        q += "(" + stringify(object["proxy_dc_title"], ' AND ', True, wrap) + ")"
    if "proxy_dc_publisher" in object:
        if q != "":
            q += ' OR '
        q += "who:(" + stringify(object["proxy_dc_publisher"], ' AND ', True, wrap) + ")"
    if "proxy_dc_language" in object:
        if q != "":
            q += ' OR '
        q += "(" + stringify(object["proxy_dc_language"], ' AND ', True, wrap) + ")"
    if "proxy_dc_format" in object:
        if q != "":
            q += ' OR '
        q += "(" + stringify(object["proxy_dc_format"], ' AND ', True, wrap) + ")"
    if "edm_datasetName" in object:
        if q != "":
            q += ' OR '
        q += "(" + stringify(object["edm_datasetName"], ' AND ', True, wrap) + ")"
    if "europeana_aggregation_edm_language" in object:
        if q != "":
            q += ' OR '
        q += "(" + stringify(object["europeana_aggregation_edm_language"], ' AND ', True, wrap) + ")"
    if "provider_aggregation_edm_dataProvider" in object:
        if q != "":
            q += ' OR '
        q += "(" + stringify(object["provider_aggregation_edm_dataProvider"], ' AND ', True, wrap) + ")"
    if "provider_aggregation_edm_provider" in object:
        if q != "":
            q += ' OR '
        q += "(" + stringify(object["provider_aggregation_edm_provider"], ' AND ', True, wrap) + ")"
    if "proxy_dc_description" in object:
        if q != "":
            q += ' OR '
        q += "(" + stringify(object["proxy_dc_description"], ' AND ', True, wrap) + ")"
    if "proxy_dc_creator" in object:
        if q != "":
            q += ' OR '
        q += "who:(" + stringify(object["proxy_dc_creator"], ' AND ', True, wrap) + ")"
    if "proxy_dc_contributor" in object:
        if q != "":
            q += ' OR '
        q += "who:(" + stringify(object["proxy_dc_contributor"], ' AND ', True, wrap) + ")"
    if "proxy_dc_type" in object:
        if q != "":
            q += ' OR '
        q += "what:(" + stringify(object["proxy_dc_type"], ' AND ', True, wrap) + ")"
    if "proxy_dc_subject" in object:
        if q != "":
            q += ' OR '
        q += "what:(" + stringify(object["proxy_dc_subject"], ' AND ', True, wrap) + ")"
    if "proxy_dcterms_temporal" in object:
        if q != "":
            q += ' OR '
        q += "when:(" + stringify(object["proxy_dcterms_temporal"], ' AND ', True, wrap) + ")"
    if "proxy_dcterms_created" in object:
        if q != "":
            q += ' OR '
        q += "when:(" + stringify(object["proxy_dcterms_created"], ' AND ', True, wrap) + ")"
    if "proxy_dc_date" in object:
        if q != "":
            q += ' OR '
        q += "when:(" + stringify(object["proxy_dc_date"], ' AND ', True, wrap) + ")"
    if "proxy_dcterms_provenance" in object:
        if q != "":
            q += ' OR '
        q += "where:(" + stringify(object["proxy_dcterms_provenance"], ' AND ', True, wrap) + ")"
    if "proxy_dcterms_spatial" in object:
        if q != "":
            q += ' OR '
        q += "where:(" + stringify(object["proxy_dcterms_spatial"], ' AND ', True, wrap) + ")"

    if "europeana_id" in object:
        if q != "":
            q += ' AND '
        q += "NOT europeana_id:\"" + stringify(object["europeana_id"], ' OR ', True, wrap) + "\""

    print('http://sol1.eanadev.org:9191/solr/search_1_shard1_replica2/select?q=' + urllib.parse.quote_plus(
            q) + '&rows=' + str(row) + '&wt=json')
    response = urllib.request.urlopen(
        'http://sol1.eanadev.org:9191/solr/search_1_shard1_replica2/select?q=' + urllib.parse.quote_plus(
            q) + '&rows=' + str(row) + '&wt=json')
    result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    #print(result)
    #print(len(result['response']['docs']))

    return result['response']['docs']

