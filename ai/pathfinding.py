from collections import deque
from game.rules import is_inside_board, is_wall_blocking

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def bfs_shortest_path(board, player_id):
    start = board.get_player_position(player_id)
    goal_row = 0 if player_id == 2 else board.size - 1

    queue = deque([(start, [])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        if r == goal_row:
            return path

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited and is_inside_board(nr, nc, board) and not is_wall_blocking(board, r, c, dr, dc):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return []


def bfs_path_length(board, player_id):

    start = board.get_player_position(player_id)
    goal_row = 0 if player_id == 2 else board.size - 1

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        (r, c), dist = queue.popleft()

        if r == goal_row:
            return dist

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited and is_inside_board(nr, nc, board) and not is_wall_blocking(board, r, c, dr, dc):
                visited.add((nr, nc))
                queue.append(((nr, nc), dist + 1))

    return 999


def has_path_to_goal(board, player_id):
    return bfs_path_length(board, player_id) < 999
