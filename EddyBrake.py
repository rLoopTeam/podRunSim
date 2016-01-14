import pandas as pd
from scipy.interpolate import LinearNDInterpolator

class EddyBrake():

  def __init__(self,filename):
    df = pd.read_csv(filename)

    df_f_drag = df[df['F_drag'].isnull()==False]
    self.f_drag = LinearNDInterpolator((df_f_drag['v'],df_f_drag['h']),df_f_drag['F_drag'])


    df_f_lift = df[df['F_lift'].isnull()==False]
    self.f_lift = LinearNDInterpolator((df_f_lift['v'],df_f_lift['h']),df_f_lift['F_lift'])


    df_f_H_y_max = df[df['H_y_max'].isnull()==False]
    self.H_y_max = LinearNDInterpolator((df_f_H_y_max['v'],df_f_H_y_max['h']),df_f_H_y_max['H_y_max'])

    df_f_H_y_mean = df[df['H_y_mean'].isnull()==False]
    self.H_y_mean = LinearNDInterpolator((df_f_H_y_mean['v'],df_f_H_y_mean['h']),df_f_H_y_mean['H_y_mean'])

    df_f_q_max = df[df['q_max_rail_surf'].isnull()==False]
    self.q_max = LinearNDInterpolator((df_f_q_max['v'],df_f_q_max['h']),df_f_q_max['q_max_rail_surf'])

    df_f_q_mean = df[df['q_rail_surf_mean'].isnull()==False]
    self.q_mean = LinearNDInterpolator((df_f_q_mean['v'],df_f_q_mean['h']),df_f_q_mean['q_rail_surf_mean'])

