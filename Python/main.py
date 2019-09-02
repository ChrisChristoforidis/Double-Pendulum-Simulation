import numpy as np
from numpy import pi
from sympy import sin
from sympy import cos
import sympy as sym
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class Pendulum:
    def __init__(self, m1, m2, L1, L2, a, b):
        self.m1 = m1
        self.m2 = m2
        self.a = a
        self.b = b
        self.L1 = L1
        self.L2 = L2
        self.Gains = np.array([0, 0, 0, 0])
        self.dX = self.getEOM()
        self.state=np.array([[0],[0],[0],[0]])
    def setSDproperties(self, k1, k2, b1, b2):
        # Set the spring and damper properties of the lower and upper spring damper system
        # 1 denotes the properties of the spring damper connected to the ground hinge joint
        # 2 denotes the properties of the spring damper between rods.
        self.Gains = np.array([k1, b1, k2, b2])

    def getEOM(self):
        # Gets the function handle to be used for numerical integration.
        #  The EOM are derived using the TMT method.
        phi1, phi2 = sym.var('phi1,phi2', real=True)
        dphi1, dphi2 = sym.var('dphi1,dphi2', real=True)
        k1, k2, b1, b2 = sym.var('k1,k2,b1,b2', real=True)
        X1, X2, X3, X4 = sym.var('X1,X2,X3,X4', real=True)
        t = sym.var('t', real=True)
        Fx = sym.var('Fx', real=True)

        g = 9.81
        q = sym.Matrix([phi1, phi2])
        dq = sym.Matrix([dphi1, dphi2])

        x1 = (self.a*self.L1)*sin(phi1)
        y1 = (self.a*self.L1)*cos(phi1)
        x2 = (self.L1)*sin(phi1)+(self.b*self.L2)*sin(phi2)
        y2 = (self.L1)*cos(phi1)+(self.b*self.L2)*cos(phi2)
        x3 = (self.L1)*sin(phi1)
        y3 = (self.L1)*cos(phi1)

        x = sym.Matrix([x1, y1, phi1, x2, y2, phi2, x3, y3])
        T = x.jacobian(q)
        G = (T*dq).jacobian(q)*dq

        I1 = (self.m1*(self.L1**2))/12
        I2 = (self.m2*(self.L2**2))/12

        M = sym.diag(self.m1, self.m1, I1, self.m2, self.m2, I2, 0, 0)
        F = sym.Matrix([0, -self.m1*g, -b1*dphi1-k1*(phi1), 0, -
                        self.m2*g, -b2*(dphi2-dphi1)-k2*(phi2-phi1), Fx, 0])

        M_bar = T.T*M*T

        Q_bar = T.T*(F-M*G)
        gen_acc = M_bar.inv()*Q_bar

        X = sym.Matrix([X1, X2, X3, X4])
        gen_acc = gen_acc.subs({phi1: X1, phi2: X2, dphi1: X3, dphi2: X4})
        dX = gen_acc.row_insert(0, sym.Matrix([X3, X4]))
        Gains = sym.Matrix([k1, b1, k2, b2])
        f = sym.lambdify([t, X, Fx, Gains], dX)
        return f

    def initSim(self, X0):
        # Initialize simulation with initial state X0 and t=0
        self.state = X0
        self.t = 0

    def getNextState(self, w, dt):
        k1 = self.dX(self.t, self.state, w, self.Gains).reshape((4, 1))
        k2 = self.dX(self.t, self.state+(k1*dt)/2, w, self.Gains).reshape((4, 1))
        k3 = self.dX(self.t+(dt/2), self.state+(k2*dt)/2, w, self.Gains).reshape((4, 1))
        k4 = self.dX(self.t+(dt), self.state+(k3*dt), w, self.Gains).reshape((4, 1))
        self.state = self.state+(dt/6)*(k1+(2*k2)+(2*k3)+k4)
        self.t += dt
        return self.state
    def getPosition(self):
        x1=np.sin(self.state[0])*self.L1
        y1=np.cos(self.state[0])*self.L1
        x2=np.sin(self.state[1])*self.L2+np.sin(self.state[0])*self.L1;
        y2=np.cos(self.state[1])*self.L2+np.cos(self.state[0])*self.L1;
        x=np.array([0 ,np.asscalar(x1) ,np.asscalar(x2)])
        y=np.array([0, np.asscalar(y1), np.asscalar(y2)])
        return (x,y)





fig = plt.figure()
grid = plt.GridSpec(1,2, wspace=0.4, hspace=0.3)
ax = fig.add_subplot(grid[0,0], aspect='equal', autoscale_on=False,
                     xlim=(-2.1, 2.1), ylim=(-2.2, 2.2))
ax2 = fig.add_subplot(grid[0,1:])
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('$\phi$ (deg)')

line, = ax.plot([], [], 'o-', lw=2)
line2, = ax2.plot([],[])
lines=[line,line2]
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
global p1
p1 =Pendulum(1,1,1,1,0.5,0.5)
p1.initSim(np.array([[0],[pi/6],[0],[0]]))
dt=0.005
xdata, ydata = [0], [0]
def init():
    """initialize animation"""
    lines[0].set_data([], [])
    lines[1].set_data([],[])
    time_text.set_text('')
    return lines[0],lines[1] ,time_text
def animate(i):
    """perform animation step"""
    p1.getNextState(0,dt)
    xdata.append(p1.t)
    if (len(xdata)>10/dt):
        xdata.pop(0)
    ydata.append(p1.state[0]*180/pi)
    lines[0].set_data(*p1.getPosition())
    lines[1].set_data(xdata,ydata)
    ax2.set_xlim([xdata[0], p1.t])
    ax2.set_ylim([min(ydata), max(ydata)])
    time_text.set_text('time = %.1f' % p1.t)    
    return lines[0],lines[1], time_text

from time import time
t0 = time()
i=0
animate(i)
t1 = time()
interval = 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, frames=300,
                              interval=interval, blit=True, init_func=init)
plt.show()