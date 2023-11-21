import os, sys, json, requests

project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)
from util.logger import log_line

def add_banned_tag_to_file(tag):
    all_lines = []
    file_path = 'banned_players_tag.log'

    if not os.path.exists(file_path):
        with open(file_path, 'w') as novo_arquivo:
            pass

    with open(file_path, 'a') as hunted_file:
        hunted_file.write(f'{tag}\n')

def do_request(url):
	with open('api_key', 'r') as arquivo:
	    api_key = arquivo.read()
	    headers = {
	        'Authorization': f'Bearer {api_key}'
	    }
	    response = requests.get(url, headers=headers)
	    return response

def get_api_players_data(tag):
	url = f'{base_url}/players/%23{tag}'
	response = do_request(url)
	if response.status_code == 200:
		return response.json()
	if response.status_code == 404:
		log_line(f'Error: 404 Not Found {url}')
		add_banned_tag_to_file(tag)
		return None
	else:
		log_line(f'Error: {response.status_code}')
		return None

def get_api_players_battlelog_data(tag):
	url = f'{base_url}/players/%23{tag}/battlelog'
	response = do_request(url)
	if response.status_code == 200:
		return response.json()
	if response.status_code == 404:
		log_line(f'Error: 404 Not Found {url}')
		add_banned_tag_to_file(tag)
		return None
	else:
		log_line(f'Error: {response.status_code}')
		return None

def main(tag):
	json_full = get_api_players_data(tag)
	to_remove = ["brawlers"]
	json_less = {key: value for key, value in json_full.items() if key not in to_remove}
	print(json.dumps(json_less, indent=2, ensure_ascii=False))

base_url='https://api.brawlstars.com/v1'

if __name__ == "__main__":
	if len(sys.argv) < 2:
		log_line("Directed started API module with no TAG informed")
		quit()
	else:
	    main(sys.argv[1])