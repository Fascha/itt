import math

"""

DESCRIPTION


"""

class PointingTechnique(object):
    def __init__(self, circles, max_radius):
        self.circles = circles
        self.last_circle = None
        self.max_radius = max_radius

    def filter(self, current_cursor_pos):

        smallest_dist = None
        nearest_circle = None
        for circle in self.circles:
            dist = self.calculate_distance(circle, current_cursor_pos)
            circle.highlighted = False

            if smallest_dist is None:
                if dist < self.max_radius:
                    smallest_dist = dist
                    nearest_circle = circle
            elif dist < smallest_dist and dist < self.max_radius:
                smallest_dist = dist
                nearest_circle = circle

        if nearest_circle is not None:
            nearest_circle.highlighted = True
            return smallest_dist
        else:
            return self.max_radius

    def calculate_distance(self, circle, cursor_position):
        return math.sqrt((circle.x - cursor_position[0])**2 + (circle.y - cursor_position[1])**2)
