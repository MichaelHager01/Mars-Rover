from scipy.interpolate import interp1d
from subfunctions import *
import matplotlib.pyplot as plt
from define_rovers import *


def efficiency_visualization():
    rover, planet  = define_rover_1()
    
    effcy_tau = rover['wheel_assembly']['speed_reducer']['effcy_tau']
    effcy = rover['wheel_assembly']['speed_reducer']['effcy']
    
    tau = np.linspace(min([t for t in effcy_tau]), max([t for t in effcy_tau]), 100)
    
    effcy_fun = interp1d(effcy_tau, effcy, kind = 'cubic')
    eff = effcy_fun(tau)

    #Plotting graph of Efficiency vs. Torque
    plt.scatter(effcy_tau, effcy, c='r' ,marker='*', s=150, label = 'Given Values') 
    plt.plot(tau,eff, label = 'Efficiency Slope')
    plt.xlabel("Torque (Nm)")
    plt.ylabel("Efficiency (%)")
    plt.title("Efficiency v. Torque")
    plt.legend()
    plt.show()
    

efficiency_visualization()

