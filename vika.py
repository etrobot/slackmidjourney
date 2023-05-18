import json

import pandas as pd
import os
from dotenv import load_dotenv

import requests
load_dotenv(dotenv_path='.env')

def vikaData(id:str):
    headersVika = {
        'Authorization':'Bearer %s'%os.environ['VIKA'],
        'Connection': 'close'
    }
    vikaUrl = 'https://api.vika.cn/fusion/v1/datasheets/dstMiuU9zzihy1LzFX/records?viewId=viwoAJhnS2NMT&fieldKey=name'
    vikajson = requests.get(vikaUrl, headers=headersVika).json()
    print(vikajson)
    return [x['fields']['value'] for x in vikajson['data']['records'] if x['recordId'] == id][0]

def vikaMjDf():
    headers = {
        'Authorization': 'Bearer %s'%os.environ['VIKA'],
    }
    params = {
        'viewId': 'viwr9fdY8TYtN',
        'fieldKey': 'name',
    }
    response = requests.get('https://api.vika.cn/fusion/v1/datasheets/dstiNYM27aCVoaMP4b/records', params=params,
                            headers=headers)
    result = response.json()
    # print(result)
    df = pd.json_normalize(result['data']['records'])
    df.drop(columns=['createdAt', 'updatedAt'],inplace=True)
    df.columns=[x.replace('fields.','') for x in df.columns]
    df['EXP']=pd.to_datetime(df['EXP'],unit='ms').dt.date
    print(df)
    return df

def register(recordId,slack_chn):
    headers = {
        'Authorization': 'Bearer %s'%os.environ['VIKA'],
    }

    params = {
        'viewId': 'viwr9fdY8TYtN',
        'fieldKey': 'name',
    }

    json_data = {
        'records': [
            {
                'recordId': recordId,
                'fields': {
                    'SL': slack_chn,
                    'EXP': 1686153600000,
                }
            }
        ],
        'fieldKey': 'name',
    }

    response = requests.patch(
        'https://api.vika.cn/fusion/v1/datasheets/dstiNYM27aCVoaMP4b/records',
        params=params,
        headers=headers,
        json=json_data,
    )

    return response