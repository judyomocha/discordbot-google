import discord
import os
from discord import Intents
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
SPREADSHEET_NAME = os.environ['SPREADSHEET_NAME']
NAME = os.environ['NAME']


from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


def last(SPREADSHEET_KEY,SPREADSHEET_NAME):
    import gspread
    credentials = NAME
    gc = gspread.service_account_from_dict(credentials)
    wb = gc.open_by_key(SPREADSHEET_KEY)
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
        row = int(value)
        ss.update_cell(row, 1, data)
        await message.channel.send(f'更新します {message.author}!{data}')
    else:
        print('error')

client.run(TOKEN)
