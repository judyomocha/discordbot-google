import discord
import os
from discord import Intents
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
SPREADSHEET_NAME = os.environ['SPREADSHEET_NAME']

# Import the Secret Manager client library.
from google.cloud import secretmanager
# GCP project in which to store secrets in Secret Manager.
project_id = "YOUR_PROJECT_ID"
# ID of the secret to create.
secret_id = "YOUR_SECRET_ID"
# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()
# Build the parent name from the project.
parent = f"projects/{project_id}"
# Create the parent secret.
secret = client.create_secret(
    request={
        "parent": parent,
        "secret_id": secret_id,
        "secret": {"replication": {"automatic": {}}},
    }
)
# Add the secret version.
version = client.add_secret_version(
    request={"parent": secret.name, "payload": {"data": b"hello world!"}}
)
# Access the secret version.
response = client.access_secret_version(request={"name": version.name})
# Print the secret payload.
#
# WARNING: Do not print the secret in a production environment - this
# snippet is showing how to access the secret material.
payload = response.payload.data.decode("UTF-8")
print("Plaintext: {}".format(payload))


import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(payload, scope)

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
        row = int(value)
        ss.update_cell(row, 1, data)
        await message.channel.send(f'更新します {message.author}!{data}')
    else:
        print('error')

client.run(TOKEN)
