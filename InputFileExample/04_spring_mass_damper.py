import sys 
sys.path.append("..")

# generate and get data from MBDyn
from MBDynMovPlot import MBDynMovPlot
from MBDynJntPlot import MBDynJntPlot

mov     = MBDynMovPlot("04_spring_mass_damper")
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
end   = [x_start_3D,y_start_3D,-1]

# spring data 2D
r     = 0.1
x_start_2D = start[0]
y_start_2D = start[2]
x_end_2D   = end[0]
y_end_2D   = end[2]

# matplotlib plot
import matplotlib.pyplot as plt

fig, (ax1,ax2) = plt.subplots(1,2)

# ax1 2D spring
point1, = ax1.plot([], [], 'bo')
point2, = ax1.plot([], [], 'ro')
points, = ax1.plot([],[])
circle = plt.Circle((0, 0), radius, color='r', alpha=0.3)
ax1.add_patch(circle)
ax1.axis('equal')
ax1.set_xlim([x_start_2D-radius,x_start_2D+radius])

# ax2 2D data
x_ax2 = list(range(len(z_node_mass)))
ax2.plot(x_ax2, z_node_mass, label="Position (m)", c="steelblue")
ax2.set_ylabel(r"Position", c="steelblue")
for tl in ax2.get_yticklabels():
    tl.set_color("steelblue")
ax22 = ax2.twinx()
ax22.plot(x_ax2, vel_z_node_mass, label="Velocity (m/s)", color="darkorange", linewidth=1, linestyle=":")
ax22.set_ylabel(r"Velocity", c="darkorange")
for tl in ax22.get_yticklabels():
    tl.set_color("darkorange")
point_ani, = ax2.plot(x_ax2[0], z_node_mass[0],"ro")
fig.legend(loc=1, bbox_to_anchor=(1,1), bbox_transform=ax2.transAxes)
plt.tight_layout()

# 2D animation
import matplotlib.animation as animation
from utilities.spring import spring2d
import matplotlib

def animate(i):
    point_a = (0,0)
    point_b = (0,z_node_mass[i])
    pointx, pointy = spring2d(point_a, point_b, 20, r*2)
    points.set_data(pointx, pointy)
    point1.set_data(0,0)
    point2.set_data(0,point_b[1])
    radius1 = radius/2
    ax1.axis('equal')
    ax1.set_xlim([x_start_2D-radius,x_start_2D+radius])
    ax1.set_ylim([min(-3.5,lim_for_plot-2*radius),0.2])
    circle.center = (0,point_b[1]-radius)
    
    point_ani.set_xdata(x_ax2[i])
    point_ani.set_ydata(z_node_mass[i])
    ax2.set_ylim(ax1.get_ylim())
    
    transFigure = fig.transFigure.inverted()
    coord1 = transFigure.transform(ax1.transData.transform(point_b))
    coord2 = transFigure.transform(ax2.transData.transform([x_ax2[i],z_node_mass[i]]))
    line = matplotlib.lines.Line2D((coord1[0],coord2[0]),(coord1[1],coord2[1]),
                                   transform=fig.transFigure,
                                   alpha = 0.3)
    line.set_linestyle('--')
    line.set_linewidth(1)
    line.set_color('r')
    fig.lines = line,
    
    return point1,point2,points,circle,point_ani

ani = animation.FuncAnimation(fig,
                              animate,
                              len(z_node_mass),
                              interval=1)

plt.show()