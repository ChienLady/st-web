import streamlit as st
import pandas as pd
import os
from streamlit_chat import message as st_mess
from google.cloud import dialogflow

THIS_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(THIS_PATH)
DDIR_PATH = os.path.dirname(DIR_PATH)
ASSET_PATH = os.path.join(DDIR_PATH, 'Assets')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(ASSET_PATH, 'credentials.json')
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
    return {
        'query_text': response.query_result.query_text,
        'intent': response.query_result.intent.display_name,
        'confidence': response.query_result.intent_detection_confidence,
        'result': response.query_result.fulfillment_text
    }

def init():
    st.session_state.idx = 0
    st.session_state.history = []

def reset():
    st.session_state.history = []

def generate_answer():
    user_message = st.session_state.input_text
    if user_message != '':
        message_bot = detect_intent_text(user_message).get('result')
    else:
        message_bot = 'Bạn có thể hỏi lại được không?'

    st.session_state.history.append({'message': user_message, 'is_user': True})
    st.session_state.history.append({'message': message_bot, 'is_user': False})

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
