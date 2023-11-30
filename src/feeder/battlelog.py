import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from util.logger import log_line, log_line_in_debug
from util.apis.brawlstars_api import get_api_clubs_members, get_api_players_battlelog_data_with_name
from util.db.mongodb import get_db_player_battlelog_data, insert_db_player_battlelog_data, update_db_player_battlelog_data

from rules.score_rules import apply_general_battlelog_rules_into_players_score

def count_all_player_score_from_battles(tag, battles):
    index = 0
    while index < len(battles):
        apply_general_battlelog_rules_into_players_score(tag, battles[index])
        index += 1

def identify_index_last_persisted_change(last_updated_battle_date, api_battles, tag):
    index = 0
    current_battle_date = api_battles[0]["battleTime"]
    while index < len(api_battles):
        log_line_in_debug(f'dates compared in API return index={index} DB({last_updated_battle_date}) API({current_battle_date})', False)
        if current_battle_date > last_updated_battle_date:
            current_battle_date = api_battles[index]["battleTime"]
            index += 1
        if current_battle_date == last_updated_battle_date:
            break
    return index

def scan_all_players_from_club(club_tag):
    members = get_api_clubs_members(club_tag).get('members')
    index = 0
    while index < len(members):
        log_line_in_debug(members[index], True)
        main(members[index]['tag'][1:])
        index += 1

def add_tag_into_crontab_file(tag):
    file_path = 'cron_tags.log'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as novo_arquivo:
            pass
    with open(file_path, 'a') as hunted_file:
        hunted_file.write(f'*/10 * * * * cd $BS_CRAWLER_HOME && python3 src/feeder/battlelog.py {tag}\n')

def main(tag):
    log_line(f'Begin with tag: {tag}')
    # add_tag_into_crontab_file(tag)

    api_player_battlelog = get_api_players_battlelog_data_with_name(tag)
    log_line_in_debug(api_player_battlelog, True)

    if api_player_battlelog:
        db_player_battlelog = get_db_player_battlelog_data(tag)

        if not db_player_battlelog:
            insert_db_player_battlelog_data(tag, api_player_battlelog)
            count_all_player_score_from_battles(tag, api_player_battlelog.get('battles', []))
        else:
            last_updated_battle_date = db_player_battlelog.get('battles', [])[0]['battleTime']
            api_battles = api_player_battlelog.get('battles', [])
            cut = identify_index_last_persisted_change(last_updated_battle_date, api_battles, tag)
            update_db_player_battlelog_data(tag, api_battles[:cut])
            count_all_player_score_from_battles(tag, api_battles[:cut])
    else:
        log_line(f'Failed getting data from API:{tag}')

#Club tag
if len(sys.argv) < 2:
    print('Use club tag?')
    club_tag = input()
    scan_all_players_from_club(club_tag)

#Player tag
if len(sys.argv) == 2:
    log_line('Loading player tag')
    tag = sys.argv[1]
    main(tag)

#Clubs tag
if len(sys.argv) >= 3:
    log_line('Loading group of clubs')
    index = 1
    while index < len(sys.argv):
        club_tag = sys.argv[index]
        scan_all_players_from_club(club_tag)
        index += 1

log_line('Ending feeder')