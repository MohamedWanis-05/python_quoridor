
from collections import deque
from copy import deepcopy
from game.constants import BOARD_SIZE
from game.rules import resolve_move, is_inside_board, is_wall_blocking

DIRECTIONS = [(-1,0),(1,0),(0,-1),(0,1)]


def shortest_path(board, player_id):
    start = board.get_player_position(player_id)
    goal_row = 0 if player_id == 2 else BOARD_SIZE - 1

    queue = deque([(start, [])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        if r == goal_row:
            return path

        for dr, dc in DIRECTIONS:

            nr = r + dr
            nc = c + dc

            if not is_inside_board(nr, nc, board):
                continue

            if is_wall_blocking(board, r, c, dr, dc):
                continue

            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return []


def evaluate_board(board):

    ai_path = shortest_path(board, 2)
    player_path = shortest_path(board, 1)

    ai_distance = len(ai_path)
    player_distance = len(player_path)

    score = (player_distance * 20) - (ai_distance * 8)

    score += board.player_2.walls_remaining * 2

    return score


def generate_wall_moves(board):

    moves = []

    if board.player_2.walls_remaining <= 0:
        return moves

    player_path = shortest_path(board, 1)

    if len(player_path) < 2:
        return moves

    for i in range(min(6, len(player_path)-1)):

        r1, c1 = player_path[i]
        r2, c2 = player_path[i+1]

        candidates = []

        if r1 != r2:

            top = min(r1, r2)

            candidates.extend([
                (top, c1, True),
                (top, c1 - 1, True),
                (top, c1 + 1, True)
            ])

        if c1 != c2:

            left = min(c1, c2)

            candidates.extend([
                (r1, left, False),
                (r1 - 1, left, False),
                (r1 + 1, left, False)
            ])

        for wr, wc, horiz in candidates:

            try:

                if board.can_place_wall(wr, wc, horiz):

                    moves.append({
                        "type": "place_wall",
                        "row": wr,
                        "col": wc,
                        "is_horizontal": horiz
                    })

            except:
                pass

    return moves


def generate_move(board):

    ai_path = shortest_path(board, 2)

    if not ai_path:
        return None

    cr, cc = board.get_player_position(2)
    tr, tc = ai_path[0]

    dr = tr - cr
    dc = tc - cc

    result = resolve_move(board, 2, dr, dc)

    if result not in [None, -100, -200]:

        return {
            "type": "pawn_move",
            "position": result
        }

    return None


def apply_move(board, move):

    temp = deepcopy(board)

    if move["type"] == "place_wall":

        if move["is_horizontal"]:
            temp.horizontal_walls.add((move["row"], move["col"]))
        else:
            temp.vertical_walls.add((move["row"], move["col"]))

        temp.player_2.walls_remaining -= 1

    elif move["type"] == "pawn_move":

        temp.player_2.position = move["position"]

    return temp


def minimax(board, depth, maximizing):

    if depth == 0:
        return evaluate_board(board)

    if maximizing:

        best = -999999

        candidate_moves = []

        move = generate_move(board)

        if move:
            candidate_moves.append(move)

        candidate_moves.extend(generate_wall_moves(board))

        for move in candidate_moves:

            temp = apply_move(board, move)

            score = minimax(temp, depth - 1, False)

            # EXTRA reward for useful wall blocks
            if move["type"] == "place_wall":

                before = len(shortest_path(board, 1))
                after = len(shortest_path(temp, 1))

                score += (after - before) * 50

            best = max(best, score)

        return best

    else:
        player_path = shortest_path(board, 1)

        if not player_path:
            return evaluate_board(board)

        return evaluate_board(board)


def get_hard_ai_move(board):

    best_score = -999999
    best_move = None

    candidate_moves = []

    move = generate_move(board)

    if move:
        candidate_moves.append(move)

    candidate_moves.extend(generate_wall_moves(board))

    for move in candidate_moves:

        temp = apply_move(board, move)

        score = minimax(temp, 2, False)

        if move["type"] == "place_wall":

            before = len(shortest_path(board, 1))
            after = len(shortest_path(temp, 1))

            score += (after - before) * 100

        if score > best_score:

            best_score = score
            best_move = move

    return best_move
