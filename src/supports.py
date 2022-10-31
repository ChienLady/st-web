import streamlit as st
import pandas as pd
import os
from streamlit_chat import message as st_mess
from google.cloud import dialogflow
from google.protobuf.json_format import MessageToJson
import json
from datetime import datetime
from .money import storage

THIS_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(THIS_PATH)
DDIR_PATH = os.path.dirname(DIR_PATH)
ASSET_PATH = os.path.join(DDIR_PATH, 'Assets')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(ASSET_PATH, 'credentials_dialogflow.json')
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

def init():
    st.session_state.idx = 0
    st.session_state.history = []

def reset():
    st.session_state.history = []

HARDCORE_INTENTS = ['get_link']
def process_hardcore(res):
    if res['intent'] == 'get_link':
        time = res['parameters'].get('date-time')
        try:
            time = time.get('startDate')
            time = time.split('T')[0]
            time = datetime.strptime(time, '%Y-%m-%d')
            month, year = time.month, time.year
        except:
            return 'Thời gian không hợp lệ!'

        dir_path, ls_ids = storage()
        data = ls_ids.get(str(year))
        if data == None:
            return 'Không tìm thấy dữ liệu!'
        id = data.get('Tháng '+ str(month))
        if id == None:
            return 'Không tìm thấy dữ liệu!'
        url = 'https://docs.google.com/spreadsheets/d/{id}/edit'.format(id = id)
        return 'Đường dẫn tới file tiền nhà tháng {m} năm {y}: {u}.'.format(m = month, y = year, u = url)

def generate_answer():
    if len(st.session_state.history) > 6:
        st.session_state.history = st.session_state.history[2:]
    user_message = st.session_state.input_text
    if user_message != '':
        res = detect_intent_text(user_message)
        if res['intent'] in HARDCORE_INTENTS:
            message_bot = process_hardcore(res)
        else:
            message_bot = res.get('result')
    else:
        message_bot = 'Bạn có thể hỏi lại được không?'

    st.session_state.history.append({'message': user_message, 'is_user': True, 'avatar_style': 'avataaars', 'seed': st.session_state.idx})
    st.session_state.history.append({'message': message_bot, 'is_user': False, 'avatar_style': 'bottts', 'seed': st.session_state.idx})

def main():
    if 'history' not in st.session_state:
        init()
    st.text_input('Đặt câu hỏi', key = 'input_text', on_change = generate_answer)

    st.button('Đặt lại bảng trả lời', key = 'btn_reset', on_click = reset)

    for chat in st.session_state.history:
        st_mess(**chat, key = st.session_state.idx)
        st.session_state.idx += 1

if __name__ == '__main__':
    main()
