function varargout = pompe_app(varargin)
% POMPE_APP MATLAB code for pompe_app.fig
%      POMPE_APP, by itself, creates a new POMPE_APP or raises the existing
%      singleton*.
%
%      H = POMPE_APP returns the handle to a new POMPE_APP or the handle to
%      the existing singleton*.
%
%      POMPE_APP('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in POMPE_APP.M with the given input arguments.
%
%      POMPE_APP('Property','Value',...) creates a new POMPE_APP or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before pompe_app_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to pompe_app_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help pompe_app

% Last Modified by GUIDE v2.5 30-Jan-2015 19:34:20

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @pompe_app_OpeningFcn, ...
                   'gui_OutputFcn',  @pompe_app_OutputFcn, ...
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


% --- Executes just before pompe_app is made visible.
function pompe_app_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to pompe_app (see VARARGIN)

% Choose default command line output for pompe_app
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes pompe_app wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = pompe_app_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
