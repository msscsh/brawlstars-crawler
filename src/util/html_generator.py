import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from util.logger import log_line
from util.db.mongodb import get_db_ranking_player_battlelog_data

def write_player_in_ranking_html_file(html):
    file_path = 'ranking.html'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as new_file:
            pass
    with open(file_path, 'w') as hunted_file:
        hunted_file.write(f'{html}<!-- FINAL DA LINHA 143 -->')

def sum_showdown_board(player):
	return player.get('sdFistPlace',0) + player.get('sdSecondPlace',0) + player.get('sdThirdPlace',0) + player.get('sdFourthPlace',0)

file = "ranking_player_battlelog"
html = ""
ranking = get_db_ranking_player_battlelog_data()
for index, player in enumerate(ranking):
	# //MAKE THE STEP THAT SAVES YOUR POSITION TO TELL WHO WAS UP AND WHO WAS DOWN.. COMPARE NOW WITH PRE-BASE
	html = html + '<tr>' + f'<td>{index+1}#</td>' + f'<td>{player.get("clubBand")}</td>' + f'<td>{player.get("name")}</td>' + f'<td>{player.get("starPlayer", 0)}</td>' + f'<td>{sum_showdown_board(player)}/{player.get("sdLosses", 0)}</td>' + f'<td>{player.get("ngWins", 0)}/{player.get("ngLosses", 0)}</td>' + f'<td>{player.get("plWins", 0)}/{player.get("plLosses", 0)}</td>' + '</tr>\n'

write_player_in_ranking_html_file(html)

