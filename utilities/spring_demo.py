import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, axes3d
from matplotlib import cm

N = 15
offset_2d = 1.5
A = 1
x = np.linspace(0, 2*np.pi, N)
y = A*np.sin(x) + offset_2d

#spring data
x_pos = 0
y_pos = 0
start = [x_pos,y_pos,0]
end   = [x_pos,y_pos,2]
r     = 1
nodes = 3
radius= 3

from spring import spring2d, spring3d

fig, (ax1,ax2) = plt.subplots(1,2)

# ax1 2D spring
point1, = ax1.plot([], [], 'bo')
point2, = ax1.plot([], [], 'ro')
points, = ax1.plot([],[])
circle = plt.Circle((0, 0), radius, color='r', alpha=0.3)
ax1.add_patch(circle)

# ax2 3D spring    
ax2 = fig.add_subplot(1, 2, 2, projection='3d')

# sphere center and radius
offset = -0.2
center = [x_pos,y_pos,end[2]+radius+offset]


x2, y2, z2 = spring3d(start,end,nodes,r)
line3d, = ax2.plot(x2,y2,z2)
pos = [start[0],start[1]]
plt.xlim([pos[0]-radius,pos[0]+radius])
plt.ylim([pos[1]-radius,pos[1]+radius])
ax2.set_zlim(start[2],end[2]+radius*2)

# sphere data
u_s = np.linspace(0, 2*np.pi, 50)
v_s = np.linspace(0, np.pi, 50)
x_s = radius * np.outer(np.cos(u_s), np.sin(v_s)) + center[0]
y_s = radius * np.outer(np.sin(u_s), np.sin(v_s)) + center[1]
z_s = radius * np.outer(np.ones(np.size(u_s)), np.cos(v_s)) + center[2]

sphere = [ax2.plot_surface(x_s, y_s, z_s,  rstride=1, cstride=1, alpha=0.5, linewidth=0, cmap=cm.coolwarm )]
ax2.set_box_aspect((1, 1, 1.3))

import matplotlib.animation as animation

def animate(i, sphere):
    # 2d animation
    point_a = (0,0)
    point_b = (0,y[i])
    pointx, pointy = spring2d(point_a, point_b, 10, r*2)
    points.set_data(pointx, pointy)
    point1.set_data(0,0)
    point2.set_data(0,y[i])
    radius1 = radius/2
    ax1.axis('equal')
    ax1.set_xlim([x_pos-radius,x_pos+radius])
    ax1.set_ylim([0,A+offset_2d+2*radius])
    circle.center = (0,y[i]+radius)
    
    # 3d animation
    end = [start[0],start[1],y[i]]
    x2, y2, z2 = spring3d(start,end,5,r)
    line3d.set_xdata(x2)
    line3d.set_ydata(y2)
    line3d.set_3d_properties(z2)
    
    # sphere
    center = [x_pos,y_pos,end[2]+radius+offset]
    z_s = radius * np.outer(np.ones(np.size(u_s)), np.cos(v_s)) + center[2]
    sphere[0].remove()
    sphere[0] = ax2.plot_surface(x_s, y_s, z_s,  rstride=1, cstride=1, alpha=0.5, linewidth=0, cmap=cm.coolwarm )
    
    return point1,point2,points,line3d,circle

ani = animation.FuncAnimation(fig,
                              animate,
                              len(y),
                              fargs=([sphere]),
                              interval=5)

plt.show()