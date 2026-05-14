from collections import deque
from game.constants import BOARD_SIZE
from game.rules import is_inside_board, is_wall_blocking


def has_path_to_goal(board, player_id):
    start = board.get_player_position(player_id)
    goal_row = BOARD_SIZE - 1 if player_id == 1 else 0

    visited = set()
    queue = deque([start])

    while queue:
        row, col = queue.popleft()

        if row == goal_row:
            return True

        if (row, col) in visited:
            continue

        visited.add((row, col))

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            if not is_inside_board(new_row, new_col):
                continue

            if is_wall_blocking(board, row, col, dr, dc):
                continue

            if (new_row, new_col) not in visited:
                queue.append((new_row, new_col))

    return False