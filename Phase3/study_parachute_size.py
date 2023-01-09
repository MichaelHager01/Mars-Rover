# Names: Michael Hager, Elizabeth Sharf, Savera Sahai
# MEEN 357 - Group 14

import numpy as np
import matplotlib.pyplot as plt
from define_edl_system import *
from subfunctions_EDL import *
from define_planet import *
from define_mission_events import *

# Load dictionaries defined from imports
edl_system = define_edl_system_1()
mars = define_planet()
mission_events = define_mission_events()

p_d = np.arange(14,19.5,0.5)

t_max = 2000
sim_time = []
rover_speed = []
success = []

for d in p_d:
    # Setting/resetting initial conditions for calculations
    edl_system['altitude'] = 11000      # meters
    edl_system['velocity'] = -578      # meters/second
    edl_system['rocket']['on'] = False
    edl_system['parachute']['deployed'] = True
    edl_system['parachute']['ejected'] = False
    edl_system['heat_shield']['ejected'] = False
    edl_system['sky_crane']['on'] = False
    edl_system['speed_control']['on'] = False
    edl_system['position_control']['on'] = False
    edl_system['parachute']['diameter'] = d
    
    # Run simulation
    T, Y, edl_system = simulate_edl(edl_system, mars, mission_events, t_max, False)
         
    sim_time.append(T[-1])
    
    # Calculatin rover speed
    speed_rover = Y[0,-1]
    speed_crane = Y[5,-1]
    tot_speed = speed_rover - speed_crane
    
    rover_speed.append(tot_speed)
    
    # Calculating total altitude
    alt_edl = Y[1,-1]
    alt_crane = Y[6,-1]
    tot_alt = alt_edl - alt_crane
    
    # Checking mission success criteria
    if abs(tot_speed) <= 1:
        if tot_alt >= 4.5:
            success.append(1)
    else:
        success.append(0)
  

# Plotting
plt.subplot(3,1,1)
plt.plot(p_d, sim_time, 'maroon')
plt.xlabel("Parachute Diameter (m)")
plt.ylabel("Simulated Time (s)")
plt.title("Time v. Diameter")
plt.subplot(3,1,2)
plt.plot(p_d, rover_speed, 'gray')
plt.xlabel("Parachute Diameter (m)")
plt.ylabel('Rover Speed (m/s)')
plt.title('Speed v. Diameter')
plt.subplot(3,1,3)
plt.plot(p_d, success, 'b*')
plt.xlabel("Parachute Diameter (m)")
plt.ylabel('Rover Landing Success')
plt.title('Success v. Diamter')

plt.tight_layout()
plt.show()

