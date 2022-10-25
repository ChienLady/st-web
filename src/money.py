import streamlit as st
import pandas as pd
import os

THIS_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(THIS_PATH)
DDIR_PATH = os.path.dirname(DIR_PATH)
ASSET_PATH = os.path.join(DDIR_PATH, 'Assets')

def check_key():
    temp1 = st.subheader('Tính năng hiện tại đang không sử dụng')
    temp2 = st.subheader('Nhập đúng KEY để truy cập')
    key = st.sidebar.text_input('Key', type = 'password')
    if st.sidebar.checkbox('Xác nhận'):
        if key == os.environ.get('KEY'):
            temp1.empty()
            temp2.empty()
            return True
    else:
        st.sidebar.error('Key nhập vào chưa đúng')
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

def init():
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

def main():
    if check_key():
        init()
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
            btn = st.button('Xác nhận', key = f'b1', on_click = add_more, args = (name, thing, price)) 
        
if __name__ == '__main__':
    main()
