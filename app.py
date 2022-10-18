import discord
import gspread
import os
import json
import requests
from discord import Intents
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ['TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
SPREADSHEET_NAME = os.environ['SPREADSHEET_NAME']
CLOUD_CREDENTIALS_SECRET = os.environ['CLOUD_CREDENTIALS_SECRET']

import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_cred_config() -> dict(str):
    secret = os.environ.get("CLOUD_CREDENTIALS_SECRET")
    if secret:
        return json.loads(secret)

key = get_cred_config()
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(key, scope)

def last(SPREADSHEET_KEY,SPREADSHEET_NAME):
    gs = gspread.authorize(credentials)
    wb = gs.open_by_key(SPREADSHEET_KEY)
    ss = wb.worksheet(SPREADSHEET_NAME)
    str_list = list(filter(None, ss.col_values(1)))
    next_row = str(len(str_list) + 1)
    last = int(next_row)
    return last

def sagyou(SPREADSHEET_KEY,SPREADSHEET_NAME):
    gs = gspread.authorize(credentials)
    wb = gs.open_by_key(SPREADSHEET_KEY)
    sagyou = wb.worksheet(SPREADSHEET_NAME)
    return sagyou

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Login!!!')

@client.event
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id != int(CHANNEL_ID):
        return

    if message.channel.id == int(CHANNEL_ID):
        data = message.content
        ss = sagyou(SPREADSHEET_KEY,SPREADSHEET_NAME)
        value = last(SPREADSHEET_KEY,SPREADSHEET_NAME)
        ss.update_cell(value, 1, data)
        await message.channel.send(f'更新します {message.author}!{data}')
    else:
        print('error')

client.run(TOKEN)

print('source.json')

import os
os.remove('source.json')
