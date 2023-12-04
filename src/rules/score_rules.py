import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from util.logger import log_line_in_debug
from util.db.mongodb import increase_player_battelog_column

def apply_general_battlelog_rules_into_players_score(tag, battle):
	log_line_in_debug(battle, True)
	especial_game = ['biggame', 'bossfight', 'roborumble', 'takedown', 'lonestar', 'presentplunder', 'supercityrampage', 'holdthetrophy', 'trophythieves', 'duels', 'botdrop', 'hunters', 'laststand', 'snowtelthieves', 'unknown' ]

	if battle["event"]["id"] == 0:
		increase_player_battelog_column(tag, 'mapMakerPlays', 1)

	elif  battle["battle"]["type"].lower() == "soloranked" or battle["battle"]["type"].lower() == "teamranked":
		if battle["battle"]["result"] == "victory":
			increase_player_battelog_column(tag, 'plWins', 1)
			increase_player_battelog_column(tag, 'points', 3)
		if battle["battle"]["result"] == "defeat":
			increase_player_battelog_column(tag, 'plLosses', 1)
		if battle["battle"].get("starPlayer") is not None:
			if battle["battle"].get("starPlayer")['tag'][1:] == tag:
				increase_player_battelog_column(tag, 'plStarPlayer', 1)
				increase_player_battelog_column(tag, 'points', 2)

	elif  battle["battle"]["mode"].lower() == "soloshowdown":
		if battle["battle"]["rank"] == 1:
			increase_player_battelog_column(tag, 'sdFistPlace', 1)
			increase_player_battelog_column(tag, 'points', 1)
		if battle["battle"]["rank"] == 2:
			increase_player_battelog_column(tag, 'sdSecondPlace', 1)
			increase_player_battelog_column(tag, 'points', 1)
		if battle["battle"]["rank"] == 3:
			increase_player_battelog_column(tag, 'sdThirdPlace', 1)
			increase_player_battelog_column(tag, 'points', 1)
		if battle["battle"]["rank"] == 4:
			increase_player_battelog_column(tag, 'sdFourthPlace', 1)
			increase_player_battelog_column(tag, 'points', 1)
		if battle["battle"]["rank"] >= 5:
			increase_player_battelog_column(tag, 'sdLosses', 1)

	elif  battle["battle"]["mode"].lower() == "duoshowdown":
		if battle["battle"]["rank"] == 1:
			increase_player_battelog_column(tag, 'sdFistPlace', 1)
			increase_player_battelog_column(tag, 'points', 1)
		if battle["battle"]["rank"] == 2:
			increase_player_battelog_column(tag, 'sdSecondPlace', 1)
			increase_player_battelog_column(tag, 'points', 1)
		if battle["battle"]["rank"] >= 3:
			increase_player_battelog_column(tag, 'sdLosses', 1)
	else:
		if battle["battle"]["result"] == "victory":
			increase_player_battelog_column(tag, 'ngWins', 1)
			increase_player_battelog_column(tag, 'points', 2)
		if battle["battle"]["result"] == "defeat":
			increase_player_battelog_column(tag, 'ngLosses', 1)
		if battle["battle"]["result"] == "draw":
			increase_player_battelog_column(tag, 'ngDraws', 1)
		if battle["battle"].get("duration"):
			increase_player_battelog_column(tag, 'ngDduration', battle["battle"].get("duration"))
		if battle["battle"].get("starPlayer") is not None:
			if battle["battle"].get("starPlayer")['tag'][1:] == tag:
				increase_player_battelog_column(tag, 'starPlayer', 1)
				increase_player_battelog_column(tag, 'points', 2)