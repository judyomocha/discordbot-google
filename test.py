import discord
import os
from discord import Intents
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
SPREADSHEET_NAME = os.environ['SPREADSHEET_NAME']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

def get_cred_config() -> Dict[str, str]:
    secret = os.environ.get("CLOUD_SQL_CREDENTIALS_SECRET")
    if secret:
        return json.loads(secret)

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
GOOGLE_APPLICATION_CREDENTIALS = get_cred_config()
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_APPLICATION_CREDENTIALS, scope)

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


ss = sagyou(SPREADSHEET_KEY, SPREADSHEET_NAME)
value = last(SPREADSHEET_KEY, SPREADSHEET_NAME)
row = int(value)
ss.update_cell(row, 1, 'テストテストテスト')
print(value)
