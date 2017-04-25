import json
import urllib.parse
import urllib.request
import imghdr
import uuid
import urllib.error
import os
from main import stringify
from main import wrap


with open('data/entities_tree.json') as json_data:
    entities = json.load(json_data)

list = []
count_thumbnail = 0
for europeana_id in entities:
    if 'ee_thumbnail_2' in entities[europeana_id]:
        count_thumbnail += 1
        print(entities[europeana_id]['ee_thumbnail_2'])
        #filename, file_extension = os.path.splitext('thumbnails/'+entities[europeana_id]['ee_thumbnail_2'])
        #print(filename)
        # '/path/to/somefile'
        #print(file_extension)
        #if file_extension != '.jpeg' and file_extension != '.jpg' and file_extension != '.png' and file_extension != '.gif':
        #    list.append(file_extension)
    # else:
    #    entities[europeana_id]['ee_thumbnail_2'] = 'no-image.png'

# with open('data/entities_tree.json', 'w') as outfile:
#    json.dump(entities, outfile)
print(str(count_thumbnail)+'/'+str(len(entities)))
print(list)
