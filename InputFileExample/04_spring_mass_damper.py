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

# 2D animation
import matplotlib.animation as animation
from utilities.spring import spring2d

def animate(i):
    # 2d animation
    point_a = (0,0)
    point_b = (0,z_node_mass[i])
    pointx, pointy = spring2d(point_a, point_b, 20, r*2)
    points.set_data(pointx, pointy)
    point1.set_data(0,0)
    point2.set_data(0,point_b[1])
    radius1 = radius/2
    ax1.axis('equal')
    ax1.set_xlim([x_start_2D-radius,x_start_2D+radius])
    #ax1.set_ylim([lim_for_plot-2*radius,0.2])
    ax1.set_ylim([-3.5,0.2])
    circle.center = (0,point_b[1]-radius)
    return point1,point2,points,circle

ani = animation.FuncAnimation(fig,
                              animate,
                              len(z_node_mass),
                              interval=1)

plt.show()