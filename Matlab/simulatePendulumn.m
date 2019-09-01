function simulatePendulumn(dX,init,dt,l1,l2,extra)
global step;
step=15000;
w=0;
duration=0.3/dt;
magnitude=300;
phi1=init(1);
phi2=init(2);

x1=sin(phi1)*l1;

y1=cos(phi1)*l1;

x2=sin(phi2)*l2+sin(phi1)*l1;

y2=cos(phi2)*l2+cos(phi1)*l1;


state=init;


GUI.fh = figure;
GUI.h1 = uicontrol('style','Edit',...
                   'string',num2str(extra.k2),...
                   'Units','normalized',...
                   'Position',[0.1 0.1 0.1 0.1],...
                   'backgroundcolor','w',...
                   'Tag','EditField');

GUI.h3 = uicontrol('Style','PushButton',...
                   'String','Change',...
                   'Units','normalized',...
                   'Position',[0.2 0.1 0.1 0.1],...
                   'callback',{@func_compute,GUI.h1},...
                   'backgroundcolor',...
                   'r','FontSize',12);
GUI.h4 = uicontrol('Style','PushButton',...
                   'String','Impulse',...
                   'Units','normalized',...
                   'Position',[0.4 0.1 0.1 0.1],...
                   'callback',{@impulseTrigger},...
                   'backgroundcolor',...
                   'g','FontSize',10);

h2=annotation('textbox', [0.1, 0.9, 0.5, 0],'FitBoxToText','on',...
  'string', "Damping = "+extra.b2+"   Stiffness = "+extra.k2);
subplot(2,2,[1 3])
p1=plot([0 x1],[0 y1],'LineWidth',3.5);
hold on
p2=plot([x1 x2],[y1 y2],'LineWidth',2,'Color','g');

p3=quiver(x1,y1,w,0,'LineWidth',2,'Color','red','MaxHeadSize',0.5);
p4=plot(x2,y2,'MarkerSize',5,'Marker','o','Color','g','LineWidth',3.5);

axis equal
t1=text(-1.3,2.1,"t = 0 s");
xlim([-1.5 1.5])
ylim([0 2.2])
subplot(2,2,[2 4])
h1=animatedline(0,phi1*180/pi);
xlabel('Time (s)')
ylabel('\phi   (deg)')
tic
i=0;
while(1)
  if (toc<dt)
    continue 
  end
  i=i+1;
  tic;
  if(step<duration)
      step= step+1;
      if( step<floor( duration/2))
         w=(magnitude*2/(duration*dt))*(dt*step);
      else
         w=-(magnitude*2/(duration*dt))*(dt*step)+2*magnitude;
      end
  else
    w=0;
    step=15000;
  end
  Gains=[extra.k1;extra.b1;extra.k2;extra.b2];
  k1=dX(dt*(i-1),state,w,Gains);
  k2=dX(dt*(i-1)+(dt/2),state+(k1*dt)/2,w,Gains);
  k3=dX(dt*(i-1)+(dt/2),state+(k2*dt)/2,w,Gains);
  k4=dX(dt*(i-1)+(dt),state+(k3*dt),w,Gains);
  state=state+(dt/6)*(k1+(2*k2)+(2*k3)+k4);  

  phi1=state(1);
  phi2=state(2);
  
  x1=sin(phi1)*l1;

  y1=cos(phi1)*l1;

  x2=sin(phi2)*l2+sin(phi1)*l1;

  y2=cos(phi2)*l2+cos(phi1)*l1;

  set(p1,'XData',[0 x1],'YData',[0 y1]);
  set(p2,'XData',[x1 x2],'YData',[y1 y2]);
  set(p3,'XData',x1,'YData',y1,'UData',w/magnitude,'VData',0);
  set(p4,'XData', x2 ,'YData', y2 );
  addpoints(h1,dt*(i-1),phi1*180/pi);
  set(t1,'String',"t = "+round(dt*(i-1),2)+" s");
  set(h2,'string',"Damping = "+extra.b2+"   Stiffness = "+extra.k2);
  drawnow 
end




function func_compute(~,~,InHandle)

    a = str2double(InHandle.String);
    extra.k2 = a;
end
function impulseTrigger(~,~)
  step = 0;
end


end



