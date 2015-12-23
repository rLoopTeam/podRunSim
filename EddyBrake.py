import pandas as pd
from scipy.interpolate import LinearNDInterpolator

class EddyBrake():

  def __init__(self,filename):
    df = pd.read_csv(filename)

    df_f_drag = df[df['F_drag'].isnull()==False]
    self.f_drag = LinearNDInterpolator((df_f_drag['v'],df_f_drag['h']),df_f_drag['F_drag'])


    df_f_lift = df[df['F_lift'].isnull()==False]
    self.f_lift = LinearNDInterpolator((df_f_lift['v'],df_f_lift['h']),df_f_lift['F_lift'])
