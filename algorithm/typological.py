import json
import urllib.request
import urllib.parse


def typological_algorithm(object, stringify, wrap, row):
    # print(object)
    q = ''

    if "proxy_dc_type" in object or "proxy_dc_subject" in object or "proxy_dc_creator" in object or "proxy_dc_contributor" in object or "proxy_dcterms_provenance" in object or "proxy_dcterms_spatial" in object:
        if "proxy_dc_type" in object:
            q += "what:(" + stringify(object["proxy_dc_type"], ' OR ', True, wrap) + ")"
        if "proxy_dc_subject" in object:
            if q != "":
                q += ' OR '
            q += "what:(" + stringify(object["proxy_dc_subject"], ' OR ', True, wrap) + ")"
        if "proxy_dc_creator" in object:
            if q != "":
                q += ' OR '
            q += "who:(" + stringify(object["proxy_dc_creator"], ' OR ', True, wrap) + ")"
        if "proxy_dc_contributor" in object:
            if q != "":
                q += ' OR '
            q += "who:(" + stringify(object["proxy_dc_contributor"], ' OR ', True, wrap) + ")"
        if "proxy_dcterms_provenance" in object:
            if q != "":
                q += ' OR '
            q += "where:(" + stringify(object["proxy_dcterms_provenance"], ' OR ', True, wrap) + ")"
        if "proxy_dcterms_spatial" in object:
            if q != "":
                q += ' OR '
            q += "where:(" + stringify(object["proxy_dcterms_spatial"], ' OR ', True, wrap) + ")"

        europeana_id_q = ''
        if "europeana_id" in object:
            europeana_id_q += "AND NOT europeana_id:\"" + stringify(object["europeana_id"], ' OR ', True, wrap) + "\""

        print('http://sol1.eanadev.org:9191/solr/search_1_shard1_replica2/select?q=%28' + urllib.parse.quote_plus(q) + '%29' + urllib.parse.quote_plus(europeana_id_q) + '&rows=' + str(row) + '&wt=json')
        response = urllib.request.urlopen('http://sol1.eanadev.org:9191/solr/search_1_shard1_replica2/select?q=%28' + urllib.parse.quote_plus(q) + '%29' + urllib.parse.quote_plus(europeana_id_q) +  '&rows=' + str(row) + '&wt=json')
        result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        # print(result)
        # print(len(result['response']['docs']))

        return result['response']['docs']
    else:
        print('no typological metadata')
        return {}
