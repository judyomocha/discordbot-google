import signal
import sys
from types import FrameType
from flask import Flask
from utils.logging import logger
app = Flask(__name__)
import discord
import json
import os
import pya3rt
from dotenv import load_dotenv
from collections import defaultdict, deque
from pathlib import Path
from discord import Intents
from discord.ext import commands
from apiclient.discovery import build
from discord.player import FFmpegPCMAudio
from discord.channel import VoiceChannel
# .envファイルの内容を読み込見込む
load_dotenv()
TOKEN = os.environ['TOKEN']
TALK_API_KEY = os.environ['TALK_API_KEY']

from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.cloud import texttospeech
from google.oauth2 import service_account
from googleapiclient.discovery import build


intents: Intents = discord.Intents.all()
client = discord.Client(intents=intents)
voiceChannel: VoiceChannel 

@client.event
async def on_ready():
    print('Login!!!')

@client.event
@client.event
async def check_queue(self, ctx):
    if message.author.bot:
        return
    else :
         text = message.content
         if message.content == '!con':
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Connected to voice channel: '{channel}'")
            await message.channel.send('読み上げるよ！')
            return
         if message.content == '!en':
            await channel.stop()
            await message.channel.send('またね！')           
            return
         elif message.content != '!con' or '!en':
              chat_client = pya3rt.TalkClient(TALK_API_KEY)
              response = chat_client.talk(message)
              txt = ((chat_client.talk(message.content)['results'][0]['reply']))
            
              from google.cloud import texttospeech
              client = texttospeech.TextToSpeechClient()
              synthesis_input = texttospeech.SynthesisInput(text=txt)
              voice = texttospeech.VoiceSelectionParams(
                  language_code="ja-JP",
                  name="ja-JP-Wavenet-D",
                  ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
              )
              audio_config = texttospeech.AudioConfig(
                   audio_encoding=texttospeech.AudioEncoding.MP3
              )
              response = client.synthesize_speech(
                  input=synthesis_input, voice=voice, audio_config=audio_config
              )
              with open("hello.mp3", "wb") as out:
                  out.write(response.audio_content)
                  print('Audio content written to file "hello.mp3"')
                  message.guild.voice_client.play(discord.FFmpegPCMAudio("hello.mp3"))
         return

client.run(TOKEN)
            
