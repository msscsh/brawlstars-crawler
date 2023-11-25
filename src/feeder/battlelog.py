import os, sys
from datetime import date

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from util.logger import log_line
from util.apis.brawlstars_api import get_api_players_battlelog_data, get_api_clubs_members, get_api_players_battlelog_data_with_name
from util.db.mongodb import increase_player_battelog_column, get_db_player_battlelog_data, insert_db_player_battlelog_data, update_db_player_battlelog_data

def apply_general_battlelog_rules_into_players_score(tag, battle):
    # print(battle)
    solo_duo_game = [ 'soloshowdown', 'duoshowdown']
    especial_game = ['biggame', 'bossfight', 'roborumble', 'takedown', 'lonestar', 'presentplunder', 'supercityrampage', 'holdthetrophy', 'trophythieves', 'duels', 'botdrop', 'hunters', 'laststand', 'snowtelthieves', 'unknown' ]

    if battle["battle"]["mode"].lower() in solo_duo_game:
        if battle["battle"]["rank"] == 1:
            increase_player_battelog_column(tag, 'sdFistPlace', 1)
        if battle["battle"]["rank"] == 2:
            increase_player_battelog_column(tag, 'sdSecondPlace', 1)
        if battle["battle"]["rank"] == 3:
            increase_player_battelog_column(tag, 'sdThirdPlace', 1)
        if battle["battle"]["rank"] == 4:
            increase_player_battelog_column(tag, 'sdFourthPlace', 1)
    else:
        if battle["battle"]["result"] == "victory":
            increase_player_battelog_column(tag, 'wins', 1)
        if battle["battle"]["result"] == "defeat":
            increase_player_battelog_column(tag, 'losses', 1)
        if battle["battle"]["result"] == "draw":
            increase_player_battelog_column(tag, 'draws', 1)
        if battle["battle"].get("duration"):
            increase_player_battelog_column(tag, 'duration', battle["battle"].get("duration"))
        if battle["battle"].get("starPlayer") is not None:
            if battle["battle"].get("starPlayer")['tag'][1:] == tag:
                increase_player_battelog_column(tag, 'starPlayer', 1)

def count_all_player_score_for_first_time(tag, battles):
    index = 0
    while index < len(battles):
        apply_general_battlelog_rules_into_players_score(tag, battles[index])
        index += 1

def identify_index_last_persisted_change(last_updated_battle_date, api_battles, tag):
    index = 0
    log_line(f'Last updated battle was at {last_updated_battle_date}')
    current_battle_date = api_battles[0]["battleTime"]
    while index < 25:
        if current_battle_date == last_updated_battle_date:
            print(f'datas iguais em {index} data do banco {last_updated_battle_date} com data da api {current_battle_date}')
            break
        else:
            print(f'datas comparadas no {index} data do banco {last_updated_battle_date} com data da api {current_battle_date}')
            apply_general_battlelog_rules_into_players_score(tag, api_battles[index])
            index += 1
            current_battle_date = api_battles[index]["battleTime"]

    print('pulou?')

    log_line(f'Finished {current_battle_date}')
    return index

def scan_all_players_from_club(club_tag):
    members = get_api_clubs_members(club_tag).get('members')
    index = 0
    while index < len(members):
        print(members[index])
        main(members[index]['tag'][1:])
        index += 1

def add_tag_into_crontab_file(tag):
    file_path = 'cron_tags.log'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as novo_arquivo:
            pass
    with open(file_path, 'a') as hunted_file:
        hunted_file.write(f'*/10 * * * * cd brawlstars-crawler && python3 src/feeder/battlelog.py {tag}\n')

def main(tag):
    log_line(f'Begin with tag: {tag}')
    # add_tag_into_crontab_file(tag)

    api_player_battlelog = get_api_players_battlelog_data_with_name(tag)

    if api_player_battlelog:
        db_player_battlelog = get_db_player_battlelog_data(tag)

        if not db_player_battlelog:
            insert_db_player_battlelog_data(tag, api_player_battlelog)
            count_all_player_score_for_first_time(tag, api_player_battlelog.get('battles', []))
        else:
            last_updated_battle_date = db_player_battlelog.get('battles', [])[0]['battleTime']
            api_battles = api_player_battlelog.get('battles', [])
            cut = identify_index_last_persisted_change(last_updated_battle_date, api_battles, tag)
            update_db_player_battlelog_data(tag, api_battles[:cut])
    else:
        log_line(f'Failed getting data from API:{tag}')

#Club tag
if len(sys.argv) < 2:
    print('Use club tag?')
    club_tag = input()
    scan_all_players_from_club(club_tag)

#Player tag
if len(sys.argv) == 2:
    print('Loading player tag')
    tag = sys.argv[1]
    main(tag)

#Clubs tag
if len(sys.argv) >= 3:
    print('Loading group of clubs')
    index = 1
    while index < len(sys.argv):
        club_tag = sys.argv[index]
        scan_all_players_from_club(club_tag)
        index += 1
