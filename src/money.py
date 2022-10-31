import streamlit as st
import pandas as pd
import numpy as np
import os

THIS_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(THIS_PATH)
DDIR_PATH = os.path.dirname(DIR_PATH)
ASSET_PATH = os.path.join(DDIR_PATH, 'Assets')

def check_key():
    st.sidebar.subheader('Tính năng hiện tại đang được thay thế, bản cũ có thể nhập Key để truy cập')
    key = st.sidebar.text_input('Key', type = 'password')
    if st.sidebar.checkbox('Xác nhận'):
        if key == 'shinichien':
            return True
    else:
        st.sidebar.warning('Key nhập vào chưa đúng')
        return False

def read_csv(path = os.path.join(ASSET_PATH, 'names.csv')):
    df = pd.read_csv(path, sep = ',', encoding = 'utf-8')
    st.session_state.df = df.sort_values(by = ['teams'])
    st.session_state.df.index = range(1, st.session_state.df.shape[0] + 1)

def get_names():
    names = st.session_state.df['names']
    first_names = [name.split(' ')[-1] for name in names]
    return names, first_names

def get_money_names():
    names = set([col[0] for col in st.session_state.money_df.columns])
    names.remove('Chung');names.remove('Tổng tiền')
    return names

def read_money_csv(path = os.path.join(ASSET_PATH, 'money.csv')):
    money_df = pd.read_csv(path, sep = ',', encoding = 'utf-8', header = [0, 1])
    money_df.index = range(1, len(money_df.index) + 1)
    st.session_state.money_df = money_df.sort_index()

def create_table_full(names):
    mn_names = get_money_names()
    if sorted(mn_names) != sorted(names):
        for name in names:
            if name not in mn_names:
                first_name = name.split(' ')[-1]
                st.session_state.money_df[first_name, 'mua'] = []
                st.session_state.money_df[first_name, 'giá'] = []
        save_csv()
    try:
        st.session_state.table_money.empty()
    except:
        pass
    read_csv()
    st.session_state.table_money = st.empty()
    with st.session_state.table_money.container():
        st.dataframe(st.session_state.money_df, use_container_width = True)

def create_table_only(name):
    first_name = name.split(' ')[-1]
    st.session_state.money_df_only = st.session_state.money_df[[first_name]]
    try:
        st.session_state.table_only.empty()
    except:
        pass
    read_csv()
    st.session_state.table_only = st.empty()
    with st.session_state.table_only.container():
        st.dataframe(st.session_state.money_df_only, use_container_width = True)

def save_csv(path = os.path.join(ASSET_PATH, 'money.csv')):
    st.session_state.money_df.to_csv(path, sep = ',', encoding = 'utf-8', index = False)

def init_old():
    read_csv()
    read_money_csv()

def add_more(name, thing, price):
    if thing != '' and price != '':
        first_name = name.split(' ')[-1]
        df_only = st.session_state.money_df[first_name]
        df_only.loc[len(df_only.index) + 1] = [thing, price]
        print(df_only.head())
        st.session_state.money_df[first_name]['mua'] = df_only
        print(df_only.values.T)
        print(st.session_state.money_df[first_name].head())
        st.session_state.money_df.fillna('Chưa có', inplace = True)
        save_csv()
    else:
        st.warning('Không được để trống các trường thông tin', icon = '⚠️')

def old():
    init_old()
    names, first_names = get_names()
    names = list(names)
    
    name = st.selectbox(
        'Lựa chọn điểm xem phù hợp',
        ('Tổng tiền', 'Chung') + tuple(names)
    )
    if name == 'Tổng tiền':
        create_table_full(first_names)
    else:
        create_table_only(name)
        thing = st.text_input('Mua gì:', key = f't1').strip()
        price = st.text_input('Giá:', key = f'p1').strip()
        st.button('Xác nhận', key = f'b1', on_click = add_more, args = (name, thing, price)) 

import gspread
from gspread import Spreadsheet
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json

def storage():
    dir_path = 'https://drive.google.com/drive/folders/1UaweXDmbHwYWplKwqei-gzXxBXH63aMK?usp=sharing'
    ls_ids = {
        '2022': {
            'Tháng 9': '1PtcvXfCidTGtbYc3RLPettgan8hJN4sdghMvfEfKzQU',
            'Tháng 10': '1kBg_GQeAMeNY2fhhfPIE6qVdSGhsCYA61kK3YD51AZE',
            'Tháng 11': '1rS51rM-NWMHfaC5JRqf5QZPr4epCXqlmWkD3hnpCJCQ',
            'Tháng 12': '1zIZ1DCgsf2LwRLBqq5cgL7My5kbwX4VyaynXbW3hBqQ'
        },
        '2023': {
            'Tháng 1': '1ngXzl-5V92GvDzK3uNQzIhgYszz7-15r9xeSF4E2nIM',
            'Tháng 2': '1CjHXewF-A5iZLRbecIhY0RaxnMl4XhDaVMBM_JEHF94',
            'Tháng 3': '1h7Fo5RHKFHk09ll8snkkCEqE_llACLj7SZ6UMs4b5YI',
            'Tháng 4': '1cYTyv0166Xa8RGXXyp9sEV0g2HJBXZYgHU9t365LAKc',
            'Tháng 5': '1EWEmNhP2bWARqURHeXA8OtXxNvBBUXyvCh1CnDTlkhw',
            'Tháng 6': '1IL8wXdOyYO5Ug03FxCh1lcB7sL8AOwUy_U7SXzW6p-k',
            'Tháng 7': '1Hc6zC0OXh4jGy_9LIyD5ky672Z8DzaiHQUQbqzrolhE',
            'Tháng 8': '13zpRLH5kCHb4GyB4Y6vDv6LnPzZRyasFlPgq-8Mw6WA',
            'Tháng 9': '1nt5XF7IeRyX2wT1On-3uYqNq6HMdWY4CI48VvB7p2S0',
            'Tháng 10': '1fbu4dVTXw1d72_ZPhOlVZBCJrB0oa_WIGLbljNlRi7A',
            'Tháng 11': '1ID7n4thzXqdiny9YreG9p8KKx4qXJiX5tl_CnuxyJX4',
            'Tháng 12': '1TUQSdOD0bpKC8w7b-QmIT0i2YQjXQfktbWJ6x15Cna0'
        }
    }
    return dir_path, ls_ids

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive']

def get_creds(scope = scope, path = os.path.join(ASSET_PATH, 'credentials_sheet.json')):
    creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
    return gspread.authorize(creds)

def open_google_spreadsheet(spreadsheet_id: str) -> Spreadsheet:
    client = get_creds(scope = ['https://spreadsheets.google.com/feeds'])
    return client.open_by_key(spreadsheet_id)

def create_summary(id):
    with st.spinner('Đang tạo link và bảng tóm tắt tháng'):
        sheet = open_google_spreadsheet(id)
        url = sheet.url
        st.write(f'Đường dẫn tới file tiền nhà của tháng: [đường dẫn]({url})')
        all_sheets = sheet.worksheets()
        name_people = [s.title for s in all_sheets][1:]
        human_read = ', '.join(name_people)
        st.markdown(f'#### Số lượng người: {len(name_people)} ({human_read}).')
        sheet1 = all_sheets[0]

        # House rent, electric, water, ...
        st.markdown('#### 1. Phí chung')
        response = sheet1.col_values(3)[1:]
        header = response[::2]
        value = response[1::2]
        df1 = pd.DataFrame([value], index = ['.'], columns = header)
        st.dataframe(df1, use_container_width = True)

        # Personal cash
        st.markdown('#### 2. Tiền mua đồ của mọi người')
        name = sheet1.col_values(1)[2:]
        price = sheet1.col_values(2)[2:]
        remain = sheet1.col_values(6)[2:]
        data = np.array([price, remain], dtype = object).T
        df2 = pd.DataFrame(data, index = name)
        df2 = df2.drop(index = '')
        df2.columns = ['Giá tiền', 'Thừa/Thiếu']
        st.dataframe(df2, use_container_width = True)


def new():
    dir_path, ls_ids = storage()
    st.header('Toàn bộ file sheet đều lưu ở đây')
    st.write(f'Đường dẫn tới Google Drive [link]({dir_path})')

    y22 = ls_ids['2022']
    y23 = ls_ids['2023']

    tab1, tab2 = st.tabs(['Năm 2022', 'Năm 2023'])
    with tab1:
        st.header('Năm 2022')
        month = st.selectbox('Chọn tháng', tuple(y22.keys()))
        id = y22.get(month)
        create_summary(id)
    with tab2:
        st.header('Năm 2023')
        month = st.selectbox('Chọn tháng', tuple(y23.keys()))
        id = y23.get(month)
        create_summary(id)
def main():
    if check_key():
        old()
    else:
        new()
        
if __name__ == '__main__':
    main()
