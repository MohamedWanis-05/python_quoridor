import random
from collections import deque
from game.constants import BOARD_SIZE
from game.rules import resolve_move, is_inside_board, is_wall_blocking


def get_shortest_path(board, player_id):
    """Returns the actual list of coordinates for the shortest path to the goal."""
    start = board.get_player_position(player_id)
    goal_row = 0 if player_id == 2 else BOARD_SIZE - 1

    queue = deque([(start, [])])
    visited = set([start])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (r, c), path = queue.popleft()

        if r == goal_row:
            return path

        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if is_inside_board(new_r, new_c) and not is_wall_blocking(board, r, c, dr, dc):
                if (new_r, new_c) not in visited:
                    visited.add((new_r, new_c))
                    # Store the actual coordinate of the path
                    queue.append(((new_r, new_c), path + [(new_r, new_c)]))
    return []


def get_medium_ai_move(board):
    player_id = 2
    opponent_id = 1

    # 1. Calculate paths for both players
    ai_path = get_shortest_path(board, player_id)
    human_path = get_shortest_path(board, opponent_id)

    ai_distance = len(ai_path) if ai_path else 999
    human_distance = len(human_path) if human_path else 999

    # ==========================================
    # 2. DEFENSIVE: Block the human if they are winning
    # ==========================================
    # If human is closer to the goal (or tied) and AI has walls
    if human_distance <= ai_distance and board.player_2.walls_remaining > 0 and len(human_path) > 0:

        # Look at the human's immediate next step
        next_human_step = human_path[0]
        target_r, target_c = next_human_step

        # Try to place a horizontal or vertical wall around their next step
        wall_placements = [
            (target_r, target_c, True),  # Horizontal above/below
            (target_r - 1, target_c, True),
            (target_r, target_c, False),  # Vertical left/right
            (target_r, target_c - 1, False)
        ]

        # Shuffle slightly so it's not 100% predictable which side it blocks
        random.shuffle(wall_placements)

        for wr, wc, is_horiz in wall_placements:
            if board.can_place_wall(wr, wc, is_horiz):
                return {
                    "type": "place_wall",
                    "row": wr,
                    "col": wc,
                    "is_horizontal": is_horiz
                }

    # ==========================================
    # 3. OFFENSIVE: Sprint to the goal
    # ==========================================
    if ai_path:
        # Move to the first coordinate in our shortest path
        target_r, target_c = ai_path[0]

        # We need to figure out the dr, dc to get there
        curr_r, curr_c = board.get_player_position(player_id)
        dr = target_r - curr_r
        dc = target_c - curr_c

        # Use existing logic to execute the move (handles jumps/diagonals automatically)
        new_pos = resolve_move(board, player_id, dr, dc)
        if new_pos not in {None, -100, -200}:
            return {"type": "pawn_move", "position": new_pos}

    # ==========================================
    # 4. FALLBACK (Failsafe)
    # ==========================================
    prioritized_directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for dr, dc in prioritized_directions:
        new_pos = resolve_move(board, player_id, dr, dc)
        if new_pos not in {None, -100, -200}:
            return {"type": "pawn_move", "position": new_pos}

    return None