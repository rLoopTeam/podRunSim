within PodRunSim;

package Utilities

  class EddyBrakeConnection

    extends ExternalObject;

    function constructor "open a connection to eddy brake server"
      input String socName;
      input String eddyBrakeDataFile;
      output EddyBrakeConnection con;
      external "C" con = initSocketConnection(socName,eddyBrakeDataFile)
        annotation(Library="eddybrakeclient",
          LibraryDirectory="modelica://PodRunSim/ExternalLibraries");
    end constructor;

    function destructor
      input EddyBrakeConnection connection;
      external "C" closeSocketConnection(connection)
        annotation(Library="eddybrakeclient",
          LibraryDirectory="modelica://PodRunSim/ExternalLibraries");
    end destructor;

  end EddyBrakeConnection;

  function getEddyBrakeData
    input EddyBrakeConnection con;
    input Real v;
    input Real h;
    output Real f_drag;
    output Real f_lift;
    output Real H_y_max;
    output Real H_y_mean;
    output Real q_max;
    output Real q_mean;
    external "C" getEddyBrakeData(con,v,h,f_drag,f_lift,H_y_max,H_y_mean,q_max,q_mean) annotation(
        Library="eddybrakeclient",
        LibraryDirectory="modelica://PodRunSim/ExternalLibraries");
  end getEddyBrakeData;
end Utilities;
