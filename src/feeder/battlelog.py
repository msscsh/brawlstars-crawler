import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from util.logger import log_line
from util.apis.brawlstars_api import get_api_players_battlelog_data
from util.db.mongodb import increase_player_battelog_column, get_db_player_battlelog_data, insert_db_player_battlelog_data, update_db_player_battlelog_data

def count_players_score(battle):
    if battle["battle"]["result"] == "victory":
        increase_player_battelog_column(tag, 'wins', 1)
    if battle["battle"]["result"] == "defeat":
        increase_player_battelog_column(tag, 'losses', 1)
    if battle["battle"]["result"] == "draw":
        increase_player_battelog_column(tag, 'draws', 1)
    if battle["battle"].get("duration"):
        increase_player_battelog_column(tag, 'duration', battle["battle"].get("duration"))

def count_all_player_score(battles):
    index = 0
    while index < len(battles):
        count_players_score(battles[index])
        index += 1

def identify_index_last_persisted_change(last_updated_battle_date, api_battles):
    index = 0
    log_line(f'Last updated battle was at {last_updated_battle_date}')
    current_battle_date = api_battles[0]["battleTime"]
    while current_battle_date != last_updated_battle_date and index < 25:
        count_players_score(api_battles[index])
        index += 1
        current_battle_date = api_battles[index]["battleTime"]
    return index

if len(sys.argv) < 2:
    log_line("Tag not found.")
    quit()

tag = sys.argv[1]
log_line(f'Begin with tag: {tag}')

api_player_battlelog = get_api_players_battlelog_data(tag)

if api_player_battlelog:
    db_player_battlelog = get_db_player_battlelog_data(tag)

    if not db_player_battlelog:
        insert_db_player_battlelog_data(tag, api_player_battlelog)
        count_all_player_score(api_player_battlelog.get('battles', []))
    else:
        print(db_player_battlelog.get('battles', [])[0])
        last_updated_battle_date = db_player_battlelog.get('battles', [])[0]['battleTime']
        api_battles = api_player_battlelog.get('battles', [])
        cut = identify_index_last_persisted_change(last_updated_battle_date, api_battles)
        update_db_player_battlelog_data(tag, api_battles[:cut])
else:
    log_line(f'Failed getting data from API:{tag}')
