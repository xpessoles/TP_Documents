function varargout = pompe(varargin)
% POMPE MATLAB code for pompe.fig
%      POMPE, by itself, creates a new POMPE or raises the existing
%      singleton*.
%
%      H = POMPE returns the handle to a new POMPE or the handle to
%      the existing singleton*.
%
%      POMPE('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in POMPE.M with the given input arguments.
%
%      POMPE('Property','Value',...) creates a new POMPE or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before pompe_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to pompe_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help pompe

% Last Modified by GUIDE v2.5 01-Feb-2015 22:52:01

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @pompe_OpeningFcn, ...
                   'gui_OutputFcn',  @pompe_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before pompe is made visible.
function pompe_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to pompe (see VARARGIN)

% Choose default command line output for pompe
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes pompe wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = pompe_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in bt_acquisition.
function bt_acquisition_Callback(hObject, eventdata, handles)
% hObject    handle to bt_acquisition (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


cla;  % Efface le graphique courant
t = [1:0.1:100];
y = t.*sin(t);
grid on;
if get(findobj(gcf,'Tag','checkposition'),'Value')
   plot (t,2*y);
end
if get(findobj(gcf,'Tag','checkpression'),'Value')
   plot (t,y);
end
if get(findobj(gcf,'Tag','checktension'),'Value')
   plot (t,-y);
end
if get(findobj(gcf,'Tag','checkcourant'),'Value')
   plot (t,-2*y);
end


% --- Executes on button press in b_quitter.
function b_quitter_Callback(hObject, eventdata, handles)
% hObject    handle to b_quitter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
close (gcf);


% --- Executes on button press in checkcourant.
function checkcourant_Callback(hObject, eventdata, handles)
% hObject    handle to checkcourant (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkcourant


% --- Executes on button press in checktension.
function checktension_Callback(hObject, eventdata, handles)
% hObject    handle to checktension (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checktension


% --- Executes on button press in checkposition.
function checkposition_Callback(hObject, eventdata, handles)
% hObject    handle to checkposition (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkposition


% --- Executes on button press in checkpression.
function checkpression_Callback(hObject, eventdata, handles)
% hObject    handle to checkpression (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkpression
