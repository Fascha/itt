"""
5.1: Implement a Pointing Experiment
Create a Python script that can be used to conduct a pointing experiment.
In particular, your script should have the following features:
• read test configuration from a .ini file¹ or .json file².
• present multiple targets on the screen that the user can click (example: Bubble Cursor (video)³. In most cases, colored circles
are a good choice - although you may present file icons, words, etc. instead. You may also use a background image as
distractor (see e.g., the Shift study). One of the targets should be highlighted in some way to indicate that the user should
try to click on this one.
• conduct multiple rounds with varying sizes/distances (colors, … - whatever you like) of targets.
• presents conditions in a counter-balanced order.
• outputs all important information (e.g., start/end position of pointer, errors, task completion time, condition) on stdout
in CSV format.


Notes:
• Have a look at fitts_law_experiment.py in GRIPS for some ideas on how to implement the script. Be aware that
this is ugly code for several reasons.

• One important design decision you have to make: where to place the targets and the pointer. The approach used in
fitts_law_experiment.py has advantages and limitations. Have a look at other pointing experiments (e.g., on
YouTube) for inspiration on pointer/target placement.

• Try to use a modular implementation where experiment design (which task should be run next, etc.) is implemented seperately
from target display and pointer tracking.


Hand in a file pointing_experiment.py


¹https://docs.python.org/3/library/configparser.html
²https://docs.python.org/3/library/json.html
³https://www.youtube.com/watch?v=AEnfV4cTrvQ


Points
• 1 The script has been submitted, is not empty, and does not print out error messages.
• 1 The code is well structured and follows PEP8.
• 1 The presentation is beautiful and follows best practices for user interfaces.
• 1 The script reads in the test configuration from a file.
• 2 The script presents targets of which one is highlighted and can be clicked
• 1 The script presents multiple pointing tasks to the user
• 1 The script outputs all necessary information on stdout in CSV format
"""

"""

TODO

Zu klärende Fragen:
nicht gehighlightete kreie immer so groß wie gehighlightet oder feste/zufällige größe?
anzahl der ablenkungskreise festlegen


TASKS:
read config     ----DONE----

present multiple targets    ----DONE----

center mousecursor on task start    ----DONE----  manchmal doppelcursor

refactor so WIDTH, Height (and Center) are constants read from config    ---DONE---

pseudo randomizing the order    ----DONE----
COUNTERBALANCING?

let targets don't overlap (siehe checkIfOverlapping)    ---DONE---

target with correct distance (siehe setuptasks)     ---DONE---

beim erstellen eines zufälligen kreises den radius des kreises von x und y abziehen
statt random.randint(0, self.window_width) => random_x = random.randint(size, self.window_width-size)  ----DONE---

set mouse cursor_start_pos to the middle of the screen after each pause (or provide small target that user has to click in order to continue?)  ----DONE----

apply distances multiple times with different conditions? We could double the target size -> each distance one time with size 20, and each with size 40    ----DONE----

for log file:
    start timer when mouse is moving ,
    end timer, when target is hit,
    count errors (wird auf stdout ausgegeben)

    create file with all data(
        participant id
        start/end pos of pointer (calculate distance the user had to travel?), 
        taks completion time, 
        error rate, 
        condition)

add new pointing technique, bubble cursor around cursor.. new file?

"""

""" setup file looks like this:
[POINTING EXPERIMENT]
user = 1
window_height = 1000
widths = 30, 50, 60, 70
distances = 100, 200, 300, 400
window_width = 1000
"""
#!/usr/bin/python3
import configparser
from enum import Enum
import math
from PyQt5 import QtGui, QtWidgets, QtCore
import random
import sys
import csv
import os
from collections import OrderedDict
from pointing_technique import PointingTechnique

"""
Description
"""


class States(Enum):
    INSTRUCTIONS = "INSTRUCTIONS"
    TEST = "TEST"
    PAUSE = "PAUSE"
    END = "END"


class Circle(object):
    def __init__(self, x, y, size, target=False, highlighted=False):
        self.x = x
        self.y = y
        self.size = size
        self.target = target
        self.highlighted = highlighted


class Model(object):

    def __init__(self, user_id, sizes, distances, window_width, window_height, cursor_start_pos, bubble=False):
        self.timer = QtCore.QTime()
        self.user_id = user_id
        self.sizes = sizes
        self.distances = distances
        self.window_width = window_width
        self.window_height = window_height
        self.num_task = 0
        self.tasks = []
        self.num_error = 0
        self.mouse_moving = False
        self.currentTarget = None
        self.bubble = bubble
        self.cursor_start_pos = cursor_start_pos
        self.setupTasks()
        self.logging_list = []

    def setupTasks(self):
        # example circles
        # self.tasks.append(Circle(400, 400, 40, True))
        # self.tasks.append(Circle(300, 400))

        for x in range(len(self.distances)):
            """
            random oder mit gewissen algorithmus?

            doppelte for schleife um listen in den listen zu erzeugen
            eine liste enthält alle circles für den task und alle diese listen sind in der oberliste


            erst den gehighlighteten kreis erstellen
            dann zufällige kreise erstellen die nicht mim highlight überschneiden
            vs.
            immer gleiche kreise erstellen und abhängig von distanz den einen highlighten

            """
            t = []
            # start_position = (self.window_width/2, self.window_height/2)
            # random point with distance around starting point
            random_angle = random.random()*2*math.pi
            current_target_x = self.cursor_start_pos[0] + math.cos(random_angle)*self.distances[x]
            current_target_y = self.cursor_start_pos[1] + math.sin(random_angle)*self.distances[x]

            self.currentTarget = Circle(current_target_x, current_target_y, self.sizes[x], target=True)

            # distance = math.sqrt((current_target_x-self.cursor_start_pos[0])**2 +
            #                      (current_target_y-self.cursor_start_pos[1])**2)

            t.append(self.currentTarget)

            for i in range(50):
                """
                random_x = random.randint(0, self.window_width)
                random_y = random.randint(0, self.window_height)
                newTarget = Circle(random_x, random_y, False)

                #check if new target is overlapping with existing targets
                if not self.checkIfOverlapping(t, newTarget):
                    t.append(newTarget)
                elif self.checkIfOverlapping(t, newTarget):
                    pass
                """

                # solange True returned wird wird ein neuer kreis erzeugt!
                # counter mitlaufen lassen um endlosschleife(wenn nicht mehr genug platz) zu vermeiden
                newTarget = self.createRandomCircle()

                while self.checkIfOverlapping(t, newTarget):
                    newTarget = self.createRandomCircle()

                t.append(newTarget)

            self.tasks.append(t)

    def createRandomCircle(self):
        random_x = random.randint(self.currentTarget.size/2, self.window_width - self.currentTarget.size/2)
        random_y = random.randint(self.currentTarget.size/2, self.window_height - self.currentTarget.size/2)
        return Circle(random_x, random_y, self.currentTarget.size)

    def checkIfOverlapping(self, existingTargets, newTarget):
        for target in existingTargets:
            # calculate distance of new target and existing target with pythagoras
            distance = math.sqrt((target.x - newTarget.x)**2 + (target.y - newTarget.y)**2)
            # return true when distance is smaller
            if distance < (target.size + newTarget.size)/2:
                return True
        return False

    def currentTask(self):
        return self.tasks[self.num_task]

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)

    def debug(self, msg):
        sys.stderr.write(self.timestamp() + ": " + str(msg) + "\n")

    def start_measurement(self):
        if not self.mouse_moving:
            self.timer.start()
            self.mouse_moving = True

    def stop_measurement(self):
        if self.mouse_moving:
            timeontask = self.timer.elapsed()
            self.mouse_moving = False
            return timeontask
        else:
            self.debug("not running")
            return -1

    def create_log(self, timeontask, click):
        print("%s; %s; %d; %d; %d;" % (self.timestamp(), self.user_id, self.num_task, timeontask, self.num_error))

        logging_dict = OrderedDict([
            ('timestamp', self.timestamp()),
            ('id', self.user_id),
            ('num_task', self.num_task),
            # error list index out of range
            ('target_distance', self.distances[self.num_task]),
            ('target_size', self.sizes[self.num_task]),
            # check if pointer is with or without bubble
            ('bubble_pointer', self.bubble),
            ('reaction_time', timeontask),
            ('number_of_errors', self.num_error),
            ('start_x', self.cursor_start_pos[0]),
            ('start_y', self.cursor_start_pos[1]),
            ('click_x', click[0]),
            ('click_y', click[1]),
        ])
        self.logging_list.append(logging_dict)
        self.num_error = 0

    def writeLogToFile(self):
        filepath_total = 'pointing_experiment_results.csv'
        if self.bubble:
            filepath = 'pointing_experiment_result_' + str(self.user_id) + '_bubble.csv'
        else:
            filepath = 'pointing_experiment_result_' + str(self.user_id) + '.csv'



        # checking if file with all experiments exists
        log_file_exists = os.path.isfile(filepath_total)

        # appending to the concatenated file
        with open(filepath_total, 'a') as f:
            writer = csv.DictWriter(f, list(self.logging_list[0].keys()))
            if not log_file_exists:
                writer.writeheader()
            writer.writerows(self.logging_list)
        # writing to a separate file
        with open(filepath, 'w') as f:
            writer = csv.DictWriter(f, list(self.logging_list[0].keys()))
            writer.writeheader()
            writer.writerows(self.logging_list)

    def checkHit(self, target, clickX, clickY):
        """
        check if distance between click and currentTarget circle is smaller than radius of currentTarget circle

        pythagoras
        """
        distance = math.sqrt((target.x - clickX)**2 + (target.y - clickY)**2)

        if distance < target.size/2:
            #  highlighted clicked
            self.create_log(self.stop_measurement(), (clickX, clickY))
            self.num_task += 1
            return True
        else:
            #  highlighted not clicked
            self.num_error += 1
            return False


class Test(QtWidgets.QWidget):

    def __init__(self, model, bubble=False):
        super(Test, self).__init__()
        self.model = model
        self.bubble = bubble
        self.bubble_size = 0
        self.max_bubble_size = 100
        self.cursor_start_pos = (self.model.window_width/2, self.model.window_height/2)
        self.current_cursor_position = self.cursor_start_pos
        self.initUI()
        self.current_state = States.INSTRUCTIONS

    def initUI(self):
        # setGeometry(int posx, int posy, int w, int h)
        self.setGeometry(0, 0, self.model.window_width, self.model.window_height)
        self.setWindowTitle('Pointing Experiment')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # setting initial Mouseposition
        # self.centerCursor()
        self.setMouseTracking(True)

        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)

        if self.current_state == States.INSTRUCTIONS:
            self.drawInstructions(event, qp)
        elif self.current_state == States.TEST:
            self.drawTest(event, qp)
        elif self.current_state == States.PAUSE:
            self.drawPause(event, qp)
        elif self.current_state == States.END:
            self.drawEnd(event, qp)
        qp.end()

    def mouseMoveEvent(self, ev):
        """
        when mosue is moved first we need to start measurement
        (setter method needs to be called)

        """
        if self.current_state == States.TEST and ev.type() == QtCore.QEvent.MouseMove:
            self.model.start_measurement()
        self.current_cursor_position = (ev.x(), ev.y())
        self.update()

    def mousePressEvent(self, ev):
        # see model.checkHit!!
        if ev.button() == QtCore.Qt.LeftButton:
            # hit = True if self.bubble and self.currentTarget.highlighted else self.model.checkHit(self.currentTarget, ev.x(), ev.y())
            if self.bubble and self.current_state == States.TEST:
                if self.currentTarget.highlighted:
                    hit = True
                else:
                    hit = False

                if hit:
                    self.model.create_log(self.model.stop_measurement(), (ev.x(), ev.y()))
                    self.model.num_task += 1
                else:
                    self.model.num_error += 1

            else:
                if self.current_state == States.TEST:
                    hit = self.model.checkHit(self.currentTarget, ev.x(), ev.y())

            if hit:
                # this executes if the position of the mosueclick is within the highlighted circle
                # print(len(self.model.tasks))
                if self.model.num_task >= len(self.model.tasks):
                    self.current_state = States.END
                else:
                    # print(self.model.num_task, len(self.model.tasks))
                    self.current_state = States.PAUSE
            self.update()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space and self.current_state is not States.TEST:
            # doppelte if-Abfrage notwendig?
            if self.current_state == States.INSTRUCTIONS:
                self.current_state = States.TEST
            elif self.current_state == States.PAUSE:
                self.current_state = States.TEST

            if self.current_state is not States.END:
                if self.bubble:
                    self.pt = PointingTechnique(self.model.currentTask(), self.max_bubble_size)

            self.centerCursor()
            self.update()

        """
        if self.current_state == States.INSTRUCTIONS and event.key() == QtCore.Qt.Key_Space:
            self.current_state = States.TEST
            self.update()
        elif self.current_state == States.PAUSE and event.key() == QtCore.Qt.Key_Space:
            self.current_state = States.TEST
            # self.centerCursor()
            self.update()
        """

    def drawEnd(self, event, qp):
        qp.setFont(QtGui.QFont('Helvetica', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "THANK YOU FOR PARTICIPATING!")

    def drawTest(self, event, qp):
        self.drawCircles(event, qp)
        if self.bubble:
            self.drawBubble(event, qp)

    def drawInstructions(self, event, qp):
        qp.setFont(QtGui.QFont('Helvetica', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "POINTING EXPERIMENT\n\n")
        qp.setFont(QtGui.QFont('Helvetica', 16))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter,
                    "IN THE FOLLOWING SCREENS YOU WILL BE PRESENTED SOME CIRCLES\nPLEASE CLICK THE HIGHLIGHTED CIRCLE")
        # self.centerCursor()

    def drawPause(self, event, qp):
        # print("drawing pause")
        qp.setFont(QtGui.QFont('Helvetica', 16))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "PRESS THE SPACE KEY WHEN YOU ARE READY TO CONTINUE")

    def drawBackground(self, event, qp):
        qp.setBrush(QtGui.QColor(22, 200, 22))
        qp.drawRect(event.rect())

    def drawBubble(self, event, qp):
        qp.setBrush(QtGui.QColor(20, 20, 200, 100))
        qp.drawEllipse(self.current_cursor_position[0]-self.bubble_size, self.current_cursor_position[1]-self.bubble_size, self.bubble_size*2, self.bubble_size*2)

    def drawCircles(self, event, qp):
        # drawin rect at centerof the screen around the cursor
        # self.centerCursor()
        qp.drawRect(self.model.window_width/2-5, self.model.window_height/2-5, 10, 10)

        if self.bubble:
            self.bubble_size = self.pt.filter(self.current_cursor_position)


        for circle in self.model.currentTask():
            x, y, size, target, highlighted = circle.x, circle.y, circle.size, circle.target, circle.highlighted

            if target:
                qp.setBrush(QtGui.QColor(20, 200, 30))
                self.currentTarget = circle
            else:
                qp.setBrush(QtGui.QColor(30, 30, 30))

            if highlighted:
                qp.setBrush(QtGui.QColor(200, 30, 20))

            qp.drawEllipse(x-size/2, y-size/2, size, size)

    def centerCursor(self):
        QtGui.QCursor.setPos(self.mapToGlobal(QtCore.QPoint(self.cursor_start_pos[0], self.cursor_start_pos[1])))

    def closeEvent(self, event):
        # checking if log was already written when you close the pyqt app
        if self.model.num_task > 0:
            self.model.writeLogToFile()


def main():
    # model erstellen
    # test model übergeben

    app = QtWidgets.QApplication(sys.argv)

    # checking if there are command line arguments
    if len(sys.argv) < 2:
        # sys.argv[0] is name of the script
        sys.stderr.write("Usage: {} <setup file> [<bubble>]\n".format(sys.argv[0]))
        sys.exit(1)

    if len(sys.argv) == 2:
        # config ini übergeben
        pass

    if len(sys.argv) == 3:
        model = Model(*read_config(sys.argv[1]), bubble=True)
        test = Test(model, bubble=True)
    else:
        print("in else")
        model = Model(*read_config(sys.argv[1]))
        test = Test(model)

    sys.exit(app.exec_())


def read_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    config = config['POINTING EXPERIMENT']

    window_width = int(config['window_width']) if config['window_width'] else 800
    window_height = int(config['window_height']) if config['window_height'] else 800
    cursor_start_x = int(config['cursor_start_x']) if config['cursor_start_x'] else 400
    cursor_start_y = int(config['cursor_start_y']) if config['cursor_start_y'] else 400

    print('window_width', window_width)
    print('window_height', window_height)

    if config['user'] and config['widths'] and config['distances']:
        widths = [int(x) for x in config['widths'].split(",")]
        distances = [int(x) for x in config['distances'].split(",")]
        return config['user'], widths, distances, window_width, window_height, (cursor_start_x, cursor_start_y)
    else:
        print("Error: wrong file format.")


if __name__ == '__main__':
    main()
