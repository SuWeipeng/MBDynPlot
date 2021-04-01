import numpy as np
import matplotlib.pyplot as plt

N = 100
x = np.linspace(0, 2*np.pi, N)
y = np.sin(x) + 1

from spring import spring2d, spring3d

fig, (ax1,ax2) = plt.subplots(1,2)

# ax1 2D spring
point1, = ax1.plot([], [], 'bo')
point2, = ax1.plot([], [], 'ro')
points, = ax1.plot([],[])
ax1.set_xlim([-1,1])
ax1.set_ylim([0,2])

# ax2 3D spring    
ax2 = fig.add_subplot(1, 2, 2, projection='3d')

start = [10,5,0]
end   = [10,5,2]
r     = 1
x2, y2, z2 = spring3d(start,end,3,r)
line3d, = ax2.plot(x2,y2,z2)
pos = [start[0],start[1]]
plt.xlim([pos[0]-r,pos[0]+r])
plt.ylim([pos[1]-r,pos[1]+r])
ax2.set_zlim(start[2],end[2])

import matplotlib.animation as animation

def animate(i):
    # 2d animation
    point_a = (0,0)
    point_b = (0,y[i])
    pointx, pointy = spring2d(point_a, point_b, 10, 1)
    points.set_data(pointx, pointy)
    point1.set_data(0,0)
    point2.set_data(0,y[i])
    
    # 3d animation
    global start, r
    end = [start[0],start[1],y[i]]
    x2, y2, z2 = spring3d(start,end,5,r)
    line3d.set_xdata(x2)
    line3d.set_ydata(y2)
    line3d.set_3d_properties(z2)
    
    return point1,point2,points,line3d

ani = animation.FuncAnimation(fig,
                              animate,
                              len(y),
                              interval=10,
                              blit=True)

plt.show()