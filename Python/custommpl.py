# -*- coding: utf-8 -*-

from PyQt5.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

Ui_MainWindow, QMainWindow = loadUiType('untitled.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw() 
if __name__ == '__main__':
    import sys
    from PyQt5 import QtWidgets
    import numpy as np
    
    fig1 = Figure()
    ax1f1 = fig1.add_subplot(111)
    ax1f1.plot(np.random.rand(5))
    
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.addmpl(fig1)
    main.show()
    sys.exit(app.exec_())
    