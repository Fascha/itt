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



class Model(object):

    def __init__(self, user_id, sizes, distances, repetitions=4):
        self.timer = QtCore.QTime()
        self.user_id = user_id
        self.sizes = sizes
        self.distances = distances
        self.repetitions = repetitions




    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)

    def debug(self, msg):
        sys.stderr.write(self.timestamp() + ": " + str(msg) + "\n")



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
            pass
        elif self.current_state == States.END:
            pass

        # self.drawBackground(event, qp)
        # self.drawText(event, qp)
        # self.drawTarget(event, qp)


        qp.end()

    def mouseMoveEvent(self, e):
        pass

    def mousePressEvent(self, e):
        pass

    def drawInstructions(self, event, qp):
        pass




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
        return config['user'], config['widths'], config['distances']
    else:
        print("Error: wrong file format.")

if __name__ == '__main__':
    main()
