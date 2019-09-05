from pendulum import Pendulum
import numpy as np
import matplotlib.pyplot as plt
k1,k2,b1,b2 = 2500,120,50,10
kc1,kc2 = 0 , 0

p1 = Pendulum(20, 80, 0.8, 0.20, 0.8, 1)
p1.initSim(np.zeros([4,1]))
p1.setSDproperties(k1,k2,b1,b2)
p1.setControl(kc1,kc2)
xdata=[]
warr=[]
step= 0
dt=0.005
duration = 0.3 /dt
magnitude = 300
while(p1.t<10):

    if(step<duration):
        step+=1;
        if( step<np.floor(duration/2)):
            w=(magnitude*2/(duration*dt))*(dt*step)
        else:
            w=-(magnitude*2/(duration*dt))*(dt*step)+2*magnitude
    else:
        w=0
        step=15000
    p1.updateState(w,0.005)
    warr.append(w)
    xdata.append(np.asscalar(p1.state[0]))

plt.plot(np.array(xdata)*180/np.pi)