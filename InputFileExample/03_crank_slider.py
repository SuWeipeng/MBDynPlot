import sys 
sys.path.append("..")
import numpy as np
import MBDynJntPlot as jp
from MBDynMovPlot import MBDynMovPlot


x0=[]
y0=[]
x1=[]
y1=[]
x2=[]
y2=[]
x3=[]
y3=[]

plot_node_trajectory = 1
plot_joint_force     = 0
plot_velocity        = 1

mov     = MBDynMovPlot("03_crank_slider")
mov.clear_run() # optional
mov_ok = mov.getData()
if mov_ok:
    t  = mov.time
    x0 = mov.data["1"]["pos_x"]
    y0 = mov.data["1"]["pos_y"]
    x1 = mov.data["2"]["pos_x"]
    y1 = mov.data["2"]["pos_y"]
    x2 = mov.data["3"]["pos_x"]
    y2 = mov.data["3"]["pos_y"]
    x3 = mov.data["4"]["pos_x"]
    y3 = mov.data["4"]["pos_y"]
    vel_x = mov.data["4"]["vel_x"]
    vel_y = mov.data["4"]["vel_y"]

jnt     = jp.MBDynJntPlot("03_crank_slider")
jnt_ok  = jnt.getData()
__force_scale    = 1e-2
__vel_scale      = 2e-1
if jnt_ok:
    u1 = jnt.data["1"].get("reaction_force_X_global")
    v1 = jnt.data["1"].get("reaction_force_Y_global")
    w1 = jnt.data["1"].get("reaction_force_Z_global")
    u1 = __force_scale*np.array(u1)
    v1 = __force_scale*np.array(v1)
    w1 = __force_scale*np.array(w1)
    u2 = jnt.data["2"].get("reaction_force_X_global")
    v2 = jnt.data["2"].get("reaction_force_Y_global")
    w2 = jnt.data["2"].get("reaction_force_Z_global")
    u2 = __force_scale*np.array(u2)
    v2 = __force_scale*np.array(v2)
    w2 = __force_scale*np.array(w2)

length_mov = len(x0)
length_jnt = len(u1)
if length_mov > length_jnt:
    len_err = length_mov - length_jnt
    t  = t[len_err::]
    x0 = x0[len_err::]
    y0 = y0[len_err::]
    x1 = x1[len_err::]
    y1 = y1[len_err::]
    x2 = x2[len_err::]
    y2 = y2[len_err::]
    x3 = x3[len_err::]
    y3 = y3[len_err::]
    vel_x = vel_x[len_err::]
    vel_y = vel_y[len_err::]
    vel_x = __vel_scale*np.array(vel_x)
    vel_y = __vel_scale*np.array(vel_y)
        
# Make 2D animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

dt = 0.02
fig = plt.figure()
ax  = fig.add_subplot(211, autoscale_on=False, xlim=(-0.2, 0.6), ylim=(-0.2, 0.2))
ax2 = fig.add_subplot(212)
length = min(len(t),len(y3))
ax2.plot(t,x3[:length],label='pos_x')
ax2.plot(t,vel_x[:length],label='vel_x')
ax2.grid()
ax2.legend()
ax2.title.set_text('position and velocity of node 4')
ax2.set_aspect('equal')
xlim = ax.get_xlim()
ylim = ax.get_ylim()
ax.set_aspect('equal')
ax.grid()

if plot_node_trajectory == 1:
    ax.plot(x1,y1,color='c',linestyle='dotted',linewidth=0.1)
    ax.plot(x2,y2,color='c',linestyle='dotted',linewidth=0.1)
    ax.plot(x3,y3,color='r',linestyle='solid',linewidth=1)
if plot_joint_force == 1:
    quiver1 = ax.quiver(x0[0], x0[0], u2[0], v2[0])
    px = 2*np.array(x1)
    py = 2*np.array(y1)
    quiver2 = ax.quiver(px[0], py[0], u2[0], v2[0])
if plot_velocity == 1:
    quiver3 = ax.quiver(x3[0], x3[0], vel_x[0], vel_y[0])
    
point, = ax.plot([], [], 'ro')
line, = ax.plot([], [], 'o-', lw=2)

def animate(i):
    s = 2.0
    o = [0, 0]
    p1    = [x1[i]*2-o[0], y1[i]*2-o[1]]
    #p2    = [p1[0]+(x2[i]-p1[0])*s, p1[1]+(y2[i]-p1[1])*s]
    p2    = [x3[i], y3[i]]
    thisx = [o[0], p1[0], p2[0]]
    thisy = [o[1], p1[1], p2[1]]
    pointx= [x0[i],x1[i],x2[i],x3[i]]
    pointy= [y0[i],y1[i],y2[i],y3[i]]
    '''
    line.set_data(thisx, thisy)
    point.set_data(pointx, pointy)
    '''
    global xlim, ylim, quiver1, quiver2, quiver3
    ax.cla()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid()
    ax.plot(x3,y3,color='r',linestyle='dotted',linewidth=1)
    if plot_node_trajectory == 1:
        ax.plot(x1,y1,color='c',linestyle='dotted',linewidth=0.1)
        ax.plot(x2,y2,color='c',linestyle='dotted',linewidth=0.1)
    if plot_joint_force == 1:
        px = 2*np.array(x1)
        py = 2*np.array(y1)
        ax.plot(px,py,color='c',linestyle='dotted',linewidth=0.1)
        
    ax.plot(thisx, thisy,'o-', lw=2)
    ax.plot(pointx, pointy, 'ro')
    ax.text(x3[i], 0.16, 'node 4')
    if plot_joint_force == 1:
        quiver1.remove()
        quiver1 = ax.quiver(x0, y0, u1, v1, width = 0.00005,  angles='xy', scale_units='xy', scale=3, color='b')
        quiver1 = ax.quiver(x0[i], y0[i], u1[i], v1[i], width = 0.003,  angles='xy', scale_units='xy', scale=3, color='r')
        quiver2.remove()
        quiver2 = ax.quiver(px, py, u2, v2, width = 0.00005,  angles='xy', scale_units='xy', scale=3, color='b')
        quiver2 = ax.quiver(px[i], py[i], u2[i], v2[i], width = 0.003,  angles='xy', scale_units='xy', scale=3, color='r')
    if plot_velocity == 1:
        quiver3.remove()
        quiver3 = ax.quiver(x3[i], y3[i], vel_x[i], vel_y[i],
                             color = 'g',
                             width = 0.003,
                             angles='xy',
                             scale_units='xy',
                             scale=3)
    
    plt.draw()

    return line, point

data_ok = mov_ok and jnt_ok

if data_ok:
    ani = animation.FuncAnimation(fig, animate, len(y1),
                                  interval=dt*1000, blit=True)
    plt.show()