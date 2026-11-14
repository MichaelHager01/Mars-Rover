import numpy as np
from subfunctions import *
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt

    
def graphs_terrain_slope():
    Crr = 0.2
    slope_list_deg = np.linspace(-10, 35, 25)
        
    omega_max = np.zeros(len(slope_list_deg), dtype = float)
    omega_nl = rover['wheel_assembly']['motor']['speed_noload']

    # Find where F_net == 0
    v_max = []
    for ii in range(len(slope_list_deg)):
        fun = lambda omega: F_net(omega, float(slope_list_deg[ii]), rover, planet, Crr)
        sol = root_scalar(fun, method = 'bisect', bracket = [0, omega_nl])
        omega_max[ii] = sol.root
        v_max.append(omega_max[ii] / get_gear_ratio(rover['wheel_assembly']['speed_reducer']) * rover['wheel_assembly']['wheel']['radius'])


    plt.plot(slope_list_deg, v_max)
    plt.ylabel('Max Rover Speed (m/s)')
    plt.xlabel('Terrain Angle (deg)')
    plt.title('Terrain Angle vs. Max Rover Speed')
    plt.show()
    
graphs_terrain_slope()

