import json
import urllib.request
import urllib.parse
from random import randint


def random_algorithm(object, stringify, wrap, row):
    # print(object)
    q = ''

    countries = ["Austria", "Belgium", "Bulgaria", "Czech Republic", "Denmark", "Estonia", "Finland", "France",
                       "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Israel", "Italy", "Latvia", "Lithuania",
                       "Luxembourg", "Malta", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Russia",
                       "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom"]
    country = countries[randint(0, (len(countries)-1))]
    types = ['IMAGE', 'TEXT', 'ART', 'MUSIC']
    type = types[randint(0, (len(types)-1))]
    sorts = ['timestamp_update', 'timestamp_created', 'europeana_id']
    sort = sorts[randint(0, (len(sorts)-1))]
    sortsOrder = ['DESC', 'ASC']
    sortOrder = sortsOrder[randint(0, (len(sortsOrder)-1))]

    art = 'qf=(DATA_PROVIDER:"Östasiatiska museet" NOT TYPE:TEXT) OR (DATA_PROVIDER:"Medelhavsmuseet") OR (DATA_PROVIDER:"Rijksmuseum") OR (europeana_collectionName: "91631_Ag_SE_SwedishNationalHeritage_shm_art") OR (DATA_PROVIDER:"Bibliothèque municipale de Lyon") OR (DATA_PROVIDER:"Museu Nacional d\'Art de Catalunya") OR (DATA_PROVIDER:"Victoria and Albert Museum") OR (DATA_PROVIDER:"Slovak national gallery") OR (DATA_PROVIDER:"Thyssen-Bornemisza Museum") OR (DATA_PROVIDER:"Museo Nacional del Prado") OR (DATA_PROVIDER:"Statens Museum for Kunst") OR (DATA_PROVIDER:"Hungarian University of Fine Arts, Budapest") OR (DATA_PROVIDER:"Hungarian National Museum") OR (DATA_PROVIDER:"Museum of Applied Arts, Budapest") OR (DATA_PROVIDER:"Szépművészeti Múzeum") OR (DATA_PROVIDER:"Museum of Fine Arts - Hungarian National Gallery, Budapest") OR (DATA_PROVIDER:"Schola Graphidis Art Collection. Hungarian University of Fine Arts - High School of Visual Arts, Budapest") OR (PROVIDER:"Ville de Bourg-en-Bresse") OR (DATA_PROVIDER:"Universitätsbibliothek Heidelberg") OR ((what:("fine art" OR "beaux arts" OR "bellas artes" OR "belle arti" OR "schone kunsten" OR konst OR "bildende kunst" OR "Opere d\'arte visiva" OR "decorative arts" OR konsthantverk OR "arts décoratifs" OR paintings OR schilderij OR pintura OR peinture OR dipinto OR malerei OR måleri OR målning OR sculpture OR skulptur OR sculptuur OR beeldhouwwerk OR drawing OR poster OR tapestry OR gobelin OR jewellery OR miniature OR prints OR träsnitt OR holzschnitt OR woodcut OR lithography OR chiaroscuro OR "old master print" OR estampe OR porcelain OR mannerism OR rococo OR impressionism OR expressionism OR romanticism OR "Neo-Classicism" OR "Pre-Raphaelite" OR Symbolism OR Surrealism OR Cubism OR "Art Deco" OR "Art Déco" OR Dadaism OR "De Stijl" OR "Pop Art" OR "art nouveau" OR "art history" OR "http://vocab.getty.edu/aat/300041273" OR "histoire de l\'art" OR kunstgeschichte OR "estudio de la historia del arte" OR Kunstgeschiedenis OR "illuminated manuscript" OR buchmalerei OR enluminure OR "manuscrito illustrado" OR "manoscritto miniato" OR boekverluchting OR kalligrafi OR calligraphy OR exlibris)) AND (provider_aggregation_edm_isShownBy:*)) NOT (what: "printed serial" OR what:"printedbook" OR "printing paper" OR "printed music" OR DATA_PROVIDER:"NALIS Foundation" OR DATA_PROVIDER:"Ministère de la culture et de la communication, Musées de France" OR DATA_PROVIDER:"CER.ES: Red Digital de Colecciones de museos de España" OR PROVIDER:"OpenUp!" OR PROVIDER:"BHL Europe" OR PROVIDER:"EFG - The European Film Gateway" OR DATA_PROVIDER: "Malta Aviation Museum Foundation" OR DATA_PROVIDER:"National Széchényi Library - Digital Archive of Pictures" OR PROVIDER:"Swiss National Library")';
    music = 'qf=(PROVIDER:"Europeana Sounds" AND provider_aggregation_edm_isShownBy:* AND music) OR (DATA_PROVIDER: "National Library of France" AND musique) OR (DATA_PROVIDER:"Sächsische Landesbibliothek - Staats- und Universitätsbibliothek Dresden" AND TYPE:SOUND) OR (edm_datasetName:" 09301_Ag_EU_Judaica_mcy78") OR (DATA_PROVIDER:"Kirsten Flagstadmuseet") OR (DATA_PROVIDER:"Ringve Musikkmuseum") OR (DATA_PROVIDER:"Netherlands Institute for Sound and Vision" AND provider_aggregation_edm_isShownBy:* AND (music OR muziek)) OR  (DATA_PROVIDER:"TV3 Televisió de Catalunya (TVC)" AND provider_aggregation_edm_isShownBy:* AND musica) OR (PROVIDER:"Institut National de l\'Audiovisuel" AND (musique OR opera OR pop OR rock OR concert OR chanson OR interpretation)) OR ((what:(music OR musique OR musik OR musica OR musicales OR "zenés előadás" OR "notated music" OR "folk songs" OR jazz OR "sheet music" OR score OR "musical instrument" OR partitur OR partituras OR gradual OR libretto OR oper OR concerto OR symphony OR sonata OR fugue OR motet OR saltarello OR organum OR ballade OR chanson OR laude OR madrigal OR pavane OR toccata OR cantata OR minuet OR partita OR sarabande OR sinfonia OR hymnes OR lied OR "music hall" OR quartet OR quintet OR requiem OR rhapsody OR scherzo OR "sinfonia concertante" OR waltz OR ballet OR zanger OR sangerin OR chanteur OR chanteuse OR cantante OR composer OR compositeur OR orchestra OR orchester OR orkester OR orchestre OR concierto OR konsert OR konzert OR koncert OR gramophone OR "record player" OR phonograph OR fonograaf OR fonograf OR grammofon OR skivspelare OR "wax cylinder" OR jukebox OR "cassette deck" OR "cassette player")) AND (provider_aggregation_edm_isShownBy:*)) OR ("gieddes samling") OR (musik AND DATA_PROVIDER:"Universitätsbibliothek Heidelberg") OR (antiphonal AND DATA_PROVIDER:"Bodleian Libraries, University of Oxford") OR (edm_datasetName:"2059208_Ag_EU_eSOUNDS_1020_CNRS-CREM") OR (title:(gradual OR antiphonal) AND edm_datasetName: "2021003_Ag_FI_NDL_fragmenta") NOT (DATA_PROVIDER:"Progetto ArtPast- CulturaItalia" OR DATA_PROVIDER:"Internet Culturale" OR DATA_PROVIDER:"Accademia Nazionale di Santa Cecilia" OR DATA_PROVIDER:"Regione Umbria" OR DATA_PROVIDER:"Regione Emilia Romagna" OR DATA_PROVIDER:"Regione Lombardia" OR DATA_PROVIDER:"Regione Piemonte" OR DATA_PROVIDER:"National Széchényi Library - Hungarian Electronic Library" OR DATA_PROVIDER:"Rijksdienst voor het Cultureel Erfgoed" OR DATA_PROVIDER:"Phonogrammarchiv - Österreichische Akademie der Wissenschaften; Austria" OR DATA_PROVIDER:"Ministère de la culture et de la communication, Musées de France" OR DATA_PROVIDER:"CER.ES: Red Digital de Colecciones de museos de España" OR DATA_PROVIDER:"MuseiD-Italia" OR DATA_PROVIDER:"Narodna biblioteka Srbije - National Library of Serbia" OR DATA_PROVIDER:"National and University Library in Zagreb" OR DATA_PROVIDER:"National Széchényi Library - Digital Archive of Pictures" OR DATA_PROVIDER:"Vast-Lab" OR DATA_PROVIDER:"Herzog August Bibliothek Wolfenbüttel" OR DATA_PROVIDER:"Centro de Documentación de FUNDACIÓN MAPFRE" OR PROVIDER:"OpenUp!" OR edm_datasetName:"9200123_Ag_EU_TEL_a1023_Sibiu" OR edm_datasetName:"2048319_Ag_EU_ApeX_NLHaNA" OR edm_datasetName:"2059202_Ag_EU_eSOUNDS_1004_Rundfunk" OR edm_datasetName:"09335_Ag_EU_Judaica_cfmj4" OR edm_datasetName:"09326_Ag_EU_Judaica_cfmj3" OR what:"opere d\'arte visiva" OR what:"operating rooms" OR what:"operating systems" OR what:"co-operation" OR what:operation)';

    if "europeana_id" in object:
        if q != "":
            q += ' AND '
        q += "NOT europeana_id:\"" + stringify(object["europeana_id"], ' OR ', True, wrap) + "\""

    if type.upper() == 'IMAGE':
        query = 'https://www.europeana.eu/api/v2/search.json?query='+urllib.parse.quote_plus(q)+'&thumbnail=true&qf=TYPE:'+type.upper()+'&qf=COUNTRY:'+urllib.parse.quote_plus(country.lower())+'&wskey=api2demo&rows='+str(row)+'&sort='+sort+'+'+sortOrder
    elif type.upper() == 'TEXT':
        query = 'https://www.europeana.eu/api/v2/search.json?query='+urllib.parse.quote_plus(q)+'&qf=TEXT_FULLTEXT:true&qf=TYPE:'+type.upper()+'&qf=COUNTRY:'+urllib.parse.quote_plus(country.lower())+'&wskey=api2demo&rows='+str(row)+'&sort='+sort+'+'+sortOrder
    elif type.upper() == 'ART':
        query = 'https://www.europeana.eu/api/v2/search.json?query='+urllib.parse.quote_plus(q)+'&'+urllib.parse.quote_plus(art)+'&qf=COUNTRY:'+urllib.parse.quote_plus(urllib.parse.quote_plus(country.lower()))+'&wskey=api2demo&rows='+str(row)+'&sort='+sort+'+'+sortOrder
    elif type.upper() == 'MUSIC':
        query = 'https://www.europeana.eu/api/v2/search.json?query='+urllib.parse.quote_plus(q)+'&'+urllib.parse.quote_plus(music)+'&qf=COUNTRY:'+urllib.parse.quote_plus(country.lower())+'&qf=SOUND_DURATION:very_short&qf=SOUND_DURATION:short&qf=SOUND_DURATION:medium&qf=SOUND_DURATION:long&qf=SOUND_HQ:true&wskey=api2demo&rows='+str(row)+'&sort='+sort+'+'+sortOrder

    print(query)
    response = urllib.request.urlopen(query)
    result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    # print(result)
    # print(len(result['response']['docs']))

    return result['items']
