class Player:
    def __init__(self, player_id, goal_row):
        self.player_id = player_id
        self.goal_row = goal_row
        self.walls_remaining = 10