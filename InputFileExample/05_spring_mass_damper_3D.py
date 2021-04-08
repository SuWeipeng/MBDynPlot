import sys 
sys.path.append("..")

# generate and get data from MBDyn
from MBDynMovPlot import MBDynMovPlot
from MBDynJntPlot import MBDynJntPlot

mov     = MBDynMovPlot("05_spring_mass_damper")
mov.clear_run() # optional
mov_ok = mov.getData()
if mov_ok:
    t  = mov.time
    node_mass_label = "2"
    x_node_mass     = mov.data[node_mass_label]["pos_x"]
    y_node_mass     = mov.data[node_mass_label]["pos_y"]
    z_node_mass     = mov.data[node_mass_label]["pos_z"]
    vel_x_node_mass = mov.data[node_mass_label]["vel_x"]
    vel_y_node_mass = mov.data[node_mass_label]["vel_y"]
    vel_z_node_mass = mov.data[node_mass_label]["vel_z"]
    lim_for_plot    = min((z_node_mass))
else:
    print("\n\n\nPlease run again.")
    sys.exit()

# body data
radius= 0.2

# spring data 3D
x_start_3D = 0
y_start_3D = 0
start = [x_start_3D,y_start_3D,0]
end   = [x_start_3D,y_start_3D,min(z_node_mass)]

# spring data 3D
from utilities.spring import spring3d
r     = 0.1
nodes = 10
x,y,z = spring3d(start,end,nodes,r)

# matplotlib plot
import matplotlib.pyplot as plt

fig, (ax1,ax2) = plt.subplots(1,2)

# ax1 3D spring
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
line3d, = ax1.plot(x,y,z)
pos = [start[0],start[1]]
view_field = min(-3.5,min(z)-radius*2)
plt.xlim([pos[0]-view_field/2,pos[0]+view_field/2])
plt.ylim([pos[1]-view_field/2,pos[1]+view_field/2])
ax1.set_zlim(view_field,start[2])

# sphere data
import numpy as np
from mpl_toolkits.mplot3d import Axes3D, axes3d
from matplotlib import cm

offset = 0.02
center = [start[0],start[1],end[2]-radius+offset]

u_s = np.linspace(0, 2*np.pi, 50)
v_s = np.linspace(0, np.pi, 50)
x_s = radius * np.outer(np.cos(u_s), np.sin(v_s)) + center[0]
y_s = radius * np.outer(np.sin(u_s), np.sin(v_s)) + center[1]
z_s = radius * np.outer(np.ones(np.size(u_s)), np.cos(v_s)) + center[2]

sphere = [ax1.plot_surface(x_s, y_s, z_s,  rstride=1, cstride=1, alpha=0.5, linewidth=0, cmap=cm.coolwarm )]
ax1.set_box_aspect((1, 1, 1))


# ax2 3D data
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
x_ax2 = list(range(len(z_node_mass)))
ax2.plot(x_ax2,np.zeros(len(z_node_mass)), z_node_mass, label="Position (m)", c="steelblue")
zlim = ax1.get_zlim()
ax2.set_zlim(zlim)
ax2.set_box_aspect((1, 1, 1))

point, = ax2.plot([x[0]], [y[0]], [z[len(z)-1]], "ro")


# 3D animation
import matplotlib.animation as animation
import matplotlib

def animate(i, sphere):
    point_a = (0,0)
    point_b = (0,z_node_mass[i])
    end = [start[0],start[1],z_node_mass[i]]
    x, y, z = spring3d(start,end,nodes,r)
    line3d.set_xdata(x)
    line3d.set_ydata(y)
    line3d.set_3d_properties(z)
    # sphere
    center = [start[0],start[1],end[2]-radius+offset]
    z_s = radius * np.outer(np.ones(np.size(u_s)), np.cos(v_s)) + center[2]
    sphere[0].remove()
    sphere[0] = ax1.plot_surface(x_s, y_s, z_s,  rstride=1, cstride=1, alpha=0.5, linewidth=0, cmap=cm.coolwarm)
    
    point.set_xdata(np.float64(x_ax2[i]))
    point.set_ydata(np.float64(0))
    point.set_3d_properties(np.float64(z[len(z)-1]))

    ax2.view_init(ax1.elev, ax1.azim)
    ax2.set_zlim(ax1.get_zlim())
    
    return line3d,point

ani = animation.FuncAnimation(fig,
                              animate,
                              len(z_node_mass),
                              fargs=([sphere]),
                              interval=20)

plt.show()