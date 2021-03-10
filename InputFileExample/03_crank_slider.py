import sys 
sys.path.append("..")
from MBDynMovPlot import MBDynMovPlot

x1=[]
y1=[]
x2=[]
y2=[]
x3=[]
y3=[]


target_pendulum = "2"

mov     = MBDynMovPlot("03_crank_slider")
mov.clear_run() # optional
data_ok = mov.getData()

if data_ok:
    x1 = mov.data["2"]["pos_x"]
    y1 = mov.data["2"]["pos_y"]
    x2 = mov.data["3"]["pos_x"]
    y2 = mov.data["3"]["pos_y"]
    x3 = mov.data["4"]["pos_x"]
    y3 = mov.data["4"]["pos_y"]
        
# Make 2D animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

dt = 0.02
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-0.2, 0.6), ylim=(-0.2, 0.2))
ax.set_aspect('equal')
ax.grid()
text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
template = 'length = %.3f'

plt.plot(x1,y1,color='c',linestyle='dotted',linewidth=0.1)
plt.plot(x2,y2,color='c',linestyle='dotted',linewidth=0.1)
plt.plot(x3,y3,color='r',linestyle='solid',linewidth=0.3)
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
    pointx= [x1[i],x2[i],x3[i]]
    pointy= [y1[i],y2[i],y3[i]]

    line.set_data(thisx, thisy)
    point.set_data(pointx, pointy)
    #text.set_text(template % (math.sqrt((thisx[2]-thisx[1])**2+(thisy[2]-thisy[1])**2)))
    return line, point, text

if data_ok:
    ani = animation.FuncAnimation(fig, animate, len(y1),
                                  interval=dt*1000, blit=True)
    plt.show()