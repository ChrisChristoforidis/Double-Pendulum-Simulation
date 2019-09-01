clear all
clc
a=0.8;
b=0.5;

m1=15;
m2=70;
L1=1;
L2=0.5;
grav=-1;

[dX,v,acc]=dp_TMT_EOM(m1,m1,a,b,L1,L2,grav);


%%
extra.b1=80;
extra.k1=3000;
extra.b2=10;
extra.k2=100000;

init=[0;0;0;0];
dt=0.005;

simulatePendulumn(dX,init,dt,L1,L2,extra);