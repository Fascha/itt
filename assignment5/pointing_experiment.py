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

read config     ----DONE----

present multiple targets

center mousecursor on task start    ----DONE----

refactor so WIDTH, Height (and Center) are constants read from config    ---DONE---

let targets don't overlap (siehe checkIfOverlapping)

target with correct distance (siehe setuptasks)

create border around highlighted target (passiert schon in checkifoverlapping)

set mouse cursor_start_pos to the middle of the screen after each pause (or provide small target that user has to click in order to continue?)

apply distances multiple times with different conditions? We could double the target size -> each distance one time with size 20, and each with size 40


Größe und Reihenfolge von Abständen pseudo randomisieren in create config oder in dem python File?

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
USER: 1
WIDTHS: 35, 60, 100, 170
DISTANCES: 170, 300, 450, 700
"""
#!/usr/bin/python3


import configparser
from enum import Enum
import math
from PyQt5 import QtGui, QtWidgets, QtCore
import random
import sys


class States(Enum):
    INSTRUCTIONS = "INSTRUCTIONS"
    TEST = "TEST"
    PAUSE = "PAUSE"
    END = "END"


class Circle(object):
    def __init__(self, x, y, highlighted, size=20):
        self.x = x
        self.y = y
        self.size = size
        self.highlighted = highlighted


class Model(object):

    def __init__(self, user_id, sizes, distances, window_width, window_height, repetitions=4):
        self.timer = QtCore.QTime()
        self.user_id = user_id
        self.sizes = sizes
        self.distances = distances
        self.window_width = window_width
        self.window_height = window_height
        self.repetitions = repetitions
        self.num_task = 0
        self.tasks = []
        self.num_error = 0

        self.mouse_moving = False

        self.currentTarget = None

        self.setupTasks()

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
            # zufällige Position im radius um den Startpunkt berechnen 
            start_position = (self.window_width/2, self.window_height/2)
            """
            Position von current target im Radius(distance) um Startposition.
            random.random() vllt nicht richtig?
        
            """
            random_angle = random.random()*2*math.pi
            current_target_x = start_position[0] + math.cos(random_angle)*self.distances[x]
            current_target_y = start_position[1] + math.sin(random_angle)*self.distances[x]
            self.currentTarget = Circle(current_target_x, current_target_y, True)
            # print(self.distances[x], current_target_x, current_target_y)
            """
            berechne nochmal die distance, weil die targets oft komisch liegen , aber wird richtig ausgegeben
            von der Startposition aus
            """
            distance = (math.sqrt((current_target_x-start_position[0])**2 + (current_target_y-start_position[1])**2))
            # print(distance)
            t.append(self.currentTarget)

            for i in range(100):
                random_x = random.randint(0, self.window_width)
                random_y = random.randint(0, self.window_height)
                newTarget = Circle(random_x, random_y, False)
                
                #check if new target is overlapping with existing targets
                if not self.checkIfOverlapping(t, newTarget):
                    t.append(newTarget)
                elif self.checkIfOverlapping(t, newTarget):
                    pass

            self.tasks.append(t)

    def checkIfOverlapping(self, existingTargets, newTarget):
        """
        durchläuft nur erstes existingtarget (rotes) -> dies wird dann von anderen nicht überlappt, 
        aber manche schwarze werden von anderen schwarzen  schon überlappt, 
        obwohl eigtl alle durchlaufen werden sollten in der forschleife?
        die Größe von existingTargets wird auch größer..
        Sollte eigtl jedes newTarget mit den bereits bestehenden targets auf Überschneidungen überprüfen..
        """
        for target in existingTargets:
            distance = math.sqrt((target.x - newTarget.x)**2 + (target.y - newTarget.y)**2)    
            if distance < (target.size + newTarget.size)*2:
                # print("True", target.x, newTarget.x, distance, target.size, newTarget.size)
                #  circles are overlapping
                return True
            else:
                #  circles are not overlapping
                # print("False", target.x, newTarget.x, distance, target.size, newTarget.size)
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

    def create_log(self, timeontask):
        print("%s; %s; %d; %d; %d;" % (self.timestamp(), self.user_id, self.num_task, timeontask, self.num_error))
        self.num_error = 0

    def checkHit(self, target, clickX, clickY):
        """

        check if distance between click and currentTarget circle is smaller than radius of currentTarget circle

        pythagoras
        """
        distance = math.sqrt((target.x - clickX)**2 + (target.y - clickY)**2)

        if distance < target.size/2:
            #  highlighted clicked
            self.num_task += 1
            self.create_log(self.stop_measurement())
            return True
        else:
            #  highlighted not clicked
            self.num_error += 1
            return False




class Test(QtWidgets.QWidget):

    WIDTH = 1000
    HEIGHT = 1000

    def __init__(self, model):
        super(Test, self).__init__()
        self.model = model
        self.cursor_start_pos = (self.WIDTH/2, self.HEIGHT/2)
        self.initUI()
        self.current_state = States.INSTRUCTIONS

    def initUI(self):
        # setGeometry(int posx, int posy, int w, int h)
        self.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.setWindowTitle('Pointing Experiment')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # setting initial Mouseposition
        self.centerCursor()
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

    def mouseMoveEvent(self, e):
        """
        when mosue is moved first we need to start measurement
        (setter method needs to be called)

        """
        if e.type() == QtCore.QEvent.MouseMove:
            self.model.start_measurement()
        pass

    def mousePressEvent(self, ev):
        # see model.checkHit!!
        if ev.button() == QtCore.Qt.LeftButton:

            hit = self.model.checkHit(self.currentTarget, ev.x(), ev.y())
            if hit:
                # this executes if the position of the mosueclick is within the highlighted circle
                if self.model.num_task == len(self.model.tasks):
                    self.current_state = States.END
                else:
                    self.current_state = States.PAUSE
                pass
            self.update()

    def keyPressEvent(self, event):
        if self.current_state == States.INSTRUCTIONS and event.key() == QtCore.Qt.Key_Space:
            self.current_state = States.TEST
            self.update()
        elif self.current_state == States.PAUSE and event.key() == QtCore.Qt.Key_Space:
            self.current_state = States.TEST
            self.centerCursor()
            self.update()

    def drawEnd(self, event, qp):
        qp.setFont(QtGui.QFont('Helvetica', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "THANK YOU FOR PARTICIPATING!")

    def drawTest(self, event, qp):
        print("drawing test")
        self.drawCircles(event, qp)

    def drawInstructions(self, event, qp):
        print("drawing instructions")
        qp.setFont(QtGui.QFont('Helvetica', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "POINTING EXPERIMENT\n\n")
        qp.setFont(QtGui.QFont('Helvetica', 16))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "IN THE FOLLOWING SCREENS YOU WILL BE PRESENTED SOME CIRCLES\nPLEASE CLICK THE HIGHLIGHTED CIRCLE")

    def drawPause(self, event, qp):
        print("drawing pause")
        qp.setFont(QtGui.QFont('Helvetica', 16))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "PRESS THE SPACE KEY WHEN YOU ARE READY TO CONTINUE")

    def drawBackground(self, event, qp):
        qp.setBrush(QtGui.QColor(22, 200, 22))
        qp.drawRect(event.rect())

    def drawCircles(self, event, qp):
        for circle in self.model.currentTask():
            x, y, size, highlighted = circle.x, circle.y, circle.size, circle.highlighted

            if highlighted:
                qp.setBrush(QtGui.QColor(200, 34, 20))
                self.currentTarget = circle
            else:
                qp.setBrush(QtGui.QColor(33, 34, 20))

            qp.drawEllipse(x-size/2, y-size/2, size, size)

    def centerCursor(self):
        QtGui.QCursor.setPos(self.mapToGlobal(QtCore.QPoint(self.cursor_start_pos[0], self.cursor_start_pos[1])))



def main():

    # model erstellen
    # test model übergeben

    app = QtWidgets.QApplication(sys.argv)

    # checking if there are command line arguments
    if len(sys.argv) < 2:
        # sys.argv[0] is name of the script
        sys.stderr.write("Usage: {} <setup file>\n".format(sys.argv[0]))
        sys.exit(1)
    # print(read_config(sys.argv[1]))

    model = Model(*read_config(sys.argv[1]))
    test = Test(model)
    sys.exit(app.exec_())


def read_config(filename):
    # lines = open(filename, 'r').readlines()
    # if lines[0].startswith("USER:"):
    #     user_id = lines[0].split(":")[1].strip()
    # else:
    #     print("Error: wrong file format.")
    #
    # if lines[1].startswith("WIDTHS:"):
    #     width_string = lines[1].split(":")[1].strip()
    #     widths = [int(x) for x in width_string.split(",")]
    # else:
    #     print("Error: wrong file format.")
    #
    # if lines[2].startswith("DISTANCES:"):
    #     distance_string = lines[2].split(":")[1].strip()
    #     distances = [int(x) for x in distance_string.split(",")]
    # else:
    #     print("Error: wrong file format.")
    #
    # return user_id, widths, distances

    config = configparser.ConfigParser()
    config.read(filename)

    config = config['POINTING EXPERIMENT']

    window_width = int(config['window_width']) if config['window_width'] else 999
    window_height = int(config['window_height']) if config['window_height'] else 999

    print('width', window_width)
    print('height', window_height)

    if config['user'] and config['widths'] and config['distances']:
        widths = [int(x) for x in config['widths'].split(",")]
        distances = [int(x) for x in config['distances'].split(",")]
        return config['user'], widths, distances, window_width, window_height
    else:
        print("Error: wrong file format.")

if __name__ == '__main__':
    main()
