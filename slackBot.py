import csv
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from vika import *

load_dotenv(dotenv_path='.env')
app = App(token=os.environ["SLACK_BOT_TOKEN"])
PROXY={'https':'http://127.0.0.1:7890'}


def PassPromptToSelfBot(prompt: str,slack_chn:str=None):
    if slack_chn is None:
        dcChannel=os.environ['MJCHNSAVE']
    elif slack_chn in chnlDf['SL'].values:
        dcChannel = chnlDf.loc[chnlDf['SL']==slack_chn,'DC'].values[0]
    else:
        return 500
    payload = {"type": 2, "application_id": "936929561302675456", "guild_id": int(os.environ["MJSEVERID"]),
               "channel_id":dcChannel, "session_id": "2fb980f65e5c9a77c96ca01f2c242cf6",
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
        'authorization': dcToken
    }
    response = requests.post("https://discord.com/api/v9/interactions",
                             json=payload, headers=header,proxies=PROXY)
    return response

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

def Variation(ack, body):
    slack_chn = body['channel']['id']
    data = body["actions"][0]["value"].split('/')
    index = data[0]
    messageId = data[1]
    messageHash = data[2]
    if variation(slack_chn,index,messageId,messageHash).status_code==204:
        ack(f'V%s send'%body["actions"][0]["value"].split('/')[0])

def variation(slack_chn,index,messageId,messageHash):
    payload = {"type": 3, "guild_id": int(os.environ["MJSEVERID"]),
               "channel_id": chnlDf.loc[chnlDf['SL']==slack_chn,'DC'].values[0],
               "message_flags": 0,
               "message_id": messageId,
               "application_id": "936929561302675456",
               "session_id": "1f3dbdf09efdf93d81a3a6420882c92c",
               "data": {"component_type": 2, "custom_id": "MJ::JOB::variation::{}::{}".format(index, messageHash)}}
    header = {
        'authorization' :vikaData('recNIX08aLFPB')
    }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header,proxies=PROXY)
    return response

@app.action("upscale1")
def upscale1(ack,body):
    Upscale(ack,body)

@app.action("upscale2")
def upscale2(ack,body):
    Upscale(ack,body)

@app.action("upscale3")
def upscale3(ack,body):
    Upscale(ack,body)

@app.action("upscale4")
def upscale4(ack,body):
    Upscale(ack,body)


def Upscale(ack,body):
    print(body)
    slack_chn = body['channel']['id']
    data=body["actions"][0]["value"].split('/')
    index=data[0]
    messageId=data[1]
    messageHash=data[2]
    if upscale(slack_chn,index,messageId,messageHash).status_code==204:
        ack(f'U%s send' % index)

def upscale(slack_chn,index,messageId,messageHash):
    payload = {"type":3,
    "guild_id":int(os.environ["MJSEVERID"]),
    "channel_id":chnlDf.loc[chnlDf['SL']==slack_chn,'DC'].values[0],
    "message_flags":0,
    "message_id": messageId,
    "application_id":"936929561302675456",
    "session_id":"45bc04dd4da37141a5f73dfbfaf5bdcf",
    "data":{"component_type":2,
            "custom_id":"MJ::JOB::upsample::{}::{}".format(index, messageHash)}
        }
    header = {
        'authorization' : vikaData('recNIX08aLFPB')
    }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header,proxies=PROXY)
    return response

@app.command("/imagine")
def handle_imagine_command(ack, body):
    slack_chn = body['channel_id']
    if slack_chn not in chnlDf['SL'].values:
        ack(f"未知账号: {body['channel_id']} ，请用/register命令发送注册码进行注册")
        return
    if chnlDf.loc[chnlDf['SL']==slack_chn,'EXP'].values[0]<datetime.now().date():
        ack(f"{slack_chn}到期")
        return
    prompt=body['command']+' '+body['text'].replace('*',' ')
    response = PassPromptToSelfBot(prompt,slack_chn)
    if response.status_code==204:
        ack(f"Your imagine: {body['text']} is being generated")
    else:
        ack(f"Failed: {body['text']}")


@app.command("/register")
def handle_register_command(ack, body):
    slack_chn = body['channel_id']
    data = body['text']
    if data in chnlDf['User'].values:
        dfSlChn = chnlDf.loc[chnlDf['User'] == data, 'SL'].values[0]
        print('dfSlChn:%s,slack_chn:%s'%(dfSlChn,slack_chn))
        if dfSlChn==slack_chn:
            ack(f"{data}已注册！")
        else:
            try:
                chnlDf.loc[chnlDf['User'] == data, 'SL'] = slack_chn
                register(chnlDf.loc[chnlDf['User'] == data, 'recordId'].values[0],slack_chn)
                ack(f"注册成功: {data}")
            except:
                ack(f"注册失败({data}),请联系管理员")
    else:
        ack(f"注册码 {data} 不存在")


@app.action("reroll")
def Reroll(ack,body):
    slack_chn=body['channel']['id']
    data=body["actions"][0]["value"].split('/')
    messageId=data[1]
    messageHash=data[2]
    payload={
        'type': 3,
        'nonce': '1102619377825480704',
        'guild_id': int(os.environ["MJSEVERID"]),
        'channel_id': chnlDf.loc[chnlDf['SL']==slack_chn,'DC'].values[0],
        'message_flags': 0,
        'message_id': messageId,
        'application_id': '936929561302675456',
        'session_id': '24de03cb9d9a886b717a4294daa6a8db',
        'data': {
            'component_type': 2,
            'custom_id': 'MJ::JOB::reroll::0::%s::SOLO'%messageHash,
        },
    }
    header = {
        'authorization' : dcToken
    }
    response = requests.post("https://discord.com/api/v9/interactions",json = payload, headers = header,proxies=PROXY)
    if response.status_code==204:
        ack(f're-roll send')
    return response


if __name__ == "__main__":
    chnlDf = vikaMjDf()
    dcToken =  vikaData('recNIX08aLFPB')
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()