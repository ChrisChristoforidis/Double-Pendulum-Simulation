from PyQt5.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from time import time
from pendulum import Pendulum
import numpy as np
from numpy import pi
import matplotlib.animation as animation

import sys
from PyQt5 import QtWidgets


Ui_MainWindow, QMainWindow = loadUiType('dpGUI.ui')


class DPSim(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(DPSim, self).__init__()
        # Setup the figure with the axes plots to be used for visualization
        self.setupUi(self)
        self.fig = Figure()
        self.k2 = 220
        self.k1 = 1000
        self.b1 = 50
        self.b2 = 20
        self.max_y = 0.1
        self.min_y = -0.1
        self.ax = self.fig.add_subplot(211, aspect='equal', autoscale_on=False,
                                       xlim=(-2.1, 2.1), ylim=(-0.2, 2.2))
        self.ax2 = self.fig.add_subplot(212)
        self.ax.set_axis_off()
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('$\phi$ (deg)')
        self.ax2.grid(linestyle='-', linewidth='0.5', color='black')
        line1, = self.ax.plot([], [], 'o-', lw=2)
        line2, = self.ax2.plot([], [])
        line3, = self.ax.plot([], [])
        self.ax.plot([-1.5,1.5],[0 ,0],color='black',linewidth='2')
        self.lines = [line1, line2, line3]
        self.time_text = self.ax.text(
            0.02, 0.90, '', transform=self.ax.transAxes)
        self.coef_text = self.ax.text(
            0.78, 0.55, '', transform=self.ax.transAxes)
        # Create the pendulum object which simulates the dynamics and gives states to be plotted.
        self.p1 = Pendulum(40, 60, 1, 0.5, 0.8, 0.15)
        self.p1.initSim(np.array([[0], [0], [0], [0]]))
        self.p1.setSDproperties(self.k1, self.k2, self.b1, self.b2)
        # Create the arrays that will hold the roll and time vectors
        self.xdata, self.ydata = [0], [0]
        self.step = 15000
        self.dt = 0.005
        self.duration = 0.3/self.dt
        self.magnitude = 300
        self.canvas = FigureCanvas(self.fig)  # create a canvas for the figure

        t0 = time()
        self.animate(0)
        t1 = time()
        interval = 1000 * self.dt - (t1 - t0)

        self.ani = animation.FuncAnimation(self.fig, self.animate, frames=300,
                                           interval=interval, blit=True, init_func=self.init)

        self.exitButton = QtWidgets.QPushButton('Quit')
        self.changeButton = QtWidgets.QPushButton('Change')
        self.impulseButton = QtWidgets.QPushButton('Impulse')
        self.resetButton = QtWidgets.QPushButton('Reset')
        self.stiffnessEdit = QtWidgets.QLineEdit('')
        self.btnLayout.addWidget(self.stiffnessEdit)
        self.btnLayout.addWidget(self.changeButton)
        self.btnLayout.addWidget(self.impulseButton)
        self.btnLayout.addWidget(self.resetButton)
        self.btnLayout.addWidget(self.exitButton)
        self.exitButton.clicked.connect(app.exit)
        self.changeButton.clicked.connect(self.changeStiffnessCallback)
        self.impulseButton.clicked.connect(self.impulseCallback)
        self.resetButton.clicked.connect(self.resetButtonCallback)
        self.exitButton.show()
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

    def init(self):
        """initialize animation"""
        self.lines[0].set_data([], [])
        self.lines[1].set_data([], [])
        self.lines[2].set_data([], [])
        self.time_text.set_text('')
        self.coef_text.set_text('')
        return self.lines[0], self.lines[1], self.lines[2], self.time_text, self.coef_text

    def animate(self, i):
        """perform animation step"""
        # input disturbance logic
        if(self.step < self.duration):
            self.step += 1
            if(self.step < np.floor(self.duration/2)):
                w = (self.magnitude*2/(self.duration*self.dt)) * \
                    (self.dt*self.step)
            else:
                w = -(self.magnitude*2/(self.duration*self.dt)) * \
                    (self.dt*self.step)+2*self.magnitude
        else:
            w = 0
            self.step = 15000

        self.p1.updateState(w, self.dt)
        self.ydata.append(self.p1.state[0]*180/pi)
        self.xdata.append(self.p1.t)
        if (len(self.xdata) > 30/self.dt):
            self.xdata.pop(0)
            self.ydata.pop(0)
        X, Y = self.p1.getPosition()
        self.lines[0].set_data(X, Y)
        self.lines[1].set_data(self.xdata, self.ydata)

        self.lines[2].set_xdata([X[1], X[1]+w/self.magnitude, X[1]+w /
                                 self.magnitude*0.9, X[1]+w/self.magnitude*0.9, X[1]+w/self.magnitude])
        self.lines[2].set_ydata(
            [Y[1], Y[1], Y[1]+w/self.magnitude*0.1, Y[1]-w/self.magnitude*0.1, Y[1]])

        self.ax2.set_xlim([self.xdata[0], self.p1.t])
#        if(self.ydata[-1] < self.min_y):
#            self.min_y = self.ydata[-1]
#        if(self.ydata[-1] > self.max_y):
#            self.max_y = self.ydata[-1]
        self.ax2.set_ylim([min(self.ydata)*1.2, max(self.ydata)*1.2])
        self.time_text.set_text('t = %.1f s' % self.p1.t)
        self.coef_text.set_text('$k_1$ = '+str(self.k1)+'\n $b_1$ = '+str(
            self.b1)+'\n $k_2$ = '+str(self.k2)+'\n $b_2$ = '+str(self.b2))
        return self.lines[0], self.lines[1], self.lines[2], self.time_text, self.coef_text

    def impulseCallback(self):
        self.step = 0

    def changeStiffnessCallback(self):
        if (self.stiffnessEdit.text()[0:3] == 'k1='):
            self.k1 = float(self.stiffnessEdit.text()[3:])
        elif (self.stiffnessEdit.text()[0:3] == 'k2='):
            self.k2 = float(self.stiffnessEdit.text()[3:])
        elif (self.stiffnessEdit.text()[0:3] == 'b1='):
            self.b1 = float(self.stiffnessEdit.text()[3:])
        elif (self.stiffnessEdit.text()[0:3] == 'b2='):
            self.b2 = float(self.stiffnessEdit.text()[3:])
        else:
            self.stiffnessEdit.setText('Malaka!')
        self.p1.setSDproperties(self.k1, self.k2, self.b1, self.b2)

    def resetButtonCallback(self):
        self.p1.initSim(np.array([[0], [0], [0], [0]]))
        self.k2 = 220
        self.k1 = 1000
        self.b1 = 50
        self.b2 = 20
        self.p1.setSDproperties(self.k1, self.k2, self.b1, self.b2)
        self.xdata.clear()
        self.ydata.clear()


app = QtWidgets.QApplication(sys.argv)
sim = DPSim()

sim.show()
app.exec_()
