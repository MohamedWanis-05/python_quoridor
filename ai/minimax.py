import copy
from game.rules import resolve_move
from ai.pathfinding import bfs_shortest_path, bfs_path_length

AI_ID = 2
HUMAN_ID = 1

WALL_GAIN_THRESHOLD = 2

MAX_CANDIDATES = 40


def get_hard_ai_move(board):
    ai_dist = bfs_path_length(board, AI_ID)
    human_dist = bfs_path_length(board, HUMAN_ID)

    best_wall = None
    best_gain = WALL_GAIN_THRESHOLD - 1

    if board.player_2.walls_remaining > 0:
        candidates = _generate_wall_candidates(board)

        for (wr, wc, is_horiz) in candidates:
            if not board.can_place_wall(wr, wc, is_horiz):
                continue

            gain = _evaluate_wall(board, wr, wc, is_horiz, ai_dist, human_dist)
            if gain > best_gain:
                best_gain = gain
                best_wall = (wr, wc, is_horiz)

    if best_wall is not None:
        wr, wc, is_horiz = best_wall
        return {"type": "place_wall", "row": wr, "col": wc, "is_horizontal": is_horiz}

    path = bfs_shortest_path(board, AI_ID)
    if path:
        move = _follow_path(board, path)
        if move is not None:
            return move

    return _fallback_move(board)

def _generate_wall_candidates(board):
    human_path = bfs_shortest_path(board, HUMAN_ID)
    ai_path = bfs_shortest_path(board, AI_ID)

    seen = set()
    candidates = []

    def add(wr, wc, is_horiz):
        key = (wr, wc, is_horiz)
        if key in seen:
            return
        seen.add(key)
        if 0 <= wr <= board.size - 2 and 0 <= wc <= board.size - 2:
            candidates.append(key)

    for (r, c) in human_path:
        add(r,     c,     True)
        add(r - 1, c,     True)
        add(r,     c,     False)
        add(r,     c - 1, False)
        if len(candidates) >= MAX_CANDIDATES:
            break

    for (r, c) in ai_path:
        if len(candidates) >= MAX_CANDIDATES:
            break
        add(r,     c,     True)
        add(r - 1, c,     True)
        add(r,     c,     False)
        add(r,     c - 1, False)

    return candidates


def _evaluate_wall(board, wr, wc, is_horiz, ai_dist, human_dist):
    sim = _board_snapshot(board)

    if is_horiz:
        sim["h_walls"].add((wr, wc))
    else:
        sim["v_walls"].add((wr, wc))

    new_ai_dist    = _sim_bfs_length(sim, AI_ID,    board.size)
    new_human_dist = _sim_bfs_length(sim, HUMAN_ID, board.size)

    if new_ai_dist == 999 or new_human_dist == 999:
        return -999

    old_advantage = human_dist - ai_dist
    new_advantage = new_human_dist - new_ai_dist
    return new_advantage - old_advantage


def _board_snapshot(board):
    return {
        "h_walls":   set(board.horizontal_walls),
        "v_walls":   set(board.vertical_walls),
        "positions": dict(board.player_positions),
        "size":      board.size,
    }


def _sim_bfs_length(sim, player_id, board_size):
    from collections import deque

    start = sim["positions"][player_id]
    goal_row = 0 if player_id == 2 else board_size - 1

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        (r, c), dist = queue.popleft()

        if r == goal_row:
            return dist

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc

            if not (0 <= nr < board_size and 0 <= nc < board_size):
                continue

            if _sim_wall_blocking(sim, r, c, dr, dc):
                continue

            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), dist + 1))

    return 999


def _sim_wall_blocking(sim, r, c, dr, dc):
    h = sim["h_walls"]
    v = sim["v_walls"]

    if dr == -1:  # moving up: row r → row r-1; wall sits at (r-1, c) or (r-1, c-1)
        return (r - 1, c) in h or (r - 1, c - 1) in h
    if dr == 1:   # moving down: wall sits at (r, c) or (r, c-1)
        return (r, c) in h or (r, c - 1) in h
    if dc == -1:  # moving left: wall sits at (r, c-1) or (r-1, c-1)
        return (r, c - 1) in v or (r - 1, c - 1) in v
    if dc == 1:   # moving right: wall sits at (r, c) or (r-1, c)
        return (r, c) in v or (r - 1, c) in v
    return False


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
