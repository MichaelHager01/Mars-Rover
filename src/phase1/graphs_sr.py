import matplotlib.pyplot as plt
from subfunctions import *

def graphs_sr():
    omega = np.linspace(0, 3.8, 100) # w_in
    dc = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    power = dc*omega
    
    Ng = get_gear_ratio(speed_reducer)
    w_out = []
    for w in omega:
        w_out.append(w / Ng)
    w_out = np.array(w_out)
    
    t_out = []
    for t in dc:
        t_out.append(t * Ng)
    t_out = np.array(t_out)
    
    table, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10,10))
    
    #subplot one
    ax1.plot(t_out, w_out)
    ax1.set_xlabel('Speed Reducer Output Shaft Torque (Nm)')
    ax1.set_ylabel('Speed Reducer Output Shaft Speed (rad/s')
    ax1.set_title('Speed Reducer Output Shaft Speed vs. Speed Reducer Output Shaft Torque')

    #subplot two
    ax2.plot(t_out, power)
    ax2.set_xlabel('Speed Reducer Output Shaft Torque (Nm)')
    ax2.set_ylabel('Speed Reducer Output Shaft Power (W)')
    ax2.set_title('Speed Reducer Output Shaft Power vs. Speed Reducer Output Shaft Torque')
    
    #subplot three
    ax3.plot(w_out, power)
    po = power.tolist()
    ymax = max(po)
    xpos = po.index(ymax)
    xmax = omega[xpos]
    ax3.set_xlabel('Speed Reducer Output Shaft Speed (rad/s)')
    ax3.set_ylabel('Speed Reducer Output Shaft Power (W)')
    ax3.set_title('Speed Reducer Output Shaft Power vs. Speed Reducer Output Shaft Speed')
    ax3.annotate(f'Max ({xmax:.3f}, {ymax:.3f})', xy = (xmax, ymax - 30))
    
    plt.tight_layout()
    plt.show()
    
graphs_sr()

