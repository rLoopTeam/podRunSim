clang -c -fPIC eddyBrakeClient.c
mkdir -p PodRun/ExternalLibraries
clang -shared eddyBrakeClient.o -o libeddybrakeClient.c
rm eddyBrakeClient.o
