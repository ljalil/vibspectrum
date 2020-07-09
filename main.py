from PyQt5 import QtGui, QtWidgets
import sys
from vibspectrum.toolbox import Bearing
from vibspectrum import signalmanager
from vibspectrum.signalprocessing import FourierAnalysis
from mainwindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
