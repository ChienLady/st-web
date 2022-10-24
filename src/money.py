import streamlit as st
import pandas as pd
import os

THIS_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(THIS_PATH)
DDIR_PATH = os.path.dirname(DIR_PATH)
ASSET_PATH = os.path.join(DDIR_PATH, 'Assets')

def read_csv(path = os.path.join(ASSET_PATH, 'names.csv')):
    df = pd.read_csv(path, sep = ',', encoding = 'utf-8')
    st.session_state.df = df.sort_values(by = ['teams'])
    st.session_state.df.index = range(1, st.session_state.df.shape[0] + 1)

def get_names():
    names = st.session_state.df['names']
    first_names = [name.split(' ')[-1] for name in names]
    return names, first_names

def get_money_names():
    columns = list(st.session_state.money_df.columns)
    names = [name for name in columns if not name.startswith('giá')]
    return names

def read_money_csv(path = os.path.join(ASSET_PATH, 'money.csv')):
    money_df = pd.read_csv(path, sep = ',', encoding = 'utf-8')
    money_df.index = range(1, money_df.shape[0] + 1)
    st.session_state.money_df = money_df.sort_index()

def create_table_full(names):
    mn_names = get_money_names()
    if sorted(mn_names) != sorted(names):
        for name in names:
            if name not in mn_names:
                st.session_state.money_df[name] = []
                first_name = name.split(' ')[-1]
                st.session_state.money_df[f'tiền {first_name}'] = []
        save_csv()
    try:
        st.session_state.table_money.empty()
    except:
        pass
    read_csv()
    st.session_state.table_money = st.empty()
    with st.session_state.table_money.container():
        st.dataframe(st.session_state.money_df, use_container_width = True)

def create_table_only(name, id):
    first_name = name.split(' ')[-1]
    st.session_state.money_df_only = st.session_state.money_df[[name, f'tiền {first_name}']]
    try:
        st.session_state.table_only[id].empty()
    except:
        pass
    read_csv()
    st.session_state.table_only[id] = st.empty()
    with st.session_state.table_only[id].container():
        st.dataframe(st.session_state.money_df_only, use_container_width = True)

def save_csv(path = os.path.join(ASSET_PATH, 'money.csv')):
    st.session_state.money_df.to_csv(path, sep = ',', encoding = 'utf-8', index = False)

def init():
    read_csv()
    read_money_csv()

def add_more(names):
    if thing != '' and price != '':
        first_name = name.split(' ')[-1]
        df_only = st.session_state.money_df[[name, f'tiền {first_name}']]
        df_only.loc[len(df_only.index) + 1] = [thing, price]
        st.session_state.money_df[[name, f'tiền {first_name}']] = df_only
        save_csv()
        create_table_full(get_names()[0])
    else:
        st.warning('Không được để trống các trường thông tin', icon = '⚠️')

def main():
    init()
    names, first_names = get_names()
    names = list(names)
    
    name = st.selectbox(
        'Bạn muốn thêm vào danh sách của ai?',
        tuple(names)
    )
    thing = st.text_input('Mua gì:', key = f't1').strip()
    price = st.text_input('Giá:', key = f'p1').strip()
    btn = st.button('Xác nhận', key = f'b1', on_click = add_more, args = (names,))
    create_table_full(names)
    # st.session_state.table_only = [st.empty()] * (len(names) + 1)
    # temp = ['Tổng', 'Phí chung'] + first_names
    # ls_tabs = st.tabs(temp)
    # for idx, tab in enumerate(ls_tabs):
    #     with tab:
    #         if idx == 0:
    #             create_table_full(names)
    #             continue
    #         elif idx == 1:
    #             create_table_only('Phí chung', 0)
    #             continue
    #         create_table_only(names[idx - 2], idx - 1)
    
if __name__ == '__main__':
    main()
