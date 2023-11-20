import sys
import requests
from pymongo import MongoClient

def retrive_data_from_api(tag):
    with open('api_key', 'r') as arquivo:
        api_key = arquivo.read()
    url = f'https://api.brawlstars.com/v1/players/%23{tag}/battlelog'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f'Success: {response.status_code}')
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return None

def insert_battle_log(battlelog_json):
    result = collection.insert_one(battlelog_json)
    print(f"ID: {result.inserted_id}")

def update_battle_log(battlelog_json, tag, battlelog_persisted):
    persisted_itens = battlelog_persisted.get('items', [])
    json_itens = battlelog_json.get('items', [])

    target_date = persisted_itens[0]['battleTime']
    current_json_date = json_itens[0]["battleTime"]
    
    max_iterations = 25
    attempts = 0

    while current_json_date != target_date and attempts < max_iterations:
        print("Not found yet.")
        attempts += 1
        current_json_date = json_itens[attempts]["battleTime"]

    print(f'Updating {attempts} battle log ')
    result = collection.update_one({'tag': tag}, {'$push': {'items': {  '$each': json_itens[:attempts], '$position': 0 }}})

if len(sys.argv) < 2:
    print("Tag not found.")
    quit()

tag = sys.argv[1]
print(f'Begin with tag: {tag}')

client = MongoClient()
db = client['brawlstars_crawler']
collection = db['battlelog']

battlelog_json = retrive_data_from_api(tag)

if battlelog_json:
    battlelog_json['tag'] = tag
    battlelog_persisted = collection.find_one({'tag': tag})
    if battlelog_persisted:
        update_battle_log(battlelog_json, tag, battlelog_persisted)
    else:
        insert_battle_log(battlelog_json)







