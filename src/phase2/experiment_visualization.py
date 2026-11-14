import matplotlib.pyplot as plt
from subfunctions import *
from define_experiment import *
from scipy.interpolate import interp1d


def experiment_visualization():
    experiment, end_event = experiment1()
    
    alpha_fun = interp1d(experiment['alpha_dist'], experiment['alpha_deg'], kind = 'cubic', fill_value = 'extrapolate')
    range_val = np.linspace(min([dist for dist in experiment['alpha_dist']]), max([dist for dist in experiment['alpha_dist']]), 100)
    
    star_vals = []
    for i in experiment['alpha_dist']:
        star_vals.append(alpha_fun(i))
    
   #Graph of Terrain Angle vs. Position
    plt.plot(range_val, alpha_fun(range_val), label='Terrain Slope')
    plt.scatter(experiment['alpha_dist'], star_vals, color='r', marker='*', s=150, label='Given Values')
    plt.ylabel('Terrain Angle (deg)')
    plt.xlabel('Position (m)')
    plt.title('Terrain Angle vs Position')
    plt.legend()
    plt.show()
    
    return


experiment_visualization()

