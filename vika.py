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

def vikaMjDf(indexCol):
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
    df = pd.DataFrame(v['fields'] for v in result['data']['records'])
    df['EXP']=pd.to_datetime(df['EXP'],unit='ms').dt.date
    df.set_index(indexCol,inplace=True)
    return df