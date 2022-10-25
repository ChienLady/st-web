import streamlit as st
import pandas as pd
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

def old():
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
        st.button('Xác nhận', key = f'b1', on_click = add_more, args = (name, thing, price)) 

def storage():
    dir_path = 'https://drive.google.com/drive/folders/1UaweXDmbHwYWplKwqei-gzXxBXH63aMK?usp=sharing'
    ls_ids = {
        2022: [
            {11: '1rS51rM-NWMHfaC5JRqf5QZPr4epCXqlmWkD3hnpCJCQ'},
            {12: '1zIZ1DCgsf2LwRLBqq5cgL7My5kbwX4VyaynXbW3hBqQ'}
        ],
        2023: [
            {1: '1ngXzl-5V92GvDzK3uNQzIhgYszz7-15r9xeSF4E2nIM'},
            {2: '1-X2IeGxvmcIg0ivEQ4WC81dhrwJHkmx7_3S7H32kTvk'},
            {3: '1-GaLXftpUtZUjfD9r_AOciriozIsz2lFrLp8cWBmXYw'},
            {4: '13cDQ3Opjt2LncdWX-v3jATqdiNWnFc6zF_VvvdY1T8E'},
            {5: '1OadtPDL-_D_fWXIUcMKF9Eqy2kZk2LSDlezaoGrwZsk'},
            {6: '19T_OFKRDUMkvb5LmvsaPGUrLFfrGAunEu4dwVyzelb8'},
            {7: '1sinG9ezzXjnt05VRAqHxzBT0sfRDsjRUgwW4Ny6mUz4'},
            {8: '1_EuN606TnqyBZFXde8FuKtsrlx40oODxOlGRhTxnCbA'},
            {9: '1_U3OYKTOGEvmfu_4DUoEHBH7KjhcDli-Qxby6isQbW8'},
            {10: '1Z9mfOBTUKAlEYJQXtk6GC7nnv6eA5PzWIFfb0CmOtIE'},
            {11: '1yVTyUcOOhDzlXiS8h9YEYQMu_5cWKQJq9aQC1AjZDSI'},
            {12: '1zOW-bjPWvOdgUX2Edpww9eHyGUzJqHZ9U-AqgEKx4AY'}
        ]
    }
    return dir_path, ls_ids

def new():
    url = 'https://docs.google.com/spreadsheets/d/{id}/edit?usp=sharing'
    dir_path, ls_ids = storage()
    st.header('Toàn bộ file sheet đều lưu ở đây')
    st.write(f'Đường dẫn tới Google Drive [link]({dir_path})')

    y22 = ls_ids[2022]
    y23 = ls_ids[2023]

    tab1, tab2 = st.tabs(['Năm 2022', 'Năm 2023'])
    with tab1:
        st.header('Năm 2022')
        for item in y22:
            m, id = list(item.items())[0]
            link = url.format(id = id)
            st.write(f'Tháng {m} [link]({link})')
    with tab2:
        st.header('Năm 2023')
        for item in y23:
            m, id = list(item.items())[0]
            link = url.format(id = id)
            st.write(f'Tháng {m} [link]({link})')

def main():
    if check_key():
        old()
    else:
        new()
        
if __name__ == '__main__':
    main()
