from game.constants import BOARD_SIZE

def is_inside_board(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def is_wall_blocking(board, r, c, dr, dc):
    """
    check if a wall prevents movement from cell (r, c) in direction (dr, dc).
    """
    if dr == -1:  # Move UP
        if (r - 1, c - 1) in board.horizontal_walls or (r - 1, c) in board.horizontal_walls:
            return True
    elif dr == 1:  # Move DOWN
        if (r, c - 1) in board.horizontal_walls or (r, c) in board.horizontal_walls:
            return True
    elif dc == -1:  # Move LEFT
        if (r - 1, c - 1) in board.vertical_walls or (r, c - 1) in board.vertical_walls:
            return True
    elif dc == 1:  # Move RIGHT
        if (r - 1, c) in board.vertical_walls or (r, c) in board.vertical_walls:
            return True

    return False

def resolve_move(board, player_id, dr, dc):
    row, col = board.get_player_position(player_id)

    opponent_id = 2 if player_id == 1 else 1
    opp_row, opp_col = board.get_player_position(opponent_id)

    if is_wall_blocking(board, row, col, dr, dc):
        return None

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
    jump_blocked = is_wall_blocking(board, opp_row, opp_col, dr, dc)
    # لو القفزة متاحة
    if is_inside_board(*jump_pos) and not jump_blocked:
        return jump_pos

    # =========================
    # Diagonal Around Opponent
    # =========================

    # حركة رأسية
    if dr != 0:

        diagonal_left = (opp_row, opp_col - 1)
        diagonal_right = (opp_row, opp_col + 1)

        if is_inside_board(*diagonal_left) and not is_wall_blocking(board, opp_row, opp_col, 0, -1):
            return diagonal_left

        if is_inside_board(*diagonal_right) and not is_wall_blocking(board, opp_row, opp_col, 0, 1):
            return diagonal_right

    # حركة أفقية
    elif dc != 0:

        diagonal_up = (opp_row - 1, opp_col)
        diagonal_down = (opp_row + 1, opp_col)

        if is_inside_board(*diagonal_up) and not is_wall_blocking(board, opp_row, opp_col, -1, 0):
            return diagonal_up

        if is_inside_board(*diagonal_down) and not is_wall_blocking(board, opp_row, opp_col, 1, 0):
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