import json

import pandas as pd
import os
from dotenv import load_dotenv

import requests
load_dotenv(dotenv_path='.env')

def vikaData(id:str):
    headersVika = {
        'Authorization': os.environ['VIKA'],
        'Connection': 'close'
    }
    vikaUrl = 'https://api.vika.cn/fusion/v1/datasheets/dstMiuU9zzihy1LzFX/records?viewId=viwoAJhnS2NMT&fieldKey=name'
    vikajson = json.loads(requests.get(vikaUrl, headers=headersVika).text)['data']['records']
    return [x['fields']['value'] for x in vikajson if x['recordId'] == id][0]

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
    df = pd.DataFrame(v['fields'] for v in result['data']['records'])
    df['EXP']=pd.to_datetime(df['EXP'],unit='ms').dt.date
    df.set_index(indexCol,inplace=True)
    return df