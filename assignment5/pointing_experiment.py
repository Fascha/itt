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

read config

present multiple targets



"""

""" setup file looks like this:
USER: 1
WIDTHS: 35, 60, 100, 170
DISTANCES: 170, 300, 450, 700
"""
#!/usr/bin/python3


import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from enum import Enum
import configparser



class States(Enum):
    INSTRUCTIONS = "INSTRUCTIONS"
    TEST = "TEST"
    PAUSE = "PAUSE"
    END = "END"


class Circle(object):
    def __init__(self, x, y, size=20, hightlighted=False):
        self.x = x
        self.y = y
        self.size = size
        self.highlighted = hightlighted


class Model(object):

    def __init__(self, user_id, sizes, distances, repetitions=4):
        self.timer = QtCore.QTime()
        self.user_id = user_id
        self.sizes = sizes
        self.distances = distances
        self.repetitions = repetitions
        self.num_task = 0
        self.tasks = []

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
            for i in range(20):
                # example
                t.append(Circle(20, 200))

            self.tasks.append(t)

    def currentTask(self):

        return self.tasks[self.num_task]

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)

    def debug(self, msg):
        sys.stderr.write(self.timestamp() + ": " + str(msg) + "\n")

    def checkHit(self, target, clickX, clickY):
        """

        check if distance between click and currentTarget circle is smaller than radius of currentTarget circle

        pythagoras
        distance = math.sqrt((target.x - clickX)**2 + (target.y - clickY)**2)

        if distance < target.size/2:
            .......
            .......
            highlighted clicked
        else:
            highlighted not clicked

        """
        pass


class Test(QtWidgets.QWidget):

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.initUI()
        self.current_state = States.INSTRUCTIONS

    def initUI(self):

        # setGeometry(int posx, int posy, int w, int h)
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('Pointing Experiment')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # setting initial Mouseposition
        # QtGui.QCursor.setPos(self.mapToGlobal(QtCore.QPoint(self.start_pos[0], self.start_pos[1])))
        # self.setMouseTracking(True)

        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)

        if self.current_state == States.INSTRUCTIONS:
            self.drawInstructions(event, qp)
        elif self.current_state == States.TEST:
            self.drawTest(event, qp)
        elif self.current_state == States.END:
            self.drawEnd(event, qp)
        qp.end()

    def mouseMoveEvent(self, e):
        """
        when mosue is moved first we need to start measurement
        (setter method needs to be called)

        """
        pass

    def mousePressEvent(self, ev):
        # see model.checkHit!!
        if ev.button() == QtCore.Qt.LeftButton:

            hit = self.model.checkHit(self.currentTarget, ev.x(), ev.y())
            if hit:
                # this executes if the position of the mosueclick is within the highlighted circle
                # QtGui.QCursor.setPos(self.mapToGlobal(QtCore.QPoint(self.start_pos[0], self.start_pos[1])))
                pass
            self.update()

    def keyPressEvent(self, event):
        if self.current_state == States.INSTRUCTIONS and event.key() == QtCore.Qt.Key_Space:
            self.current_state = States.TEST
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


def main():

    # model erstellen
    # test model übergeben

    app = QtWidgets.QApplication(sys.argv)

    # checking if there are command line arguments
    if len(sys.argv) < 2:
        # sys.argv[0] is name of the script
        sys.stderr.write("Usage: {} <setup file>\n".format(sys.argv[0]))
        sys.exit(1)
    print(read_config(sys.argv[1]))

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

    if config['user'] and config['widths'] and config['distances']:
        widths = [int(x) for x in config['widths'].split(",")]
        distances = [int(x) for x in config['distances'].split(",")]
        return config['user'], widths, distances
    else:
        print("Error: wrong file format.")

if __name__ == '__main__':
    main()
