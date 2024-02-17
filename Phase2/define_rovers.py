from subfunctions import *

def define_rover_1():
    # Initialize Rover dict for testing
    wheel = {'radius':0.30,
             'mass':1}
    speed_reducer = {'type':'reverted',
                     'diam_pinion':0.04,
                     'diam_gear':0.07,
                     'mass':1.5,
                     'effcy_tau':[0, 10, 20, 40, 75, 165],
                     'effcy':[0, 0.60, 0.75, 0.73, 0.55, 0.05]}
    motor = {'torque_stall':170,
             'torque_noload':0,
             'speed_noload':3.80,
             'mass':5.0}
    
        
    chassis = {'mass':659}
    science_payload = {'mass':75}
    power_subsys = {'mass':90}
    
    wheel_assembly = {'wheel':wheel,
                      'speed_reducer':speed_reducer,
                      'motor':motor}
    
    rover = {'wheel_assembly':wheel_assembly,
             'chassis':chassis,
             'science_payload':science_payload,
             'power_subsys':power_subsys}
    
    planet = {'g':3.72}
    
    # return everything we need
    return rover, planet

def define_rover_2():
    # Initialize Rover dict for testing
    wheel = {'radius':0.30,
             'mass':2} 
    speed_reducer = {'type':'reverted',
                     'diam_pinion':0.04,
                     'diam_gear':0.06,
                     'mass':1.5}
    motor = {'torque_stall':180,
             'torque_noload':0,
             'speed_noload':3.70,
             'mass':5.0}    
    
    chassis = {'mass':659}
    science_payload = {'mass':75}
    power_subsys = {'mass':90}
    
    wheel_assembly = {'wheel':wheel,
                      'speed_reducer':speed_reducer,
                      'motor':motor}
    
    rover = {'wheel_assembly':wheel_assembly,
             'chassis':chassis,
             'science_payload':science_payload,
             'power_subsys':power_subsys}
    
    planet = {'g':3.72}
    
    # return everything we need
    return rover, planet

def define_rover_3():
    # Initialize Rover dict for testing
    wheel = {'radius':0.30,
             'mass':2} 
    speed_reducer = {'type':'standard',
                     'diam_pinion':0.04,
                     'diam_gear':0.06,
                     'mass':1.5}
    motor = {'torque_stall':180,
             'torque_noload':0,
             'speed_noload':3.70,
             'mass':5.0}
    
    chassis = {'mass':659}
    science_payload = {'mass':75}
    power_subsys = {'mass':90}
    
    wheel_assembly = {'wheel':wheel,
                      'speed_reducer':speed_reducer,
                      'motor':motor}
    
    rover = {'wheel_assembly':wheel_assembly,
             'chassis':chassis,
             'science_payload':science_payload,
             'power_subsys':power_subsys}
    
    planet = {'g':3.72}
    
    # return everything we need
    return rover, planet

# print(F_net(np.array([0,.5,1,2,3,3.8]),np.array([-5,0,5,10,20,30]),define_rover_1(),define_rover_1(),.1))
# rover, planet = define_rover_1()
# print(rover['wheel_assembly']['motor']['torque_stall'])
