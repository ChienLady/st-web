import streamlit as st
import numpy as np
import random
import pandas as pd

# tic tac toe
def init_tic(post_init = False):
    if not post_init:
        st.session_state.opponent = 'Người'
        st.session_state.win = {'X': 0, 'O': 0}
    st.session_state.board = np.full((3, 3), '.', dtype=str)
    st.session_state.player = 'X'
    st.session_state.warning = False
    st.session_state.winner = None
    st.session_state.over = False


def check_available_moves(extra=False) -> list:
    raw_moves = [row for col in st.session_state.board.tolist() for row in col]
    num_moves = [i for i, spot in enumerate(raw_moves) if spot == '.']
    if extra:
        return [(i // 3, i % 3) for i in num_moves]
    return num_moves


def check_rows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return None


def check_diagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1:
        return board[0][len(board) - 1]
    return None


def check_state():
    if st.session_state.winner:
        winner = '❌' if st.session_state.winner == 'X' else '⭕'
        st.success(f'Chúc mừng! {winner} đã chiến thắng ván này! 🎈')
    if st.session_state.warning and not st.session_state.over:
        st.warning('⚠️ Nước đi đã tồn tại')
    if st.session_state.winner and not st.session_state.over:
        st.session_state.over = True
        st.session_state.win[st.session_state.winner] = (
            st.session_state.win.get(st.session_state.winner, 0) + 1
        )
    elif not check_available_moves() and not st.session_state.winner:
        st.info(f'Một ván hòa cờ 📍')
        st.session_state.over = True


def check_win(board):
    for new_board in [board, np.transpose(board)]:
        result = check_rows(new_board)
        if result:
            return result
    return check_diagonals(board)


def computer_player():
    moves = check_available_moves(extra = True)
    if moves:
        i, j = random.choice(moves)
        handle_click(i, j)


def handle_click(i, j):
    if (i, j) not in check_available_moves(extra=True):
        st.session_state.warning = True
    elif not st.session_state.winner:
        st.session_state.warning = False
        st.session_state.board[i, j] = st.session_state.player
        st.session_state.player = 'O' if st.session_state.player == 'X' else 'X'
        winner = check_win(st.session_state.board)
        if winner != '.':
            st.session_state.winner = winner


def main_tic():
    st.write(
        '''
        # ❎🅾️ Cờ caro
        '''
    )

    if 'board' not in st.session_state:
        init_tic()

    reset, score, player, settings = st.columns([0.5, 0.6, 1, 1])
    reset.button('Ván mới', on_click = init_tic, args = (True,), key = 'btn_new_tic')

    with settings.expander('Cài đặt'):
        st.write('**Lưu ý**: thay đổi sẽ làm mới ván chơi')
        st.selectbox(
            'Chọn đối thủ',
            ['Người', 'Máy'],
            key = 'opponent',
            on_change = init_tic,
            args = (True,),
        )

    for i, row in enumerate(st.session_state.board):
        cols = st.columns([10, 1, 1, 1, 10])
        for j, field in enumerate(row):
            cols[j + 1].button(
                field,
                key=f'{i}-{j}',
                on_click=handle_click
                if st.session_state.player == 'X'
                or st.session_state.opponent == 'Người'
                else computer_player(),
                args=(i, j),
            )

    check_state()

    score.button(f'❌{st.session_state.win["X"]} 🆚 {st.session_state.win["O"]}⭕')
    player.button(
        f'Lượt của {"❌" if st.session_state.player == "X" else "⭕"}'
        if not st.session_state.winner
        else f'🏁 Trò chơi kết thúc'
    )

# guess number
def get_number(length: int) -> int:
    return random.randint(1, length)

def init_gue(length: int = 10, post_init = False):
    if not post_init:
        st.session_state.input = 0
    st.session_state.number = get_number(length)
    st.session_state.tries = 0
    st.session_state.over = False

def restart():
    init_gue(st.session_state.length, post_init=True)
    st.session_state.input += 1


def main_gue():
    st.write(
        """
        # 🔢 Đoán số
        """
    )

    if 'number' not in st.session_state:
        init_gue()

    reset, win, set_range = st.columns([0.39, 1, 1])
    reset.button('Ván mới', on_click = restart, key = 'btn_new_gue')

    with set_range.expander('Cài đặt'):
        st.select_slider(
            'Chọn khoảng dự đoán',
            [10**i for i in range(1, 6)],
            value = 10,
            key = 'length',
            on_change=restart,
        )

    placeholder, debug = st.empty(), st.empty()
    guess = placeholder.number_input(
        f'Đoán một số từ 1 đến {st.session_state.length}',
        key = st.session_state.input,
        min_value = 0,
        max_value = st.session_state.length,
    )

    if guess:
        st.session_state.tries += 1
        if guess < st.session_state.number:
            debug.warning(f'{guess} quá thấp!')
        elif guess > st.session_state.number:
            debug.warning(f'{guess} quá cao!')
        else:
            debug.success(
                f'Tuyệt vời! Bạn đã đoán đúng, và chỉ mất {st.session_state.tries} lần thử 🎈'
            )
            st.session_state.over = True
            placeholder.empty()

def main():
    st.markdown(
        '''
        <h1 align="center">
            Chào mừng tới trang chủ 👋
        </h1>

        ---
        ''',
        unsafe_allow_html = True,
    )
    with st.expander('Về trang web', True):
        st.markdown(
            '''
            Tôi làm một trang web viết bằng streamlit,
            mặc dù không đúng mục đích lắm nhưng nó đơn giản.
            Trang web chỉ có mục đích sử dụng để quản lý nhân sự,
            công việc và tiền nong trong nhà riêng.
            
            Địa chỉ ngôi nhà hiện tại ở: Số 21, ngõ 133, phố Tân Ấp,
            phường Phúc Xá, quận Ba Đình, thành phố Hà Nội.

            Mọi chi tiết liên hệ tới mail:
            tmchien@rd.misa.com.vn hoặc chientranminh0511@gmail.com
            '''
        )
        df = pd.DataFrame(
            np.array([[21.0486864, 105.8453098]]),
            columns = ['lat', 'lon'])

        st.map(df, zoom = 15)

    # option = st.selectbox('Chọn trò chơi', ('Đoán số', 'Cờ caro'), key = 'game_opt')
    # if option == 'Cờ caro':
    #     main_tic()
    # elif option == 'Đoán số':
    #     main_gue()
    tab1, tab2 = st.tabs(['Đoán số', 'Cờ caro'])
    with tab1:
        main_gue()
    with tab2:
        main_tic()

if __name__ == '__main__':
    main_tic()
