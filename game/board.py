from game.constants import BOARD_SIZE


class Board:
    def __init__(self):
        self.size = BOARD_SIZE

        self.player_positions = {
            1: (0, 4),
            2: (8, 4)
        }

        self.horizontal_walls = set()
        self.vertical_walls = set()

        self.current_player = 1

    def get_player_position(self, player_id):
        return self.player_positions[player_id]

    def set_player_position(self, player_id, position):
        self.player_positions[player_id] = position

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1