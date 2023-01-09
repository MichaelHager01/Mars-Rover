import numpy as np
from subfunctions import *
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def bisection(fun, lb, ub):
    errTol = 1e-3
    itermax = 1000
    step = 0
    
    if not callable(fun):
        raise Exception("Not callable")
        
    if np.sign(fun(lb)) == np.sign(fun(ub)):
        return 'Nan', 0                                     
        raise Exception("There is no root between lower and upper bound")
        
    if not isinstance(lb, (int, float)):
        raise Exception("Lower bound is an invalid input")
        
    if not isinstance(ub, (int, float)):
        raise Exception("Upper bound is an invalid input")
        
    if fun(lb) == 0:
        return lb , 0, step
        
    if fun(ub) == 0: 
        return ub, 0, step
    
    while True:
        step += 1
        xr = (lb + ub)/2
        
        if fun(xr) == np.isinf:
            SystemExit(-2)
        
        if isnan(fun(xr)):
            SystemExit(-2)
            
        if fun(xr) == 0:
            return xr, 0, step, 1
    
        if fun(lb)*fun(xr) < 0:
            ub = xr
        else:
            lb = xr
    
        error_est = abs((ub - lb)/(ub+lb)) * 100
    
        if error_est < errTol:
            return xr, error_est, step, 
        
        if step >= itermax:
            return xr, error_est, step, 0


def omega_vel(omega):
    Fnet = F_net(omega, slope_sample, rover, planet, Crr_sample)
    return Fnet

  
Crr_array = np.linspace(0.01, 0.4, 25)
slope_list_deg = np.linspace(-10, 35, 25)
r = rover['wheel_assembly']['wheel']['radius']
    
omega_max = np.zeros(len(Crr_array), dtype = float)
omega_nl = rover['wheel_assembly']['motor']['speed_noload']

CRR, SLOPE = np.meshgrid(Crr_array, slope_list_deg)
VMAX = np.zeros(np.shape(CRR), dtype = float)

N = np.shape(CRR)[0]
for i in range(25):
    for j in range(25):
        Crr_sample = float(CRR[i,j])
        slope_sample = float(SLOPE[i,j])
        root  = float(bisection(omega_vel, 0.0, omega_nl)[0])/get_gear_ratio(rover['wheel_assembly']['speed_reducer'])*r
        VMAX[i, j] = root

figure = plt.figure()
ax = Axes3D(figure, elev = 35, azim = 20) 
ax.set_xlabel('Rolling Resistance (N)')
ax.set_ylabel('Slope of Terrain (deg)')
ax.set_zlabel('Velocity (m/s)')
ax.plot_surface(CRR, SLOPE, VMAX)
plt.show()

