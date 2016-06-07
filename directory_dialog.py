import sys
from PySide import QtGui
import sys, os

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class DialogGUIBox(QtGui.QWidget):

    def __init__(self, build_plot_display):
        super(DialogGUIBox, self).__init__()

        # Callback for bgsub plotting function
        self.build_plot_display = build_plot_display

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        # Folder Browser
        lbBroswer = QtGui.QLabel('Directory:', self)
        lbBroswer.move(15, 40)

        self.etBrowser = QtGui.QLineEdit('', self)
        self.etBrowser.resize(210,20)
        self.etBrowser.move(90, 37)
        self.etBrowser.setEnabled(0)
        self.etBrowser.isReadOnly = 0
        self.selected_directory = None

        btnBrowse = QtGui.QPushButton('Browse...', self)
        btnOpen = QtGui.QPushButton('Open', self)
        btnClose = QtGui.QPushButton('Close', self)
        btnBrowse.setToolTip('Select directory for project location.')
        btnBrowse.resize(70,20)
        btnBrowse.move(305, 37)
        btnOpen.resize(70, 20)
        btnOpen.move(305, 90)
        btnClose.resize(70, 20)
        btnClose.move(235, 90)

        # Connects the action of clicking the buttons to calling methods
        btnBrowse.clicked.connect(self.selectDirectory)
        btnOpen.clicked.connect(self.run_bgsub)
        btnClose.clicked.connect(self.close)

        self.setWindowTitle('Folder Utility')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def selectDirectory(self):
        selected_directory = QtGui.QFileDialog.getExistingDirectory(self)
        self.etBrowser.setText(selected_directory)
        self.selected_directory = str(selected_directory)

    def run_bgsub(self):
        self.close()
        self.build_plot_display(self.selected_directory)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = DialogGUIBox(None)
    sys.exit(app.exec_())