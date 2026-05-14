from game.constants import BOARD_SIZE


def is_inside_board(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def resolve_move(board, player_id, dr, dc):
    row, col = board.get_player_position(player_id)

    opponent_id = 2 if player_id == 1 else 1
    opp_row, opp_col = board.get_player_position(opponent_id)

    next_pos = (row + dr, col + dc)

    # خارج البورد
    if not is_inside_board(*next_pos):
        return None

    # حركة عادية
    if next_pos != (opp_row, opp_col):
        return next_pos

    # =========================
    # Jump Over Opponent
    # =========================
    jump_pos = (opp_row + dr, opp_col + dc)

    # لو القفزة متاحة
    if is_inside_board(*jump_pos):
        return jump_pos

    # =========================
    # Diagonal Around Opponent
    # =========================

    # حركة رأسية
    if dr != 0:

        diagonal_left = (opp_row, opp_col - 1)
        diagonal_right = (opp_row, opp_col + 1)

        if is_inside_board(*diagonal_left):
            return diagonal_left

        if is_inside_board(*diagonal_right):
            return diagonal_right

    # حركة أفقية
    elif dc != 0:

        diagonal_up = (opp_row - 1, opp_col)
        diagonal_down = (opp_row + 1, opp_col)

        if is_inside_board(*diagonal_up):
            return diagonal_up

        if is_inside_board(*diagonal_down):
            return diagonal_down

    return None


def check_winner(board):
    player1_row, _ = board.get_player_position(1)
    player2_row, _ = board.get_player_position(2)

    if player1_row == BOARD_SIZE - 1:
        return 1

    if player2_row == 0:
        return 2

    return None