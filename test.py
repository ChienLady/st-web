import streamlit as st
from streamlit_chat import message

message('Welcome to Streamlit-Chat')

if 'message_history' not in st.session_state:
    st.session_state.message_history = []

for message_ in st.session_state.message_history:
    message(message_,is_user=True) # display all the previous message

placeholder = st.empty() # placeholder for latest message
input_ = st.text_input('you')
st.session_state.message_history.append(input_)

with placeholder.container():
    message( st.session_state.message_history[-1], is_user=True) # display the latest message
