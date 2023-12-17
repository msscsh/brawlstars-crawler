import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from util.logger import log_line
from util.db.mongodb import get_db_ranking_player_battlelog_data, set_db_player_field_value

def write_value(value):
    return f'<td>{value}</td>'

def write_player_value(player, field):
    return f'<td>{player.get(field, 0)}</td>'

def write_player_in_ranking_html_file(html):
    file_path = 'ranking.html'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as new_file:
            pass
    with open(file_path, 'w') as hunted_file:
        hunted_file.write(f'{html}<!-- FINAL 132 -->')

def sum_showdown_board(player):
	return player.get('sdFistPlace',0) + player.get('sdSecondPlace',0) + player.get('sdThirdPlace',0) + player.get('sdFourthPlace',0)

file = "ranking_player_battlelog"
html = ""
ranking = get_db_ranking_player_battlelog_data()
for index, player in enumerate(ranking):

    oldPosition = 90
    if player.get('position'):
        oldPosition = int(player.get('position'))

    set_db_player_field_value(player.get('tag'), 'position', index+1)
    emoji = ''

    if index+1 == 1:
        emoji += '🥇'
    if index+1 == 2:
        emoji += '🥈'
    if index+1 == 3:
        emoji += '🥉'

    if index+1 == oldPosition :
        emoji += ''
    elif index+1 < oldPosition :
        emoji += '🚀'
    elif index+1 > oldPosition :
        emoji += '🔻'

    strShowdown = f"{sum_showdown_board(player)}/{player.get('sdLosses', 0)}"
    strNormalGame = f"{player.get('ngWins', 0)}/{player.get('ngLosses', 0)}"
    strPowerLeague = f"{player.get('plWins', 0)}/{player.get('plLosses', 0)}"

    html += '<tr>'\
    f'<td>{emoji}{index+1}#</td>'\
    f"{write_player_value(player, 'clubBand')}"\
    f"{write_player_value(player, 'name')}"\
    f"{write_player_value(player, 'points')}"\
    f"{write_player_value(player, 'starPlayer')}"\
    f"{write_value(strShowdown)}"\
    f"{write_value(strNormalGame)}"\
    f"{write_value(strPowerLeague)}"\
    '</tr>\n'

write_player_in_ranking_html_file(html)

