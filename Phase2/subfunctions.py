# Names: Michael Hager, Elizabeth Sharf, Savera Sahai
# MEEN 357 - Group 14


import math
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
from scipy.integrate import simpson
from statistics import mean


# Computes rover mass in kg
def get_mass(rover):
    if type(rover) != dict:
        raise Exception('Input must be a dict')

    m = rover['chassis']['mass'] + rover['power_subsys']['mass'] + rover['science_payload']['mass'] + 6*rover['wheel_assembly']['motor']['mass'] + 6*rover['wheel_assembly']['speed_reducer']['mass'] + 6*rover['wheel_assembly']['wheel']['mass']

    return m


# Computes gear ratio
def get_gear_ratio(speed_reducer):
    if type(speed_reducer) != dict:
        raise Exception('Input must be a dict')

    if speed_reducer['type'].lower() != 'reverted':
        raise Exception('The speed reducer type is not recognized.')

    d1 = speed_reducer['diam_pinion']
    d2 = speed_reducer['diam_gear']

    Ng = (d2/d1)**2

    return Ng


# Computes motor shaft torque in Nm
def tau_dcmotor(omega, motor):
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')

    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega],dtype=float) # make the scalar a numpy array

    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    if type(motor) != dict:
        raise Exception('Second input must be a dict')

    tau_s    = motor['torque_stall']
    tau_nl   = motor['torque_noload']
    omega_nl = motor['speed_noload']

    tau = np.zeros(len(omega),dtype = float)

    for ii in range(len(omega)):
        if omega[ii] >= 0 and omega[ii] <= omega_nl:
            tau[ii] = tau_s - (tau_s-tau_nl)/omega_nl *omega[ii]
        elif omega[ii] < 0:
            tau[ii] = tau_s
        elif omega[ii] > omega_nl:
            tau[ii] = 0

    return tau




# Computes force on rover due to rolling resistance
def F_rolling(omega, terrain_angle, rover, planet, Crr):
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega],dtype=float) # make the scalar a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    if (type(terrain_angle) != int) and (type(terrain_angle) != float) and (not isinstance(terrain_angle, np.ndarray)):
        raise Exception('Second input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(terrain_angle, np.ndarray):
        terrain_angle = np.array([terrain_angle],dtype=float) # make the scalar a numpy array
    elif len(np.shape(terrain_angle)) != 1:
        raise Exception('Second input must be a scalar or a vector. Matrices are not allowed.')

    if len(omega) != len(terrain_angle):
        raise Exception('First two inputs must be the same size')

    if max([abs(x) for x in terrain_angle]) > 75:    
        raise Exception('All elements of the second input must be between -75 degrees and +75 degrees')

    if type(rover) != dict:
        raise Exception('Third input must be a dict')

    if type(planet) != dict:
        raise Exception('Fourth input must be a dict')

    if (type(Crr) != int) and (type(Crr) != float):
        raise Exception('Fifth input must be a scalar')

    if Crr <= 0:
        raise Exception('Fifth input must be a positive number')

    m = get_mass(rover)
    g = planet['g']
    r = rover['wheel_assembly']['wheel']['radius']
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])

    v_rover = r*omega/Ng

    Fn = np.array([m*g*math.cos(math.radians(x)) for x in terrain_angle],dtype=float)
    Frr_simple = -Crr*Fn
    Frr = np.array([math.erf(40*v_rover[ii]) * Frr_simple[ii] for ii in range(len(v_rover))], dtype = float)

    return Frr


# Computes force on rover due to gravity in N
def F_gravity(terrain_angle, rover, planet):
    if (type(terrain_angle) != int) and (type(terrain_angle) != float) and (not isinstance(terrain_angle, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(terrain_angle, np.ndarray):
        terrain_angle = np.array([terrain_angle],dtype=float) # make the scalar a numpy array
    elif len(np.shape(terrain_angle)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    if max([abs(x) for x in terrain_angle]) > 75:    
        raise Exception('All elements of the first input must be between -75 degrees and +75 degrees')

    if type(rover) != dict:
        raise Exception('Second input must be a dict')

    if type(planet) != dict:
        raise Exception('Third input must be a dict')

    m = get_mass(rover)
    g = planet['g']
    Fgt = np.array([-m*g*math.sin(math.radians(x)) for x in terrain_angle], dtype = float)

    return Fgt


# Computes force on rover due to drive system in N
def F_drive(omega, rover):
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega],dtype=float) # make the scalar a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    if type(rover) != dict:
        raise Exception('Second input must be a dict')

    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    tau_out = tau*Ng

    r = rover['wheel_assembly']['wheel']['radius']

    Fd_wheel = tau_out/r 

    Fd = 6*Fd_wheel

    return Fd


# Computes net force acting on rover in direction of motion in N
def F_net(omega, terrain_angle, rover, planet, Crr):
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega],dtype=float) # make the scalar a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    if (type(terrain_angle) != int) and (type(terrain_angle) != float) and (not isinstance(terrain_angle, np.ndarray)):
        raise Exception('Second input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(terrain_angle, np.ndarray):
        terrain_angle = np.array([terrain_angle],dtype=float) # make the scalar a numpy array
    elif len(np.shape(terrain_angle)) != 1:
        raise Exception('Second input must be a scalar or a vector. Matrices are not allowed.')

    if len(omega) != len(terrain_angle):
        raise Exception('First two inputs must be the same size')

    if max([abs(x) for x in terrain_angle]) > 75:    
        raise Exception('All elements of the second input must be between -75 degrees and +75 degrees')

    if type(rover) != dict:
        raise Exception('Third input must be a dict')

    if type(planet) != dict:
        raise Exception('Fourth input must be a dict')

    if (type(Crr) != int) and (type(Crr) != float):
        raise Exception('Fifth input must be a scalar')

    if Crr <= 0:
        raise Exception('Fifth input must be a positive number')

    Fd = F_drive(omega, rover)
    Frr = F_rolling(omega, terrain_angle, rover, planet, Crr)
    Fg = F_gravity(terrain_angle, rover, planet)
    Fnet = Fd + Frr + Fg # signs are handled in individual functions

    return Fnet




# Computes the rotational speed of the motor shaft in rad/s
def motorW(v, rover):
    if (type(v) != int) and (type(v) != float) and (not isinstance(v, np.ndarray)):
        raise Exception('v input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(v, np.ndarray):
        v = np.array([v],dtype=float) # make the scalar a numpy array
    elif len(np.shape(v)) != 1:
        raise Exception('v input must be a scalar or a vector. Matrices are not allowed.')

    if type(rover) != dict:
        raise Exception('rover input must be a dict')

    r = rover['wheel_assembly']['wheel']['radius']
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    w = v*Ng/r

    return w


# Computes the derivative of the state vector (state vector is: [velocity, position]) for the rover given its current state
def rover_dynamics(t, y, rover, planet, experiment):
    if (type(t) != int) and (type(t) != float) and (not isinstance(t, np.ndarray)) and (not isinstance(t,np.float64)):
        raise Exception('t input must be a scalar.')
    elif isinstance(t, np.ndarray):
        if len(t) == 1:
            t = float(t) # make a scalar
        else:
            raise Exception('t input must be a scalar.')

    if (not isinstance(y, np.ndarray)) or (len(y) != 2):
        raise Exception('y must be a 2x1 numpy array.')
    elif isinstance(y[0], np.ndarray):
        y = np.array([float(y[0]),float(y[1])]) # this will turn the column vector into a row

    if type(rover) != dict:
        raise Exception('rover input must be a dict')

    if type(planet) != dict:
        raise Exception('planet input must be a dict')

    if type(experiment) != dict:
        raise Exception('experiment input must be a dict')

    v = float(y[0]) # velocity
    x = float(y[1]) # position

    omega = motorW(v, rover)   
    alpha_fun = interp1d(experiment['alpha_dist'].ravel(), experiment['alpha_deg'].ravel(), kind = 'cubic', fill_value="extrapolate")
    terrain_angle = float(alpha_fun(x))
    F = F_net(omega, terrain_angle, rover, planet, experiment['Crr'])

    m = get_mass(rover)
    accel = float(F/m)
    dydt = np.array([accel, v], dtype = float)

    return dydt


# Computes the instantaneous mechanical power output by a single DC motor at each point in a given velocity profile
def mechpower(v, rover):
    if (type(v) != int) and (type(v) != float) and (not isinstance(v, np.ndarray)):
        raise Exception('v input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(v, np.ndarray):
        v = np.array([v],dtype=float) # make the scalar a numpy array
    elif len(np.shape(v)) != 1:
        raise Exception('v input must be a scalar or a vector. Matrices are not allowed.')

    if type(rover) != dict:
        raise Exception('rover input must be a dict')

    omega = motorW(v, rover)  
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor']) 
    P = tau*omega

    return P


# Computes the total electrical energy consumed from the rover battery pack over a simulation profile, defined as time-velocity pairs
def battenergy(t,v,rover):
    if (not isinstance(t, np.ndarray)):
        raise Exception('t input must be a scalar or a vector. If t is a vector, it should be defined as a numpy array.')
    elif len(np.shape(t)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    if (not isinstance(v, np.ndarray)):
        raise Exception('v input must be a scalar or a vector. If v is a vector, it should be defined as a numpy array.')
    elif len(np.shape(v)) != 1:
        raise Exception('v input must be a scalar or a vector. Matrices are not allowed.')

    if len(t) != len(v):
        raise Exception('First two inputs must be the same size')

    P = mechpower(v, rover) # calculate power at each time/velocity
    omega = motorW(v, rover) # calculate motor speed (used in next line)
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor']) # calculate torque (used for efficiency info)

    #effcy_tau = rover['wheel_assembly']['motor']['effcy_tau'] # change to 1D array
    #effcy = rover['wheel_assembly']['motor']['effcy']
    effcy_fun = interp1d([0, 10, 20, 40, 75, 165], [0, 0.60, 0.75, 0.73, 0.55, 0.05], kind = 'cubic') # fit the cubic spline
    effcy_dat = effcy_fun(tau)

    P_batt = P/effcy_dat
    E_motor = simpson(P_batt, t)
    E = 6*E_motor # 6 wheels, each with a dedicated motor

    return E


# Integrates the trajectory of the rover
def simulate_rover(rover,planet,experiment,end_event):
    if type(rover) != dict:
        raise Exception('rover input must be a dict')

    if type(planet) != dict:
        raise Exception('planet input must be a dict')

    if type(experiment) != dict:
        raise Exception('experiment input must be a dict')

    if type(end_event) != dict:
        raise Exception('end_event input must be a dict')

    fun = lambda t,y: rover_dynamics(t, y, rover, planet, experiment) # differential equation
    t_span = experiment['time_range'] # time span
    y0 = experiment['initial_conditions'].ravel() # initial conditions
    events = end_of_mission_event(end_event) # stopping criteria
    sol = solve_ivp(fun, t_span, y0, method = 'BDF', events=events) #t_eval=(np.linspace(0, 3000, 1000)))  # need a stiff solver like BDF

    v_max = max(sol.y[0,:])
    v_avg = mean(sol.y[0,:])
    P = mechpower(sol.y[0,:], rover)
    E = battenergy(sol.t,sol.y[0,:],rover)

    telemetry = {'Time' : sol.t,

                 'completion_time' : sol.t[-1],

                 'velocity' : sol.y[0,:],

                 'position' : sol.y[1,:],

                 'distance_traveled' : sol.y[1,-1],  # Matlab version had an integration of velocity over time, but if velocity must be positive (defined by min_velocity), then the final position is the distance traveled

                 'max_velocity' : v_max,

                 'average_velocity' : v_avg,

                 'power' : P,

                 'battery_energy' : E,

                 'energy_per_distance' : E/sol.y[1,-1]}

    rover['telemetry'] = telemetry

    return rover


# Defines an event that terminates the mission simulation
def end_of_mission_event(end_event):
    mission_distance = end_event['max_distance']
    mission_max_time = end_event['max_time']
    mission_min_velocity = end_event['min_velocity']

    distance_left = lambda t,y: mission_distance - y[1]
    distance_left.terminal = True    

    time_left = lambda t,y: mission_max_time - t
    time_left.terminal = True
    time_left.direction = -1

    velocity_threshold = lambda t,y: y[0] - mission_min_velocity;
    velocity_threshold.terminal = True

    events = [distance_left, time_left, velocity_threshold]

    return events

