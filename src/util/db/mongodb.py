import os, sys
from pymongo import MongoClient
from datetime import datetime

project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)
from util.logger import log_line, log_line_in_debug

def clear_monitored_players():
	collection = use_collection_battlelog()
	collection.update_many({}, {'$set': {'isMonitored': 0}})
	# collection.update_many({}, {"$unset": {"battles": []}})
	
def clear_players_from_club():
	collection = use_collection_battlelog()
	collection.update_many({}, {'$set': {'isBRZ': 0}})

def set_db_player_field_value(tag, field, value):
	log_line(f'Setting players({tag}) field {field}')
	collection = use_collection_battlelog()
	result = collection.update_one({'tag': tag}, {'$set': {f'{field}': value }})

def get_db_ranking_player_battlelog_data():
	log_line(f'Retriving ranking player battlelog')
	collection = use_collection_battlelog()
	ranking = collection.find({'isBRZ': 1}).sort('points', -1).limit(90)
	return ranking

def get_db_player_battlelog_data(tag):
	log_line(f'Retriving player battlelog')
	collection = use_collection_battlelog()
	player_battlelog_persisted = collection.find_one({'tag': tag})
	return player_battlelog_persisted

def insert_db_player_battlelog_data(tag, api_player_battlelog):
    log_line(f'Inserting player with battlelog')
    collection = use_collection_battlelog()
    api_player_battlelog['created_at'] = datetime.now()
    result = collection.insert_one(api_player_battlelog)	

def update_db_player_battlelog_data(tag, api_player_battlelog_battles):
    log_line(f'Updating {len(api_player_battlelog_battles)} battlelog battle(s) for player({tag})')
    collection = use_collection_battlelog()
    result = collection.update_one({'tag': tag}, {'$push': {'battles': {  '$each': api_player_battlelog_battles, '$position': 0 }}})

def increase_player_battelog_column(tag, name, value):
    log_line_in_debug(f'One {name} to player {tag}', False)
    collection = use_collection_battlelog()
    collection.update_one({'tag': tag}, {"$inc": {name: value}})

def init_db_brawlstars_crawler():
	client = MongoClient()
	db = client['brawlstars_crawler']
	return db

def use_collection_battlelog():
	db = init_db_brawlstars_crawler()
	collection = db['battlelog']
	return collection