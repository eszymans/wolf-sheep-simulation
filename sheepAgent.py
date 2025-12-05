import random


class SheepAgent:

    def __init__(self, number, init_pos=10.0, distance=0.5):
        self.position_x = random.uniform(-init_pos, init_pos)
        self.position_y = random.uniform(-init_pos, init_pos)
        self.distance = distance
        self.meadow_range = (-init_pos, init_pos)
        self.alive = True
        self.id = number

    def move(self, direction):
        if direction == "UP":
            self.position_y -= self.distance
        if direction == "DOWN":
            self.position_y += self.distance
        if direction == "RIGHT":
            self.position_x += self.distance
        if direction == "LEFT":
            self.position_x -= self.distance
        self.check_moves()

    def check_moves(self):
        min_limit = self.meadow_range[0]
        max_limit = self.meadow_range[1]
        # checks for X
        if self.position_x < min_limit:
            self.position_x = min_limit
        elif self.position_x > max_limit:
            self.position_x = max_limit

        # checks for Y
        if self.position_y < min_limit:
            self.position_y = min_limit
        elif self.position_y > max_limit:
            self.position_y = max_limit

    def random_move(self, logging):
        direction = random.choice(["UP", "DOWN", "RIGHT", "LEFT"])
        logging.debug(f"Sheep {self.id} chose direction: {direction}")
        self.move(direction)
        logging.debug(f"Sheep {self.id} moved to: "
                      f"{self.get_position()}")

    def died(self):
        self.alive = False
        self.position_y = None
        self.position_x = None

    def get_position(self):
        return self.position_x, self.position_y

    def is_alive(self):
        return self.alive

    def __str__(self):
        return f"Sheep position: ({self.position_x}, {self.position_y})"
