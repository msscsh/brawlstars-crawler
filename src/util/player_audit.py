import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from util.logger import log_line
from util.db.mongodb import get_db_ranking_player_battlelog_data, set_db_player_field_value, update_db_player_battlelog_data

def audit(tag, battles):
	count_normal_game_win = 0
	count_normal_game_loss = 0
	count_normal_game_draw = 0
	count_pl_round_win = 0
	count_pl_round_loss = 0
	count_showdown_win_1st = 0
	count_showdown_win_2nd = 0
	count_showdown_win_3th = 0
	count_showdown_win_4th = 0
	count_showdown_loss = 0

	count_hunter_win = 0
	count_hunter_loss = 0

	count_mapmaker = 0
	count_starplayer = 0
	count_pl_starplayer = 0
	points = 0
	count_ng_duration = 0

	list_battles = set()
	duplicate_index = []

	for index, battle in enumerate(battles):

		if battle.get('battleTime') not in list_battles:
		    list_battles.add(battle.get('battleTime'))
		else:
			duplicate_index.append(index)
			continue

		if battle["event"]["id"] == 0:
			count_mapmaker += 1

		elif 'type' not in battle["battle"]:
			if battle["battle"]["mode"] == "bigGame":
				continue

		elif  battle["battle"]["type"].lower() == "soloranked" or battle["battle"]["type"].lower() == "teamranked":
			if battle["battle"]["result"] == "victory":
				count_pl_round_win += 1
				points += 3
			if battle["battle"]["result"] == "defeat":
				count_pl_round_loss += 1
			if battle["battle"].get("starPlayer") is not None:
				if battle["battle"].get("starPlayer")['tag'][1:] == tag:
					count_pl_starplayer += 1
					points += 2

		elif  battle["battle"]["mode"].lower() == "soloshowdown":
			if battle["battle"]["rank"] == 1:
				count_showdown_win_1st += 1
				points += 1
			if battle["battle"]["rank"] == 2:
				count_showdown_win_2nd += 1
				points += 1
			if battle["battle"]["rank"] == 3:
				count_showdown_win_3th += 1
				points += 1
			if battle["battle"]["rank"] == 4:
				count_showdown_win_4th += 1
				points += 1
			if battle["battle"]["rank"] >= 5:
				count_showdown_loss += 1

		elif  battle["battle"]["mode"].lower() == "duoshowdown":
			if battle["battle"]["rank"] == 1:
				count_showdown_win_1st += 1
				points += 1
			if battle["battle"]["rank"] == 2:
				count_showdown_win_2nd += 1
				points += 1
			if battle["battle"]["rank"] >= 3:
				count_showdown_loss += 1

		elif  battle["battle"]["mode"].lower() == "hunters":
			if battle["battle"]["rank"] == 1:
				count_hunter_win += 1
				points += 1
			if battle["battle"]["rank"] == 2:
				count_hunter_win += 1
				points += 1
			if battle["battle"]["rank"] == 3:
				count_hunter_win += 1
				points += 1
			if battle["battle"]["rank"] == 4:
				count_hunter_win += 1
				points += 1
			if battle["battle"]["rank"] >= 5:
				count_hunter_loss += 1

		else:
			if battle["battle"]["result"] == "victory":
				count_normal_game_win += 1
				points += 2
			if battle["battle"]["result"] == "defeat":
				count_normal_game_loss += 1
			if battle["battle"]["result"] == "draw":
				count_normal_game_draw += 1
			if battle["battle"].get("duration"):
				count_ng_duration += battle["battle"].get("duration")
			if battle["battle"].get("starPlayer") is not None:
				if battle["battle"].get("starPlayer")['tag'][1:] == tag:
					count_starplayer += 1
					points += 2

	set_db_player_field_value(player.get('tag'), 'ngWins', count_normal_game_win)
	set_db_player_field_value(player.get('tag'), 'ngLosses', count_normal_game_loss)
	set_db_player_field_value(player.get('tag'), 'ngDraws', count_normal_game_draw)
	set_db_player_field_value(player.get('tag'), 'plWins', count_pl_round_win)
	set_db_player_field_value(player.get('tag'), 'plLosses', count_pl_round_loss)
	set_db_player_field_value(player.get('tag'), 'sdFistPlace', count_showdown_win_1st)
	set_db_player_field_value(player.get('tag'), 'sdSecondPlace', count_showdown_win_2nd)
	set_db_player_field_value(player.get('tag'), 'sdThirdPlace', count_showdown_win_3th)
	set_db_player_field_value(player.get('tag'), 'sdFourthPlace', count_showdown_win_4th)
	set_db_player_field_value(player.get('tag'), 'sdLosses', count_showdown_loss)
	set_db_player_field_value(player.get('tag'), 'hunterWin', count_hunter_win)
	set_db_player_field_value(player.get('tag'), 'hunterLosses', count_hunter_loss)
	set_db_player_field_value(player.get('tag'), 'mapMakerPlays', count_mapmaker)
	set_db_player_field_value(player.get('tag'), 'starPlayer', count_starplayer)
	set_db_player_field_value(player.get('tag'), 'plStarPlayer', count_pl_starplayer)
	set_db_player_field_value(player.get('tag'), 'points', points)
	set_db_player_field_value(player.get('tag'), 'ngDduration', count_ng_duration)

	return duplicate_index

def remove_duplicate_index(duplicate_index, battles):
	print(f'battles: {len(battles)}')
	print(f'duplicate_index: {len(duplicate_index)}')
	for index_to_remove in reversed(duplicate_index):
		del battles[index_to_remove]
	print(f'battles tratadas: {len(battles)}')
	return battles

players = get_db_ranking_player_battlelog_data()
for index, player in enumerate(players):
	print(f'player({player.get("tag")}) with {len(player.get("battles"))} battles')
	duplicate_index = audit(player.get("tag"), player.get('battles'))
	final_battles = remove_duplicate_index(duplicate_index, player.get('battles'))
	set_db_player_field_value(player.get('tag'), 'battles', final_battles)