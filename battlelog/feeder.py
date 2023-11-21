import sys
import requests
from pymongo import MongoClient
from datetime import datetime

def log_line(line):
    with open('python.log', 'a') as log_file:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dated_line = f'{now} : {line}'
        log_file.write(f'{dated_line}\n')
        print(dated_line)


def retrive_data_from_api(tag):
    with open('api_key', 'r') as arquivo:
        api_key = arquivo.read()
    url = f'https://api.brawlstars.com/v1/players/%23{tag}/battlelog'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log_line(f'Error: {response.status_code}')
        return None

def insert_battle_log(battlelog_json):
    result = collection.insert_one(battlelog_json)
    log_line(f"ID: {result.inserted_id}")

def update_battle_log(battlelog_json, tag, battlelog_persisted):
    persisted_itens = battlelog_persisted.get('items', [])
    json_itens = battlelog_json.get('items', [])

    target_date = persisted_itens[0]['battleTime']
    current_json_date = json_itens[0]["battleTime"]

    max_iterations = 25
    attempts = 0
    wins = 0
    loss = 0
    draw = 0

    while current_json_date != target_date and attempts < max_iterations:
        attempts += 1
        if json_itens[0]["battle"]["result"] == "victory":
            wins += 1
        if json_itens[0]["battle"]["result"] == "defeat":
            loss += 1
        if json_itens[0]["battle"]["result"] == "defeat":
            draw += 1
        current_json_date = json_itens[attempts]["battleTime"]

    log_line(f'Updating {attempts} battle log ')
    log_line(f'wins:{wins} - loss:{loss} - draw:{draw}')
    result = collection.update_one({'tag': tag}, {'$push': {'items': {  '$each': json_itens[:attempts], '$position': 0 }}})

if len(sys.argv) < 2:
    log_line("Tag not found.")
    quit()

tag = sys.argv[1]
log_line(f'Begin with tag: {tag}')

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







