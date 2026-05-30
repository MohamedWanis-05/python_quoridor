from game.constants import BOARD_SIZE
from game.player import Player
from ai.pathfinding import has_path_to_goal


class Board:
    def __init__(self,size=9):

        self.size = size
        center_col = self.size // 2
        self.player_positions = {
            1: (0, center_col),
            2: (self.size - 1, center_col)
        }
        self.player_1 = Player(1,self.size+1)
        self.player_2 = Player(2,self.size+1)

        self.horizontal_walls = set()
        self.vertical_walls = set()

        self.current_player = self.player_1

    def get_player_position(self, player_id):
        return self.player_positions[player_id]

    def set_player_position(self, player_id, position):
        self.player_positions[player_id] = position

    def switch_turn(self):
        self.current_player = self.player_2 if self.current_player.player_id == 1 else self.player_1

    def place_wall(self, r, c, is_horizontal):
        if self.current_player.walls_remaining <= 0:
            return False

        if not self.can_place_wall(r, c, is_horizontal):
            return False


        if is_horizontal:
            self.horizontal_walls.add((r, c))
        else:
            self.vertical_walls.add((r, c))

        self.current_player.walls_remaining -= 1


        player1_has_path = has_path_to_goal(self, 1)
        player2_has_path = has_path_to_goal(self, 2)

        if not player1_has_path or not player2_has_path:

            if is_horizontal:
                self.horizontal_walls.remove((r, c))
            else:
                self.vertical_walls.remove((r, c))
            self.current_player.walls_remaining += 1

            return False

        return True
            
    def can_place_wall(self, r, c, is_horizontal):

        if is_horizontal:

            if r < 0 or r >= self.size - 1:
                return False

            if c < 0 or c >= self.size - 1:
                return False

            if (r, c) in self.horizontal_walls:
                return False

            if (r, c + 1) in self.horizontal_walls:
                return False
            if (r, c - 1) in self.horizontal_walls:
                return False

            if (r, c) in self.vertical_walls:
                return False

        else:

            if r < 0 or r >= self.size - 1:
                return False

            if c < 0 or c >= self.size - 1:
                return False

            if (r, c) in self.vertical_walls:
                return False

            if (r + 1, c) in self.vertical_walls:
                return False

            if (r - 1, c) in self.vertical_walls:
                return False

            if (r, c) in self.horizontal_walls:
                return False

        return True