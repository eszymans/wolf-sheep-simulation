class WolfAgent:
    def __init__(self, distance=1.0):
        self.position_x = 0.0
        self.position_y = 0.0
        self.distance = distance

    def set_position(self, distance_x, distance_y):
        self.position_x = distance_x
        self.position_y = distance_y

    def euclidean_distance(self, sheep):
        first_statement = self.position_x - sheep.position_x
        second_statement = self.position_y - sheep.position_y
        return (first_statement ** 2 + second_statement ** 2) ** 0.5

    def find_closest_sheep(self, sheeps):
        alive_sheeps = [s for s in sheeps if s.alive]
        closest_sheep = alive_sheeps[0]
        for sheep in alive_sheeps:
            if sheep.is_alive():
                if self.euclidean_distance(
                        sheep) < self.euclidean_distance(
                        closest_sheep):
                    closest_sheep = sheep
        return closest_sheep

    def calculate_new_position(self, sheep):
        distance = self.euclidean_distance(sheep)
        ratio = self.distance / distance
        x = self.position_x + (
                    sheep.position_x - self.position_x) * ratio
        y = self.position_y + (
                    sheep.position_y - self.position_y) * ratio
        return x, y

    def move(self, sheep, sheeps):
        if self.euclidean_distance(sheep) <= self.distance:
            self.set_position(sheep.position_x, sheep.position_y)
            sheep.died()
            print(f"Wolf killed a sheep {sheeps.index(sheep) + 1}")
            return True
        else:
            x, y = self.calculate_new_position(sheep)
            self.set_position(x, y)
            print(f"Wolf moved to a sheep {sheeps.index(sheep) + 1}")
            return False

    def get_position(self):
        return self.position_x, self.position_y

    def __str__(self):
        return f"Wolf at ({self.position_x}, {self.position_y})"
