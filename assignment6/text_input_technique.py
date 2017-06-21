from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class AutoComplete(QtWidgets.QCompleter):
    insertText = QtCore.pyqtSignal(str)

    def __init__(self):
        words = self.setup_wordlist()

        QtWidgets.QCompleter.__init__(self, words)
        self.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.highlighted.connect(self.setHighlighted)

    def setHighlighted(self, text):
        self.lastSelected = text

    def getSelected(self):
        return self.lastSelected

    def setup_wordlist(self):
        words = []
        # filepath = 'word_list_gt1.txt'
        filepath = 'word_list_gt2'
        # filepath = 'word_list_gt3.txt'
        # filepath = 'word_list_gt4.txt'
        # filepath = 'phrases2.txt'
        try:

            with open(filepath, 'r') as f:
                for line in f:
                    for word in line.split(' '):
                        words.append(word.strip())
            return list(set(words))
        except IOError:
            sys.stderr.write('File with wordlist not found!')

        return ['']
