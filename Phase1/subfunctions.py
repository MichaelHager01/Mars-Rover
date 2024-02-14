import numpy as np
from math import *


# Computes rover mass in kg
def get_mass(rover):
    if (str(type(rover)) != "<class 'dict'>"):
        raise Exception('Variable is not a dictionary')
    
    m_chassis = rover['chassis']['mass']
    m_power_subsys = rover['power_subsys']['mass']
    m_science_payload = rover['science_payload']['mass']
    m_wheel_assemblies = (6 * rover['wheel_assembly']['wheel']['mass']) + (6 * rover['wheel_assembly']['speed_reducer']['mass']) + (6 * rover['wheel_assembly']['motor']['mass'])
    
    m =  m_chassis + m_power_subsys + m_science_payload + m_wheel_assemblies
    
    return m


# Computes gear ratio
def get_gear_ratio(speed_reducer):
    if (str(type(speed_reducer)) != "<class 'dict'>"):
        raise Exception('Variable is not a dictionary')
    
    if (speed_reducer['type'].lower() != 'reverted'):
        raise Exception('Variable type is not reverted')
    
    Ng = (speed_reducer['diam_gear'] / speed_reducer['diam_pinion'])**2
    
    return Ng


# Computes motor shaft torque in Nm
def tau_dcmotor(omega, motor):
    if (not ((str(type(omega)) == "<class 'numpy.ndarray'>") or (str(type(omega)) == "<class 'float'>") or (str(type(omega)) == "<class 'int'>"))):
        raise Exception('Omega is not scalar or array')
    
    if (str(type(motor)) != "<class 'dict'>"):
        raise Exception('Variable is not a dictionary')
    
    w_nl = motor['speed_noload']
    t_nl = motor['torque_noload']
    t_s = motor['torque_stall']
    
    if ((str(type(omega)) == "<class 'numpy.ndarray'>")):
        try:    
            new_w = []
            for w in omega:
                if (w > w_nl):
                    tau = 0
                elif (w < 0):
                    tau = t_s
                else:
                    tau = t_s - (((t_s - t_nl) / radians(w_nl)) * radians(w))
                    
                new_w.append(tau)
                
            tau = np.array(new_w)
        except:
            raise Exception('First input must be a scalar or a vector, Matrices are not allowed')
        
    else:
        w = omega
        if (w > w_nl):
            tau = 0
        elif (w < 0):
            tau = t_s
        else:
            tau = t_s - (((t_s - t_nl) / radians(w_nl)) * radians(w))

    return tau


# Computes force on rover due to drive system in N
def F_drive(omega, rover):
    if (not ((str(type(omega)) == "<class 'numpy.ndarray'>") or (str(type(omega)) == "<class 'float'>") or (str(type(omega)) == "<class 'int'>"))):
        raise Exception('Omega is not scalar or array')
    
    if (str(type(rover)) != "<class 'dict'>"):
        raise Exception('Variable is not a dictionary')
        
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    r = rover['wheel_assembly']['wheel']['radius']

    if ((str(type(tau)) == "<class 'numpy.ndarray'>")):
        Fdd = []
        for t in tau:
            temp = 6 * t * Ng / r
            Fdd.append(temp)
            
        Fd = np.array(Fdd)
          
    else:
        Fd = 6 * (tau * Ng) / r
        
    return Fd


# Computes force on rover due to gravity in N
def F_gravity(terrain_angle, rover, planet):
    if (not ((str(type(terrain_angle)) == "<class 'numpy.ndarray'>") or (str(type(terrain_angle)) == "<class 'float'>") or (str(type(terrain_angle)) == "<class 'int'>"))):
        raise Exception('Terrain angle is not scalar or array')
    
    if ((str(type(terrain_angle)) == "<class 'numpy.ndarray'>")):
        try:
            for angle in terrain_angle:
                if ((angle < -75) or (angle > 75)):
                    raise Exception('Angle(s) not valid')
        except:
            raise Exception('First input must be a scalar or a vector, Matrices are not allowed')
            
    else:
        if ((terrain_angle < -75) or (terrain_angle > 75)):
            raise Exception('Angle(s) not valid')
            
    if ((str(type(rover)) != "<class 'dict'>") or (str(type(planet)) != "<class 'dict'>")):
        raise Exception('Variable(s) is not a dictionary')
        
    m = get_mass(rover)
    
    if ((str(type(terrain_angle)) == "<class 'numpy.ndarray'>")):
        angle_new = []
        for angle in terrain_angle:
            Fgt = -m * planet['g'] * sin(radians(angle))
            angle_new.append(Fgt)
            
        Fgt = np.array(angle_new)
    
    else:
        Fgt = -m * planet['g'] * sin(radians(terrain_angle))

    return Fgt


# Computes force on rover due to rolling resistance
def F_rolling(omega, terrain_angle, rover, planet, Crr):
    if (not ((str(type(omega)) == "<class 'numpy.ndarray'>") or (str(type(omega)) == "<class 'float'>") or (str(type(omega)) == "<class 'int'>"))):
        raise Exception('Omega is not scalar or array')
        
    if (not ((str(type(terrain_angle)) == "<class 'numpy.ndarray'>") or (str(type(terrain_angle)) == "<class 'float'>") or (str(type(terrain_angle)) == "<class 'int'>"))):
        raise Exception('Terrain angle is not scalar or array')
        
    if (str(type(terrain_angle)) == "<class 'numpy.ndarray'>") and (str(type(omega)) == "<class 'numpy.ndarray'>"):
        if (len(omega) != len(terrain_angle)):
            raise Exception('Terrain angle and Omega are not the same size')
    elif ((str(type(omega)) == "<class 'float'>") or (str(type(omega)) == "<class 'int'>")) and ((str(type(terrain_angle)) == "<class 'float'>") or (str(type(terrain_angle)) == "<class 'int'>")):
        Frr = 0
    else:
        raise Exception('Terrain angle and Omega are not the same type')
    
    if ((str(type(terrain_angle)) == "<class 'numpy.ndarray'>")):
        try:
            for angle in terrain_angle:
                if ((angle < -75) or (angle > 75)):
                    raise Exception('Angle(s) not valid')
        except:
            raise Exception('First input must be a scalar or a vector, Matrices are not allowed')
            
    else:
        if ((terrain_angle < -75) or (terrain_angle > 75)):
            raise Exception('Angle(s) not valid')

    if ((str(type(rover)) != "<class 'dict'>") or (str(type(planet)) != "<class 'dict'>")):
        raise Exception('Variable(s) is not a dictionary')
        
    try:
        if (Crr < 0):
            raise Exception('Crr is negative')
    except:
        raise Exception('Crr is not a scalar')
        
    m = get_mass(rover)
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    r = rover['wheel_assembly']['wheel']['radius']
    
    if (str(type(omega)) == "<class 'numpy.ndarray'>"):
        try:
            v_r = []
            for w in omega:
                v = w * r
                v_r.append(v)
                
            v_rover = np.array(v_r)
        except:
            raise Exception('First input must be a scalar or a vector, Matrices are not allowed')
            
    else:
        v_rover = r * omega
    
    if (str(type(terrain_angle)) == "<class 'numpy.ndarray'>"):
        Fn = []
        for angle in terrain_angle:
            F = -m * planet['g'] * cos(radians(angle))
            Fn.append(F)
            
        Fn = np.array(Fn)
    else:
        Fn = -m * planet['g'] * cos(radians(terrain_angle))
        
    if (str(type(terrain_angle)) == "<class 'numpy.ndarray'>"):
        Frr = []
        for F in Fn:
            Fr = Crr * F
            Frr.append(Fr)
            
        Frr_simple = np.array(Frr)
    else:
        Frr_simple = Crr * Fn

    if (str(type(terrain_angle)) == "<class 'numpy.ndarray'>"):
        Frr = []
        for i in range(len(v_rover)):
            Fr = erf(40 * v_rover[i]) * Frr_simple[i]
            Frr.append(Fr)
            
        Frr = np.array(Frr)
    else:
        Frr = erf(40 * v_rover) * Frr_simple
    
    return Frr


# Computes net force acting on rover in direction of motion in N
def F_net(omega, terrain_angle, rover, planet, Crr):
    if (not ((str(type(omega)) == "<class 'numpy.ndarray'>") or (str(type(omega)) == "<class 'float'>") or (str(type(omega)) == "<class 'int'>"))):
        raise Exception('Omega is not scalar or array')
        
    if (not ((str(type(terrain_angle)) == "<class 'numpy.ndarray'>") or (str(type(terrain_angle)) == "<class 'numpy.float64'>") or (str(type(terrain_angle)) == "<class 'float'>") or (str(type(terrain_angle)) == "<class 'int'>"))):
        raise Exception('Terrain angle is not scalar or array')
        
    if (str(type(terrain_angle)) == "<class 'numpy.ndarray'>") and (str(type(omega)) == "<class 'numpy.ndarray'>"):
        if (len(omega) != len(terrain_angle)):
            raise Exception('Terrain angle and Omega are not the same size')
    elif ((str(type(omega)) == "<class 'float'>") or (str(type(omega)) == "<class 'int'>")) and ((str(type(terrain_angle)) == "<class 'float'>") or (str(type(terrain_angle)) == "<class 'int'>")):
        Frr = 0
    else:
        raise Exception('Terrain angle and Omega are not the same type')
    
    if ((str(type(terrain_angle)) == "<class 'numpy.ndarray'>")):
        for angle in terrain_angle:
            if ((angle < -75) or (angle > 75)):
                raise Exception('Angle(s) not valid')
    else:
        if ((terrain_angle < -75) or (terrain_angle > 75)):
            raise Exception('Angle(s) not valid')

    if ((str(type(rover)) != "<class 'dict'>") or (str(type(planet)) != "<class 'dict'>")):
        raise Exception('Variable(s) is not a dictionary')
        
    try:
        if (Crr < 0):
            raise Exception('Crr is negative')
    except:
        raise Exception('Crr is not a scalar')
        
    F_d = F_drive(omega, rover)
    F_g = F_gravity(terrain_angle, rover, planet)
    F_r = F_rolling(omega, terrain_angle, rover, planet, Crr)
    
    if (str(type(F_d)) == "<class 'numpy.ndarray'>") and (str(type(F_g)) == "<class 'numpy.ndarray'>") and (str(type(F_r)) == "<class 'numpy.ndarray'>"):
        F_n = []
        for i in range(len(F_d)):
            Fnet = F_d[i] + F_g[i] + F_r[i]
            F_n.append(Fnet)
            
        Fnet = np.array(F_n)
    else:
        Fnet = F_d + F_g + F_r
        
    return Fnet



