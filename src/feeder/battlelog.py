import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from util.logger import log_line, log_line_in_debug
from util.apis.brawlstars_api import get_api_clubs_members, get_api_players_battlelog_data_with_name
from util.db.mongodb import increase_player_battelog_column, get_db_player_battlelog_data, insert_db_player_battlelog_data, update_db_player_battlelog_data

def apply_general_battlelog_rules_into_players_score(tag, battle):
    log_line_in_debug(battle, true)

    especial_game = ['biggame', 'bossfight', 'roborumble', 'takedown', 'lonestar', 'presentplunder', 'supercityrampage', 'holdthetrophy', 'trophythieves', 'duels', 'botdrop', 'hunters', 'laststand', 'snowtelthieves', 'unknown' ]

    if battle["event"]["id"] == 0:
        increase_player_battelog_column(tag, 'mapMakerPlays', 1)

    elif  battle["battle"]["type"].lower() == "soloranked" or battle["battle"]["type"].lower() == "teamranked":
        if battle["battle"]["result"] == "victory":
            increase_player_battelog_column(tag, 'plWins', 1)
        if battle["battle"]["result"] == "defeat":
            increase_player_battelog_column(tag, 'plLosses', 1)
        if battle["battle"].get("starPlayer") is not None:
            if battle["battle"].get("starPlayer")['tag'][1:] == tag:
                increase_player_battelog_column(tag, 'plStarPlayer', 1)

    elif  battle["battle"]["mode"].lower() == "soloshowdown":
        if battle["battle"]["rank"] == 1:
            increase_player_battelog_column(tag, 'sdFistPlace', 1)
        if battle["battle"]["rank"] == 2:
            increase_player_battelog_column(tag, 'sdSecondPlace', 1)
        if battle["battle"]["rank"] == 3:
            increase_player_battelog_column(tag, 'sdThirdPlace', 1)
        if battle["battle"]["rank"] == 4:
            increase_player_battelog_column(tag, 'sdFourthPlace', 1)
        if battle["battle"]["rank"] >= 5:
            increase_player_battelog_column(tag, 'sdLosses', 1)

    elif  battle["battle"]["mode"].lower() == "duoshowdown":
        if battle["battle"]["rank"] == 1:
            increase_player_battelog_column(tag, 'sdFistPlace', 1)
        if battle["battle"]["rank"] == 2:
            increase_player_battelog_column(tag, 'sdSecondPlace', 1)
        if battle["battle"]["rank"] >= 3:
            increase_player_battelog_column(tag, 'sdLosses', 1)
    else:
        if battle["battle"]["result"] == "victory":
            increase_player_battelog_column(tag, 'ngWins', 1)
        if battle["battle"]["result"] == "defeat":
            increase_player_battelog_column(tag, 'ngLosses', 1)
        if battle["battle"]["result"] == "draw":
            increase_player_battelog_column(tag, 'ngDraws', 1)
        if battle["battle"].get("duration"):
            increase_player_battelog_column(tag, 'ngDduration', battle["battle"].get("duration"))
        if battle["battle"].get("starPlayer") is not None:
            if battle["battle"].get("starPlayer")['tag'][1:] == tag:
                increase_player_battelog_column(tag, 'starPlayer', 1)

def count_all_player_score_from_battles(tag, battles):
    index = 0
    while index < len(battles):
        apply_general_battlelog_rules_into_players_score(tag, battles[index])
        index += 1

def identify_index_last_persisted_change(last_updated_battle_date, api_battles, tag):
    index = 0
    current_battle_date = api_battles[0]["battleTime"]
    while index < len(api_battles):
        log_line_in_debug(f'dates compared in API return index={index} DB({last_updated_battle_date}) API({current_battle_date})')
        if current_battle_date > last_updated_battle_date:
            index += 1
            current_battle_date = api_battles[index]["battleTime"]
        if current_battle_date == last_updated_battle_date:
            break
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
        hunted_file.write(f'*/10 * * * * cd $BS_CRAWLER_HOME && python3 src/feeder/battlelog.py {tag}\n')

def main(tag):
    log_line(f'Begin with tag: {tag}')
    # add_tag_into_crontab_file(tag)

    api_player_battlelog = get_api_players_battlelog_data_with_name(tag)
    log_line_in_debug(api_player_battlelog, false)

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
