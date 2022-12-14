import streamlit as st
import pandas as pd
import datetime
import calendar
import os

try:
    from src.libs.mplcal import MplCalendar
except:
    from libs.mplcal import MplCalendar

THIS_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(THIS_PATH)
DDIR_PATH = os.path.dirname(DIR_PATH)
ASSET_PATH = os.path.join(DDIR_PATH, 'Assets')

DAYS_REMAIN_PATH = os.path.join(ASSET_PATH, 'remain.txt')

def read_csv(path = os.path.join(ASSET_PATH, 'names.csv')):
    return pd.read_csv(path, sep = ',', encoding = 'utf-8')

def init():
    st.session_state.now = datetime.datetime.today()

def write_days_remain(path = DAYS_REMAIN_PATH):
    contents = str(st.session_state.team_count) + '|' + str(st.session_state.count) + '|' + str(st.session_state.now.month)
    with open(path, 'w', encoding = 'utf-8') as f:
        f.write(contents)

def read_days_remain(path = DAYS_REMAIN_PATH):
    with open(path, 'r', encoding = 'utf-8') as f:
        contents = f.read()
    team_count, days, this_months = contents.split('|')
    st.session_state.team_count, st.session_state.count = int(team_count), int(days)
    if st.session_state.now.month != int(this_months):
        df = read_csv()
        teams = df['teams'].unique()
        max_days = calendar.monthrange(st.session_state.now.year, int(this_months))[1]
        for day in range(1, max_days + 1):
            if st.session_state.count == 0:
                st.session_state.team_count += 1
                if st.session_state.team_count == len(teams):
                    st.session_state.team_count = 0
                st.session_state.count = 7
            st.session_state.count -= 1
        write_days_remain()

def create_calen(month, year, df):
    teams = df['teams'].unique()
    max_days = calendar.monthrange(year, month)[1]
    calen = MplCalendar(year, month)
    for day in range(1, max_days + 1):
        if st.session_state.count == 0:
            st.session_state.team_count += 1
            if st.session_state.team_count == len(teams):
                st.session_state.team_count = 0
            st.session_state.count = 7
        calen.add_event(day, teams[st.session_state.team_count])
        st.session_state.count -= 1
    return calen.get()

def change_calen(op, df):
    days = calendar.monthrange(st.session_state.now.year, st.session_state.now.month)[1]
    st.session_state.now = eval(f'st.session_state.now {op} datetime.timedelta(days = {days})')
    if op == '-':
        days2 = calendar.monthrange(st.session_state.now.year, st.session_state.now.month)[1]
        teams = df['teams'].unique()
        for day in range(1, days + days2 + 1):
            if st.session_state.count == 7:
                if st.session_state.team_count == 0:
                    st.session_state.team_count = len(teams) - 1
                else:
                    st.session_state.team_count -= 1
                st.session_state.count = 0
            st.session_state.count += 1

def create_info(df):
    num_people = df.shape[0]
    teams = df['teams'].unique()
    des = '\n'
    for team in teams:
        info = df.loc[df['teams'] == team]
        names = info['names']
        temp = ', '.join(names)
        des += f'- Nh??m {team}: {temp.strip(", ")}\n'
    # print(des)
    with st.expander('Th??ng tin c???n bi???t', False):
        st.markdown(
            f'''
            Hi???n t???i nh?? c?? {num_people} ng?????i chia th??nh {len(teams)} nh??m g???m:
            {des}
            '''
        )
        url = 'https://calendar.google.com/calendar/u/0/embed?src=chientranminh0511@gmail.com&ctz=Asia/Ho_Chi_Minh'
        st.write(f'???????ng d???n nh???c nh??? l???ch theo l???ch v???n ni??n: [???????ng d???n]({url})')

def main():
    init()
    read_days_remain()

    df = read_csv()
    create_info(df)
    calen = create_calen(st.session_state.now.month, st.session_state.now.year, df)
    st.pyplot(calen)
    pre, aft = st.columns(2, gap = 'large')
    with pre:
        st.button('Th??ng tr?????c', on_click = change_calen, args = ('-', df))
    with aft:
        st.button('Th??ng sau', on_click = change_calen, args = ('+', df))

if __name__ == '__main__':
    # main()
    path = 'E:\Plan\Assets\\names.csv'
    r = read_csv(path)
    create_info(r)
