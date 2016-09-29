within PodRunSim;
package Examples
  model HelloPodRunSim
  Components.EddyBrakeData eddyBrakeData1(dataFile = "/home/adam/projects/podRunSim/run/analysis012/eddyBrakeData.csv", socket = "/home/adam/projects/podRunSim/socket")  annotation(Placement(visible = true, transformation(origin = {-4, 72}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Mechanics.Translational.Components.Mass mass1(m = 385, v(start = 149))  annotation(Placement(visible = true, transformation(origin = {-10, 10}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Sensors.SpeedSensor speedSensor1 annotation(Placement(visible = true, transformation(origin = {26, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Sources.Force force1 annotation(Placement(visible = true, transformation(origin = {-46, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 0.001)  annotation(Placement(visible = true, transformation(origin = {-74, 72}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.Gain gain1(k = -24)  annotation(Placement(visible = true, transformation(origin = {44, 80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    equation
    connect(gain1.y, force1.f) annotation(Line(points = {{56, 80}, {64, 80}, {64, 94}, {-50, 94}, {-50, 54}, {-70, 54}, {-70, 40}, {-58, 40}}, color = {0, 0, 127}));
    connect(eddyBrakeData1.f_drag, gain1.u) annotation(Line(points = {{6, 80}, {30, 80}, {30, 80}, {32, 80}}, color = {0, 0, 127}));
    connect(mass1.flange_b, speedSensor1.flange) annotation(Line(points = {{0, 10}, {6, 10}, {6, 40}, {16, 40}}, color = {0, 127, 0}));
    connect(force1.flange, mass1.flange_b) annotation(Line(points = {{-36, 40}, {3, 40}, {3, 10}, {0, 10}}, color = {0, 127, 0}));
    connect(const.y, eddyBrakeData1.h) annotation(Line(points = {{-62, 72}, {-48, 72}, {-48, 68}, {-14, 68}, {-14, 68}}, color = {0, 0, 127}));
    connect(speedSensor1.v, eddyBrakeData1.v) annotation(Line(points = {{38, 40}, {46, 40}, {46, 54}, {-36, 54}, {-36, 76}, {-14, 76}, {-14, 76}}, color = {0, 0, 127}));
    annotation(uses(Modelica(version = "3.2.2")));
  end HelloPodRunSim;
end Examples;