import random
from game.rules import resolve_move
from ai.pathfinding import bfs_shortest_path

AI_ID = 2
HUMAN_ID = 1

_WALL_CHANCE = 0.25


def get_easy_ai_move(board):
    if board.player_2.walls_remaining > 0 and random.random() < _WALL_CHANCE:
        wall = _try_random_wall(board)
        if wall is not None:
            return wall

    path = bfs_shortest_path(board, AI_ID)
    if path:
        move = _follow_path(board, path)
        if move is not None:
            return move
    return _fallback_move(board)

def _try_random_wall(board):
    hr, hc = board.get_player_position(HUMAN_ID)
    wall_r = hr
    wall_c = max(0, min(board.size - 2, hc + random.choice([-1, 0])))

    if board.can_place_wall(wall_r, wall_c, True):
        return {"type": "place_wall", "row": wall_r, "col": wall_c, "is_horizontal": True}
    return None


def _follow_path(board, path):
    curr_r, curr_c = board.get_player_position(AI_ID)
    target_r, target_c = path[0]
    dr = target_r - curr_r
    dc = target_c - curr_c

    new_pos = resolve_move(board, AI_ID, dr, dc)
    if new_pos not in {None, -100, -200}:
        return {"type": "pawn_move", "position": new_pos}
    return None


def _fallback_move(board):
    for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        new_pos = resolve_move(board, AI_ID, dr, dc)
        if new_pos not in {None, -100, -200}:
            return {"type": "pawn_move", "position": new_pos}
    return None
