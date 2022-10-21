import streamlit as st
import pandas as pd
import os
from streamlit_chat import message
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
    st.session_state.message_history = []

def reset():
    st.session_state.message_history = []
    st.session_state.placeholder.empty()

def main():
    if 'message_history' not in st.session_state:
        init()
    st.session_state.placeholder = st.empty()

    text_in = st.empty()
    input_ = text_in.text_input('Đặt câu hỏi:')
    st.button('Đặt lại', key = 'btn_reset', on_click = reset)

    if input_ != '':
        st.session_state.message_history.append(input_)
        with st.spinner(text = 'Đang xử lý ...'):
            ans = detect_intent_text(input_).get('result')
        
        st.session_state.message_history.append(ans)
        with st.session_state.placeholder.container():
            for mess in st.session_state.message_history:
                message(mess, key = f't{st.session_state.idx}', is_user = True if st.session_state.idx % 2 == 0 else False)
                st.session_state.idx += 1
    input_ = text_in.text_input('Đặt câu hỏi:')

if __name__ == '__main__':
    main()
