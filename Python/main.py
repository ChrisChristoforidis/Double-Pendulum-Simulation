from time import time
from pendulum import Pendulum
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import pi
import numpy as np

fig = plt.figure()
grid = plt.GridSpec(1, 2, wspace=0.4, hspace=0.3)
ax = fig.add_subplot(grid[0, 0], aspect='equal', autoscale_on=False,
                     xlim=(-2.1, 2.1), ylim=(-2.2, 2.2))
ax2 = fig.add_subplot(grid[0, 1:])
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('$\phi$ (deg)')

line, = ax.plot([], [], 'o-', lw=2)
line2, = ax2.plot([], [])
lines = [line, line2]
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
global p1
p1 = Pendulum(1, 1, 1, 1, 0.5, 0.5)
p1.initSim(np.array([[0], [pi/6], [0], [0]]))
dt = 0.005
xdata, ydata = [0], [0]


def init():
    """initialize animation"""
    lines[0].set_data([], [])
    lines[1].set_data([], [])
    time_text.set_text('')
    return lines[0], lines[1], time_text


def animate(i):
    """perform animation step"""
    p1.getNextState(0, dt)
    xdata.append(p1.t)
    if (len(xdata) > 10/dt):
        xdata.pop(0)
    ydata.append(p1.state[0]*180/pi)
    lines[0].set_data(*p1.getPosition())
    lines[1].set_data(xdata, ydata)
    ax2.set_xlim([xdata[0], p1.t])
    ax2.set_ylim([min(ydata), max(ydata)])
    time_text.set_text('time = %.1f' % p1.t)
    return lines[0], lines[1], time_text


t0 = time()
i = 0
animate(i)
t1 = time()
interval = 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, frames=300,
                              interval=interval, blit=True, init_func=init)
plt.show()
