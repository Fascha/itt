"""
5.2: Implement a Novel Pointing Technique
Conduct a few test runs of your pointing experiment and invent or find an interaction technique that might help the user in
selecting objects on a computer screen with a certain input device (e.g., mouse, touch screen). Either implement a technique from
the literature (see tips below) or design your own.
Examples:
• the paper “Probabilistic Pointing Target Prediction via Inverse Optimal Control”4 contains a good overview of general ap-
proaches on page 1.
• Bubble Cursor5
• switch between high and low CD gain depending on task (e.g., high CD gain if no target is close by, low CD gain if multiple
targets are close by)
• magnetic targets: once the cursor is close to a target (and no other potential targets are close), ‘pull’ the cursor towards the
target (An Evaluation of Sticky and Force Enhanced Targets in Multi Target Situations6)
• extrapolate the pointer trajectory and highlight the target that will be probably selected, allowing the user to click it earlier.
The pointing technique should be implemented as a separate Python class/object that extends your experiment script from assign-
ment 5.1. This object gets passed a list of available targets (and other necessary information) upon instantiation. Every pointer
event (or a set of coordinates) is then passed to a function filter() of this object. This function returns the new (optimized)
coordinates for the pointer which are then used by . (You are free to implement this any other sensible way, as long as you keep
the implementation of the pointing technique clearly separated from the rest of the application.) Include a comment at the top of
the file explaining concisely how the pointing technique works. The test script from assignment 5.1 should be extended in a way
that allows you to enable/disable use of the pointing technique programmatically (e.g., via the configuration file, via a shortcut,
and/or via a command-line parameter) . The CSV output of the test script should also indicate whether the pointing technique was
activated.
Hand in a file pointing_technique.py (which does not need to be executable on its own).
Points
•
•
•
•
1 The script has been submitted, is not empty, and does not print out error messages.
1 The code is well structured and follows PEP8.
2 The pointing technique is sensible and described in appropriate detail
2 The pointing technique is implemented well (i.e., using it seems to subjectively improve pointing performance)

"""


"""

- das objekt benötigt die targets (muss wissen welches gehighlighted ist bzw. geklickt werden soll)
- in filter soll die "verbesserung" stattfinden 
    mit bubblecursor: einfärben des bei aktuellen klick ausgewählten objekts? (objekt mit niedrigster distanz?)

"""

import math

class PointingTechnique(object):
    def __init__(self, circles, max_radius):
        print("initialized")
        self.circles = circles
        self.last_circle = None
        self.max_radius = max_radius


    """
    Every pointer event (or a set of coordinates) is then passed to a function filter() of this object.
    This function returns the new (optimized) coordinates for the pointer which are then used by.
    (You are free to implement this any other sensible way, as long as you keep
    the implementation of the pointing technique clearly separated from the rest of the application.)
    """
    def filter(self, current_cursor_pos):
        """
        nearest_circle = None
        smallest_dist = None

        for circle in self.circles:
            dist = self.calculate_distance(circle, current_cursor_pos)
            if nearest_circle is None:
                nearest_circle = circle
                smallest_dist = dist
            elif dist < smallest_dist:
                nearest_circle = circle

        if self.last_circle is None:
            self.last_circle = nearest_circle
        elif self.last_circle == nearest_circle:
            print("sind gleich")
        else:
            self.last_circle.highlighted = False

        nearest_circle.highlighted = True
        """

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
