import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from util.logger import log_line
from util.apis.brawlstars_api import get_api_players_battlelog_data
from util.db.mongodb import increase_player_battelog_column, get_db_player_battlelog_data, insert_db_player_battlelog_data, update_db_player_battlelog_data

def count_players_score(item):
    if item["battle"]["result"] == "victory":
        increase_player_battelog_column(tag, 'wins')
    if item["battle"]["result"] == "defeat":
        increase_player_battelog_column(tag, 'losses')
    if item["battle"]["result"] == "draw":
        increase_player_battelog_column(tag, 'draws')

def identify_index_last_persisted_change(last_updated_item_date, api_items):
    index = 0
    log_line(f'Last updated item was at {last_updated_item_date}')
    current_item_date = api_items[0]["battleTime"]
    while current_item_date != last_updated_item_date and index < 25:
        count_players_score(api_items[index])
        index += 1
        current_item_date = api_items[index]["battleTime"]
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
    else:
        last_updated_item_date = db_player_battlelog.get('items', [])[0]['battleTime']
        api_items = api_player_battlelog.get('items', [])
        cut = identify_index_last_persisted_change(last_updated_item_date, api_items)
        update_db_player_battlelog_data(tag, api_items[:cut])
else:
    log_line(f'Failed getting data from API:{tag}')
