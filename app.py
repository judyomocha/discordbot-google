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
TOKEN = os.environ['TOKEN']


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
async def on_message(message):
    global voiceChannel
    if message.author.bot:
        return
    else :
        text = message.content
        if message.content == '!con':
            voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
            await message.channel.send('読み上げるよ！')
            return
        if message.content == '!en':
            message.guild.voice_client.stop()
            await message.channel.send('またね！')
            await VoiceChannel.disconnect()
            return
        elif message.content != '!con' or '!en':
            from google.cloud import texttospeech
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="ja-JP",
                name="ja-JP-Wavenet-B",
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
            
