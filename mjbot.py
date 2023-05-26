import csv
from pathlib import Path
import discord
import numpy as np
from discord.ext import commands
import logging

from vika import *

PROXY='http://127.0.0.1:7890'
load_dotenv(dotenv_path=Path('.') / '.env')
#discord Bot
bot = commands.Bot(intents=discord.Intents.all(), proxy=PROXY)

@bot.event
async def on_ready():
    print("Logged in as mjwrap bot")
    logging.getLogger(__name__).debug(f"Logged in as mjwrap bot")

@bot.event
async def on_message(message):
    if not 'chnlDf' in globals():
        chnlDf=vikaMjDf()
    url=None
    for attachment in message.attachments:
        url=attachment.url
        break
    print(message.channel.id, url,message.content,str(message.id),message)
    if url:
        hash = str(url.split("_")[-1]).split(".")[0]
        with open('midjourney.csv', mode='a') as file:
            file.write('\n%s, "%s", %s, %s'%(message.content.replace(' (fast)','').split('**')[1].strip(),message.channel.id,hash,'https://cdn.midjourney.com/%s/0_' % hash))
        if message.channel.id != int(os.environ["MJCHNSAVE"]):
            if pd.isnull(chnlDf.loc[chnlDf['DC']==str(message.channel.id),'SL'].values[0]):
                chnlDf=vikaMjDf()
            sendSlack(chnlDf.loc[chnlDf['DC']==str(message.channel.id),'SL'].values[0], url,message.content,str(message.id),message.author.name)

def sendSlack(slack_ch:str,url:str,prompt:str,id:str,serviceName:str):
    hash=str(url.split("_")[-1]).split(".")[0]
    imgUrl = url
    if 'Image #' not in prompt:
        imgUrl='https://cdn.midjourney.com/%s/grid_0.webp'%hash
        print(imgUrl)
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
                                "value": '/'.join(["1",id,hash,serviceName]),
                                "action_id": "upscale1"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "U2"
                                },
                                "value": '/'.join(["2",id,hash,serviceName]),
                                "action_id": "upscale2"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "U3"
                                },
                                "value": '/'.join(["3",id,hash,serviceName]),
                                "action_id": "upscale3"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "U4"
                                },
                                "value": '/'.join(["4",id,hash,serviceName]),
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
                                "value": '/'.join(["1",id,hash,serviceName]),
                                "action_id": "variation1"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "V2"
                                },
                                "value": '/'.join(["2",id,hash,serviceName]),
                                "action_id": "variation2"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "V3"
                                },
                                "value": '/'.join(["3",id,hash,serviceName]),
                                "action_id": "variation3"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "V4"
                                },
                                "value": '/'.join(["4",id,hash,serviceName]),
                                "action_id": "variation4"
                            }
                        ]
                    }]
    json_data = {
        'channel': slack_ch,
        "attachments": [
            {
                "blocks": [
                    {
                        "type": "image",
                        "image_url":imgUrl,
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
    global chnlDf
    bot.run(os.environ["DC_BOT_TOKEN"])