clear all
clc
a=0.5;
b=1;

m1=20;
m2=80;
L1=1;
L2=0.25;
grav=-1;

[dX,v,acc]=dp_TMT_EOM(m1,m1,a,b,L1,L2,grav);


%%
extra.b1=50;
extra.k1=3000;
extra.b2=10;
extra.k2=100000;

init=[0;0;0;0];
dt=0.005;

simulatePendulumn(dX,init,dt,L1,L2,extra);