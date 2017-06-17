import sys
from PyQt5 import Qt, QtGui, QtCore, QtWidgets
from text_input_technique import AutoComplete

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

- keyrelease not working when completer is on
- read and parse 5000 msot common words list

- add space when autocompleting?

- think about when a word is finished
    currently hitting "space"
    maybe if len(current_typed_word) == len(word) ??


"""

"""
completer ressource
http://rowinggolfer.blogspot.de/2010/08/qtextedit-with-autocompletion-using.html

https://stackoverflow.com/questions/28956693/pyqt5-qtextedit-auto-completion


"""



class Test(QtWidgets.QWidget):
    WIDTH = 800
    HEIGHT = 800
    def __init__(self):
        super(Test, self).__init__()

        # self.sentences = ['fabian', 'This is Sentence 1', 'HEre is the second example sentence', ' And the third one']
        self.sentences = ['Fabian Schatz', 'This is Sentence 1']

        self.sentences = self.read_sentences_from_file()

        self.word_timer = QtCore.QTime()
        self.word_timer_running = False

        self.sentence_timer = QtCore.QTime()
        self.sentence_timer_running = False

        self.test_time = 0
        self.text_length = 0

        self.current_task_number = -1
        self.text_edit = TextEdit()


        self.text_edit.set_reference(self)
        self.sentence_display = QtWidgets.QLabel()
        self.initUI()
        self.next_sentence()

    def initUI(self):
        self.setGeometry(300, 300, self.WIDTH, self.HEIGHT)
        self.setWindowTitle('Text Entry Test')

        self.vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.vlayout)

        self.vlayout.addWidget(self.sentence_display)
        self.vlayout.addWidget(self.text_edit)
        self.show()

    def read_sentences_from_file(self):
        sentences = []
        try:
            filepath = 'phrases2.txt'
            with open(filepath, 'r') as f:
                for line in f:
                    sentences.append(line.strip())
        except IOError:
            sys.stderr.write('File with sentences not found!')
            sys.exit(1)

        return sentences

    def next_sentence(self):
        self.current_task_number += 1
        if self.current_task_number < len(self.sentences):
            next_sentence = self.sentences[self.current_task_number]
            self.text_length += len(next_sentence)
            self.text_edit.set_current_sentence(next_sentence)
            self.sentence_display.setText(next_sentence)
        else:
            self.text_edit.setText('Your Statistics:\nWPM: {}'.format(self.calculate_wpm()))
            self.sentence_display.setText('Test finished! Thank You for participating!')

            self.text_edit.log('test_finished,None')

    def set_completer(self, completer):
        self.text_edit.set_completer(completer)

    def start_word_timer(self):
        if not self.word_timer_running:
            self.word_timer_running = True
            self.word_timer.start()

    def stop_word_timer(self):
        if self.word_timer_running:
            self.word_timer_running = False
            return self.word_timer.elapsed()

    def start_sentence_timer(self):
        if not self.sentence_timer_running:
            self.sentence_timer_running = True
            self.sentence_timer.start()

    def stop_sentence_timer(self):
        if self.sentence_timer_running:
            self.sentence_timer_running = False
            time = self.sentence_timer.elapsed()
            self.test_time += time
            return time

    def calculate_wpm(self):
        """
        Entry speed metric: Entry speed is calculated by dividing the length of the transcribed text by the
        entry time (in seconds), multiplying by sixty (seconds in a minute), and dividing by five (the accepted
        word length, including spaces (Yamada 1980)). Thus, the result is reported in words-per-minute (wpm).

        currently the time between the sentences is not measured!
        we could you a third timer or display all sentences at once instead of one at a time
        """
        return (self.text_length / (self.test_time / 1000.0)) * 60.0 / 5.0


class TextEdit(QtWidgets.QTextEdit):

    def __init__(self):
        super(TextEdit, self).__init__()
        # self.example = 'Text Edit Sample Text'
        # self.setText(self.example)
        self.current_word = ''
        self.current_sentence = ''
        self.completer = None

    def set_completer(self, completer):
        if self.completer:
            self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return

        completer.setWidget(self)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.completer = completer
        self.completer.insertText.connect(self.insertCompletion)



    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) - len(self.completer.completionPrefix()))
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
        self.completer.popup().hide()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtWidgets.QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, ev):
        if self.completer:
            tc = self.textCursor()

            if ev.key() == QtCore.Qt.Key_Tab and self.completer.popup().isVisible():
                self.completer.insertText.emit(self.completer.getSelected())
                self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
                self.log('auto_completion', event_value=self.completer.getSelected())
                return

            super(TextEdit, self).keyPressEvent(ev)

            tc.select(QtGui.QTextCursor.WordUnderCursor)
            cr = self.cursorRect()

            if len(tc.selectedText()) > 0:
                self.completer.setCompletionPrefix(tc.selectedText())
                popup = self.completer.popup()
                popup.setCurrentIndex(self.completer.completionModel().index(0,0))

                cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                            + self.completer.popup().verticalScrollBar().sizeHint().width())
                self.completer.complete(cr)
            else:
                self.completer.popup().hide()
        else:
            super(TextEdit, self).keyPressEvent(ev)

        if not self.test.sentence_timer_running:
            self.test.start_sentence_timer()
        if not self.test.word_timer_running:
            self.test.start_word_timer()

        if ev.key() == QtCore.Qt.Key_Return:
            self.log('key_pressed', event_value='enter')
        elif ev.key() == QtCore.Qt.Key_Tab:
            self.log('key_pressed', event_value='tab')
        elif ev.key() == QtCore.Qt.Key_Space:
            self.log('key_pressed', event_value='space')
        else:
            self.log('key_pressed', event_value=ev.text())

    def keyReleaseEvent(self, ev):
        super(TextEdit, self).keyReleaseEvent(ev)
        if ev.key() == QtCore.Qt.Key_Return:
            self.log('key_released', event_value='enter')
            self.check_word()
            self.check_sentence()
        elif ev.key() == QtCore.Qt.Key_Tab:
            self.log('key_pressed', event_value='tab')
        elif ev.key() == QtCore.Qt.Key_Space:
            self.log('key_released', event_value='space')
            self.check_word()
        else:
            self.log('key_released', event_value=ev.text())

    def check_word(self):
        last_word = self.toPlainText().lower().split(' ')
        if len(last_word) > 1:
            last_word = last_word[-2]
        else:
            last_word = last_word[-1]

        if last_word == self.current_word:
            word_correct = True
        else:
            word_correct = False

        self.log('word_complete', event_value=word_correct, timeontask=self.test.stop_word_timer())

    def check_sentence(self):
        # print(self.toPlainText().lower().strip())
        if self.toPlainText().lower().strip() == self.current_sentence:
            sentence_correct = True
        else:
            sentence_correct = False

        self.log('sentence_complete', event_value=sentence_correct, timeontask=self.test.stop_sentence_timer())
        self.test.next_sentence()

    def set_reference(self, test):
        self.test = test

    def set_current_word(self, word):
        self.current_word = str(word).lower()

    def set_current_sentence(self, sentence):
        self.setText('')
        self.current_sentence = str(sentence).lower()
        self.set_current_word(str(sentence).lower().split(' ')[0])

    def log(self, event, event_value=None, timeontask=None):
        print('{}, {}, {}, {}'.format(event, event_value, self.timestamp(), timeontask))

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)


def main():
    auto_complete = False
    if len(sys.argv) > 1 and sys.argv[1] == 'on':
        auto_complete = True

    app = QtWidgets.QApplication(sys.argv)
    test = Test()

    if auto_complete:
        ac = AutoComplete()
        test.set_completer(ac)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
