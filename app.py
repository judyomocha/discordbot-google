import discord
import gspread
import os
from discord import Intents
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
SPREADSHEET_NAME = os.environ['SPREADSHEET_NAME']
NAME = os.environ['NAME']

from google.oauth2 import service_account
service_account_key = NAME
credentials = service_account.Credentials.from_service_account_info(service_account_key)
scoped_credentials = credentials.with_scopes(
  [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/analytics.readonly'
  ])

def sagyou(SPREADSHEET_KEY,SPREADSHEET_NAME):
    gc = gspread.gspread.authorize(scoped_credentials)
    wb = gs.open_by_key(SPREADSHEET_KEY)
    sagyou = wb.worksheet(SPREADSHEET_NAME)
    return sagyou


def last(SPREADSHEET_KEY,SPREADSHEET_NAME):
    gc = gspread.gspread.authorize(scoped_credentials)
    wb = gc.open_by_key(SPREADSHEET_KEY)
    ss = wb.worksheet(SPREADSHEET_NAME)
    str_list = list(filter(None, ss.col_values(1)))
    next_row = str(len(str_list) + 1)
    last = int(next_row)
    return last


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
        row = int(value)
        ss.update_cell(row, 1, data)
        await message.channel.send(f'更新します {message.author}!{data}')
    else:
        print('error')

client.run(TOKEN)
