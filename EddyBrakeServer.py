import argparse
from EddyBrake import EddyBrake
import numpy as np
import socket

parser = argparse.ArgumentParser()
parser.add_argument('socketPath',help='socket path')
args = parser.parse_args()

s1 = socket.socket(socket.AF_UNIX)
s1.bind(args.socketPath)
s1.listen(0)

acceptingConnections = True

while acceptingConnections:
  print("waiting for a connection...")
  s2,s2info = s1.accept()
  filename = s2.recv(2048)
  eddyBrake = EddyBrake(filename)
  print("connection accepted")
  print('Loaded file: {}'.format(filename))
  s2.sendall("ready")
  ok = True
  while ok:
    try:
      inputArr = np.frombuffer(s2.recv(1024),dtype="double")
      v = inputArr[0]
      h = inputArr[1]
      print("recieved v: {} and h: {}".format(v,h))
      outputArr = np.array([
        eddyBrake.f_drag(v,h),
        eddyBrake.f_lift(v,h),
        eddyBrake.H_y_max(v,h),
        eddyBrake.H_y_mean(v,h),
        eddyBrake.q_max(v,h),
        eddyBrake.q_mean(v,h)],dtype="double")
      s2.sendall(outputArr.tostring())
      print(outputArr)
    except:
      print("closing connection")
      s2.close()
      ok = False

s1.close()
os.unlink(args.socketPath)
