% Simscape(TM) Multibody(TM) version: 4.9

% This is a model data file derived from a Simscape Multibody Import XML file using the smimport function.
% The data in this file sets the block parameter values in an imported Simscape Multibody model.
% For more information on this file, see the smimport function help page in the Simscape Multibody documentation.
% You can modify numerical values, but avoid any other changes to this file.
% Do not add code to this file. Do not edit the physical units shown in comments.

%%%VariableName:smiData


%============= RigidTransform =============%

%Initialize the RigidTransform structure array by filling in null values.
smiData.RigidTransform(11).translation = [0.0 0.0 0.0];
smiData.RigidTransform(11).angle = 0.0;
smiData.RigidTransform(11).axis = [0.0 0.0 0.0];
smiData.RigidTransform(11).ID = '';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(1).translation = [-11.897715053763358 0 0];  % mm
smiData.RigidTransform(1).angle = 2.0943951023931953;  % rad
smiData.RigidTransform(1).axis = [-0.57735026918962584 -0.57735026918962584 0.57735026918962584];
smiData.RigidTransform(1).ID = 'B[sphere-1:-:poignet-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(2).translation = [4.2632564145606011e-14 -44.102284946236701 44.999999999999986];  % mm
smiData.RigidTransform(2).angle = 2.0943951023931957;  % rad
smiData.RigidTransform(2).axis = [-0.57735026918962584 -0.57735026918962562 -0.57735026918962584];
smiData.RigidTransform(2).ID = 'F[sphere-1:-:poignet-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(3).translation = [0 0 64.000000000000057];  % mm
smiData.RigidTransform(3).angle = 3.1415926535897931;  % rad
smiData.RigidTransform(3).axis = [1 0 0];
smiData.RigidTransform(3).ID = 'B[chaise-1:-:bati-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(4).translation = [6.3948846218409017e-14 1.4210854715202004e-14 -64.000000000000114];  % mm
smiData.RigidTransform(4).angle = 1.0353843514823591e-15;  % rad
smiData.RigidTransform(4).axis = [0.56301729540561529 -0.8264451131649011 -2.408836667531356e-16];
smiData.RigidTransform(4).ID = 'F[chaise-1:-:bati-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(5).translation = [0 0 0];  % mm
smiData.RigidTransform(5).angle = 0;  % rad
smiData.RigidTransform(5).axis = [0 0 0];
smiData.RigidTransform(5).ID = 'B[bras-1:-:chaise-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(6).translation = [0 57.999999999999943 353];  % mm
smiData.RigidTransform(6).angle = 2.0943951023931957;  % rad
smiData.RigidTransform(6).axis = [0.57735026918962584 -0.57735026918962573 0.57735026918962573];
smiData.RigidTransform(6).ID = 'F[bras-1:-:chaise-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(7).translation = [210.71075268817197 0 48.000000000000014];  % mm
smiData.RigidTransform(7).angle = 0;  % rad
smiData.RigidTransform(7).axis = [0 0 0];
smiData.RigidTransform(7).ID = 'B[avant bras-1:-:poignet-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(8).translation = [-2.7394753132625738e-14 7.6938455606523348e-14 -7.0000000000007638];  % mm
smiData.RigidTransform(8).angle = 3.227063611521286e-17;  % rad
smiData.RigidTransform(8).axis = [-0.99778515785660904 0.066519010523773806 -1.0709281896641417e-18];
smiData.RigidTransform(8).ID = 'F[avant bras-1:-:poignet-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(9).translation = [282.00000000000006 0 126];  % mm
smiData.RigidTransform(9).angle = 3.1415926535897931;  % rad
smiData.RigidTransform(9).axis = [1 0 0];
smiData.RigidTransform(9).ID = 'B[bras-1:-:avant bras-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(10).translation = [-106.78924731182786 3.5527136788005009e-14 163.00000000000077];  % mm
smiData.RigidTransform(10).angle = 3.1415926535897931;  % rad
smiData.RigidTransform(10).axis = [-1 -9.9390846030819586e-18 5.7245874707234622e-17];
smiData.RigidTransform(10).ID = 'F[bras-1:-:avant bras-1]';

%Translation Method - Cartesian
%Rotation Method - Arbitrary Axis
smiData.RigidTransform(11).translation = [-128.82954374505215 -328.65171330520258 58.000000000000149];  % mm
smiData.RigidTransform(11).angle = 1.605272101768245;  % rad
smiData.RigidTransform(11).axis = [0.96608641734055412 -0.18263791593569048 -0.18253883393064671];
smiData.RigidTransform(11).ID = 'RootGround[bati-1]';


%============= Solid =============%
%Center of Mass (CoM) %Moments of Inertia (MoI) %Product of Inertia (PoI)

%Initialize the Solid structure array by filling in null values.
smiData.Solid(6).mass = 0.0;
smiData.Solid(6).CoM = [0.0 0.0 0.0];
smiData.Solid(6).MoI = [0.0 0.0 0.0];
smiData.Solid(6).PoI = [0.0 0.0 0.0];
smiData.Solid(6).color = [0.0 0.0 0.0];
smiData.Solid(6).opacity = 0.0;
smiData.Solid(6).ID = '';

%Inertia Type - Custom
%Visual Properties - Simple
smiData.Solid(1).mass = 5.5649661309075009;  % kg
smiData.Solid(1).CoM = [13.947329222260169 1.7221923273403459 73.969728157571168];  % mm
smiData.Solid(1).MoI = [30005.693205382911 151867.58537026579 143649.43768189155];  % kg*mm^2
smiData.Solid(1).PoI = [-810.55924681529837 -8858.7046326783639 -1392.2465229587124];  % kg*mm^2
smiData.Solid(1).color = [0.89803921568627454 0.91764705882352937 0.92941176470588238];
smiData.Solid(1).opacity = 1;
smiData.Solid(1).ID = 'bras*:*Défaut';

%Inertia Type - Custom
%Visual Properties - Simple
smiData.Solid(2).mass = 1.8424860004287908;  % kg
smiData.Solid(2).CoM = [18.663344986038691 -0.00019380608295110744 99.829651664470376];  % mm
smiData.Solid(2).MoI = [3663.5450553416131 23143.368394426194 22600.516490455087];  % kg*mm^2
smiData.Solid(2).PoI = [-0.0038243779380794968 61.225255676957779 0.055603542153021407];  % kg*mm^2
smiData.Solid(2).color = [0.89803921568627454 0.91764705882352937 0.92941176470588238];
smiData.Solid(2).opacity = 1;
smiData.Solid(2).ID = 'avant bras*:*Défaut';

%Inertia Type - Custom
%Visual Properties - Simple
smiData.Solid(3).mass = 0.12615401081623093;  % kg
smiData.Solid(3).CoM = [48.468831011126454 0 0];  % mm
smiData.Solid(3).MoI = [11.900019072577345 203.54028757091217 203.54028757091217];  % kg*mm^2
smiData.Solid(3).PoI = [0 0 0];  % kg*mm^2
smiData.Solid(3).color = [0.89803921568627454 0.91764705882352937 0.92941176470588238];
smiData.Solid(3).opacity = 1;
smiData.Solid(3).ID = 'sphere*:*Défaut';

%Inertia Type - Custom
%Visual Properties - Simple
smiData.Solid(4).mass = 0.10857522424716801;  % kg
smiData.Solid(4).CoM = [0 -36.461525852781598 45];  % mm
smiData.Solid(4).MoI = [202.96519187623181 205.87251486464459 105.55857071799551];  % kg*mm^2
smiData.Solid(4).PoI = [0 0 0];  % kg*mm^2
smiData.Solid(4).color = [0.89803921568627454 0.91764705882352937 0.92941176470588238];
smiData.Solid(4).opacity = 1;
smiData.Solid(4).ID = 'poignet*:*Défaut';

%Inertia Type - Custom
%Visual Properties - Simple
smiData.Solid(5).mass = 14.374025527242805;  % kg
smiData.Solid(5).CoM = [-26.709066453346665 -116.44799269584385 236.1091741894096];  % mm
smiData.Solid(5).MoI = [260620.83334554304 240171.91051588135 136890.93723652139];  % kg*mm^2
smiData.Solid(5).PoI = [34425.123712696375 16094.054994755115 -22328.889822980225];  % kg*mm^2
smiData.Solid(5).color = [0.89803921568627454 0.91764705882352937 0.92941176470588238];
smiData.Solid(5).opacity = 1;
smiData.Solid(5).ID = 'chaise*:*Défaut';

%Inertia Type - Custom
%Visual Properties - Simple
smiData.Solid(6).mass = 10.948971951767058;  % kg
smiData.Solid(6).CoM = [0 0 88.626543346207654];  % mm
smiData.Solid(6).MoI = [49284.971751952522 49284.971751952522 42696.2785874049];  % kg*mm^2
smiData.Solid(6).PoI = [0 0 0];  % kg*mm^2
smiData.Solid(6).color = [0.89803921568627454 0.91764705882352937 0.92941176470588238];
smiData.Solid(6).opacity = 1;
smiData.Solid(6).ID = 'bati*:*Défaut';


%============= Joint =============%
%X Revolute Primitive (Rx) %Y Revolute Primitive (Ry) %Z Revolute Primitive (Rz)
%X Prismatic Primitive (Px) %Y Prismatic Primitive (Py) %Z Prismatic Primitive (Pz) %Spherical Primitive (S)
%Constant Velocity Primitive (CV) %Lead Screw Primitive (LS)
%Position Target (Pos)

%Initialize the RevoluteJoint structure array by filling in null values.
smiData.RevoluteJoint(4).Rz.Pos = 0.0;
smiData.RevoluteJoint(4).ID = '';

smiData.RevoluteJoint(1).Rz.Pos = 18.297523398476677;  % deg
smiData.RevoluteJoint(1).ID = '[sphere-1:-:poignet-1]';

smiData.RevoluteJoint(2).Rz.Pos = -0.9363132073744912;  % deg
smiData.RevoluteJoint(2).ID = '[chaise-1:-:bati-1]';

smiData.RevoluteJoint(3).Rz.Pos = 89.999999999999957;  % deg
smiData.RevoluteJoint(3).ID = '[bras-1:-:chaise-1]';

smiData.RevoluteJoint(4).Rz.Pos = 89.999999999999986;  % deg
smiData.RevoluteJoint(4).ID = '[avant bras-1:-:poignet-1]';

