function [x,y]=animator(action) 

switch(action)
case 'start'
    set(gcbf,'WindowButtonMotionFcn','animator move;')
    set(gcbf,'WindowButtonUpFcn', 'animator stop')
case 'move'
    if ~isempty(findobj(gca,'Tag','toto'))
        delete(findobj(gca,'Tag','toto')) 
    end
    currpt=get(gca,'CurrentPoint'); 
    h=findobj(gcbf,'Tag','text2');
    set(h,'string',['t= ',num2str(currpt(1,1)),' y= ',num2str(currpt(1,2))])
    x=currpt(1,1);
    y=currpt(1,2); 
    text(x,y,'\bullet','Tag','toto');
case 'stop' 
    set(gcbf,'WindowButtonMotionFcn',''); 
    set(gcbf,'WindowButtonUpFcn','');
end