#Thermal Calcs for determining the temperature rise in i-Beam while braking
#The idea is to put the total energy into the volume between the eddy brake and
#the i_Beam

import numpy as np
from matplotlib import pyplot as plt

m_pod = 385.0 #Mass of pod in Kg
v_max = 88.0 #Max Velocity of the pod in m/s
L_brake = 300.0 #Length over which brake is to be applied in meters
rho_Al = 2700 #Density of Aluminium 6061-T6 in Kg/m3
c_Al = 897.0 #Specific heat capacity of Al 6061-T6 in J/Kg.K
h_eb = 0.0762 # Height of eddy brake in meters
flange_t = 0.0079502 #Flange thickness of the i-Beam

mass = flange_t*L_brake*h_eb*rho_Al

energy = 0.5*m_pod*v_max**2

T = (energy)/(mass*c_Al)

print T 















#ref - http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA6061t6
