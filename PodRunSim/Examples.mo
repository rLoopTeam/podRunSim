within PodRunSim;
package Examples
  model HelloPodRunSim
  Components.EddyBrakeData eddyBrakeData1(dataFile = "/home/adam/projects/podRunSim/run/analysis012/eddyBrakeData.csv", socket = "/home/adam/projects/podRunSim/socket")  annotation(Placement(visible = true, transformation(origin = {-4, 72}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Mechanics.Translational.Components.Mass mass1(m = 300, v(start = 50))  annotation(Placement(visible = true, transformation(origin = {-10, 10}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Sensors.SpeedSensor speedSensor1 annotation(Placement(visible = true, transformation(origin = {26, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Sources.Force force1 annotation(Placement(visible = true, transformation(origin = {-46, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 0.010)  annotation(Placement(visible = true, transformation(origin = {-74, 72}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    equation
    connect(mass1.flange_b, speedSensor1.flange) annotation(Line(points = {{0, 10}, {6, 10}, {6, 40}, {16, 40}}, color = {0, 127, 0}));
    connect(force1.flange, mass1.flange_b) annotation(Line(points = {{-36, 40}, {3, 40}, {3, 10}, {0, 10}}, color = {0, 127, 0}));
    connect(eddyBrakeData1.f_drag, force1.f) annotation(Line(points = {{6, 80}, {28, 80}, {28, 58}, {-70, 58}, {-70, 40}, {-58, 40}}, color = {0, 0, 127}));
    connect(const.y, eddyBrakeData1.h) annotation(Line(points = {{-62, 72}, {-48, 72}, {-48, 68}, {-14, 68}, {-14, 68}}, color = {0, 0, 127}));
    connect(speedSensor1.v, eddyBrakeData1.v) annotation(Line(points = {{38, 40}, {46, 40}, {46, 54}, {-36, 54}, {-36, 76}, {-14, 76}, {-14, 76}}, color = {0, 0, 127}));
    annotation(uses(Modelica(version = "3.2.2")));
  end HelloPodRunSim;
end Examples;