from pymongo import MongoClient

client = MongoClient('mongodb://144.76.218.178:27017/')
db = client.evaluation
collection = db.corpus

langs = {}
itemsError = []
errors = 0
total = 0

for post in collection.find():
    if 'proxies' in post['record'] and 'language' in post['record']['proxies'][0] and 'literal' in post['record']['proxies'][0]['language']:
        langItem = post['record']['proxies'][0]['language']['literal'][0]
        if langItem in langs:
            langs[langItem] += 1
        else:
            langs[langItem] = 1
        total += 1
    else:
        itemsError.append(post['about'])
        errors += 1

print(langs)
print('total > '+str(total))
print('errors > '+str(errors))
print(itemsError)