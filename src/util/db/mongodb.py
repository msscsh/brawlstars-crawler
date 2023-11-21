import os, sys
from pymongo import MongoClient

project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)
from util.logger import log_line

def get_db_player_battlelog_data(tag):
	log_line(f'Retriving player battlelog')
	collection=use_collection_battlelog()
	player_battlelog_persisted = collection.find_one({'tag': tag})
	return player_battlelog_persisted

def insert_db_player_battlelog_data(tag, api_player_battlelog):
    log_line(f'Inserting player with battlelog')
    collection = use_collection_battlelog()
    api_player_battlelog['tag'] = tag
    result = collection.insert_one(api_player_battlelog)	

def update_db_player_battlelog_data(tag, api_player_battlelog_items):
    log_line(f'Updating {len(api_player_battlelog_items)} battlelog item(s)')
    collection = use_collection_battlelog()
    result = collection.update_one({'tag': tag}, {'$push': {'items': {  '$each': api_player_battlelog_items, '$position': 0 }}})

def increase_player_battelog_column(tag, name):
    log_line(f'One {name} to player {tag}')
    collection = use_collection_battlelog()
    collection.update_one({'tag': tag}, {"$inc": {name: 1}})
    
def init_db_brawlstars_crawler():
	client = MongoClient()
	db = client['brawlstars_crawler']
	return db

def use_collection_battlelog():
	db = init_db_brawlstars_crawler()
	collection = db['battlelog']
	return collection

print('imported mongodb')