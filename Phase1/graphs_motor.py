import matplotlib.pyplot as plt
from subfunctions import *

def graphs_motor():
    omega = np.linspace(0, 3.8, 100)
    dc = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    power = dc*omega
    
    table, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10,10))
    
    #subplot one
    ax1.plot(dc, omega)
    ax1.set_xlabel('Motor Shaft Torque (Nm)')
    ax1.set_ylabel('Motor Shaft Speed (rad/s')
    ax1.set_title('Motor Shaft Speed vs. Motor Shaft Torque')

    #subplot two
    ax2.plot(dc, power)
    ax2.set_xlabel('Motor Shaft Torque (Nm)')
    ax2.set_ylabel('Motor Shaft Power (W)')
    ax2.set_title('Motor Shaft Power vs. Motor Shaft Torque')
    
    #subplot three
    ax3.plot(omega, power)
    po = power.tolist()
    ymax = max(po)
    xpos = po.index(ymax)
    xmax = omega[xpos]
    ax3.set_xlabel('Motor Shaft Speed (rad/s)')
    ax3.set_ylabel('Motor Shaft Power (W)')
    ax3.set_title('Motor Shaft Power vs. Motor Shaft Speed')
    ax3.annotate(f'Max ({xmax:.3f}, {ymax:.3f})', xy = (xmax, ymax - 30))
    
    plt.tight_layout()
    plt.show()
    
graphs_motor()

