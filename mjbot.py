import os
from pathlib import Path
import discord
from discord.ext import commands
import logging
import requests
from dotenv import load_dotenv
from discord import MessageType

from datetime import *
from slackBotDB import engine,Message
from sqlalchemy.orm import sessionmaker

load_dotenv(dotenv_path=Path('.') / '.env')
#discord Bot
bot = commands.Bot(intents=discord.Intents.all(), proxy='http://127.0.0.1:7890')

@bot.event
async def on_ready():
    print("Logged in as mjwrap bot")
    logging.getLogger(__name__).debug(f"Logged in as mjwrap bot")

@bot.event
async def on_message(message):
    print(message)
    url=None
    for attachment in message.attachments:
        url=attachment.url
        break
    if url:
        sendSlack(url,message.content,str(message.id),message.type.value)

def sendSlack(url:str,prompt:str,id:str,msgType:int):
    hash=str(url.split("_")[-1]).split(".")[0]
    headers = {
        'Authorization': 'Bearer ' + os.environ["SLACK_BOT_TOKEN"],
    }
    btns=[{
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "U1"
                                },
                                "value": '/'.join(["1",id,hash]),
                                "action_id": "upscale1"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "U2"
                                },
                                "value": '/'.join(["2",id,hash]),
                                "action_id": "upscale2"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "U3"
                                },
                                "value": '/'.join(["3",id,hash]),
                                "action_id": "upscale3"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "U4"
                                },
                                "value": '/'.join(["4",id,hash]),
                                "action_id": "upscale4"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "🔄"
                                },
                                "value": '/'.join(["r", id, hash]),
                                "action_id": "reroll"
                            }
                        ]
                    },
        {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "V1"
                                },
                                "value": '/'.join(["1",id,hash]),
                                "action_id": "variation1"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "V2"
                                },
                                "value": '/'.join(["2",id,hash]),
                                "action_id": "variation2"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "V3"
                                },
                                "value": '/'.join(["3",id,hash]),
                                "action_id": "variation3"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "V4"
                                },
                                "value": '/'.join(["4",id,hash]),
                                "action_id": "variation4"
                            }
                        ]
                    }]
    json_data = {
        'channel': 'D054Y580GS0',
        "attachments": [
            {
                "blocks": [
                    {
                        "type": "image",
                        "image_url":url,
                        "alt_text":prompt
                    }
                ]
            }
        ]
    }
    if 'Image #' not in prompt:
        json_data['attachments'][0]['blocks'].extend(btns)
    response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, json=json_data)
    print(response.text)

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()
    bot.run(os.environ["DC_BOT_TOKEN"])