import random
from collections import deque
from game.constants import BOARD_SIZE
from game.rules import resolve_move, is_inside_board, is_wall_blocking


def get_easy_ai_move(board):
    player_id = 2
    opponent_id = 1

    # 1. OFFENSIVE TACTIC: Try to place a wall
    # Give the AI a 35% chance to try and block you if it still has walls
    if board.player_2.walls_remaining > 0 and random.random() < 0.35:
        p1_r, p1_c = board.get_player_position(opponent_id)

        wall_r = max(0, min(BOARD_SIZE - 2, p1_r + random.choice([-1, 0])))
        wall_c = max(0, min(BOARD_SIZE - 2, p1_c + random.choice([-1, 0])))
        is_horiz = random.choice([True, False])

        if board.can_place_wall(wall_r, wall_c, is_horiz):
            return {
                "type": "place_wall",
                "row": wall_r,
                "col": wall_c,
                "is_horizontal": is_horiz
            }

    # 2. SMART MOVEMENT: Shortest Path (BFS)
    start = board.get_player_position(player_id)
    goal_row = 0

    queue = deque([(start, [])])
    visited = set([start])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (r, c), path = queue.popleft()

        if r == goal_row:
            if path:
                dr, dc = path[0]
                new_pos = resolve_move(board, player_id, dr, dc)
                if new_pos not in {None, -100, -200}:
                    return {"type": "pawn_move", "position": new_pos}
            break

        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if is_inside_board(new_r, new_c,board) and not is_wall_blocking(board, r, c, dr, dc):
                if (new_r, new_c) not in visited:
                    visited.add((new_r, new_c))
                    queue.append(((new_r, new_c), path + [(dr, dc)]))

    prioritized_directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for dr, dc in prioritized_directions:
        new_pos = resolve_move(board, player_id, dr, dc)
        if new_pos not in {None, -100, -200}:
            return {"type": "pawn_move", "position": new_pos}

    return None