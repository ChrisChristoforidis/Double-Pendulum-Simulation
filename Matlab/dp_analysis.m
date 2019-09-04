clear all
clc
a=0.5;
b=0.5;

m1=20;
m2=80;
L1=1;
L2=0.5;
grav=-1;

[dX,v,acc]=dp_TMT_EOM(m1,m2,L1,L2,a,b,grav);


%%
extra.b1=50;
extra.k1=3000;
extra.b2=10;
extra.k2=300;

init=[0;0;0;0];
dt=0.005;
#'$k_1$ = '+str(self.k1)+' $b_1$ = '+str(self.b1)+' $k_2$ = '+str(self.k2)+' $b_2$ = '+str(self.b2)

simulatePendulumn(dX,init,dt,L1,L2,extra);