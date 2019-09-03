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


global p1
p1 = Pendulum(1, 1, 1, 1, 0.5, 0.5)
p1.initSim(np.array([[pi/2], [pi/2], [0], [0]]))
p1.setSDproperties(3000, 10, 100, 10)

xdata, ydata = [0], [0]
global step
step=0
dt = 0.005
duration=0.3/dt
magnitude=300

def init():
    """initialize animation"""
    lines[0].set_data([], [])
    lines[1].set_data([], [])
    time_text.set_text('')
    return lines[0], lines[1], time_text

def animate(i):
    """perform animation step"""
#    if(step<duration):
#        step+=1;
#        if( step<np.floor( duration/2)):
#            w=(magnitude*2/(duration*dt))*(dt*step)
#        else:
#            w=-(magnitude*2/(duration*dt))*(dt*step)+2*magnitude
#    else:
#        w=0
#        step=15000
  
    p1.getNextState(0, dt)
    ydata.append(p1.state[0]*180/pi)
    xdata.append(p1.t)
    if (len(xdata) > 10/dt):
        xdata.pop(0)
        ydata.pop(0)
    lines[0].set_data(*p1.getPosition())
    lines[1].set_data(xdata, ydata)
    ax2.set_xlim([xdata[0], p1.t])
    ax2.set_ylim([min(ydata), max(ydata)])
    time_text.set_text('time = %.1f' % p1.t)
    return lines[0], lines[1], time_text


fig = Figure()
ax = fig.add_subplot(121, aspect='equal', autoscale_on=False,
                     xlim=(-2.1, 2.1), ylim=(-2.2, 2.2))
ax2 = fig.add_subplot(122)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('$\phi$ (deg)')

line, = ax.plot([], [], 'o-', lw=2)
line2, = ax2.plot([], [])
lines = [line, line2]
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

Ui_MainWindow, QMainWindow = loadUiType('untitled.ui')
t0 = time()
i = 0
animate(i)
t1 = time()
interval = 1000 * dt - (t1 - t0)

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None):
        global fig
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.ani = animation.FuncAnimation(fig, animate, frames=300,
                              interval=interval, blit=True, init_func=init)
        
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw() 
        

    
    
    
app = QtWidgets.QApplication(sys.argv)
main = Main()       
main.addmpl(fig)
main.show()
sys.exit(app.exec_())
    
  
    

