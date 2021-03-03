import sys 
sys.path.append("..")
import MBDynMovPlot as mp
import MBDynJntPlot as jp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

plot_mode = "2d"

mov = mp.MBDynMovPlot("01_pendulum")
jnt = jp.MBDynJntPlot("01_pendulum")

mov.clear_run()

mov_ok = mov.getData()
jnt_ok = jnt.getData()

node_label = "1"
joint_label= "1002"

__force_scale    = 0.01
__ani_markersize = 10
__ani_marker     = "o"


if plot_mode == "3d":
    def update_points_3d(num):
        global quiver, x, y, z, xlim, ylim, zlim

        plt.cla()
        ax.plot(x, y, z, label='Px,Py,Pz')
        
        quiver.remove()
        quiver = ax.quiver(x[num], y[num], z[num], u[num], v[num], w[num])
        
        ax.plot([0,x[num]], [0,y[num]], [0,z[num]], "ro-", linewidth=0.3)
        print(type(ax))
        plt.xlim(xlim)
        plt.ylim(ylim)
        ax.set_zlim(zlim)
        ax.set_xlabel('x[m]')
        ax.set_ylabel('y[m]')
        ax.set_zlabel('z[m]')
        plt.draw()

        return point_ani_p3d,
else:
    def update_points_pzpx(num):     
        global x, z, quiver
        
        plt.cla()
        plt.plot(x,z,label='Pz(Px)',color='c')
        plt.ylabel('Pz[m]')
        plt.xlabel('Px[m]')
        plt.legend()            
        plt.grid()
        plt.axis('equal')
        plt.suptitle('Z global position component as function of X global position component. Node: '+ node_label)
        plt.plot([0,x[num]], [0,z[num]], "ro-", linewidth = 0.3)
        quiver.remove()
        quiver = plt.quiver(x[num], z[num], u[num], w[num], width = 0.003,  angles='xy', scale_units='xy', scale=2)
        quiver = plt.quiver(x, z, u, w, width = 0.0001,  angles='xy', scale_units='xy', scale=2, color='b')
        plt.draw()
        
        return point_ani_pzpx,
    
if mov_ok is not None and jnt_ok is not None:
    x = mov.data[node_label].get("pos_x")
    y = mov.data[node_label].get("pos_y")
    z = mov.data[node_label].get("pos_z")
    u = jnt.data[joint_label].get("reaction_force_X_global")
    v = jnt.data[joint_label].get("reaction_force_Y_global")
    w = jnt.data[joint_label].get("reaction_force_Z_global")

    u = -__force_scale*np.array(u)
    v = -__force_scale*np.array(v)
    w = -__force_scale*np.array(w)
    
    length_mov = len(x)
    length_jnt = len(u)
    if length_mov > length_jnt:
        len_err = length_mov - length_jnt
        x = x[len_err::]
        y = y[len_err::]
        z = z[len_err::]

    if plot_mode == "3d":
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(x, y, z, label='Px,Py,Pz')
        ax.legend()            
        
        plt.legend()
        plt.grid()
        plt.suptitle('Global 3D trajectory. Node: '+ node_label)

        point_ani_p3d, = ax.plot(x[0], y[0], z[0], "ro")
        xlim = plt.xlim()
        ylim = plt.ylim()
        zlim = ax.get_zlim()
        print(type(ax))
        quiver = ax.quiver(x[0], y[0], z[0], u[0], v[0], w[0])
        
        ani = animation.FuncAnimation(fig      = fig,
                                      func     = update_points_3d,
                                      frames   = len(x),
                                      interval = 10,
                                      repeat   = True,
                                      blit     = True)
        plt.show()
    else:
        length = min(len(x), len(z))
        fig = plt.figure()
        plt.plot(x,z,label='Pz(Px)',color='c')
        plt.ylabel('Pz[m]')
        plt.xlabel('Px[m]')
        plt.legend()            
        plt.grid()
        plt.axis('equal')
        plt.suptitle('Z global position component as function of X global position component. Node: '+ node_label)

        point_ani_pzpx, = plt.plot([0,x[0]], [0,z[0]], "ro-")
        quiver = plt.quiver(x[0], z[0], u[0], w[0])
        
        ani = animation.FuncAnimation(fig      = fig,
                                      func     = update_points_pzpx,
                                      frames   = length,
                                      interval = 10,
                                      repeat   = True,
                                      blit     = True)
        plt.show()
