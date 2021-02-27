# Get data from "*.mov" file
from MBDynMovPlot import MBDynMovPlot

x1=[]
y1=[]
x2=[]
y2=[]

pendulum_No = {"1":("1","3"),
               "2":("4","6")}

target_pendulum = "1"

mov     = MBDynMovPlot("doublependulum")
data_ok = mov.getData()

if data_ok:
    if target_pendulum == "1":
        x1 = mov.data[pendulum_No[target_pendulum][0]]["pos_x"]
        y1 = mov.data[pendulum_No[target_pendulum][0]]["pos_y"]
        x2 = mov.data[pendulum_No[target_pendulum][1]]["pos_x"]
        y2 = mov.data[pendulum_No[target_pendulum][1]]["pos_y"]
    if target_pendulum == "2":
        x1 = mov.data[pendulum_No[target_pendulum][0]]["pos_z"]
        y1 = mov.data[pendulum_No[target_pendulum][0]]["pos_y"]
        x2 = mov.data[pendulum_No[target_pendulum][1]]["pos_z"]
        y2 = mov.data[pendulum_No[target_pendulum][1]]["pos_y"]
        
# Make 2D animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

dt = 0.02
fig = plt.figure()
if target_pendulum == "1":
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1.5, 1.5), ylim=(-2, 1))
if target_pendulum == "2":
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(4, 0), ylim=(-1.6, 1))
ax.set_aspect('equal')
ax.grid()
text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
template = 'length = %.3f'

point, = ax.plot([], [], 'ro')
line, = ax.plot([], [], 'o-', lw=2)

def animate(i):
    if target_pendulum == "1":
        s = 0.0
        o = [0, 0]
    if target_pendulum == "2":
        s = 2.1
        o = [1.941, 0]
    p1    = [x1[i], y1[i]]
    p2    = [x2[i], y2[i]]
    p1    = [x1[i]*2-o[0], y1[i]*2-o[1]]
    p2    = [x2[i]+(x2[i]-p1[0])*s, y2[i]+(y2[i]-p1[1])*s]
    thisx = [o[0], p1[0], p2[0]]
    thisy = [o[1], p1[1], p2[1]]
    pointx= [x1[i],x2[i]]
    pointy= [y1[i],y2[i]]

    line.set_data(thisx, thisy)
    point.set_data(pointx, pointy)
    #text.set_text(template % (math.sqrt((thisx[2]-thisx[1])**2+(thisy[2]-thisy[1])**2)))
    return line, point, text

if data_ok:
    ani = animation.FuncAnimation(fig, animate, len(y1),
                                  interval=dt*1000, blit=True)
    plt.show()