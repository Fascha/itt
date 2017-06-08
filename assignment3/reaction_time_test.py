import csv
import os
import random
import sys
import datetime
from PyQt5 import QtGui, QtWidgets, QtCore
from collections import OrderedDict

"""
A = Attentive (Even/Odd)
P = Pre-Attentive (Red/Blue)

D = Distraction
N = No Distraction

B = Blue
R = Red

E = Even
O = Odd

5xADB f
5xADR j

5xANB f
5xANR j

5xPDE f
5xPDO j

5xPNE f
5xPNO j

ADE
ADO

ANE
ANO

PDB
PDR

PNB
PNR
"""


class ReactionTimeExperiment(QtWidgets.QWidget):

    WIDTH = 960
    HEIGHT = 960
    CIRCLE_RADIUS = 100
    NUM_SQUARES = 10
    SQUARE_WIDTH = WIDTH / NUM_SQUARES
    SQUARE_HEIGHT = HEIGHT / NUM_SQUARES
    BLINK_SPEED = 1000

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initConfig()

        self.current_task = -1

        """
        possible states:
        'Start'
        'Pause'
        'Trial'
        'End'
        """
        self.current_state = 'Start'

        self.tasks = {'ADE': self.taskADE,
                      'ADO': self.taskADO,
                      'ANE': self.taskANE,
                      'ANO': self.taskANO,
                      'PDB': self.taskPDB,
                      'PDR': self.taskPDR,
                      'PNB': self.taskPNB,
                      'PNR': self.taskPNR}

        self.counter = 0
        self.current_trial = None
        # timer for automated blinking while distraction is on
        self.timer_draw = QtCore.QTimer(self)
        self.timer_draw.timeout.connect(self.drawDistraction)
        self.timer_draw.start(self.BLINK_SPEED)

        self.log_written_to_file = False
        self.logging_list = []

    def initUI(self):
        # setGeometry(int posx, int posy, int w, int h)
        self.setGeometry(480, 480, self.WIDTH, self.HEIGHT)
        self.setWindowTitle('Reaction Time Experiment')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()

    def initConfig(self):
        # reading settings from config file
        with open(sys.argv[1]) as config_file:
            for line in config_file:
                if line.startswith('PARTICIPANT'):
                    print(line)
                    self.participant_id = line.split(" ")[1].rstrip()
                elif line.startswith('TRIALS'):
                    print(line)
                    self.trials = line.split('[')[1][:-2].replace(" ", "").replace("'", "").split(",")

    def drawDistraction(self):
        print(self.current_state)
        self.update()

    def drawPauseScreen(self, event, qp):
        self.current_state = 'Pause'

        qp.setFont(QtGui.QFont('Helvetica', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "PAUSE\n\nPRESS 'SPACE' TO SHOW NEXT STIMULUS!")
        self.update()

    def drawStartScreen(self, event, qp):
        self.current_state = 'Start'

        qp.setFont(QtGui.QFont('Helvetica', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "REACTION TIME TEST\n\n\n\n\n\n")
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "\n\n\n\n\n\n\n Press 'SPACE' to start the test!")

        qp.setFont(QtGui.QFont('Helvetica', 16))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter,
                    "In the following test you will see 40 Stimuli\n"
                    "If you see a BLUE CIRCLE or an EVEN NUMBER you have to press 'F'\n"
                    "If you see a RED CIRCLE or an ODD NUMBER you have to press 'J'")
        self.update()

    def drawEndScreen(self, event, qp):
        self.current_state = 'End'

        qp.setFont(QtGui.QFont('Helvetica', 32))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "THANK YOU FOR PARTICIPATING!")
        self.update()

    def startNextTask(self):
        print("start next task")
        self.current_task += 1

        # checking if there are tasks left
        if self.current_task < len(self.trials):
            self.current_state = 'Trial'

            self.current_trial = self.trials[self.current_task]
            # getting timestamp for task start
            self.task_start_time = datetime.datetime.now()
            print(self.current_trial)
        else:
            self.current_state = 'End'

        # getting a random even or odd 3-digit number
        if self.current_trial[2] == 'E':
            self.current_number = str(random.choice(range(100, 1000, 2)))
        elif self.current_trial[2] == 'O':
            self.current_number = str(random.choice(range(101, 1000, 2)))
        self.update()

    def taskADE(self, event, qp):
        qp.setFont(QtGui.QFont('Helvetica', 48))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.current_number)
        self.update()

    def taskADO(self, event, qp):
        qp.setFont(QtGui.QFont('Helvetica', 48))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.current_number)
        self.update()

    def taskANE(self, event, qp):
        qp.setFont(QtGui.QFont('Helvetica', 48))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.current_number)
        self.update()

    def taskANO(self, event, qp):
        qp.setFont(QtGui.QFont('Helvetica', 48))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.current_number)
        self.update()

    def taskPDB(self, event, qp):
        qp.setBrush(QtGui.QColor(0, 0, 255))
        qp.drawEllipse(self.WIDTH / 2 - self.CIRCLE_RADIUS, self.HEIGHT / 2 - self.CIRCLE_RADIUS,
                       self.CIRCLE_RADIUS * 2, self.CIRCLE_RADIUS * 2)
        self.update()

    def taskPDR(self, event, qp):
        qp.setBrush(QtGui.QColor(255, 0, 0))
        qp.drawEllipse(self.WIDTH / 2 - self.CIRCLE_RADIUS, self.HEIGHT / 2 - self.CIRCLE_RADIUS,
                       self.CIRCLE_RADIUS * 2, self.CIRCLE_RADIUS * 2)
        self.update()

    def taskPNB(self, event, qp):
        qp.setBrush(QtGui.QColor(0, 0, 255))
        qp.drawEllipse(self.WIDTH / 2 - self.CIRCLE_RADIUS, self.HEIGHT / 2 - self.CIRCLE_RADIUS,
                       self.CIRCLE_RADIUS * 2, self.CIRCLE_RADIUS * 2)
        self.update()

    def taskPNR(self, event, qp):
        qp.setBrush(QtGui.QColor(255, 0, 0))
        qp.drawEllipse(self.WIDTH / 2 - self.CIRCLE_RADIUS, self.HEIGHT / 2 - self.CIRCLE_RADIUS,
                       self.CIRCLE_RADIUS * 2, self.CIRCLE_RADIUS * 2)
        self.update()

    def handleInput(self, key):
        # getting timestamp for end of task
        self.task_end_time = datetime.datetime.now()
        self.current_state = 'Pause'
        self.update()

        # calculation the time needed
        self.timedelta = self.task_end_time - self.task_start_time

        logging_dict = OrderedDict([
            ('id', self.participant_id),
            ('shown_stimulus', self.current_trial[2]),
            ('mental_complexity', self.current_trial[0]),
            ('distraction', 'yes' if self.current_trial[1] == 'D' else 'no'),
            ('pressed_key', key),
            ('correct_key_pressed', None),
            ('reaction_time_in_microseconds', (self.timedelta.seconds * 1000000 + self.timedelta.microseconds)),
            ('timestamp', int(self.task_end_time.timestamp()))
        ])

        # deciding wheter the correct key was pressed or not
        if self.current_trial in ['ADE', 'ANE', 'PDB', 'PNB'] and key == QtCore.Qt.Key_F:
            logging_dict['correct_key_pressed'] = 'true'
        elif self.current_trial in ['ADO', 'ANO', 'PDR', 'PNR'] and key == QtCore.Qt.Key_J:
            logging_dict['correct_key_pressed'] = 'true'
        else:
            logging_dict['correct_key_pressed'] = 'false'

        self.logging_list.append(logging_dict)

        print("appended to list")

    def writeLogToFile(self):
        filepath_total = 'reaction_time_results.csv'
        filepath = 'reaction_time_result_' + str(self.participant_id) + '.csv'

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

        self.log_written_to_file = True

    def keyPressEvent(self, event):
        if self.current_state == 'Start':
            if event.key() == QtCore.Qt.Key_Space:
                self.current_state = 'Pause'
        elif self.current_state == 'Pause':
            if event.key() == QtCore.Qt.Key_Space:
                self.startNextTask()
        elif self.current_state == 'Trial':
            if event.key() == QtCore.Qt.Key_F:
                self.handleInput(QtCore.Qt.Key_F)
            elif event.key() == QtCore.Qt.Key_J:
                self.handleInput(QtCore.Qt.Key_J)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)

        if self.current_state == 'Start':
            self.drawStartScreen(event, qp)
        elif self.current_state == 'End':
            self.drawEndScreen(event, qp)
        elif self.current_state == 'Pause':
            self.drawPauseScreen(event, qp)
        elif self.current_state == 'Trial':
            # checking if distraction should be drawn or not
            if 'D' in self.current_trial:
                for x in range(self.NUM_SQUARES):
                    for y in range(self.NUM_SQUARES):
                        qp.setBrush(
                            QtGui.QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                        self.rect = QtCore.QRect(x * self.SQUARE_WIDTH, y * self.SQUARE_HEIGHT, self.SQUARE_WIDTH,
                                                 self.SQUARE_HEIGHT)
                        # if not (y > 2 and y < 7):
                        qp.drawRect(self.rect)

            self.tasks[self.current_trial](event, qp)

        qp.end()

    def closeEvent(self, event):
        # checking if log was already written when you close the pyqt app
        if not self.log_written_to_file and self.current_task > 0:
            self.writeLogToFile()


def main():
    app = QtWidgets.QApplication(sys.argv)
    experiment = ReactionTimeExperiment()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
