import requests

print('Rest consumer')

with open('api_key', 'r') as arquivo:
    api_key = arquivo.read()

tag = input('Which tag: ')
url = f'https://api.brawlstars.com/v1/players/%23{tag}'
headers = {
    'Authorization': f'Bearer {api_key}'
}

response = requests.get(url, headers=headers)
data = response.json()

if response.status_code == 200:
	print(f'Name: {data["name"]}')
else:
	print(f'Error: {response.status_code}')