import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from util.logger import log_line
from util.apis.brawlstars_api import get_api_players_data, get_api_players_battlelog_data
from util.db.mongodb import get_db_player_battlelog_data

def get_players_trophy_count(tag):
    player = get_api_players_data(tag)
    if player:
        return player["trophies"]
    else:
        return 0;

def get_tags_in_this_match(player_battlelog_battles):
    all_tags = []
    for battlelog in player_battlelog_battles:
        if battlelog['battle']['mode'].lower() not in not_hunted_event_list:
            for team in battlelog['battle']['teams']:
                for player in team:
                    all_tags.append(player['tag'][1:])
    return set(all_tags)

def add_tag_to_controll_file(tag):
    file_path = 'hunted_player_tags.log'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as novo_arquivo:
            pass
    with open(file_path, 'a') as hunted_file:
        hunted_file.write(f'{tag}\n')

def recursively_hunt_players(tag, deep):
    if deep >= 0:            
        trophies = get_players_trophy_count(tag)
        print(f'Player({tag}) trophies is {trophies} in deep {deep}')

        if trophies >= 50000 or tag == "2QPVJ099C":

            add_tag_to_controll_file(tag)
            player_battlelog_battles = []

            db_player_battlelog = get_db_player_battlelog_data(tag)
            if db_player_battlelog:
                player_battlelog_battles = db_player_battlelog.get('battles', [])
            else:
                api_player_battlelog = get_api_players_battlelog_data(tag)
                player_battlelog_battles = api_player_battlelog.get('battles', [])

            all_tags = get_tags_in_this_match(player_battlelog_battles)

            for tagii in all_tags:
                print(f'TAG Father: {tag} to son {tagii} ')
                recursively_hunt_players(tagii, deep-1)

            print(f'Finished relations from tag {tag}')
            return



tag = "2QPVJ099C"
not_hunted_event_list = [ 'soloshowdown', 'duoshowdown', 'biggame', 'bossfight', 'roborumble', 'takedown', 'lonestar', 'presentplunder', 'supercityrampage', 'holdthetrophy', 'trophythieves', 'duels', 'botdrop', 'hunters', 'laststand', 'snowtelthieves', 'unknown' ]

recursively_hunt_players(tag, 2)