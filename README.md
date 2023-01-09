# Mars-Rover
In my Engineering Analysis course here at Texas A&M University, I was given a semester project dealing with a rover on mars. This involved building functions, writing scripts, and professionally reporting our teams progress. This repository will include our code which was all in Python, as well as our reports. There were four phases for this project.

# Phase 1
In phase 1 of this project, we implemented Python functions for analyzing the rover, built Python script files to visually show the changes of the rovers speed given changes in the rovers properties, and answered questions related to our work. This phase is split up into three parts.

## Part 1
In phase 1 part 1, our team was responsible for implementing several Python functions that would be used for analyzing the rover's capabilities. These functions were then reused during the following phases of the project.

### get_mass
Returns calculated total mass of rover using information in rover dictionary.

### get_gear_ratio
Returns the speed reduction ratio for the speed reducer based on speed_reducer dictionary.

### tau_dcmotor
Returns the motor shaft torque when given motor shaft speed and a dicitonary conataining important specifications for the motor.

### F_drive
Returns the force applied to the rover by the drive system given information about the drive system (wheel_assembly) and the motor shaft speed. 

### F_gravity
Returns the magnitude of the force component acting on the rover in the direction of its translational motion due to gravity as a function of terrain inclination angle and rover properties.

### F_rolling
Returns the magnitude of the force acting on the rover in the direction of its translational motion due to rolling resistances given the terrain inclination angle, rover properties, and a rolling resistance coefficient.

### F_net
Returns the magnitude of net force acting on the rover in the direction of its translational motion.

## Part 2
In phase 1 part 2, we built Python scripts to help analyze our current functions and the rover system. These python scripts included the following Python files.

### *graphs_motor.py*
Graphs of the DC motor.

### *graphs_sr.py*
Graphs of the impact of the speed reducer.

### *analysis_terrain_slope.py*
Analysis of maximum attainable rover speed over various terrain situations using root-finding methods.

### *analysis_rolling_resistance.py*
Analysis of speed of rover at various values for the coefficient of rolling resistance using root-finding methods.

### *analysis_combined_terrain.py*
Analysis of speed of rover given various values for the coefficient of rolling resistance and terrain slope using root-finding methods.

## Part 3
In phase 1 part 3, our group submitted a report answering coding questions related to the Python functions and scripts that were made in this phase. These questions included the following.

### Question 1:
We had you define the acceleration due to gravity as a field in a structure that you had to pass as an input argument to several functions. Instead, we could have had you type the value for the constant, 3.72 m/s2, directly in those functions. Do you believe there is an advantage to how we had you do it? Explain. Would you have done it differently? Explain why or why not.

### Question 2:
What happens if you try to call F_gravity using a terrain slope of 110 degrees? Is this desirable behavior? Explain why you think this.

### Question 3:
What is the maximum power output by a single rover motor? At what motor shaft speed does this occur? Provide graphs or other data to support your answer.

### Question 4:
What impact does the speed reducer have on the power output of the drive system? Again, provide any graphs or supporting data.

### Question 5:
Examine the graph you generated using *analysis_terrain_slope.py*. (Provide the graph in your response for reference.) Explain the trend you observe. Does it make sense physically? Why or why not? Please be precise. For example, if the graph appears linear or non-linear, can you explain why it should be the way you observed? Refer back to the rover model and how slope impacts rover behavior.

### Question 6:
Examine the graph you generated using *analysis_rolling_resistance.py*. (Provide the graph in your response for reference.) Explain the trend you observe. Does it make sense physically? Why or why not? Please be precise. For example, if the graph appears linear or non-linear, can you explain why it should be the way you observed? Refer back to the rover model and how the coefficient of rolling resistance impacts rover behavior.

### Question 7:
Examine the surface plot you generated using *analysis_combined_terrain.py*. (Provide the graph in your response for reference.) What does this graph tell you about the physical conditions under which it is appropriate to operate the rover? Based on what you observe, which factor, terrain slope or coefficient of rolling resistance, is the dominant consideration in how fast the rover can travel? Please explain your reasoning.

# Phase 2
In phase 2 of the project, we implemented code in Python geared towards simulating the trajectory of the rover and estimating the energy storage needs of the rover. This phase contains nine tasks.

### Task 1: Helper function motorW
To simplify coding and minimize the possibility of typos and other bugs, programmers often create several “helper” functions that compute commonly-needed results. You are instructed to create a helper function in Python called motorW, which computes the rotational speed of the motor given the translational velocity of the rover and a definition for the rover itself. This function should be added to your subfunctions.py file.

### Task 2: Visualizing the Terrain
To test the rover system you have been provided with a terrain representation containing distance and terrain-angle pairs. This data is in the *define_experiment.py* file. You will create a Python script called *experiment_visualization.py* to graph the experimental terrain. To calculate terrain angles between data points, you will first define an interpolation function using the following line of code (note that the interp1d function is part of the scipy.interpolate library):

*alpha_fun = interp1d(alpha_dist, alpha_deg, kind = 'cubic', fill_value=’extrapolate’) # 
fit the cubic spline*

This function can then be used to calculate the terrain angle at various distances along your rover’s path. Your script should evaluate the terrain angle using 100 points, evenly spaced between the minimum and maximum distance (experiment[‘alpha_dist’] contains distance information) in the experiment file. The script should create a single figure of terrain angle vs. position with the data contained in *define_experiment.py* plotted as starsymbols, and the 100 evaluated terrain angles plotted as a line. Axes should be labeled appropriately. Please include a copy of your figure and an explanation of what you are observing in your write-up.

### Task 3: rover_dynamics
For this task you will implement a function called rover_dynamics that is compatible for use with an ODE solver. This function should be added to your *subfunctions.py* file.

### Task 4: mechpower
For this task you will create a Python function called mechpower that computes the instantaneous mechanical power output by a single DC motor at each point in a simulation run, in Watts. This function takes data about rover velocity during a simulation run, in m/s, and a rover dictionary as input. This function should be added to your *subfunctions.py* file.

### Task 5: Visualizing Motor Efficiency
In this task you will create a script called *efficiency_visualization.py* to plot motor torque vs. efficiency. The rover dictionary should contain data points for efficiency as a function of torque as noted in Section 4. To calculate efficiency values at torque values not listed in the rover dictionary, define an interpolation function using the following line of code:

*effcy_fun = interp1d(effcy_tau, effcy, kind = 'cubic') # fit the cubic spline*

where effcy_tau is the torque data and effcy is the efficiency data in the rover dictionary. Your script should evaluate the efficiency using 100 points, evenly spaced between the minimum and maximum motor torque given in the rover dictionary. The script should create a single figure of efficiency vs. torque with the data contained in the rover struct plotted as star symbols, and the 100 evaluated efficiencies plotted as a line. Axes should be labeled appropriately. Please include a copy of your figure and an explanation of what you are observing in your write-up.

### Task 6: battenergy
For this task you will create a Python function called battenergy that computes the total energy consumed, in Joules, from the rover batteries over the course of a simulation run. The function takes time-velocity data pairs from a simulation run and a rover dictionary as input. This function should be added to your *subfunctions.py* file.

### Task 7: simulate_rover
For this task you will integrate a trajectory of the rover specified by the experiment and end_event dictionaries. The function should populate all subfields of the rover[‘telemetry’] dictionary. This function should be added to your *subfunctions.py* file.

### Task 8: Rover Simulation
For this task you will create a Python script, *rover_experiment1.py* to simulate the trajectory of the rover using the simulate_rover function. You need to load the experiment and end_event dictionaries. You should also set end_event fields to the following values:

- end_event.max_distance = 1000
- end_event.max_time = 10000
- end_event.min_velocity = 0.01

The script should create a single figure with three subfigures (in a 3x1 arrangement):

1. Position vs. time
2. Velocity vs. time
3. Power vs. time

For this task you should also include the figure in your write-up and explain what you observe. The explanation must be based on what you know about the particular terrain that the rover must traverse. Do the results make sense? Why or why not?

Finally, please include a table of the rover[‘telemetry’] data for the fields: completion_time, distance_traveled, max_velocity, average_velocity, battery_energy, and batt_energy_per_distance. 

### Task 9: Analysis of Energy Needs
Your boss has informed you that the rover will be equipped with a 0.9072e6 [J] Lithium Iron Phosphate battery back. Can the rover complete the case defined by experiment1 (in *define_experiment.py*) with this battery pack? Please include your answer to this question and how you arrived at it in your write-up.

# Phase 3
In phase 3, we are going to analyze the entry, descent, and landing process of the rover. Our challenge as a group is to take over the EDL analysis where another team has left off. This phase contains six tasks.

### Task 1: Create Documentation for the Data Dictionaries used in the code
The previous team used Python dictionaries extensively in their code. These dictionaries are defined in separate files that are called from the main script. Although they did an okay job at commenting the files that define the dictionaries, they made no formal documentation of their contents. Your task is to go through the code and create documentation for the dictionaries. For each dictionary, you should identify and describe every one of its fields (some fields may themselves be dictionaries). Be sure to include the name of the field, its default value, its units (if applicable) and a description of its meaning.

### Task 2: Create Documentation for Each Function in *subfunctions_EDL.py*
Your predecessors created many functions in Python, all of which are included in the zip file in *subfunctions_EDL.py*. Create documentation for each of these. This documentation should include the following:

1. Function name. Please get the case correct.
2. Calling syntax. There may be more than one valid way to call this function. The calling syntax should list all valid variations on how the function can be called.
3. Description. This describes how the function behaves. This may depend on how the function is called, so be sure to clarify such dependencies. Please note any physics of the EDL that are modeled by the function.
4. Input arguments. List the input arguments in their calling order, state their “type” (vector, scalar, string, etc.), define their meaning, and, if applicable, note their units. If an input argument is optional, note this fact and, if applicable, indicate its default value.
5. Output arguments. List the arguments in their return order, state their type, and define their meaning and, if applicable, units.

You can use the documentation approach we have been using in previous phases of the project as a rough template.

### Task 3: Explain the Loop in simulate_edl
There is a while loop inside the function simulate_edl. The purpose of this loop is to simulate the EDL system as it descends through the Martian atmosphere and lowers the rover to the Martian surface. Notice that there is a call to an ODE solver (specifically, DOP853 because we need the higher accuracy over RK45) and a call to another function, update_edl_state, that is in *subfunctions_EDL.py* as well. The loop continues until some termination condition is met. The ODE solver is run every pass through the loop, but with different initial conditions and, potentially, a redefined edl_system dictionary. Since the purpose of this loop is to simulate the EDL system, any redefinition of edl_system has to do with changes in the physical operation of the system.

Your team is instructed to create detailed documentation of how this loop works. This includes explaining how calls to DOP853 and update_edl_state work together to simulate the appropriate physics regime as the system goes through its different operational phases (parachute only, firing rockets, etc.). It is recommended that you create a flowchart or other illustration to support your explanation.

### Task 4: Document the Execution Flow of the Code
One thing you are told about this code is that executing the script *main_edl_simulation.py* launches a simulation of the EDL process. Your team must document the dependencies between functions (which functions/scripts call other functions and in what order). Create a flow chart, block diagram, or something similar to illustrate the execution flow of the code. Include an explanation along with your illustration in your report.

### Task 5: Evaluate the Impact of Changing the Parachute Size
Your team has been asked to conduct a study of the impact on EDL performance of changing the parachute size. For this task, you must do two things: (1) create a Python script called *study_parachute_size.py* that conducts the analysis and generates useful visualizations of the results (defined below) and (2) include in your report an interpretation of these results. Use the following initial conditions:

- EDL System Altitude: 11 km
- EDL System Velocity: -578 m/s
- Rockets: Off
- Parachute: Deployed, not ejected
- Heat shield: Not ejected
- Sky crane: Off 
- Speed controller: Off
- Position controller: Off

The parachute study should consider parachute diameters from 14 to 19 meters at 0.5 meter intervals. The critical figure of merit is whether the rover reaches the ground safely. Your script should create a 3x1 array of plots (using the plt.subplots command):

1. Simulated time (i.e., time at termination of simulation) vs. parachute diameter
2. Rover speed (relative to ground) at simulation termination vs. parachute diameter
3. Rover landing success (1=success; 0=failure) vs. parachute diameter

Make sure each graph has its axes labeled clearly with associated units.

In your interpretation, please make a well-supported recommendation as to the appropriate diameter or range of diameters for the parachute. The critical requirement is that the rover reaches the ground safely. A secondary consideration is the time it takes to get the rover on the ground (we prefer to minimize this time). 

### Task 6: Improve the Parachute Drag Model
The drag model used in the code you are given involves a strong assumption: that the coefficient of drag for the parachute is independent of the speed of descent. We know this is incorrect from physical experimentation on similar parachutes. In particular, drag near and above Mach 1 is nonlinear. However, it is unclear whether this idealization is significant for our purposes (i.e., it may or may not affect conclusions we draw about the design). Your team is tasked with revising the drag model and reexamining your parachute diameter recommendations using the revised model.

You can model the modified parachute drag using the following relationship:

*CD,mod = MEF(M) ∙ CD*,

where 𝐶𝐷 is the coefficient of drag at sub-Mach speeds and 𝑀𝐸𝐹 is a Mach efficiency factor that is determined experimentally and is a function of the descent velocity, 𝑀, expressed in Mach number. You can used the function v2M_Mars to convert from speed in m/s to a Mach number.

You will need to create a model for the 𝑀𝐸𝐹 value at a given Mach number. You are given the following data (see table) obtained from tests of similar parachute systems. 

Modify the drag code included in the code distribution to use this new model.

In your report, you must document: (1) how you created a continuous model for 
your MEF data, including the rationale for your modeling choices and (2) your 
assessment of whether the parachute diameter recommendations require 
modification. Please include any supporting data and graphs in your report. If you 
created any new scripts/functions to support your analysis, please name them and 
explain what they do in your report.

# Phase 4
In phase 4, we designed an edl+rover system that we believe best solves the problem of this semester project. We submitted this design to compete against other groups in the class. The goal of the design is for the rover to land safely and travel along the martian surface to reach a set point in the terrain faster than the other groups.
