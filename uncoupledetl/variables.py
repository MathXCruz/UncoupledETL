URL = 'https://pokeapi.co/api/v2/'
ENDPOINTS = ['pokemon/' + f'{i}' for i in range(1, 10)]
DOTA_URL = 'https://api.opendota.com/api/'
DOTA_ENDPOINT = 'players/76561198059243072'
WOW_URL = 'https://raider.io/api/v1/'
WOW_ENDPOINT = 'characters/profile?region=us&realm=hakkar&name=Golois'
LOCAL_DATABASE = (
    'sqlite+aiosqlite:////home/matheus/Poke_API/poke_api_training.db'
)
