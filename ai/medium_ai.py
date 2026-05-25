import random
from game.rules import resolve_move
from ai.pathfinding import bfs_shortest_path, bfs_path_length

AI_ID = 2
HUMAN_ID = 1


def get_medium_ai_move(board):
    ai_dist = bfs_path_length(board, AI_ID)
    human_dist = bfs_path_length(board, HUMAN_ID)

    if human_dist <= ai_dist and board.player_2.walls_remaining > 0:
        wall = _blocking_wall(board)
        if wall is not None:
            return wall

    path = bfs_shortest_path(board, AI_ID)
    if path:
        move = _follow_path(board, path)
        if move is not None:
            return move

    return _fallback_move(board)


def _blocking_wall(board):
    human_path = bfs_shortest_path(board, HUMAN_ID)
    if not human_path:
        return None

    tr, tc = human_path[0]

    candidates = [
        (tr,     tc,     True),
        (tr - 1, tc,     True),
        (tr,     tc,     False),
        (tr,     tc - 1, False),
    ]
    random.shuffle(candidates)

    for wr, wc, is_horiz in candidates:
        if board.can_place_wall(wr, wc, is_horiz):
            return {"type": "place_wall", "row": wr, "col": wc, "is_horizontal": is_horiz}
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
