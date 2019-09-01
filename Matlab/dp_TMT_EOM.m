function [dX,v,acc]=dp_TMT_EOM(m1,m2,L1,L2,a,b,grav)
g=9.81;
syms phi1 phi2 Fx b1 b2 k1 k2 t real
syms dphi1 dphi2 real 
syms ddphi1 ddphi2 real


q=[phi1;phi2];
dq=[dphi1;dphi2];
ddq=[ddphi1;ddphi2];

x1=(a*L1)*sin(phi1);
y1=(a*L1)*cos(phi1);
x2=(L1)*sin(phi1)+(b*L2)*sin(phi2);
y2=(L1)*cos(phi1)+(b*L2)*cos(phi2);
x3=(L1)*sin(phi1);
y3=(L1)*cos(phi1);

x=[x1;y1;phi1;x2;y2;phi2;x3;y3];
T=jacobian(x,q);
G=jacobian(T*dq,q)*dq;

v=simplify(T*dq);
acc=simplify(T*ddq+G);

I1=(m1*(L1^2))/12;
I2=(m2*(L2^2))/12;
M=diag([m1;m1;I1;m2;m2;I2;0;0]);

% -1 for gravity along negative y and 1 for gravity along positive x:
if grav==-1
    F=[0 -m1*g -b1*dphi1-k1*(phi1) 0 -m2*g -b2*(dphi2-dphi1)-k2*(phi2-phi1) Fx 0]';
elseif grav==1
    F=[m1*g 0 0 m2*g 0 0 Fx 0]';
end

M_bar=T'*M*T;
Q_bar=T'*(F-M*G);

gen_acc=M_bar\Q_bar;

syms X1 X2 X3 X4 
X=[X1;X2;X3;X4];
assume(X,'real')
gq=[q;dq];
gen_acc=subs(gen_acc,gq,X);
acc=subs(acc,ddq,gen_acc);
dX=[X3;X4;gen_acc];
Gains=[k1;b1;k2;b2];
dX=matlabFunction(dX,'vars',{t,X,Fx,Gains});

v=subs(v,gq,X);
v=matlabFunction(v,'vars',{t,X,Fx});

acc=subs(acc,gq,X);
acc=matlabFunction(acc,'vars',{t,X,Fx,Gains});
end
