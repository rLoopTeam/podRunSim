clang -c -fPIC eddyBrakeClient.c
mkdir -p PodRunSim/ExternalLibraries
clang -shared eddyBrakeClient.o -o PodRunSim/ExternalLibraries/libeddybrakeclient.so
rm eddyBrakeClient.o
