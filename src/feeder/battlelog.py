import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from util.logger import log_line, log_line_in_debug
from util.apis.brawlstars_api import get_api_clubs, get_api_clubs_members, get_api_players_battlelog_data_with_name
from util.db.mongodb import get_db_player_battlelog_data, insert_db_player_battlelog_data, update_db_player_battlelog_data, set_db_player_field_value, clear_players_from_club, clear_monitored_players
from util.file_master import read_lines_from_file, remove_file, add_content_in_file
from rules.score_rules import apply_general_battlelog_rules_into_players_score

def monitored_players():
    tags_failed_again = []
    file_path = 'monitored_players.log'
    file_failed_tag = read_lines_from_file(file_path)
    clear_monitored_players()
    for tag in file_failed_tag:
        log_line(f'Monitoring player({tag.strip()}) ')
        main(tag.strip(), None)
        set_db_player_field_value(tag.strip(), 'isMonitored', 1)

def reprocess_failed():
    tags_failed_again = []
    file_path = 'failed_tag.log'
    file_failed_tag = read_lines_from_file(file_path)
    for tag in file_failed_tag:
        if not main(tag.strip(), None) :
            if tag.strip() not in tags_failed_again:
                tags_failed_again = tags_failed_again + [tag.strip()]

    remove_file(file_path)
    for tag in tags_failed_again:
        add_content_in_file(file_path, tag + '\n')

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
    clubBand = get_api_clubs(club_tag).get('name')[-1]
    members = get_api_clubs_members(club_tag).get('members')
    index = 0
    while index < len(members):
        log_line_in_debug(members[index], True)
        set_db_player_field_value(members[index]['tag'][1:], 'isBRZ', 1)
        set_db_player_field_value(members[index]['tag'][1:], 'role', members[index].get('role'))
        log_line(f'Player({members[index]["tag"][1:]}) {index} ')
        main(members[index]['tag'][1:], clubBand)
        index += 1

def main(tag, clubBand):
    api_player_battlelog = get_api_players_battlelog_data_with_name(tag)
    log_line(f'Begin with player: {api_player_battlelog["name"]}')
    log_line_in_debug(api_player_battlelog, True)

    if api_player_battlelog:
        if clubBand:
            api_player_battlelog = {'clubBand': clubBand, **api_player_battlelog}

        db_player_battlelog = get_db_player_battlelog_data(tag)
        if not db_player_battlelog:
            insert_db_player_battlelog_data(tag, api_player_battlelog)
        else:
            db_battles = db_player_battlelog.get('battles', [])
            api_battles = api_player_battlelog.get('battles', [])
            if len(db_battles) > 0:
                last_updated_battle_date = db_battles[0]['battleTime']
                cut = identify_index_last_persisted_change(last_updated_battle_date, api_battles, tag)
                update_db_player_battlelog_data(tag, api_battles[:cut])
            else:
                update_db_player_battlelog_data(tag, api_battles)
            set_db_player_field_value(tag, 'name', api_player_battlelog['name'])
        return True

    else:
        log_line(f'Failed getting data from API:{tag}')
        return False

offset_param = 0
if 'debug' in sys.argv:
    offset_param += 1

if 'reprocess_failed' in sys.argv:
    log_line(f'Init "reprocess_failed"')
    reprocess_failed()

if 'monitored_players' in sys.argv:
    log_line(f'Init "monitored_players"')
    monitored_players()

#Club tag
elif len(sys.argv) < 2+offset_param:
    log_line('Use club tag?')
    club_tag = input()
    scan_all_players_from_club(club_tag)

#Player tag
elif len(sys.argv) == 2+offset_param:
    log_line('Loading player tag')
    tag = sys.argv[1]
    main(tag, None)

#Clubs tag
elif len(sys.argv) > 3+offset_param:
    log_line('Loading group of clubs')
    index = 1
    clear_players_from_club()
    while index < len(sys.argv)-offset_param:
        club_tag = sys.argv[index]
        scan_all_players_from_club(club_tag)
        index += 1

log_line('Ending feeder')