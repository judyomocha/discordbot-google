import signal
import sys
from types import FrameType
from flask import Flask
from utils.logging import logger
app = Flask(__name__)
import discord
import json
import os
from dotenv import load_dotenv
from collections import defaultdict, deque
from pathlib import Path
from discord import Intents
from apiclient.discovery import build
from discord.ext import commands
from discord.player import FFmpegPCMAudio
from discord.channel import VoiceChannel
# .envファイルの内容を読み込見込む
load_dotenv()

from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.cloud import texttospeech
from google.oauth2 import service_account
from googleapiclient.discovery import build


intents: Intents = discord.Intents.all()
client = discord.Client(intents=intents)
voiceChannel: VoiceChannel 

load_dotenv()
TOKEN = os.environ['TOKEN']
GUILD_ID = os.environ['GUILD_ID']
CHANNEL_ID = os.environ['CHANNEL_ID']
SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
SHEET_NAME = os.environ['SHEET_NAME']
GCP_SA_KEY = os.environ['GCP_SA_KEY']




intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id != int(CHANNEL_ID):
        return

    if message.channel.id == int(CHANNEL_ID):
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        parsed = json.loads(GCP_SA_KEY)
        gc = gspread.service_account_from_dict(parsed)
        sh = gc.open_by_key(SPREADSHEET_KEY)
        ws = sh.worksheet(SHEET_NAME)
        def next_available_row(ws):
            str_list = list(filter(None, ws.col_values(1)))
            return str(len(str_list) + 1)
        next_row = next_available_row(ws)
        ws.update_cell(next_row, 1, message.content)
        await message.channel.send(f'更新します {message.author}!')
        return

client.run(TOKEN)
