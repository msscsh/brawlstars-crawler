import os, sys, json, requests

project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)
from util.logger import log_line

def add_banned_url_to_file(tag):
    file_path = 'banned_url.log'

    if not os.path.exists(file_path):
        with open(file_path, 'w') as novo_arquivo:
            pass

    with open(file_path, 'a') as hunted_file:
        hunted_file.write(f'{tag}\n')

def clean_trash_columns_from_json(json_from_api):
	to_remove = ["paging"]
	json_less = {key: value for key, value in json_from_api.items() if key not in to_remove}
	return json.dumps(json_less, indent=2, ensure_ascii=False)

def do_request(url):
	with open('api_key', 'r') as arquivo:
	    api_key = arquivo.read()
	    headers = {
	        'Authorization': f'Bearer {api_key}'
	    }
	    response = requests.get(url, headers=headers)
	    if response.status_code == 200:
	    	return clean_trash_columns_from_json(response.json())
	    if response.status_code == 404:
	    	log_line(f'Error: 404 Not Found {url}')
	    	add_banned_url_to_file(url)
	    	return None
	    else:
	    	log_line(f'Error: {response.status_code}')
	    	return None

def get_api_players_data(tag):
	url = f'{base_url_players}{tag}'
	return do_request(url)

def get_api_players_battlelog_data(tag):
	url = f'{base_url_players}{tag}/battlelog'
	return do_request(url)

def get_api_clubs(tag):
	url = f'{base_url_clubs}{tag}'
	return do_request(url)

def get_api_clubs_members(tag):
	url = f'{base_url_clubs}{tag}/members'
	return do_request(url)

def get_api_rankings_countrycode_powerplay_seasons(country_code):
	url = f'{base_url_rankings}/{country_code}/powerplay/seasons'
	return do_request(url)

def get_api_rankings_countrycode_powerplay_seasons_seasonsid(country_code, seasonid):
	url = f'{base_url_rankings}/{country_code}/powerplay/seasons/{seasonid}'
	return do_request(url)

def get_api_rankings_countrycode_clubs(country_code):
	url = f'{base_url_rankings}/{country_code}/clubs'
	return do_request(url)

def get_api_rankings_countrycode(country_code):
	url = f'{base_url_rankings}/{country_code}/brawlers/{brawlersid}'
	return do_request(url)

def get_api_rankings_countrycode(country_code):
	url = f'{base_url_rankings}/players'
	return do_request(url)

def get_api_brawlers():
	url = f'{base_url_brawlers}'
	return do_request(url)

def get_api_brawler(id):
	url = f'{base_url_brawlers}/{id}'
	return do_request(url)

def get_api_events_rotation(id):
	url = f'{base_url_events}/{id}'
	return do_request(url)

def main(tag):
	print(get_api_players_data(tag))


base_url='https://api.brawlstars.com/v1'
base_url_players=f'{base_url}/players/%23'
base_url_clubs=f'{base_url}/clubs/%23'
base_url_brawlers=f'{base_url}/brawlers'
base_url_rankings=f'{base_url}/rankings'
base_url_events=f'{base_url}/events/rotation'

if __name__ == "__main__":
	if len(sys.argv) < 2:
		log_line("Directed started API module with no TAG informed")
		quit()
	else:
	    main(sys.argv[1])