import sys
from PyQt5 import Qt, QtGui, QtCore, QtWidgets

"""

6.2: Design an implement a tool for measuring text entry speed
Implement a tool that allows for measuring and logging typing speed (i.e., a window with an editable textbox).
• download the example file textedit.py and adjust it.
• test data should be logged to stdout (not to a file) in CSV format (see http://www.cse.yorku.ca/~stevenc/tema/ for best
practices of logging such data).
• the application should measure how long it takes to write a sentence (delimited at the end with a newline) and each individual
word. Find out how to best define beginning/end of word/sentence (and when to start/stop measuring the time).
• you do not need to log typing errors for this assignment
• log appropriate data for the following events (indicate which event you are logging as the first field in the log data):
– key pressed
– word typed
– sentence typed
– test finished (all sentences typed)
• informally test whether your tool works as expected
Hand in the following file:
text_entry_speed_test.py: a Python/PyQt script implementing a typing speed test.
Points
• 2 Script conforms to PEP8, is well structured and includes comments
• 2 Script works as expected
• 2 Script outputs sensible and valid CSV data

"""


"""

Entry speed metric: Entry speed is calculated by
dividing the length of the transcribed text by the entry
time (in seconds), multiplying by sixty (seconds in a
minute), and dividing by five (the accepted word
length, including spaces [11]). Thus, the result is
reported in words-per-minute (wpm).



Entry speed metric: Entry speed is calculated by dividing the length of the transcribed text by the
entry time (in seconds), multiplying by sixty (seconds in a minute), and dividing by five (the accepted
word length, including spaces (Yamada 1980)). Thus, the result is reported in words-per-minute (wpm).

"""



"""
TODO:

- the application should measure how long it takes to write a sentence (delimited at the end with a newline)
- and each individual word.




present sentence
when space pressed check if word matches
when enter pressed check if sentence matches


"""


class Test(QtWidgets.QWidget):

    def __init__(self):
        super(Test, self).__init__()

        WIDTH = 800
        HEIGHT = 800

        vlayout = QtWidgets.QVBoxLayout()

        sentence_display = QtWidgets.QLabel("TEST SATZ ETC")
        # sentence_display.setText("This is Sentence 1")

        vlayout.addWidget(sentence_display)

        text_edit = TextEdit()
        vlayout.addWidget(text_edit)

        self.setLayout(vlayout)

        self.setGeometry(300, 300, WIDTH, HEIGHT)
        self.setWindowTitle('Text Entry Test')
        self.show()


class TextEdit(QtWidgets.QTextEdit):

    def __init__(self):
        super(TextEdit, self).__init__()

        self.example = 'Text Edit Sample Text'
        self.setText(self.example)

        self.timer = QtCore.QTime()

        # self.initUI()

    def initUI(self):
        self.setGeometry(1200, 300, 800, 800)
        # self.setWindowTitle('TextLogger')
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.setMouseTracking(True)
        # self.show()

    def keyPressEvent(self, ev):
        super(TextEdit, self).keyPressEvent(ev)
        if ev.key() == QtCore.Qt.Key_Return:
            self.log('pressed,enter')
        elif ev.key() == QtCore.Qt.Key_Space:
            self.log('pressed,space')
        else:
            self.log('pressed,' + ev.text())


    def keyReleaseEvent(self, ev):
        super(TextEdit, self).keyReleaseEvent(ev)
        if ev.key() == QtCore.Qt.Key_Return:
            self.log('released,enter')
        elif ev.key() == QtCore.Qt.Key_Space:
            self.log('released,space')
        else:
            self.log('released,' + ev.text())

    def log(self, event):
        print('{}, {}'.format(event, self.timestamp()))

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)


def main():
    app = QtWidgets.QApplication(sys.argv)
    # text_edit = TextEdit()
    # chord_input = ChordInputMethod()
    # text_logger.installEventFilter(chord_input)

    test = Test()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
