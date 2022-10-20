import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

THIS_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(THIS_PATH)
DDIR_PATH = os.path.dirname(DIR_PATH)
ASSET_PATH = os.path.join(DDIR_PATH, 'Assets')
load_dotenv(os.path.join(ASSET_PATH, '.env'))

def check_key():
    temp1 = st.subheader('Nhập đúng KEY để truy cập')
    key = st.sidebar.text_input('Key', type = 'password')
    if st.sidebar.checkbox('Xác nhận'):
        if key == os.environ.get('KEY'):
            temp1.empty()
            return True
    else:
        st.sidebar.error('Key nhập vào chưa đúng')
        return False

def read_csv(path = os.path.join(ASSET_PATH, 'names.csv')):
    df = pd.read_csv(path, sep = ',', encoding = 'utf-8')
    st.session_state.df = df.sort_values(by = ['teams'])
    st.session_state.df.index = range(1, st.session_state.df.shape[0] + 1)

def save_csv(path = os.path.join(ASSET_PATH, 'names.csv')):
    st.session_state.df.to_csv(path, sep = ',', encoding = 'utf-8', index = False)

def create_table():
    try:
        st.session_state.table.empty()
    except:
        pass
    read_csv()
    st.session_state.table = st.empty()
    with st.session_state.table.container():
        st.dataframe(st.session_state.df, use_container_width = True)

def add_df():
    name = st.text_input('Tên:', key = 'n1')
    team = st.text_input('Nhóm:', key = 't1')
    mail = st.text_input('Mail:', key = 'm1')
    btn = st.button('Xác nhận', key = 'b1')
    if btn and name != None and team != None and mail != None:
        st.session_state.df.loc[len(st.session_state.df.index) + 1] = [team, name, mail]
        save_csv()
        create_table()

def change_df():
    stt = st.text_input('Người thứ:', key = 's2')
    name = st.text_input('Tên:', key = 'n2')
    team = st.text_input('Nhóm:', key = 't2')
    mail = st.text_input('Mail:', key = 'm2')
    btn = st.button('Xác nhận', key = 'b2')
    if btn and stt != None and name != None and team != None and mail != None:
        try:
            stt = int(stt)
            if stt < len(st.session_state.df.index) + 1:
                st.session_state.df.loc[stt] = [team, name, mail]
                save_csv()
                create_table()
        except:
            pass

def delete_df():
    stt = st.text_input('Người thứ:', key = 's3')
    btn = st.button('Xác nhận', key = 'b3')
    if btn and stt != None:
        try:
            stt = int(stt)
            if stt < len(st.session_state.df.index) + 1:
                st.session_state.df = st.session_state.df.drop([stt])
                save_csv()
                create_table()
        except:
            pass

def add_df_t():
    pass

def change_df_t():
    pass

def delete_df_t():
    pass

def main():
    if check_key():
        read_csv()
        t1, t2, t3, t4, t5, t6 = st.tabs(['Thêm người', 'Sửa người', 'Xóa người', 'Thêm nhóm', 'Sửa nhóm', 'Xóa nhóm'])
        with t1:
            add_df()
        with t2:
            change_df()
        with t3:
            delete_df()
        with t4:
            add_df_t()
        with t5:
            change_df_t()
        with t6:
            delete_df_t()
        create_table()

if __name__ == '__main__':
    main()
