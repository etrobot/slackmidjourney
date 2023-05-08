import logging
from pathlib import Path

from dotenv import load_dotenv
logging.basicConfig(level=logging.DEBUG)
import os,requests

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from datetime import *
from slackBotDB import engine,Message
from sqlalchemy.orm import sessionmaker

load_dotenv(dotenv_path=Path('.') / '.env')
app = App(token=os.environ["SLACK_BOT_TOKEN"])

def PassPromptToSelfBot(prompt: str):
    payload = {"type": 2, "application_id": "936929561302675456", "guild_id": int(os.environ["MJSEVERID"]),
               "channel_id": int(os.environ["MJCHANNELID"]), "session_id": "2fb980f65e5c9a77c96ca01f2c242cf6",
               "data": {"version": "1077969938624553050", "id": "938956540159881230", "name": "imagine", "type": 1,
                        "options": [{"type": 3, "name": "prompt", "value": prompt}],
                        "application_command": {"id": "938956540159881230",
                                                "application_id": "936929561302675456",
                                                "version": "1077969938624553050",
                                                "default_permission": True,
                                                "default_member_permissions": None,
                                                "type": 1, "nsfw": False, "name": "imagine",
                                                "description": "Create images with Midjourney",
                                                "dm_permission": True,
                                                "options": [{"type": 3, "name": "prompt",
                                                             "description": "The prompt to imagine",
                                                             "required": True}]},
                        "attachments": []}}

    header = {
        'authorization': os.environ["DCTOKEN"]
    }
    response = requests.post("https://discord.com/api/v9/interactions",
                             json=payload, headers=header)
    print(response.text)
    return 200

@app.action("variation1")
def variation1(ack,body):
    Variation(ack, body)

@app.action("variation2")
def variation2(ack,body):
    Variation(ack, body)

@app.action("variation3")
def variation3(ack,body):
    Variation(ack, body)

@app.action("variation4")
def variation4(ack,body):
    Variation(ack, body)

def Variation(ack,body):
    data=body["actions"][0]["value"].split('/')
    index=data[0]
    messageId=data[1]
    messageHash=data[2]
    payload = {"type":3, "guild_id":int(os.environ["MJSEVERID"]),
            "channel_id": int(os.environ["MJCHANNELID"]),
            "message_flags":0,
            "message_id": messageId,
            "application_id": "936929561302675456",
            "session_id":"1f3dbdf09efdf93d81a3a6420882c92c",
            "data":{"component_type":2,"custom_id":"MJ::JOB::variation::{}::{}".format(index, messageHash)}}
    header = {
        'authorization' :os.environ["DCTOKEN"]
    }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header)
    if response.status_code==204:
        addMsg(messageId,body['user']['id'],body['channel']['id'],20)
        ack('V%s send'%index)
    return 200

@app.action("upscale1")
def upscale4(ack,body):
    Upscale(ack,body)

@app.action("upscale2")
def upscale4(ack,body):
    Upscale(ack,body)

@app.action("upscale3")
def upscale4(ack,body):
    Upscale(ack,body)

@app.action("upscale4")
def upscale4(ack,body):
    Upscale(ack,body)


def Upscale(ack,body):
    data=body["actions"][0]["value"].split('/')
    index=data[0]
    messageId=data[1]
    messageHash=data[2]
    payload = {"type":3,
    "guild_id":int(os.environ["MJSEVERID"]),
    "channel_id":int(os.environ["MJCHANNELID"]),
    "message_flags":0,
    "message_id": messageId,
    "application_id":"936929561302675456",
    "session_id":"45bc04dd4da37141a5f73dfbfaf5bdcf",
    "data":{"component_type":2,
            "custom_id":"MJ::JOB::upsample::{}::{}".format(index, messageHash)}
        }
    header = {
        'authorization' : os.environ["DCTOKEN"]
    }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header)
    if response.status_code==204:
        addMsg(messageId,body['user']['id'],body['channel']['id'],19)
        ack('U%s send'%index)
    return 200

@app.command("/imagine")
def handle_imagine_command(ack, body, command):
    # df=pd.DataFrame(data=[time_stamp,incoming_text,user,channel],columns=['date','sPrompt','sUserId','sChannel'])
    prompt=body['command']+' '+body['text'].replace('*',' ')
    print(body)
    response = PassPromptToSelfBot(prompt)
    if response.status_code==204:
        ack(f"Your imagine: {body['text']} is being generated")
    else:
        ack(f"Failed: {body['text']}")

@app.action("reroll")
def Reroll(ack,body):
    print(body)
    data=body["actions"][0]["value"].split('/')
    messageId=data[1]
    messageHash=data[2]
    payload = {"type":3,
    "guild_id":int(os.environ["MJSEVERID"]),
    "channel_id":int(os.environ["MJCHANNELID"]),
    "message_flags":0,
    "message_id": messageId,
    "application_id":"936929561302675456",
    "session_id":"45bc04dd4da37141a5f73dfbfaf5bdcf",
    "data":{"component_type":2,
            "custom_id":"J::JOB::reroll::0::%s::SOLO"%messageHash}
        }
    header = {
        'authorization' : os.environ["DCTOKEN"]
    }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header)
    if response.status_code==204:
        addMsg(messageId,body['user']['id'],body['channel']['id'],19)
        ack('re-roll send')
    return response

def addMsg(msgid,userid,channelid,prompt,msgType):
    new_message = Message(msgid=msgid, createTime=datetime.now(), userid=userid, channelid=channelid,
                          prompt=prompt, msgType=msgType)
    session.add(new_message)
    session.commit()

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()