from game.constants import BOARD_SIZE

def is_inside_board(row, col, board):
    return 0 <= row < board.size and 0 <= col < board.size


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
        return -100  # flag for wall block

    next_pos = (row + dr, col + dc)

    # خارج البورد
    if not is_inside_board(*next_pos, board=board):
        return -200  # flag for outside board block

    # حركة عادية
    if next_pos != (opp_row, opp_col):
        return next_pos

    # =========================
    # Jump Over Opponent
    # =========================
    jump_pos = (opp_row + dr, opp_col + dc)
    jump_blocked = is_wall_blocking(board, opp_row, opp_col, dr, dc)

    # لو القفزة متاحة
    if is_inside_board(*jump_pos, board=board) and not jump_blocked:
        return jump_pos

    return None


def resolve_diagonal_move(board, player_id, new_position):
    row, col = board.get_player_position(player_id)

    opponent_id = 2 if player_id == 1 else 1
    opp_row, opp_col = board.get_player_position(opponent_id)

    new_row, new_col = new_position

    if not is_inside_board(new_row, new_col, board=board):
        return -200  # outside board block

    dr = new_row - row
    dc = new_col - col


    if abs(dr) != 1 or abs(dc) != 1:
        return None


    opp_dr = opp_row - row
    opp_dc = opp_col - col

    if abs(opp_dr) + abs(opp_dc) != 1:
        return None

    if opp_dc == 0:
        straight_jump_row = opp_row + opp_dr
        straight_blocked = not is_inside_board(straight_jump_row, opp_col, board=board) or \
                           is_wall_blocking(board, opp_row, opp_col, opp_dr, 0)

        if not straight_blocked:
            return None

        if is_wall_blocking(board, opp_row, opp_col, 0, dc):
            return -100  # Wall blocking the side step

        return new_position

    elif opp_dr == 0:
        straight_jump_col = opp_col + opp_dc
        straight_blocked = not is_inside_board(opp_row, straight_jump_col, board=board) or \
                           is_wall_blocking(board, opp_row, opp_col, 0, opp_dc)

        if not straight_blocked:
            return None

        if is_wall_blocking(board, opp_row, opp_col, dr, 0):
            return -100  # Wall blocking the side step

        return new_position

    return None


def check_winner(board):
    player1_row, _ = board.get_player_position(1)
    player2_row, _ = board.get_player_position(2)

    if player1_row == board.size - 1:
        return 1

    if player2_row == 0:
        return 2

    return None