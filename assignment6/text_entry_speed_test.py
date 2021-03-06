import sys
from PyQt5 import Qt, QtGui, QtCore, QtWidgets
from text_input_technique import AutoComplete
import os

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
        # staring with first sentence
        self.next_sentence()

    def initUI(self):
        self.setGeometry(300, 300, self.WIDTH, self.HEIGHT)
        self.setWindowTitle('Text Entry Test')

        # initializing layout
        self.vlayout = QtWidgets.QVBoxLayout()
        # setting layout of widget
        self.setLayout(self.vlayout)

        # adding widgets to the layout
        self.vlayout.addWidget(self.sentence_display)
        self.vlayout.addWidget(self.text_edit)
        self.show()

    def read_sentences_from_file(self):
        """
        reading sentences from file
        """
        sentences = []
        try:
            filepath = 'phrases2.txt'
            with open(filepath, 'r') as f:
                for line in f:
                    sentences.append(line.strip())
        except IOError:
            sys.stderr.write('File with sentences not found!')
            sys.exit()

        return sentences[:8]

    def next_sentence(self):
        """
        increasing current task number
        setting up all necessary variables
        setting display and cleaning the textedit
        """
        self.current_task_number += 1
        if self.current_task_number < len(self.sentences):
            next_sentence = self.sentences[self.current_task_number]
            self.text_length += len(next_sentence)
            self.text_edit.set_current_sentence(next_sentence)
            self.sentence_display.setText(next_sentence)
        else:
            wpm = self.calculate_wpm()
            self.text_edit.setText('Your Statistics:\nWPM: {}'.format(wpm))
            self.sentence_display.setText('Test finished! Thank You for participating!')
            self.text_edit.log('test_finished', wpm)

    def set_id(self, id):
        self.text_edit.set_id(id)

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
        # connecting method
        self.completer.insertText.connect(self.insertCompletion)

    def set_id(self, id):
        self.id = id

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
            self.completer.setWidget(self)
        QtWidgets.QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, ev):
        if self.completer:  # checking if autocompletion is turned on
            tc = self.textCursor()
            # checking if tab or return is pressed while the popup is visible
            if (ev.key() == QtCore.Qt.Key_Tab or ev.key() == QtCore.Qt.Key_Return) \
                    and self.completer.popup().isVisible():
                self.completer.insertText.emit(self.completer.getSelected())
                self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
                self.log('auto_completion', event_value=self.completer.getSelected())
                return

            if ev.key() is not QtCore.Qt.Key_Return:
                super(TextEdit, self).keyPressEvent(ev)

            tc.select(QtGui.QTextCursor.WordUnderCursor)
            cr = self.cursorRect()
            # checking if somthing is written
            if len(tc.selectedText()) > 0:
                self.completer.setCompletionPrefix(tc.selectedText())
                popup = self.completer.popup()
                popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

                cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                            + self.completer.popup().verticalScrollBar().sizeHint().width())
                self.completer.complete(cr)
            else:
                self.key_logging(ev)
                self.completer.popup().hide()
        else:
            super(TextEdit, self).keyPressEvent(ev)
            self.key_logging(ev)

        # starting timers if they are not running
        if not self.test.sentence_timer_running:
            self.test.start_sentence_timer()
        if not self.test.word_timer_running:
            self.test.start_word_timer()

    # logging
    def key_logging(self, ev):
        if ev.key() == QtCore.Qt.Key_Return:
            self.log('key_pressed', event_value='enter')
            self.check_word()
            self.check_sentence()
        elif ev.key() == QtCore.Qt.Key_Tab:
            self.log('key_pressed', event_value='tab')
        elif ev.key() == QtCore.Qt.Key_Space:
            self.log('key_pressed', event_value='space')
            self.check_word()
        else:
            self.log('key_pressed', event_value=ev.text())

    def keyReleaseEvent(self, ev):
        super(TextEdit, self).keyReleaseEvent(ev)
        if ev.key() == QtCore.Qt.Key_Return:
            self.log('key_released', event_value='enter')
        elif ev.key() == QtCore.Qt.Key_Tab:
            self.log('key_pressed', event_value='tab')
        elif ev.key() == QtCore.Qt.Key_Space:
            self.log('key_released', event_value='space')
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
        if self.toPlainText().lower().strip() == self.current_sentence:
            sentence_correct = True
        else:
            sentence_correct = False

        if len(self.toPlainText().strip()) == len(self.current_sentence):
            self.log('sentence_complete', event_value=sentence_correct, timeontask=self.test.stop_sentence_timer())
        else:
            self.log('sentence_incomplete', event_value=sentence_correct, timeontask=self.test.stop_sentence_timer())
        if self.completer:
            if not self.completer.popup().isVisible():
                self.test.next_sentence()
        else:
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

        if self.completer:
            c = 'on'
        else:
            c = 'off'
        filepath = 'text_entry_speed_test_log_{}_{}.csv'.format(self.id, c)
        # checking if file with all experiments exists
        log_file_exists = os.path.isfile(filepath)

        # appending to the concatenated file
        with open(filepath, 'a') as f:
            if not log_file_exists:
                f.write('event,event_value,timestamp,timeontask\n')
            f.write('{},{},{},{}\n'.format(event, event_value, self.timestamp(), timeontask))

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)


def main():
    auto_complete = False
    # checking if autocompleting is turned on via commandline parameter
    if len(sys.argv) > 1 and sys.argv[1] == 'on':
        auto_complete = True

    if len(sys.argv) > 2:
        id = sys.argv[2]
    else:
        sys.stderr.write("Usage: {} <on/off> <id>\n".format(sys.argv[0]))
        sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    test = Test()
    test.set_id(id)

    if auto_complete:
        ac = AutoComplete()
        test.set_completer(ac)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
