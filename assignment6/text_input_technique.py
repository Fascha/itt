from PyQt5 import QtCore, QtGui, QtWidgets


class AutoComplete(QtWidgets.QCompleter):
    insertText = QtCore.pyqtSignal(str)

    def __init__(self):
        # super(AutoComplete, self).__init__()
        print("Auto complete initialized")

        words = ['Fabian', 'Florian', 'Farbius', 'Fisch']

        QtWidgets.QCompleter.__init__(self, words)
        self.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.highlighted.connect(self.setHighlighted)

    def setHighlighted(self, text):
        self.lastSelected = text

    def getSelected(self):
        return self.lastSelected





