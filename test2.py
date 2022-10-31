# import dateparser

# settings = {'TIMEZONE': 'UTC', 'TO_TIMEZONE': 'Asia/Ho_Chi_Minh'}
# r = dateparser.parse('tháng này', languages = ['vi'], locales = ['vi'], settings = settings)
# print(r)

import streamlit as st
import pandas as pd
import os
from streamlit_chat import message as st_mess
from google.cloud import dialogflow
from google.protobuf.json_format import MessageToJson
import json

THIS_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(THIS_PATH)
DDIR_PATH = os.path.dirname(DIR_PATH)
ASSET_PATH = os.path.join(DDIR_PATH, 'Assets')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'E:\st-web\Assets\credentials_dialogflow.json'
os.environ['GOOGLE_CLOUD_PROJECT'] = '935238694151'

PROJECT_ID = 'homecb-qrl9'
SESSION_ID = '1234'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(PROJECT_ID, SESSION_ID)

def detect_intent_text(text, language_code = 'vi-VN'):
    text_input = dialogflow.TextInput(text = text, language_code = language_code)
    query_input = dialogflow.QueryInput(text = text_input)

    response = session_client.detect_intent(
        request = {'session': session, 'query_input': query_input}
    )
    json_response = json.loads(MessageToJson(response._pb)).get('queryResult')
    return {
        'query_text': json_response.get('queryText'),
        'parameters':json_response.get('parameters'),
        'intent': json_response.get('intent').get('displayName'),
        'confidence': json_response.get('intentDetectionConfidence'),
        'result': json_response.get('fulfillmentMessages')[0]['text']['text'][0]
    }

print(detect_intent_text('tiền nhà tháng trước'))
print(detect_intent_text('xin chào'))

# r = detect_intent_text('tiền nhà tháng trước')
# print(r)

