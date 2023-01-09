# Names: Michael Hager, Elizabeth Sharf, Savera Sahai
# MEEN 357 - Group 14

import numpy as np

def experiment1():
    experiment = {'time_range' : np.array([0,20000]),
                  'initial_conditions' : np.array([0.3125,0]),
                  'alpha_dist' : np.array([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]),
                  'alpha_deg' : np.array([11.509, 2.032, 7.182, 2.478, 5.511, 10.981, 5.601, -0.184, 0.714, 4.151, 4.042]),
                  'Crr' : 0.1}
    
    # Below are default values for example only:
    end_event = {'max_distance' : 50,
                 'max_time' : 5000,
                 'min_velocity' : 0.01}
    
    return experiment, end_event

