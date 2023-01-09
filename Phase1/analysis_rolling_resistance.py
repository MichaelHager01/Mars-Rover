import numpy as np
from subfunctions import *
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt

    
def graphs_rolling_resistance():
    Crr_array = np.linspace(0.01, 0.4, 25)
    slope_list_deg = 0
        
    omega_max = np.zeros(len(Crr_array), dtype = float)
    omega_nl = rover['wheel_assembly']['motor']['speed_noload']

    # Find where F_net == 0
    v_max = []
    for ii in range(len(Crr_array)):
        fun = lambda omega: F_net(omega, slope_list_deg, rover, planet, Crr_array[ii])
        sol = root_scalar(fun, method = 'bisect', bracket = [0, omega_nl])
        omega_max[ii] = sol.root
        v_max.append(omega_max[ii] / get_gear_ratio(rover['wheel_assembly']['speed_reducer']) * rover['wheel_assembly']['wheel']['radius'])


    plt.plot(Crr_array, v_max)
    plt.ylabel('Max Rover Speed (m/s)')
    plt.xlabel('Rolling Resistance')
    plt.title('Rolling Resistance vs. Max Rover Speed')
    plt.show()
    
graphs_rolling_resistance()

