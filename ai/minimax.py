import random
from collections import deque
from game.rules import resolve_move, resolve_diagonal_move, is_inside_board, is_wall_blocking


def get_path_length(board, player_id):
    start = board.get_player_position(player_id)
    goal_row = 0 if player_id == 2 else board.size - 1

    queue = deque([(start, 0)])
    visited = set([start])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (r, c), dist = queue.popleft()
        if r == goal_row:
            return dist
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if is_inside_board(new_r, new_c, board) and not is_wall_blocking(board, r, c, dr, dc):
                if (new_r, new_c) not in visited:
                    visited.add((new_r, new_c))
                    queue.append(((new_r, new_c), dist + 1))
    return 999


def get_shortest_path(board, player_id):
    start = board.get_player_position(player_id)
    goal_row = 0 if player_id == 2 else board.size - 1

    queue = deque([(start, [start])])
    visited = set([start])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (r, c), path = queue.popleft()
        if r == goal_row:
            return path
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if is_inside_board(new_r, new_c, board) and not is_wall_blocking(board, r, c, dr, dc):
                if (new_r, new_c) not in visited:
                    visited.add((new_r, new_c))
                    queue.append(((new_r, new_c), path + [(new_r, new_c)]))
    return []


def evaluate_board(board, h_dist, ai_dist):
    if ai_dist == 0:
        return 100000
    if h_dist == 0:
        return -100000

    dist_advantage = (h_dist - ai_dist) * 15
    wall_bonus = board.player_2.walls_remaining * 3
    wall_penalty = board.player_1.walls_remaining * 3
    ai_r, ai_c = board.get_player_position(2)
    center_bonus = -abs(ai_c - (board.size // 2)) * 2
    progress_bonus = (board.size - 1 - ai_r) * 3

    if h_dist <= 2:
        urgency = (h_dist - ai_dist) * 30
    else:
        urgency = 0

    return dist_advantage + wall_bonus - wall_penalty + center_bonus + progress_bonus + urgency


def get_wall_candidates(board, player_id):
    opp_id = 1 if player_id == 2 else 2
    player_obj = board.player_2 if player_id == 2 else board.player_1

    if player_obj.walls_remaining <= 0:
        return []

    opp_path = get_shortest_path(board, opp_id)
    if not opp_path:
        return []

    opp_goal_row = board.size - 1 if opp_id == 1 else 0

    # A horizontal wall at (wr, wc) blocks moving DOWN from row wr to row wr+1.
    # It fires when is_wall_blocking is called with dr=1 from row wr:
    #   checks (wr, wc-1) and (wr, wc) in horizontal_walls.
    # So to block a player moving DOWN through a path cell (r, c),
    # we need a horizontal wall at row r-1 (blocks entering row r from above)
    # OR row r (blocks leaving row r downward).
    # The most useful is at the row BEFORE the next path cell,
    # which is current_row (blocks the very next step forward).
    #
    # Path now includes current pos as path[0], so path[1] is the next cell.
    # To block step from path[0] to path[1]:
    #   if moving down (dr=1): wall at row path[0][0]  (blocks dr=1 from that row)
    #   if moving up  (dr=-1): wall at row path[1][0]  (blocks dr=-1 arriving there)

    wall_candidates = set()

    for i in range(len(opp_path) - 1):
        cur_r, cur_c = opp_path[i]
        nxt_r, nxt_c = opp_path[i + 1]

        if i >= 6:
            break

        moving_down = nxt_r > cur_r

        if moving_down:
            # horizontal wall at cur_r blocks moving down out of cur_r
            wr = cur_r
        else:
            # horizontal wall at nxt_r blocks moving up into nxt_r
            wr = nxt_r

        for wc in range(max(cur_c - 2, 0), min(cur_c + 3, board.size - 1)):
            if 0 <= wr < board.size - 1:
                wall_candidates.add((wr, wc))

    result = []
    for wr, wc in wall_candidates:
        if board.can_place_wall(wr, wc, True):
            result.append({"type": "place_wall", "row": wr, "col": wc, "is_horizontal": True})
        if board.can_place_wall(wr, wc, False):
            result.append({"type": "place_wall", "row": wr, "col": wc, "is_horizontal": False})

    def wall_score(m):
        if m["is_horizontal"]:
            board.horizontal_walls.add((m["row"], m["col"]))
        else:
            board.vertical_walls.add((m["row"], m["col"]))
        opp_new = get_path_length(board, opp_id)
        if m["is_horizontal"]:
            board.horizontal_walls.discard((m["row"], m["col"]))
        else:
            board.vertical_walls.discard((m["row"], m["col"]))
        return -opp_new

    result.sort(key=wall_score)
    return result[:12]


def get_candidate_moves(board, player_id):
    moves = []
    row, col = board.get_player_position(player_id)

    pawn_moves = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pos = resolve_move(board, player_id, dr, dc)
        if new_pos not in {None, -100, -200}:
            pawn_moves.append({"type": "pawn_move", "position": new_pos})

    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        new_pos = resolve_diagonal_move(board, player_id, (row + dr, col + dc))
        if new_pos not in {None, -100, -200}:
            pawn_moves.append({"type": "pawn_move", "position": new_pos})

    if player_id == 2:
        pawn_moves.sort(key=lambda m: m["position"][0])
    else:
        pawn_moves.sort(key=lambda m: -m["position"][0])

    moves.extend(pawn_moves)
    moves.extend(get_wall_candidates(board, player_id))

    return moves


def minimax(board, depth, alpha, beta, maximizing_player):
    h_dist = get_path_length(board, 1)
    ai_dist = get_path_length(board, 2)

    if depth == 0 or h_dist == 0 or ai_dist == 0:
        return evaluate_board(board, h_dist, ai_dist), None

    if maximizing_player:
        max_eval = -float('inf')
        best_move = None
        for move in get_candidate_moves(board, 2):
            if move["type"] == "pawn_move":
                orig_pos = board.get_player_position(2)
                board.set_player_position(2, move["position"])
            else:
                if move["is_horizontal"]:
                    board.horizontal_walls.add((move["row"], move["col"]))
                else:
                    board.vertical_walls.add((move["row"], move["col"]))

                if get_path_length(board, 1) == 999 or get_path_length(board, 2) == 999:
                    if move["is_horizontal"]:
                        board.horizontal_walls.remove((move["row"], move["col"]))
                    else:
                        board.vertical_walls.remove((move["row"], move["col"]))
                    continue

                board.player_2.walls_remaining -= 1

            eval_score, _ = minimax(board, depth - 1, alpha, beta, False)

            if move["type"] == "pawn_move":
                board.set_player_position(2, orig_pos)
            else:
                if move["is_horizontal"]:
                    board.horizontal_walls.remove((move["row"], move["col"]))
                else:
                    board.vertical_walls.remove((move["row"], move["col"]))
                board.player_2.walls_remaining += 1

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        if best_move is None:
            return -float('inf'), None
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_candidate_moves(board, 1):
            if move["type"] == "pawn_move":
                orig_pos = board.get_player_position(1)
                board.set_player_position(1, move["position"])
            else:
                if move["is_horizontal"]:
                    board.horizontal_walls.add((move["row"], move["col"]))
                else:
                    board.vertical_walls.add((move["row"], move["col"]))

                if get_path_length(board, 1) == 999 or get_path_length(board, 2) == 999:
                    if move["is_horizontal"]:
                        board.horizontal_walls.remove((move["row"], move["col"]))
                    else:
                        board.vertical_walls.remove((move["row"], move["col"]))
                    continue

                board.player_1.walls_remaining -= 1

            eval_score, _ = minimax(board, depth - 1, alpha, beta, True)

            if move["type"] == "pawn_move":
                board.set_player_position(1, orig_pos)
            else:
                if move["is_horizontal"]:
                    board.horizontal_walls.remove((move["row"], move["col"]))
                else:
                    board.vertical_walls.remove((move["row"], move["col"]))
                board.player_1.walls_remaining += 1

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        if best_move is None:
            return float('inf'), None
        return min_eval, best_move


def get_medium_ai_move(board):
    _, move = minimax(board, depth=2, alpha=-float('inf'), beta=float('inf'), maximizing_player=True)
    return move if move else get_fallback(board)


def get_hard_ai_move(board):
    _, move = minimax(board, depth=3, alpha=-float('inf'), beta=float('inf'), maximizing_player=True)
    return move if move else get_fallback(board)


def get_fallback(board):
    for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        pos = resolve_move(board, 2, dr, dc)
        if pos not in {None, -100, -200}:
            return {"type": "pawn_move", "position": pos}
    return None