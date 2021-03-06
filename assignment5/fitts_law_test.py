#!/usr/bin/python3

""" Copyright 2014-2017 Raphael Wimmer <raphael.wimmer@ur.de> 
License: CC-0 (essentially: do what you want with it, no attribution required)
"""

import sys
import random
import math
import itertools
from PyQt5 import QtGui, QtWidgets, QtCore

SIZES = [35, 60, 100, 170]
DISTANCES = [170, 300, 450, 700]
REPETITIONS = 4

""" setup file looks like this:
USER: 1
WIDTHS: 35, 60, 100, 170
DISTANCES: 170, 300, 450, 700
"""


# This example code contains several anti-patterns and ugly approaches.
# Do not directly copy it but mine it for useful API calls and snippets.


class FittsLawModel(object):

    def __init__(self, user_id, sizes, distances, repetitions=4):
        self.timer = QtCore.QTime()
        self.user_id = user_id
        self.sizes = sizes
        self.distances = distances
        self.repetitions = repetitions
        # gives us a list of (distance, width) tuples:
        self.targets = repetitions * list(itertools.product(distances, sizes))
        random.shuffle(self.targets)
        self.elapsed = 0
        self.mouse_moving = False
        print("timestamp (ISO); user_id; trial; target_distance; target_size; movement_time (ms); click_offset_x; click_offset_y")

    def current_target(self):
        if self.elapsed >= len(self.targets):
            return None
        else:
            return self.targets[self.elapsed]

    def register_click(self, target_pos, click_pos):
        dist = math.sqrt((target_pos[0]-click_pos[0]) * (target_pos[0]-click_pos[0]) +
                         (target_pos[1]-click_pos[1]) * (target_pos[1]-click_pos[1]))
        if dist > self.current_target()[1]:
            return False
        else:
            click_offset = (target_pos[0] - click_pos[0], target_pos[1] - click_pos[1])
            self.log_time(self.stop_measurement(), click_offset)
            self.elapsed += 1
            return True

    def log_time(self, time, click_offset):
        distance, size = self.current_target()
        print("%s; %s; %d; %d; %d; %d; %d; %d" % (self.timestamp(), self.user_id, self.elapsed, distance, size, time, click_offset[0], click_offset[1]))

    def start_measurement(self):
        if not self.mouse_moving:
            self.timer.start()
            self.mouse_moving = True

    def stop_measurement(self):
        if self.mouse_moving:
            elapsed = self.timer.elapsed()
            self.mouse_moving = False
            return elapsed
        else:
            self.debug("not running")
            return -1

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)

    def debug(self, msg):
        sys.stderr.write(self.timestamp() + ": " + str(msg) + "\n")


class FittsLawTest(QtWidgets.QWidget):

    def __init__(self, model):
        super(FittsLawTest, self).__init__()
        self.model = model
        self.start_pos = (400, 400)
        self.initUI()

    def initUI(self):
        self.text = "Please click on the target"
        self.setGeometry(0, 0, 1920, 800)
        self.setWindowTitle('FittsLawTest')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtGui.QCursor.setPos(self.mapToGlobal(QtCore.QPoint(self.start_pos[0], self.start_pos[1])))
        self.setMouseTracking(True)
        self.show()

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            tp = self.target_pos(self.model.current_target()[0])
            hit = self.model.register_click(tp, (ev.x(), ev.y()))
            if hit:
                QtGui.QCursor.setPos(self.mapToGlobal(QtCore.QPoint(self.start_pos[0], self.start_pos[1])))
            self.update()

    def mouseMoveEvent(self, ev):
        if (abs(ev.x() - self.start_pos[0]) > 5) or (abs(ev.y() - self.start_pos[1]) > 5):
            self.model.start_measurement()
            self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        self.drawText(event, qp)
        self.drawTarget(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 32))
        self.text = "%d / %d (%05d ms)" % (self.model.elapsed, len(self.model.targets), self.model.timer.elapsed())
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def target_pos(self, distance):
        x = self.start_pos[0] + distance
        y = self.start_pos[1]
        return (x, y)

    def drawBackground(self, event, qp):
        if self.model.mouse_moving:
            qp.setBrush(QtGui.QColor(220, 190, 190))
        else:
            qp.setBrush(QtGui.QColor(200, 200, 200))
        qp.drawRect(event.rect())

    def drawTarget(self, event, qp):
        if self.model.current_target() is not None:
            distance, size = self.model.current_target()
        else:
            sys.stderr.write("no targets left...")
            sys.exit(1)
        x, y = self.target_pos(distance)
        qp.setBrush(QtGui.QColor(200, 34, 20))
        qp.drawEllipse(x-size/2, y-size/2, size, size)


def main():
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <setup file>\n" % sys.argv[0])
        sys.exit(1)
    model = FittsLawModel(*parse_setup(sys.argv[1]))
    fitts_law_test = FittsLawTest(model)
    sys.exit(app.exec_())


def parse_setup(filename):
    lines = open(filename, "r").readlines()
    if lines[0].startswith("USER:"):
        user_id = lines[0].split(":")[1].strip()
    else:
        print("Error: wrong file format.")
    if lines[1].startswith("WIDTHS:"):
        width_string = lines[1].split(":")[1].strip()
        widths = [int(x) for x in width_string.split(",")]
    else:
        print("Error: wrong file format.")
    if lines[2].startswith("DISTANCES:"):
        distance_string = lines[2].split(":")[1].strip()
        distances = [int(x) for x in distance_string.split(",")]
    else:
        print("Error: wrong file format.")
    return user_id, widths, distances

if __name__ == '__main__':
    main()
