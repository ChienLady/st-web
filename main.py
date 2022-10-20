import streamlit as st
import numpy as np
import random

from src import home, cleans, people

def init():
    st.session_state.pages = {
        '🏠 Trang chủ': home.main,
        '🧹 Lịch Dọn dẹp': cleans.main,
        '🙍 Quản lý nhân sự': people.main
        # 2: money.main,
    }

def draw_style():
    st.set_page_config(page_title = 'Quản lý nhà chung',
                       page_icon = '🏠',
                       layout = 'wide',
                       menu_items = {
                          'Get help': 'https://www.facebook.com/chienlady/',
                          'Report a Bug': 'https://www.facebook.com/chienlady/',
                          'About': 'Trang web có mục đích riêng rư **phi lợi nhuận**.'
                       })

    style = '''
        <style>
            header {visibility: visible;}
            footer {visibility: hidden;}
        </style>
    '''
    st.markdown(style, unsafe_allow_html = True)

def load_page(page_name):
    st.session_state.pages[page_name]()

def main():
    init()
    draw_style()
    with st.sidebar:
        st.markdown('# Menu quản lý trong nhà')
        st.image('https://media.giphy.com/media/cYxRo3zzej4vTAcd4r/giphy.gif')
        page = st.selectbox('Chọn đích đến',
                            ('🏠 Trang chủ', '🧹 Lịch Dọn dẹp', '🙍 Quản lý nhân sự'),
                            key = 'choose_page')
    st.balloons()
    load_page(page)

if __name__ == '__main__':
    main()

