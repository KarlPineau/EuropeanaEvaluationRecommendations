import json
import urllib.request
import urllib.parse


def europeana_publishing_framework_algorithm(object, stringify, wrap, row):
    # print(object)
    q = ''
    spec = ''

    if stringify(object['proxy_edm_type'], '', False, wrap) == 'IMAGE':
        spec = "qf=IMAGE_SIZE%3Amedium&qf=IMAGE_SIZE%3Alarge&qf=IMAGE_SIZE%3Aextra_large&thumbnail=true"
    elif stringify(object['proxy_edm_type'], '', False, wrap) == 'TEXT':
        spec = "qf=TEXT_FULLTEXT%3Atrue"
    elif stringify(object['proxy_edm_type'], '', False, wrap) == 'SOUND':
        spec = "qf=SOUND_DURATION%3Avery_short&qf=SOUND_DURATION%3Ashort&qf=SOUND_DURATION%3Amedium&qf=SOUND_DURATION%3Along"
    elif stringify(object['proxy_edm_type'], '', False, wrap) == 'VIDEO':
        spec = "qf=VIDEO_DURATION%3Ashort&qf=VIDEO_DURATION%3Amedium&qf=VIDEO_DURATION%3Along"
    elif stringify(object['proxy_edm_type'], '', False, wrap) == '3D':
        spec = "qf=TYPE:3D"

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
    if "proxy_dc_title" in object:
        if q != "":
            q += ' OR '
        q += "title:(" + stringify(object["proxy_dc_title"], ' OR ', True, wrap) + ")"
    if "provider_aggregation_edm_dataProvider" in object:
        if q != "":
            q += ' OR '
        q += "DATA_PROVIDER:" + stringify(object["provider_aggregation_edm_dataProvider"],
                                                                  ' OR ', True, wrap) + ""
    if "europeana_id" in object:
        if q != "":
            q += ' AND '
        q += "NOT europeana_id:\"" + stringify(object["europeana_id"], ' OR ', True, wrap) + "\""

    print('https://www.europeana.eu/api/v2/search.json?query=' + urllib.parse.quote_plus(
            q) + '&' + spec + '&rows=' + str(row) + '&wskey=api2demo')
    response = urllib.request.urlopen(
        'https://www.europeana.eu/api/v2/search.json?query=' + urllib.parse.quote_plus(
            q) + '&' + spec + '&rows=' + str(row) + '&wskey=api2demo')
    result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    #print(result)
    #print(len(result['items']))

    return result['items']