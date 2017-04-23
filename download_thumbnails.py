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

count_thumbnail = 0
for europeana_id in entities:
    if 'ee_thumbnail_2' in entities[europeana_id]:
        count_thumbnail += 1
print(str(count_thumbnail)+'/'+str(len(entities)))


def rename_file(file_name, entities, europeana_id):
    file_extension = imghdr.what('./thumbnails/' + file_name)
    if file_extension is not None:
        new_name = uuid.uuid4()
        os.rename('./thumbnails/' + file_name, './thumbnails/' + str(new_name) + '.' + file_extension)
        entities[europeana_id]['ee_thumbnail_2'] = str(new_name) + '.' + file_extension
        print(str(europeana_id) + ': ' + str(str(new_name) + '.' + file_extension))
        with open('data/entities_tree.json', 'w') as outfile:
            json.dump(entities, outfile)
        return True
    else:
        return False

for europeana_id in entities:
    if 'ee_thumbnail_2' not in entities[europeana_id]:
        url = None
        listThumbnailProperties = ['edmObject', 'edmPreview', 'edmIsShownBy', 'none']
        isDownload = False
        for propertyThumbnail in listThumbnailProperties:
            if propertyThumbnail == 'none':
                url = 'http://europeana-evaluation.karl-pineau.fr/web/images/no_image_available.png'
                try:
                    file_name = url.split('/')[-1]
                    if len(file_name) > 250:
                        file_name = file_name[:250]
                    u = urllib.request.urlretrieve(url, './thumbnails/' + file_name)
                    isDownload = rename_file(file_name, entities, europeana_id)
                    break
                except urllib.error.URLError as e:
                    print(e.reason)
                except UnicodeEncodeError:
                    print("There was an error encrypting...")
                except IsADirectoryError:
                    print("There was an error for directory...")
                except ConnectionResetError:
                    print("Connection reset by peer ...")
                except TimeoutError:
                    print("TimeoutError ...")
            elif propertyThumbnail in entities[europeana_id] and entities[europeana_id][propertyThumbnail] is not None:
                url = stringify(entities[europeana_id][propertyThumbnail], ' OR ', False, wrap)
                try:
                    if url != '':
                        file_name = url.split('/')[-1]
                        if len(file_name) > 250:
                            file_name = file_name[:250]
                        u = urllib.request.urlretrieve(url, './thumbnails/' + file_name)
                        isDownload = rename_file(file_name, entities, europeana_id)
                        break
                except urllib.error.URLError as e:
                    print(e.reason)
                except UnicodeEncodeError:
                    print("There was an error encrypting...")
                except IsADirectoryError:
                    print("There was an error for directory...")
                except ConnectionResetError:
                    print("Connection reset by peer ...")
                except TimeoutError:
                    print("TimeoutError ...")

            if isDownload is True:
                break
