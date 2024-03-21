from os import getenv

from dotenv import load_dotenv
from requests import post

load_dotenv()

bot_token = getenv('BOT_DUMBER_TOKEN')
chat_id = getenv('DB_DUMB_CHANNEL_ID')

url = f'https://api.telegram.org/bot{bot_token}/sendDocument'

files = {'document': open('main.db', 'rb')}
data = {'chat_id': chat_id}

response = post(url, files=files, data=data)

if response.status_code != 200:
    print('FATAL FATAL FATAL', response.text)  # mb need catch? and do anything
