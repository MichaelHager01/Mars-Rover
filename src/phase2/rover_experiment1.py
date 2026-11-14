from define_experiment import *
from subfunctions import simulate_rover
import matplotlib.pyplot as plt
from define_rovers import *


def rover_experiment1():
    experiment, end_event = experiment1()
    rover, planet = define_rover_1()
    
    end_event['max_distance'] = 1000
    end_event['max_time'] = 10000
    end_event['min_velocity'] = 0.01
    
    rover = simulate_rover(rover, planet, experiment, end_event)
    
    # For Table
    completion_time = rover['telemetry']['completion_time']
    distance_traveled = rover['telemetry']['distance_traveled']
    max_velocity = rover['telemetry']['max_velocity']
    average_velocity = rover['telemetry']['average_velocity']
    battery_energy = rover['telemetry']['battery_energy']
    batt_energy_per_dist = rover['telemetry']['energy_per_distance']
    # print(completion_time)
    # print(distance_traveled)
    # print(max_velocity)
    # print(average_velocity)
    # print(battery_energy)
    # print(batt_energy_per_dist)
    
    # For Graphs
    time = rover['telemetry']['Time']
    position = rover['telemetry']['position']
    velocity = rover['telemetry']['velocity']
    power = rover['telemetry']['power']
    
    #Graph of Position vs. Time
    plt.subplot(3,1,1)
    plt.plot(time, position)
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Position vs. Time")
    
    #Graph of Velocity vs. Time
    plt.subplot(3,1,2)
    plt.plot(time, velocity)
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity vs. Time")
    
    #Graph of Power vs. Time
    plt.subplot(3,1,3)
    plt.plot(time, power)
    plt.xlabel("Time (s)")
    plt.ylabel("Power (W)")
    plt.title("Power vs. Time")
    
    plt.tight_layout()
    plt.show()
    
    
rover_experiment1()

