import os, sys
from datetime import datetime

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from util.logger import log_line
from util.db.mongodb import get_db_ranking_player_battlelog_data, set_db_player_field_value, update_db_player_battlelog_data

def audit(tag, battles):
	count_normal_game_win = 0
	count_normal_game_loss = 0
	count_normal_game_draw = 0

	count_5v5_game_win = 0
	count_5v5_game_loss = 0
	count_5v5_game_draw = 0

	pl_object = {}
	count_pl_win = 0
	count_pl_loss = 0

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

		battle_time = datetime.strptime(battle.get('battleTime').replace('Z', ''), "%Y%m%dT%H%M%S.%f")

		#2024 only allowed
		if battle_time.year < 2024:
		    continue

		if battle["event"]["id"] == 0:
			count_mapmaker += 1

		elif 'type' not in battle["battle"]:
			if battle["battle"]["mode"] == "bigGame":
				continue

		elif  battle["battle"]["type"].lower() == "soloranked" or battle["battle"]["type"].lower() == "teamranked":

			tags_team_0 = ''
			for player_team_0 in battle["battle"].get("teams")[0]:
				tags_team_0 = tags_team_0 + player_team_0.get('tag')

			tags_team_1 = ''
			for player_team_1 in battle["battle"].get("teams")[1]:
				tags_team_1 = tags_team_1 + player_team_1.get('tag')

			if pl_object.get('id') is not None and pl_object.get('id') != tags_team_0+tags_team_1:
				if pl_object.get("countWin", 0) > pl_object.get("countLoss", 0):
					count_pl_win += 1
				else:
					count_pl_loss += 1
				points += pl_object.get("countWin", 0) * 3
				pl_object = {"id": tags_team_0+tags_team_1, "countWin": 0, "countLoss": 0}
			else:
				pl_object = {"id": tags_team_0+tags_team_1, "countWin": pl_object.get("countWin", 0), "countLoss": pl_object.get("countLoss", 0)}

			if battle["battle"]["result"] == "victory":
				pl_object = {"id": tags_team_0+tags_team_1, "countWin": pl_object.get("countWin", 0)+1, "countLoss": pl_object.get("countLoss", 0)}
			elif battle["battle"]["result"] == "defeat":
				pl_object = {"id": tags_team_0+tags_team_1, "countWin": pl_object.get("countWin", 0), "countLoss": pl_object.get("countLoss", 0)+1}

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
				
		elif 'trophyChange' in battle["battle"]:	

			if battle["battle"].get("duration"):
				count_ng_duration += battle["battle"].get("duration")
			if battle["battle"].get("starPlayer") is not None:
				if battle["battle"].get("starPlayer")['tag'][1:] == tag:
					count_starplayer += 1
					points += 2

			if len(battle["battle"]["teams"][0]) == 3
				if battle["battle"]["result"] == "victory":
					count_normal_game_win += 1
					points += 2
				if battle["battle"]["result"] == "defeat":
					count_normal_game_loss += 1
				if battle["battle"]["result"] == "draw":
					count_normal_game_draw += 1

			if len(battle["battle"]["teams"][0]) == 5
				if battle["battle"]["result"] == "victory":
					count_5v5_game_win += 1
					points += 2
				if battle["battle"]["result"] == "defeat":
					count_5v5_game_loss += 1
				if battle["battle"]["result"] == "draw":
					count_5v5_game_draw += 1

	set_db_player_field_value(player.get('tag'), 'ngWins', count_normal_game_win)
	set_db_player_field_value(player.get('tag'), 'ngLosses', count_normal_game_loss)
	set_db_player_field_value(player.get('tag'), 'ngDraws', count_normal_game_draw)
	set_db_player_field_value(player.get('tag'), 'plWins', count_pl_win)
	set_db_player_field_value(player.get('tag'), 'plLosses', count_pl_loss)
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
	#No battles, nothing to do
	if player.get("battles"):
		print(f'player({player.get("tag")}) with {len(player.get("battles"))} battles')
		duplicate_index = audit(player.get("tag"), player.get('battles'))
		final_battles = remove_duplicate_index(duplicate_index, player.get('battles'))
		set_db_player_field_value(player.get('tag'), 'battles', final_battles)