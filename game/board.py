from game.constants import BOARD_SIZE
from game.player import Player


class Board:
    def __init__(self):
        player_1 = Player(1)
        player_2 = Player(2)

        self.size = BOARD_SIZE
        self.player_positions = {
            1: (0, 4),
            2: (8, 4)
        }

        self.horizontal_walls = set()
        self.vertical_walls = set()

        self.current_player = player_1

    def get_player_position(self, player_id):
        return self.player_positions[player_id]

    def set_player_position(self, player, position):
        self.player_positions[player.player_id] = position

    def switch_turn(self):
        self.current_player.player_id = 2 if self.current_player.player_id == 1 else 1

    def place_wall(self, r, c, is_horizontal):
        # check if occupied by another wall
        if (r, c) in self.horizontal_walls or (r, c) in self.vertical_walls:
            return False

        if is_horizontal:
            # check if a horizontal wall overlaps with adjacent horizontal walls
            if (r, c - 1) in self.horizontal_walls or (r, c + 1) in self.horizontal_walls:
                return False
            self.horizontal_walls.add((r, c))
            return True
        else:
            # check if a vertical wall overlaps with adjacent vertical walls
            if (r - 1, c) in self.vertical_walls or (r + 1, c) in self.vertical_walls:
                return False
            self.vertical_walls.add((r, c))
            return True