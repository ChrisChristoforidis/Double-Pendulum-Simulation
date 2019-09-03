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
        self.fig=Figure()
        self.stiffness=100
        ax = self.fig.add_subplot(121, aspect='equal', autoscale_on=False,
                     xlim=(-2.1, 2.1), ylim=(-2.2, 2.2))
        self.ax2 = self.fig.add_subplot(122)
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('$\phi$ (deg)')
        
        line1, = ax.plot([], [], 'o-', lw=2)
        line2, = self.ax2.plot([], [])
        self.lines = [line1, line2]
        self.time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
        #Create the pendulum object which simulates the dynamics and gives states to be plotted.
        self.p1 = Pendulum(20, 80, 1, 0.5, 0.5, 0.5)
        self.p1.initSim(np.array([[0], [0], [0], [0]]))
        self.p1.setSDproperties(3000,50,100, 10)
        # Create the arrays that will hold the roll and time vectors
        self.xdata, self.ydata = [0], [0]
        self.step=15000
        self.dt = 0.005
        self.duration=0.3/self.dt
        self.magnitude=300
        self.canvas = FigureCanvas(self.fig) # create a canvas for the figure
        
        t0 = time()
        self.animate(0)
        t1 = time()
        interval = 1000 * self.dt - (t1 - t0)

        self.ani = animation.FuncAnimation(self.fig, self.animate, frames=300,
                              interval=interval, blit=True, init_func=self.init)
        
        self.exitButton = QtWidgets.QPushButton('Quit')
        self.impulseButton = QtWidgets.QPushButton('Impulse')
        self.stiffnessEdit = QtWidgets.QLineEdit(str(self.stiffness))
        self.btnLayout.addWidget(self.stiffnessEdit)
        self.btnLayout.addWidget(self.exitButton)
        self.btnLayout.addWidget(self.impulseButton)
        self.exitButton.clicked.connect(app.exit)
        #self.p1.setSDproperties(3000,float(self.stiffnessEdit.text()),10,10)
        self.impulseButton.clicked.connect(self.impulseCallback)
        self.exitButton.show()
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw() 
        
    def init(self):
        """initialize animation"""
        self.lines[0].set_data([], [])
        self.lines[1].set_data([], [])
        self.time_text.set_text('')
        return self.lines[0], self.lines[1], self.time_text        
    
    def animate(self,i):
        """perform animation step"""
        if(self.step<self.duration):
            self.step+=1;
            if( self.step<np.floor( self.duration/2)):
                w=(self.magnitude*2/(self.duration*self.dt))*(self.dt*self.step)
            else:
                w=-(self.magnitude*2/(self.duration*self.dt))*(self.dt*self.step)+2*self.magnitude
        else:
            w=0
            self.step=15000
      
        self.p1.getNextState(w, self.dt)
        self.ydata.append(self.p1.state[0]*180/pi)
        self.xdata.append(self.p1.t)
        if (len(self.xdata) > 10/self.dt):
            self.xdata.pop(0)
            self.ydata.pop(0)
        self.lines[0].set_data(*self.p1.getPosition())
        self.lines[1].set_data(self.xdata, self.ydata)
        self.ax2.set_xlim([self.xdata[0], self.p1.t])
        self.ax2.set_ylim([min(self.ydata), max(self.ydata)])
        self.time_text.set_text('time = %.1f' % self.p1.t)
        return self.lines[0], self.lines[1], self.time_text    
    def impulseCallback(self):
        self.step=0
    
app = QtWidgets.QApplication(sys.argv)
sim = DPSim()

sim.show()
app.exec_()    
  
    

