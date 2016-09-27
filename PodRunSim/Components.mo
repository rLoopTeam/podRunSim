within PodRunSim;

package Components


  model EddyBrakeData
    import PodRunSim.Utilities.EddyBrakeConnection;
    import PodRunSim.Utilities.getEddyBrakeData;
    parameter String socket "path and name of socket";
    parameter String dataFile "Eddy brake data file";
    EddyBrakeConnection con = EddyBrakeConnection(socket,dataFile);
    Integer status;
    
  Modelica.Blocks.Interfaces.RealInput v annotation(Placement(visible = true, transformation(origin = {-102, 42}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-100, 40}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput h annotation(Placement(visible = true, transformation(origin = {-96, -46}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-100, -40}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput f_drag annotation(Placement(visible = true, transformation(origin = {96, 74}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {102, 80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput f_lift annotation(Placement(visible = true, transformation(origin = {98, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {104, 50}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput H_y_max annotation(Placement(visible = true, transformation(origin = {96, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {102, 16}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput H_y_mean annotation(Placement(visible = true, transformation(origin = {92, -32}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {104, -20}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput q_max annotation(Placement(visible = true, transformation(origin = {96, -64}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {106, -54}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput q_mean annotation(Placement(visible = true, transformation(origin = {104, -92}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {106, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  annotation(uses(Modelica(version = "3.2.2")));
  equation
    //status = getEddyBrakeData(con,v,h,f_drag,f_lift,H_y_max,H_y_mean,q_max,q_mean);
    f_drag=v*h;
    f_lift =f_drag;
    H_y_max = f_drag;
    H_y_mean = f_drag;
    q_max = f_drag;
    q_mean = f_drag;
    status = 0;
  end EddyBrakeData;
end Components;
