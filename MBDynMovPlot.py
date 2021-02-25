import os, subprocess, re, math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from sys import platform

mov_file_structure = {"node_label": 0,
                      "pos_x"     : 1,
                      "pos_y"     : 2,
                      "pos_z"     : 3,
                      "angle_x"   : 4,
                      "angle_y"   : 5,
                      "angle_z"   : 6,
                      "vel_x"     : 7,
                      "vel_y"     : 8,
                      "vel_z"     : 9,
                      "angular_x" : 10,
                      "angular_y" : 11,
                      "angular_z" : 12}

class MBDynMovPlot:
    __ani_interval   = 10
    __ani_markersize = 10
    __ani_marker     = "o"
    def __init__(self, MBDynInPutFile=None):
        self.inputFile = MBDynInPutFile
        self.dataFile = {"input":None,
                         "mov":None,
                         "frc":None,
                         "ine":None,
                         "jnt":None}
        self.data = {}
        self.animation_label = {}
        self.initial_time = 0
        self.final_time   = 1
        self.time_step    = 1e-3
        self.time         = np.arange(self.initial_time, self.final_time, self.time_step)
        # Animation
        self.enableAnimation = True
        
        check_result = self.check_file(self.inputFile)
        if self.inputFile is not None:
            if check_result == True:
                if self.dataFile.get("mov") is None:
                    self.notify(3)
                    if platform == "linux" or platform == "linux2": 
                        mbdyn = subprocess.Popen(["mbdyn", "-f", self.dataFile.get("input")])
                    if platform == "win32":
                        mbdyn = subprocess.Popen(r'mbdyn.exe -f '+ self.dataFile.get("input"))
                    try:
                        mbdyn.wait(timeout = 10)
                    except:
                        print("===== process timeout =====")
                        mbdyn.kill()
            else:
                self.notify(2)
        elif check_result is None:
            self.notify(1)

    def check_file(self, input_file = None):
        result    = None
        dirName  = os.sep.join(os.getcwd().split("\\"))
        fileList = os.listdir(dirName)
        for fname in fileList:
            suffix = fname.strip().split(".")[-1]
            if input_file == None:
                if "mov" == suffix:
                    print("Find: "+fname)
                    if self.dataFile.get("mov") == None:
                        if platform == "linux" or platform == "linux2": 
                            self.dataFile["mov"] = dirName+"/"+fname
                        if platform == "win32":
                            self.dataFile["mov"] = dirName+"\\"+fname
                        print("--- " + fname + " is used now. ---")
                        result = True
            else:
                if input_file == fname:
                    result    = True
                    if platform == "linux" or platform == "linux2": 
                        self.dataFile["input"] = dirName+"/"+fname
                    if platform == "win32":
                        self.dataFile["input"] = dirName+"\\"+fname
                if "mov" == suffix:
                    if platform == "linux" or platform == "linux2": 
                        self.dataFile["mov"] = dirName+"/"+input_file.strip().split(".")[0]+".mov"
                    if platform == "win32":
                        self.dataFile["mov"] = dirName+"\\"+input_file.strip().split(".")[0]+".mov"
        return result
    
    def notify(self, num):
        if num == 1:
            print("Please run MBDyn to generate simulation data...")
        if num == 2:
            print(self.inputFile + " file is not found!")
        if num == 3:
            print(self.inputFile + " found, MBDyn is running..")
            print("Plese run again after MBDyn is done.")
 
    def reset(self):
        self.data = {}
        
    def getData(self):
        if self.dataFile.get("mov") == None:
            return None
        if self.dataFile.get("input") is not None:
            with open(self.dataFile.get("input"),"r") as file:
                for i, line in enumerate(file):
                    line_list = re.split(':|;| ',line.strip())
                    if 'initial' in line_list and 'time' in line_list:
                        self.initial_time = float(line_list[-2])
                    if 'final' in line_list and 'time' in line_list:
                        self.final_time = float(line_list[-2])
                    if 'time' in line_list and 'step' in line_list:
                        self.time_step = float(line_list[-2])
                self.time = np.arange(self.initial_time, self.final_time, self.time_step)  

        with open(self.dataFile.get("mov"),"r") as file:
            for i, line in enumerate(file):
                line_list = line.strip().split(" ")
                
                # get corresponding information
                node      = line_list[mov_file_structure.get("node_label")]
                pos_x     = np.float64(line_list[mov_file_structure.get("pos_x")])
                pos_y     = np.float64(line_list[mov_file_structure.get("pos_y")])
                pos_z     = np.float64(line_list[mov_file_structure.get("pos_z")])
                angle_x   = np.float64(line_list[mov_file_structure.get("angle_x")])
                angle_y   = np.float64(line_list[mov_file_structure.get("angle_y")])
                angle_z   = np.float64(line_list[mov_file_structure.get("angle_z")])
                vel_x     = np.float64(line_list[mov_file_structure.get("vel_x")])
                vel_y     = np.float64(line_list[mov_file_structure.get("vel_y")])
                vel_z     = np.float64(line_list[mov_file_structure.get("vel_z")])
                angular_x = np.float64(line_list[mov_file_structure.get("angular_x")])
                angular_y = np.float64(line_list[mov_file_structure.get("angular_y")])
                angular_z = np.float64(line_list[mov_file_structure.get("angular_z")])
                
                if self.data.get(node) == None:
                    self.data[node] = {"pos_x"    :[pos_x],
                                       "pos_y"    :[pos_y],
                                       "pos_z"    :[pos_z],
                                       "angle_x"  :[angle_x],
                                       "angle_y"  :[angle_y],
                                       "angle_z"  :[angle_z],
                                       "vel_x"    :[vel_x],
                                       "vel_y"    :[vel_y],
                                       "vel_z"    :[vel_z],
                                       "angular_x":[angular_x],
                                       "angular_y":[angular_y],
                                       "angular_z":[angular_z]}
                else:
                    self.data[node].get("pos_x").append(pos_x)
                    self.data[node].get("pos_y").append(pos_y)
                    self.data[node].get("pos_z").append(pos_z)
                    self.data[node].get("angle_x").append(angle_x)
                    self.data[node].get("angle_y").append(angle_y)
                    self.data[node].get("angle_z").append(angle_z)
                    self.data[node].get("vel_x").append(vel_x)
                    self.data[node].get("vel_y").append(vel_y)
                    self.data[node].get("vel_z").append(vel_z)
                    self.data[node].get("angular_x").append(angular_x)
                    self.data[node].get("angular_y").append(angular_y)
                    self.data[node].get("angular_z").append(angular_z)
        return True
    
# --- Animation Position ---
    def update_points_3d(self, num):
        node_label = self.animation_label["P3D"]
        x = self.data[node_label].get("pos_x")
        y = self.data[node_label].get("pos_y")
        z = self.data[node_label].get("pos_z")
        
        self.point_ani_p3d.set_marker(self.__ani_marker)
        self.point_ani_p3d.set_markersize(self.__ani_markersize)

        self.point_ani_p3d.set_xdata(x[num])
        self.point_ani_p3d.set_ydata(y[num])
        self.point_ani_p3d.set_3d_properties(z[num])
        return self.point_ani_p3d,
    
    def update_points_pxt(self, num):     
        node_label = self.animation_label["Px(t)"]
        t = self.time
        x = self.data[node_label].get("pos_x")

        self.point_ani_pxt.set_marker(self.__ani_marker)
        self.point_ani_pxt.set_markersize(self.__ani_markersize)

        self.point_ani_pxt.set_xdata(t[num])
        self.point_ani_pxt.set_ydata(x[num])
        return self.point_ani_pxt,

    def update_points_pyt(self, num):     
        node_label = self.animation_label["Py(t)"]
        t = self.time
        y = self.data[node_label].get("pos_y")

        self.point_ani_pyt.set_marker(self.__ani_marker)
        self.point_ani_pyt.set_markersize(self.__ani_markersize)

        self.point_ani_pyt.set_xdata(t[num])
        self.point_ani_pyt.set_ydata(y[num])
        return self.point_ani_pyt,

    def update_points_pzt(self, num):     
        node_label = self.animation_label["Pz(t)"]
        t = self.time
        z = self.data[node_label].get("pos_z")

        self.point_ani_pzt.set_marker(self.__ani_marker)
        self.point_ani_pzt.set_markersize(self.__ani_markersize)

        self.point_ani_pzt.set_xdata(t[num])
        self.point_ani_pzt.set_ydata(z[num])
        return self.point_ani_pzt,
    
    def update_points_pxpy(self, num):     
        node_label = self.animation_label["Px(Py)"]
        x = self.data[node_label].get("pos_x")
        y = self.data[node_label].get("pos_y")

        self.point_ani_pxpy.set_marker(self.__ani_marker)
        self.point_ani_pxpy.set_markersize(self.__ani_markersize)

        self.point_ani_pxpy.set_xdata(y[num])
        self.point_ani_pxpy.set_ydata(x[num])
        return self.point_ani_pxpy,
    
    def update_points_pxpz(self, num):     
        node_label = self.animation_label["Px(Pz)"]
        x = self.data[node_label].get("pos_x")
        z = self.data[node_label].get("pos_z")

        self.point_ani_pxpz.set_marker(self.__ani_marker)
        self.point_ani_pxpz.set_markersize(self.__ani_markersize)

        self.point_ani_pxpz.set_xdata(z[num])
        self.point_ani_pxpz.set_ydata(x[num])
        return self.point_ani_pxpz,

    def update_points_pypx(self, num):     
        node_label = self.animation_label["Py(Px)"]
        x = self.data[node_label].get("pos_x")
        y = self.data[node_label].get("pos_y")

        self.point_ani_pypx.set_marker(self.__ani_marker)
        self.point_ani_pypx.set_markersize(self.__ani_markersize)

        self.point_ani_pypx.set_xdata(x[num])
        self.point_ani_pypx.set_ydata(y[num])
        return self.point_ani_pypx,
    
    def update_points_pypz(self, num):     
        node_label = self.animation_label["Py(Pz)"]
        y = self.data[node_label].get("pos_y")
        z = self.data[node_label].get("pos_z")

        self.point_ani_pypz.set_marker(self.__ani_marker)
        self.point_ani_pypz.set_markersize(self.__ani_markersize)

        self.point_ani_pypz.set_xdata(z[num])
        self.point_ani_pypz.set_ydata(y[num])
        return self.point_ani_pypz,

    def update_points_pzpx(self, num):     
        node_label = self.animation_label["Pz(Px)"]
        x = self.data[node_label].get("pos_x")
        z = self.data[node_label].get("pos_z")

        self.point_ani_pzpx.set_marker(self.__ani_marker)
        self.point_ani_pzpx.set_markersize(self.__ani_markersize)

        self.point_ani_pzpx.set_xdata(x[num])
        self.point_ani_pzpx.set_ydata(z[num])
        return self.point_ani_pzpx,
    
    def update_points_pzpy(self, num):     
        node_label = self.animation_label["Pz(Py)"]
        y = self.data[node_label].get("pos_y")
        z = self.data[node_label].get("pos_z")

        self.point_ani_pzpy.set_marker(self.__ani_marker)
        self.point_ani_pzpy.set_markersize(self.__ani_markersize)

        self.point_ani_pzpy.set_xdata(y[num])
        self.point_ani_pzpy.set_ydata(z[num])
        return self.point_ani_pzpy,
    
    def update_points_pt(self, num):     
        node_label = self.animation_label["P(t)"]
        t = self.time
        x = self.data[node_label].get("pos_x")
        y = self.data[node_label].get("pos_y")
        z = self.data[node_label].get("pos_z")
        
        # Ptx
        self.point_ani_ptx.set_marker(self.__ani_marker)
        self.point_ani_ptx.set_markersize(self.__ani_markersize)

        self.point_ani_ptx.set_xdata(t[num])
        self.point_ani_ptx.set_ydata(x[num])
        
        #Pty
        self.point_ani_pty.set_marker(self.__ani_marker)
        self.point_ani_pty.set_markersize(self.__ani_markersize)

        self.point_ani_pty.set_xdata(t[num])
        self.point_ani_pty.set_ydata(y[num])

        #Ptz
        self.point_ani_ptz.set_marker(self.__ani_marker)
        self.point_ani_ptz.set_markersize(self.__ani_markersize)

        self.point_ani_ptz.set_xdata(t[num])
        self.point_ani_ptz.set_ydata(z[num])
        
        return self.point_ani_ptx, self.point_ani_pty, self.point_ani_ptz,
    
# --- Animation Velocity ---
    def update_points_v3d(self, num):
        node_label = self.animation_label["V3D"]
        x = self.data[node_label].get("vel_x")
        y = self.data[node_label].get("vel_y")
        z = self.data[node_label].get("vel_z")
        
        self.point_ani_v3d.set_marker(self.__ani_marker)
        self.point_ani_v3d.set_markersize(self.__ani_markersize)

        self.point_ani_v3d.set_xdata(x[num])
        self.point_ani_v3d.set_ydata(y[num])
        self.point_ani_v3d.set_3d_properties(z[num])
        return self.point_ani_v3d,
    
    def update_points_vxt(self, num):     
        node_label = self.animation_label["Vx(t)"]
        t = self.time
        x = self.data[node_label].get("vel_x")

        self.point_ani_vxt.set_marker(self.__ani_marker)
        self.point_ani_vxt.set_markersize(self.__ani_markersize)

        self.point_ani_vxt.set_xdata(t[num])
        self.point_ani_vxt.set_ydata(x[num])
        return self.point_ani_vxt,

    def update_points_vyt(self, num):     
        node_label = self.animation_label["Vy(t)"]
        t = self.time
        y = self.data[node_label].get("vel_y")

        self.point_ani_vyt.set_marker(self.__ani_marker)
        self.point_ani_vyt.set_markersize(self.__ani_markersize)

        self.point_ani_vyt.set_xdata(t[num])
        self.point_ani_vyt.set_ydata(y[num])
        return self.point_ani_vyt,

    def update_points_vzt(self, num):     
        node_label = self.animation_label["Vz(t)"]
        t = self.time
        z = self.data[node_label].get("vel_z")

        self.point_ani_vzt.set_marker(self.__ani_marker)
        self.point_ani_vzt.set_markersize(self.__ani_markersize)

        self.point_ani_vzt.set_xdata(t[num])
        self.point_ani_vzt.set_ydata(z[num])
        return self.point_ani_vzt,

    def update_points_vxvy(self, num):     
        node_label = self.animation_label["Vx(Vy)"]
        x = self.data[node_label].get("vel_x")
        y = self.data[node_label].get("vel_y")

        self.point_ani_vxvy.set_marker(self.__ani_marker)
        self.point_ani_vxvy.set_markersize(self.__ani_markersize)

        self.point_ani_vxvy.set_xdata(y[num])
        self.point_ani_vxvy.set_ydata(x[num])
        return self.point_ani_vxvy,

    def update_points_vxvz(self, num):     
        node_label = self.animation_label["Vx(Vz)"]
        x = self.data[node_label].get("vel_x")
        z = self.data[node_label].get("vel_z")

        self.point_ani_vxvz.set_marker(self.__ani_marker)
        self.point_ani_vxvz.set_markersize(self.__ani_markersize)

        self.point_ani_vxvz.set_xdata(z[num])
        self.point_ani_vxvz.set_ydata(x[num])
        return self.point_ani_vxvz,

    def update_points_vyvx(self, num):     
        node_label = self.animation_label["Vy(Vx)"]
        x = self.data[node_label].get("vel_x")
        y = self.data[node_label].get("vel_y")

        self.point_ani_vyvx.set_marker(self.__ani_marker)
        self.point_ani_vyvx.set_markersize(self.__ani_markersize)

        self.point_ani_vyvx.set_xdata(x[num])
        self.point_ani_vyvx.set_ydata(y[num])
        return self.point_ani_vyvx,

    def update_points_vyvz(self, num):     
        node_label = self.animation_label["Vy(Vz)"]
        y = self.data[node_label].get("vel_y")
        z = self.data[node_label].get("vel_z")

        self.point_ani_vyvz.set_marker(self.__ani_marker)
        self.point_ani_vyvz.set_markersize(self.__ani_markersize)

        self.point_ani_vyvz.set_xdata(z[num])
        self.point_ani_vyvz.set_ydata(y[num])
        return self.point_ani_vyvz,

    def update_points_vzvx(self, num):     
        node_label = self.animation_label["Vz(Vx)"]
        x = self.data[node_label].get("vel_x")
        z = self.data[node_label].get("vel_z")

        self.point_ani_vzvx.set_marker(self.__ani_marker)
        self.point_ani_vzvx.set_markersize(self.__ani_markersize)

        self.point_ani_vzvx.set_xdata(x[num])
        self.point_ani_vzvx.set_ydata(z[num])
        return self.point_ani_vzvx,

    def update_points_vzvy(self, num):     
        node_label = self.animation_label["Vz(Vy)"]
        y = self.data[node_label].get("vel_y")
        z = self.data[node_label].get("vel_z")

        self.point_ani_vzvy.set_marker(self.__ani_marker)
        self.point_ani_vzvy.set_markersize(self.__ani_markersize)

        self.point_ani_vzvy.set_xdata(y[num])
        self.point_ani_vzvy.set_ydata(z[num])
        return self.point_ani_vzvy,

    def update_points_vt(self, num):     
        node_label = self.animation_label["V(t)"]
        t = self.time
        x = self.data[node_label].get("vel_x")
        y = self.data[node_label].get("vel_y")
        z = self.data[node_label].get("vel_z")
        
        # Vtx
        self.point_ani_vtx.set_marker(self.__ani_marker)
        self.point_ani_vtx.set_markersize(self.__ani_markersize)

        self.point_ani_vtx.set_xdata(t[num])
        self.point_ani_vtx.set_ydata(x[num])
        
        #Vty
        self.point_ani_vty.set_marker(self.__ani_marker)
        self.point_ani_vty.set_markersize(self.__ani_markersize)

        self.point_ani_vty.set_xdata(t[num])
        self.point_ani_vty.set_ydata(y[num])

        #Vtz
        self.point_ani_vtz.set_marker(self.__ani_marker)
        self.point_ani_vtz.set_markersize(self.__ani_markersize)

        self.point_ani_vtz.set_xdata(t[num])
        self.point_ani_vtz.set_ydata(z[num])
        
        return self.point_ani_vtx, self.point_ani_vty, self.point_ani_vtz,
    
# --- Animation angular velocity ---
    def update_points_w3d(self, num):
        node_label = self.animation_label["W3D"]
        x = self.data[node_label].get("angular_x")
        y = self.data[node_label].get("angular_y")
        z = self.data[node_label].get("angular_z")
        
        self.point_ani_w3d.set_marker(self.__ani_marker)
        self.point_ani_w3d.set_markersize(self.__ani_markersize)

        self.point_ani_w3d.set_xdata(x[num])
        self.point_ani_w3d.set_ydata(y[num])
        self.point_ani_w3d.set_3d_properties(z[num])
        return self.point_ani_w3d,
    
    def update_points_wxt(self, num):     
        node_label = self.animation_label["Wx(t)"]
        t = self.time
        x = self.data[node_label].get("angular_x")

        self.point_ani_wxt.set_marker(self.__ani_marker)
        self.point_ani_wxt.set_markersize(self.__ani_markersize)

        self.point_ani_wxt.set_xdata(t[num])
        self.point_ani_wxt.set_ydata(x[num])
        return self.point_ani_wxt,

    def update_points_wyt(self, num):     
        node_label = self.animation_label["Wy(t)"]
        t = self.time
        y = self.data[node_label].get("angular_y")

        self.point_ani_wyt.set_marker(self.__ani_marker)
        self.point_ani_wyt.set_markersize(self.__ani_markersize)

        self.point_ani_wyt.set_xdata(t[num])
        self.point_ani_wyt.set_ydata(y[num])
        return self.point_ani_wyt,

    def update_points_wzt(self, num):     
        node_label = self.animation_label["Wz(t)"]
        t = self.time
        z = self.data[node_label].get("angular_z")

        self.point_ani_wzt.set_marker(self.__ani_marker)
        self.point_ani_wzt.set_markersize(self.__ani_markersize)

        self.point_ani_wzt.set_xdata(t[num])
        self.point_ani_wzt.set_ydata(z[num])
        return self.point_ani_wzt,

    def update_points_wxwy(self, num):     
        node_label = self.animation_label["Wx(Wy)"]
        x = self.data[node_label].get("angular_x")
        y = self.data[node_label].get("angular_y")

        self.point_ani_wxwy.set_marker(self.__ani_marker)
        self.point_ani_wxwy.set_markersize(self.__ani_markersize)

        self.point_ani_wxwy.set_xdata(y[num])
        self.point_ani_wxwy.set_ydata(x[num])
        return self.point_ani_wxwy,

    def update_points_wxwz(self, num):     
        node_label = self.animation_label["Wx(Wz)"]
        x = self.data[node_label].get("angular_x")
        z = self.data[node_label].get("angular_z")

        self.point_ani_wxwz.set_marker(self.__ani_marker)
        self.point_ani_wxwz.set_markersize(self.__ani_markersize)

        self.point_ani_wxwz.set_xdata(z[num])
        self.point_ani_wxwz.set_ydata(x[num])
        return self.point_ani_wxwz,

    def update_points_wywx(self, num):     
        node_label = self.animation_label["Wy(Wx)"]
        x = self.data[node_label].get("angular_x")
        y = self.data[node_label].get("angular_y")

        self.point_ani_wywx.set_marker(self.__ani_marker)
        self.point_ani_wywx.set_markersize(self.__ani_markersize)

        self.point_ani_wywx.set_xdata(x[num])
        self.point_ani_wywx.set_ydata(y[num])
        return self.point_ani_wywx,

    def update_points_wywz(self, num):     
        node_label = self.animation_label["Wy(Wz)"]
        y = self.data[node_label].get("angular_y")
        z = self.data[node_label].get("angular_z")

        self.point_ani_wywz.set_marker(self.__ani_marker)
        self.point_ani_wywz.set_markersize(self.__ani_markersize)

        self.point_ani_wywz.set_xdata(z[num])
        self.point_ani_wywz.set_ydata(y[num])
        return self.point_ani_wywz,

    def update_points_wzwx(self, num):     
        node_label = self.animation_label["Wz(Wx)"]
        x = self.data[node_label].get("angular_x")
        z = self.data[node_label].get("angular_z")

        self.point_ani_wzwx.set_marker(self.__ani_marker)
        self.point_ani_wzwx.set_markersize(self.__ani_markersize)

        self.point_ani_wzwx.set_xdata(x[num])
        self.point_ani_wzwx.set_ydata(z[num])
        return self.point_ani_wzwx,

    def update_points_wzwy(self, num):     
        node_label = self.animation_label["Wz(Wy)"]
        y = self.data[node_label].get("angular_y")
        z = self.data[node_label].get("angular_z")

        self.point_ani_wzwy.set_marker(self.__ani_marker)
        self.point_ani_wzwy.set_markersize(self.__ani_markersize)

        self.point_ani_wzwy.set_xdata(y[num])
        self.point_ani_wzwy.set_ydata(z[num])
        return self.point_ani_wzwy,

    def update_points_wt(self, num):     
        node_label = self.animation_label["W(t)"]
        t = self.time
        x = self.data[node_label].get("angular_x")
        y = self.data[node_label].get("angular_y")
        z = self.data[node_label].get("angular_z")
        
        # Wtx
        self.point_ani_wtx.set_marker(self.__ani_marker)
        self.point_ani_wtx.set_markersize(self.__ani_markersize)

        self.point_ani_wtx.set_xdata(t[num])
        self.point_ani_wtx.set_ydata(x[num])
        
        #Wty
        self.point_ani_wty.set_marker(self.__ani_marker)
        self.point_ani_wty.set_markersize(self.__ani_markersize)

        self.point_ani_wty.set_xdata(t[num])
        self.point_ani_wty.set_ydata(y[num])

        #Wtz
        self.point_ani_wtz.set_marker(self.__ani_marker)
        self.point_ani_wtz.set_markersize(self.__ani_markersize)

        self.point_ani_wtz.set_xdata(t[num])
        self.point_ani_wtz.set_ydata(z[num])
        
        return self.point_ani_wtx, self.point_ani_wty, self.point_ani_wtz,
    
# --- Animation Orientation ---
    def update_points_o3d(self, num):
        node_label = self.animation_label["O3D"]
        x = self.data[node_label].get("angle_x")
        y = self.data[node_label].get("angle_y")
        z = self.data[node_label].get("angle_z")
        
        self.point_ani_o3d.set_marker(self.__ani_marker)
        self.point_ani_o3d.set_markersize(self.__ani_markersize)

        self.point_ani_o3d.set_xdata(x[num])
        self.point_ani_o3d.set_ydata(y[num])
        self.point_ani_o3d.set_3d_properties(z[num])
        return self.point_ani_o3d,
    
    def update_points_oxt(self, num):     
        node_label = self.animation_label["roll(t)"]
        t = self.time
        x = self.data[node_label].get("angle_x")

        self.point_ani_oxt.set_marker(self.__ani_marker)
        self.point_ani_oxt.set_markersize(self.__ani_markersize)

        self.point_ani_oxt.set_xdata(t[num])
        self.point_ani_oxt.set_ydata(x[num])
        return self.point_ani_oxt,

    def update_points_oyt(self, num):     
        node_label = self.animation_label["pitch(t)"]
        t = self.time
        y = self.data[node_label].get("angle_y")

        self.point_ani_oyt.set_marker(self.__ani_marker)
        self.point_ani_oyt.set_markersize(self.__ani_markersize)

        self.point_ani_oyt.set_xdata(t[num])
        self.point_ani_oyt.set_ydata(y[num])
        return self.point_ani_oyt,

    def update_points_ozt(self, num):     
        node_label = self.animation_label["yaw(t)"]
        t = self.time
        z = self.data[node_label].get("angle_z")

        self.point_ani_ozt.set_marker(self.__ani_marker)
        self.point_ani_ozt.set_markersize(self.__ani_markersize)

        self.point_ani_ozt.set_xdata(t[num])
        self.point_ani_ozt.set_ydata(z[num])
        return self.point_ani_ozt,

    def update_points_oxoy(self, num):     
        node_label = self.animation_label["roll(pitch)"]
        x = self.data[node_label].get("angle_x")
        y = self.data[node_label].get("angle_y")

        self.point_ani_oxoy.set_marker(self.__ani_marker)
        self.point_ani_oxoy.set_markersize(self.__ani_markersize)

        self.point_ani_oxoy.set_xdata(y[num])
        self.point_ani_oxoy.set_ydata(x[num])
        return self.point_ani_oxoy,

    def update_points_oxoz(self, num):     
        node_label = self.animation_label["roll(yaw)"]
        x = self.data[node_label].get("angle_x")
        z = self.data[node_label].get("angle_z")

        self.point_ani_oxoz.set_marker(self.__ani_marker)
        self.point_ani_oxoz.set_markersize(self.__ani_markersize)

        self.point_ani_oxoz.set_xdata(z[num])
        self.point_ani_oxoz.set_ydata(x[num])
        return self.point_ani_oxoz,

    def update_points_oyox(self, num):     
        node_label = self.animation_label["pitch(roll)"]
        x = self.data[node_label].get("angle_x")
        y = self.data[node_label].get("angle_y")

        self.point_ani_oyox.set_marker(self.__ani_marker)
        self.point_ani_oyox.set_markersize(self.__ani_markersize)

        self.point_ani_oyox.set_xdata(x[num])
        self.point_ani_oyox.set_ydata(y[num])
        return self.point_ani_oyox,

    def update_points_oyoz(self, num):     
        node_label = self.animation_label["pitch(yaw)"]
        y = self.data[node_label].get("angle_y")
        z = self.data[node_label].get("angle_z")

        self.point_ani_oyoz.set_marker(self.__ani_marker)
        self.point_ani_oyoz.set_markersize(self.__ani_markersize)

        self.point_ani_oyoz.set_xdata(z[num])
        self.point_ani_oyoz.set_ydata(y[num])
        return self.point_ani_oyoz,

    def update_points_ozox(self, num):     
        node_label = self.animation_label["yaw(roll)"]
        x = self.data[node_label].get("angle_x")
        z = self.data[node_label].get("angle_z")

        self.point_ani_ozox.set_marker(self.__ani_marker)
        self.point_ani_ozox.set_markersize(self.__ani_markersize)

        self.point_ani_ozox.set_xdata(x[num])
        self.point_ani_ozox.set_ydata(z[num])
        return self.point_ani_ozox,

    def update_points_ozoy(self, num):     
        node_label = self.animation_label["yaw(pitch)"]
        y = self.data[node_label].get("angle_y")
        z = self.data[node_label].get("angle_z")

        self.point_ani_ozoy.set_marker(self.__ani_marker)
        self.point_ani_ozoy.set_markersize(self.__ani_markersize)

        self.point_ani_ozoy.set_xdata(y[num])
        self.point_ani_ozoy.set_ydata(z[num])
        return self.point_ani_ozoy,

    def update_points_ot(self, num):     
        node_label = self.animation_label["O(t)"]
        t = self.time
        x = self.data[node_label].get("angle_x")
        y = self.data[node_label].get("angle_y")
        z = self.data[node_label].get("angle_z")
        
        # roll
        self.point_ani_otx.set_marker(self.__ani_marker)
        self.point_ani_otx.set_markersize(self.__ani_markersize)

        self.point_ani_otx.set_xdata(t[num])
        self.point_ani_otx.set_ydata(x[num])
        
        # pitch
        self.point_ani_oty.set_marker(self.__ani_marker)
        self.point_ani_oty.set_markersize(self.__ani_markersize)

        self.point_ani_oty.set_xdata(t[num])
        self.point_ani_oty.set_ydata(y[num])

        # yaw
        self.point_ani_otz.set_marker(self.__ani_marker)
        self.point_ani_otz.set_markersize(self.__ani_markersize)

        self.point_ani_otz.set_xdata(t[num])
        self.point_ani_otz.set_ydata(z[num])
        
        return self.point_ani_otx, self.point_ani_oty, self.point_ani_otz,
    
# --- Plot Position ---        
    def Px(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("pos_x")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("pos_x")[:length],
                     label='Px(t)',
                     color='red')
            plt.ylabel('Px[m]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global position component as function of time. Node: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Px(t)"] = node_label
                self.point_ani_pxt, = plt.plot(self.time[0],
                                               self.data[node_label].get("pos_x")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_pxt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)           
            plt.show()
        if t == "Py":
            length = min(len(self.data[node_label].get("pos_x")), len(self.data[node_label].get("pos_y")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("pos_y")[:length],
                     self.data[node_label].get("pos_x")[:length],
                     label='Px(Py)',
                     color='black')
            plt.ylabel('Px[m]')
            plt.xlabel('Py[m]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global position component as function of Y global position component. Node: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Px(Py)"] = node_label
                self.point_ani_pxpy, = plt.plot(self.data[node_label].get("pos_y")[0],
                                                self.data[node_label].get("pos_x")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_pxpy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Pz":
            length = min(len(self.data[node_label].get("pos_x")), len(self.data[node_label].get("pos_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("pos_z")[:length],self.data[node_label].get("pos_x")[:length],label='Px(Pz)',color='black')
            plt.ylabel('Px[m]')
            plt.xlabel('Pz[m]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global position component as function of Z global position component. Node: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Px(Pz)"] = node_label
                self.point_ani_pxpz, = plt.plot(self.data[node_label].get("pos_z")[0],
                                                self.data[node_label].get("pos_x")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_pxpz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def Py(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("pos_y")))
            fig = plt.figure()
            plt.plot(self.time[:length],self.data[node_label].get("pos_y")[:length],label='Py(t)',color='green')
            plt.ylabel('Py[m]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Y global position component as function of time. Node: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Py(t)"] = node_label
                self.point_ani_pyt, = plt.plot(self.time[0],
                                               self.data[node_label].get("pos_y")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_pyt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Px":
            length = min(len(self.data[node_label].get("pos_x")), len(self.data[node_label].get("pos_y")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("pos_x")[:length],self.data[node_label].get("pos_y")[:length],label='Py(Px)',color='black')
            plt.ylabel('Py[m]')
            plt.xlabel('Px[m]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Y global position component as function of X global position component. Node: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Py(Px)"] = node_label
                self.point_ani_pypx, = plt.plot(self.data[node_label].get("pos_x")[0],
                                                self.data[node_label].get("pos_y")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_pypx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Pz":
            length = min(len(self.data[node_label].get("pos_y")), len(self.data[node_label].get("pos_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("pos_z")[:length],self.data[node_label].get("pos_y")[:length],label='Py(Pz)',color='black')
            plt.ylabel('Py[m]')
            plt.xlabel('Pz[m]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Y global position component as function of Z global position component. Node: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Py(Pz)"] = node_label
                self.point_ani_pypz, = plt.plot(self.data[node_label].get("pos_z")[0],
                                                self.data[node_label].get("pos_y")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_pypz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def Pz(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("pos_z")))
            fig = plt.figure()
            plt.plot(self.time[:length],self.data[node_label].get("pos_z")[:length],label='Pz(t)',color='blue')
            plt.ylabel('Pz[m]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Z global position component as function of time. Node: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Pz(t)"] = node_label
                self.point_ani_pzt, = plt.plot(self.time[0],
                                               self.data[node_label].get("pos_z")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_pzt,
                                              frames   = len(self.time),
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Px":
            length = min(len(self.data[node_label].get("pos_x")), len(self.data[node_label].get("pos_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("pos_x")[:length],self.data[node_label].get("pos_z")[:length],label='Pz(Px)',color='black')
            plt.ylabel('Pz[m]')
            plt.xlabel('Px[m]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Z global position component as function of X global position component. Node: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Pz(Px)"] = node_label
                self.point_ani_pzpx, = plt.plot(self.data[node_label].get("pos_x")[0],
                                                self.data[node_label].get("pos_z")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_pzpx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Py":
            length = min(len(self.data[node_label].get("pos_y")), len(self.data[node_label].get("pos_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("pos_y")[:length],self.data[node_label].get("pos_z")[:length],label='Py(Pz)',color='black')
            plt.ylabel('Pz[m]')
            plt.xlabel('Py[m]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Z global position component as function of Y global position component. Node: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Pz(Py)"] = node_label
                self.point_ani_pzpy, = plt.plot(self.data[node_label].get("pos_y")[0],
                                                self.data[node_label].get("pos_z")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_pzpy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def P(self, node_label="1"):
        length = min(len(self.time), len(self.data[node_label].get("pos_x")))
        length = min(length, len(self.data[node_label].get("pos_y")))
        length = min(length, len(self.data[node_label].get("pos_z")))
        fig = plt.figure()
        plt.plot(self.time[:length],self.data[node_label].get("pos_x")[:length],label='Px(t)',color='red')
        plt.plot(self.time[:length],self.data[node_label].get("pos_y")[:length],label='Py(t)',color='green')
        plt.plot(self.time[:length],self.data[node_label].get("pos_z")[:length],label='Pz(t)',color='blue')
        plt.ylabel('P[m]')
        plt.xlabel('t[s]')
        plt.legend()            
        plt.grid()
        plt.suptitle('Global position as function of time. Node: '+ node_label)
        if self.enableAnimation == True:
            self.animation_label["P(t)"] = node_label
            self.point_ani_ptx, = plt.plot(self.time[0],
                                           self.data[node_label].get("pos_x")[0],
                                           "ro")
            self.point_ani_pty, = plt.plot(self.time[0],
                                           self.data[node_label].get("pos_y")[0],
                                           "ro")
            self.point_ani_ptz, = plt.plot(self.time[0],
                                           self.data[node_label].get("pos_z")[0],
                                           "ro") 
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_pt,
                                          frames   = length,
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()

    def P3D(self, node_label="1"):
        x = self.data[node_label].get("pos_x")
        y = self.data[node_label].get("pos_y")
        z = self.data[node_label].get("pos_z")
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(x, y, z, label='Px,Py,Pz')
        ax.legend()            
        ax.set_xlabel('x[m]')
        ax.set_ylabel('y[m]')
        ax.set_zlabel('z[m]')
        plt.legend()
        plt.grid()
        plt.suptitle('Global 3D trajectory. Node: '+ node_label)
        if self.enableAnimation == True:
            self.animation_label["P3D"] = node_label
            self.point_ani_p3d, = ax.plot([x[0]], [y[0]], [z[0]], "ro")
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_3d,
                                          frames   = len(x),
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()
        
# --- Plot Velocity ---
    def Vx(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("vel_x")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("vel_x")[:length],
                     label='Vx(t)',
                     color='red')
            plt.ylabel('Vx[m/s]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global velocity component as function of time. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1)          
            if self.enableAnimation == True:
                self.animation_label["Vx(t)"] = node_label
                self.point_ani_vxt, = plt.plot(self.time[0],
                                               self.data[node_label].get("vel_x")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_vxt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)           
            plt.show()
        if t == "Vy":
            length = min(len(self.data[node_label].get("vel_x")), len(self.data[node_label].get("vel_y")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("vel_y")[:length],
                     self.data[node_label].get("vel_x")[:length],
                     label='Vx(Vy)',
                     color='black')
            plt.ylabel('Vx[m/s]')
            plt.xlabel('Vy[m/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global velocity component as function of Y global velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Vx(Vy)"] = node_label
                self.point_ani_vxvy, = plt.plot(self.data[node_label].get("vel_y")[0],
                                                self.data[node_label].get("vel_x")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_vxvy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Vz":
            length = min(len(self.data[node_label].get("vel_x")), len(self.data[node_label].get("vel_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("vel_z")[:length],
                     self.data[node_label].get("vel_x")[:length],
                     label='Vx(Vz)',
                     color='black')
            plt.ylabel('Vx[m/s]')
            plt.xlabel('Vz[m/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global velocity component as function of Z global velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Vx(Vz)"] = node_label
                self.point_ani_vxvz, = plt.plot(self.data[node_label].get("vel_z")[0],
                                                self.data[node_label].get("vel_x")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_vxvz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def Vy(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("vel_y")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("vel_y")[:length],
                     label='Vy(t)',
                     color='green')
            plt.ylabel('Vy[m/s]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Y global velocity component as function of time. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Vy(t)"] = node_label
                self.point_ani_vyt, = plt.plot(self.time[0],
                                               self.data[node_label].get("vel_y")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_vyt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Vx":
            length = min(len(self.data[node_label].get("vel_x")), len(self.data[node_label].get("vel_y")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("vel_x")[:length],
                     self.data[node_label].get("vel_y")[:length],
                     label='Vy(Vx)',
                     color='black')
            plt.ylabel('Vy[m/s]')
            plt.xlabel('Vx[m/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Y global velocity component as function of X global velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Vy(Vx)"] = node_label
                self.point_ani_vyvx, = plt.plot(self.data[node_label].get("vel_x")[0],
                                                self.data[node_label].get("vel_y")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_vyvx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Vz":
            length = min(len(self.data[node_label].get("vel_y")), len(self.data[node_label].get("vel_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("vel_z")[:length],
                     self.data[node_label].get("vel_y")[:length],
                     label='Vy(Vz)',
                     color='black')
            plt.ylabel('Vy[m/s]')
            plt.xlabel('Vz[m/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Y global velocity component as function of Z global velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Vy(Vz)"] = node_label
                self.point_ani_vyvz, = plt.plot(self.data[node_label].get("vel_z")[0],
                                                self.data[node_label].get("vel_y")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_vyvz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def Vz(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("vel_z")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("vel_z")[:length],
                     label='Vz(t)',
                     color='blue')
            plt.ylabel('Vz[m/s]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Z global velocity component as function of time. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Vz(t)"] = node_label
                self.point_ani_vzt, = plt.plot(self.time[0],
                                               self.data[node_label].get("vel_z")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_vzt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Vx":
            length = min(len(self.data[node_label].get("vel_x")), len(self.data[node_label].get("vel_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("vel_x")[:length],
                     self.data[node_label].get("vel_z")[:length],
                     label='Vz(Vx)',
                     color='black')
            plt.ylabel('Vz[m/s]')
            plt.xlabel('Vx[m/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Z global velocity component as function of X global velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Vz(Vx)"] = node_label
                self.point_ani_vzvx, = plt.plot(self.data[node_label].get("vel_x")[0],
                                                self.data[node_label].get("vel_z")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_vzvx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Vy":
            length = min(len(self.data[node_label].get("vel_y")), len(self.data[node_label].get("vel_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("vel_y")[:length],
                     self.data[node_label].get("vel_z")[:length],
                     label='Vz(Vy)',
                     color='black')
            plt.ylabel('Vz[m/s]')
            plt.xlabel('Vy[m/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Z global velocity component as function of Y global velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Vz(Vy)"] = node_label
                self.point_ani_vzvy, = plt.plot(self.data[node_label].get("vel_y")[0],
                                                self.data[node_label].get("vel_z")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_vzvy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def V(self, node_label="1"):
        length = min(len(self.time), len(self.data[node_label].get("vel_x")))
        length = min(length, len(self.data[node_label].get("vel_y")))
        length = min(length, len(self.data[node_label].get("vel_z")))
        fig = plt.figure()
        plt.plot(self.time[:length],self.data[node_label].get("vel_x")[:length],label='Vx(t)',color='red')
        plt.plot(self.time[:length],self.data[node_label].get("vel_y")[:length],label='Vy(t)',color='green')
        plt.plot(self.time[:length],self.data[node_label].get("vel_z")[:length],label='Vz(t)',color='blue')
        plt.ylabel('V[m/s]')
        plt.xlabel('t[s]')
        plt.legend()            
        plt.grid()
        plt.suptitle('Global velocity as function of time. Node: '+ node_label)
        if self.enableAnimation == True:
            self.animation_label["V(t)"] = node_label
            self.point_ani_vtx, = plt.plot(self.time[0],
                                           self.data[node_label].get("vel_x")[0],
                                           "ro")
            self.point_ani_vty, = plt.plot(self.time[0],
                                           self.data[node_label].get("vel_y")[0],
                                           "ro")
            self.point_ani_vtz, = plt.plot(self.time[0],
                                           self.data[node_label].get("vel_z")[0],
                                           "ro") 
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_vt,
                                          frames   = length,
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()

    def V3D(self, node_label="1"):
        x = self.data[node_label].get("vel_x")
        y = self.data[node_label].get("vel_y")
        z = self.data[node_label].get("vel_z")
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(x, y, z, label='Vx,Vy,Vz')
        ax.legend()            
        ax.set_xlabel('x[m/s]')
        ax.set_ylabel('y[m/s]')
        ax.set_zlabel('z[m/s]')
        plt.legend()
        plt.grid()
        plt.suptitle('Global 3D velocity. Node: '+ node_label)
        xlim = plt.xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            plt.xlim(xmin = xlim[0] - 0.1)
            plt.xlim(xmax = xlim[1] + 0.1)  
        ylim = plt.ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            plt.ylim(ymin = ylim[0] - 0.1)
            plt.ylim(ymax = ylim[1] + 0.1)
        zlim = ax.get_zlim()
        if math.fabs(zlim[0]-zlim[1]) < 1e-3:
            ax.set_zlim(zlim[0] - 0.1,
                        zlim[1] + 0.1)
        if self.enableAnimation == True:
            self.animation_label["V3D"] = node_label
            self.point_ani_v3d, = ax.plot([x[0]], [y[0]], [z[0]], "ro")
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_v3d,
                                          frames   = len(self.time),
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()
        
# --- Plot Angular Velocity ---
    def Wx(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("angular_x")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("angular_x")[:length],
                     label='Wx(t)',
                     color='red')
            plt.ylabel('Wx[rad/s]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global angular velocity component as function of time. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1)          
            if self.enableAnimation == True:
                self.animation_label["Wx(t)"] = node_label
                self.point_ani_wxt, = plt.plot(self.time[0],
                                               self.data[node_label].get("angular_x")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_wxt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)           
            plt.show()
        if t == "Wy":
            length = min(len(self.data[node_label].get("angular_x")), len(self.data[node_label].get("angular_y")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angular_y")[:length],
                     self.data[node_label].get("angular_x")[:length],
                     label='Wx(Wy)',
                     color='black')
            plt.ylabel('Wx[rad/s]')
            plt.xlabel('Wy[rad/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global angular velocity component as function of Y global angular velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Wx(Wy)"] = node_label
                self.point_ani_wxwy, = plt.plot(self.data[node_label].get("angular_y")[0],
                                                self.data[node_label].get("angular_x")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_wxwy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Wz":
            length = min(len(self.data[node_label].get("angular_x")), len(self.data[node_label].get("angular_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angular_z")[:length],
                     self.data[node_label].get("angular_x")[:length],
                     label='Wx(Wz)',
                     color='black')
            plt.ylabel('Wx[m/s]')
            plt.xlabel('Wz[m/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('X global angular velocity component as function of Z global angular velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Wx(Wz)"] = node_label
                self.point_ani_wxwz, = plt.plot(self.data[node_label].get("angular_z")[0],
                                                self.data[node_label].get("angular_x")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_wxwz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def Wy(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("angular_y")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("angular_y")[:length],
                     label='Wy(t)',
                     color='green')
            plt.ylabel('Wy[m/s]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Y global angular velocity component as function of time. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Wy(t)"] = node_label
                self.point_ani_wyt, = plt.plot(self.time[0],
                                               self.data[node_label].get("angular_y")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_wyt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Wx":
            length = min(len(self.data[node_label].get("angular_x")), len(self.data[node_label].get("angular_y")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angular_x")[:length],
                     self.data[node_label].get("angular_y")[:length],
                     label='Wy(Wx)',
                     color='black')
            plt.ylabel('Wy[rad/s]')
            plt.xlabel('Wx[rad/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Y global angular velocity component as function of X global angular velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Wy(Wx)"] = node_label
                self.point_ani_wywx, = plt.plot(self.data[node_label].get("angular_x")[0],
                                                self.data[node_label].get("angular_y")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_wywx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Wz":
            length = min(len(self.data[node_label].get("angular_y")), len(self.data[node_label].get("angular_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angular_z")[:length],
                     self.data[node_label].get("angular_y")[:length],
                     label='Wy(Wz)',
                     color='black')
            plt.ylabel('Wy[rad/s]')
            plt.xlabel('Wz[rad/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Y global angular velocity component as function of Z global angular velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Wy(Wz)"] = node_label
                self.point_ani_wywz, = plt.plot(self.data[node_label].get("angular_z")[0],
                                                self.data[node_label].get("angular_y")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_wywz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def Wz(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("angular_z")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("angular_z")[:length],
                     label='Wz(t)',
                     color='blue')
            plt.ylabel('Wz[rad/s]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Z global angular velocity component as function of time. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Wz(t)"] = node_label
                self.point_ani_wzt, = plt.plot(self.time[0],
                                               self.data[node_label].get("angular_z")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_wzt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Wx":
            length = min(len(self.data[node_label].get("angular_x")), len(self.data[node_label].get("angular_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angular_x")[:length],
                     self.data[node_label].get("angular_z")[:length],
                     label='Wz(Wx)',
                     color='black')
            plt.ylabel('Wz[m/s]')
            plt.xlabel('Wx[m/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Z global angular velocity component as function of X global angular velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Wz(Wx)"] = node_label
                self.point_ani_wzwx, = plt.plot(self.data[node_label].get("angular_x")[0],
                                                self.data[node_label].get("angular_z")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_wzwx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Wy":
            length = min(len(self.data[node_label].get("angular_y")), len(self.data[node_label].get("angular_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angular_y")[:length],
                     self.data[node_label].get("angular_z")[:length],
                     label='Wz(Wy)',
                     color='black')
            plt.ylabel('Wz[rad/s]')
            plt.xlabel('Wy[rad/s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Z global angular velocity component as function of Y global angular velocity component. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Wz(Wy)"] = node_label
                self.point_ani_wzwy, = plt.plot(self.data[node_label].get("angular_y")[0],
                                                self.data[node_label].get("angular_z")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_wzwy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def W(self, node_label="1"):
        length = min(len(self.time), len(self.data[node_label].get("angular_x")))
        length = min(length, len(self.data[node_label].get("angular_y")))
        length = min(length, len(self.data[node_label].get("angular_z")))
        fig = plt.figure()
        plt.plot(self.time[:length],self.data[node_label].get("angular_x")[:length],label='Wx(t)',color='red')
        plt.plot(self.time[:length],self.data[node_label].get("angular_y")[:length],label='Wy(t)',color='green')
        plt.plot(self.time[:length],self.data[node_label].get("angular_z")[:length],label='Wz(t)',color='blue')
        plt.ylabel('W[rad/s]')
        plt.xlabel('t[s]')
        plt.legend()            
        plt.grid()
        plt.suptitle('Global angular velocity as function of time. Node: '+ node_label)
        xlim = plt.xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            plt.xlim(xmin = xlim[0] - 0.1)
            plt.xlim(xmax = xlim[1] + 0.1)  
        ylim = plt.ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            plt.ylim(ymin = ylim[0] - 0.1)
            plt.ylim(ymax = ylim[1] + 0.1) 
        if self.enableAnimation == True:
            self.animation_label["W(t)"] = node_label
            self.point_ani_wtx, = plt.plot(self.time[0],
                                           self.data[node_label].get("angular_x")[0],
                                           "ro")
            self.point_ani_wty, = plt.plot(self.time[0],
                                           self.data[node_label].get("angular_y")[0],
                                           "ro")
            self.point_ani_wtz, = plt.plot(self.time[0],
                                           self.data[node_label].get("angular_z")[0],
                                           "ro") 
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_wt,
                                          frames   = length,
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()

    def W3D(self, node_label="1"):
        x = self.data[node_label].get("angular_x")
        y = self.data[node_label].get("angular_y")
        z = self.data[node_label].get("angular_z")
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(x, y, z, label='Wx,Wy,Wz')
        ax.legend()            
        ax.set_xlabel('Wx[rad/s]')
        ax.set_ylabel('Wy[rad/s]')
        ax.set_zlabel('Wz[rad/s]')
        plt.legend()
        plt.grid()
        plt.suptitle('Global 3D angular velocity. Node: '+ node_label)
        xlim = plt.xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            plt.xlim(xmin = xlim[0] - 0.1)
            plt.xlim(xmax = xlim[1] + 0.1)  
        ylim = plt.ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            plt.ylim(ymin = ylim[0] - 0.1)
            plt.ylim(ymax = ylim[1] + 0.1)
        zlim = ax.get_zlim()
        if math.fabs(zlim[0]-zlim[1]) < 1e-3:
            ax.set_zlim(zlim[0] - 0.1,
                        zlim[1] + 0.1)
        if self.enableAnimation == True:
            self.animation_label["W3D"] = node_label
            self.point_ani_w3d, = ax.plot([x[0]], [y[0]], [z[0]], "ro")
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_w3d,
                                          frames   = len(self.time),
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()
        
# --- Plot Orientation ---
    def roll(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("angle_x")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("angle_x")[:length],
                     label='roll(t)',
                     color='red')
            plt.ylabel('roll[deg]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Global roll as function of time. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1)          
            if self.enableAnimation == True:
                self.animation_label["roll(t)"] = node_label
                self.point_ani_oxt, = plt.plot(self.time[0],
                                               self.data[node_label].get("angle_x")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_oxt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)           
            plt.show()
        if t == "pitch":
            length = min(len(self.data[node_label].get("angle_x")), len(self.data[node_label].get("angle_y")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angle_y")[:length],
                     self.data[node_label].get("angle_x")[:length],
                     label='roll(pitch)',
                     color='black')
            plt.ylabel('roll[deg]')
            plt.xlabel('pitch[deg]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Global roll as function of absolute pitch. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["roll(pitch)"] = node_label
                self.point_ani_oxoy, = plt.plot(self.data[node_label].get("angle_y")[0],
                                                self.data[node_label].get("angle_x")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_oxoy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "yaw":
            length = min(len(self.data[node_label].get("angle_x")), len(self.data[node_label].get("angle_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angle_z")[:length],
                     self.data[node_label].get("angle_x")[:length],
                     label='roll(yaw)',
                     color='black')
            plt.ylabel('roll[deg]')
            plt.xlabel('yaw[deg]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Global roll as function of absolute pitch. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["roll(yaw)"] = node_label
                self.point_ani_oxoz, = plt.plot(self.data[node_label].get("angle_z")[0],
                                                self.data[node_label].get("angle_x")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_oxoz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def pitch(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("angle_y")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("angle_y")[:length],
                     label='pitch(t)',
                     color='green')
            plt.ylabel('pitch[deg]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Global pitch as function of time. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["pitch(t)"] = node_label
                self.point_ani_oyt, = plt.plot(self.time[0],
                                               self.data[node_label].get("angle_y")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_oyt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "roll":
            length = min(len(self.data[node_label].get("angle_x")), len(self.data[node_label].get("angle_y")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angle_x")[:length],
                     self.data[node_label].get("angle_y")[:length],
                     label='pitch(roll)',
                     color='black')
            plt.ylabel('pitch[deg]')
            plt.xlabel('roll[deg]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Global pitch as function of absolute roll. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["pitch(roll)"] = node_label
                self.point_ani_oyox, = plt.plot(self.data[node_label].get("angle_x")[0],
                                                self.data[node_label].get("angle_y")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_oyox,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "yaw":
            length = min(len(self.data[node_label].get("angle_y")), len(self.data[node_label].get("angle_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angle_z")[:length],
                     self.data[node_label].get("angle_y")[:length],
                     label='pitch(yaw)',
                     color='black')
            plt.ylabel('pitch[deg]')
            plt.xlabel('yaw[deg]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Global pitch as function of absolute yaw. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["pitch(yaw)"] = node_label
                self.point_ani_oyoz, = plt.plot(self.data[node_label].get("angle_z")[0],
                                                self.data[node_label].get("angle_y")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_oyoz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def yaw(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("angle_z")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("angle_z")[:length],
                     label='yaw(t)',
                     color='blue')
            plt.ylabel('yaw[deg]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Global yaw as function of time. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["yaw(t)"] = node_label
                self.point_ani_ozt, = plt.plot(self.time[0],
                                               self.data[node_label].get("angle_z")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ozt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "roll":
            length = min(len(self.data[node_label].get("angle_x")), len(self.data[node_label].get("angle_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angle_x")[:length],
                     self.data[node_label].get("angle_z")[:length],
                     label='yaw(roll)',
                     color='black')
            plt.ylabel('yaw[deg]')
            plt.xlabel('roll[deg]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Global yaw as function of absolute roll. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["yaw(roll)"] = node_label
                self.point_ani_ozox, = plt.plot(self.data[node_label].get("angle_x")[0],
                                                self.data[node_label].get("angle_z")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ozox,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "pitch":
            length = min(len(self.data[node_label].get("angle_y")), len(self.data[node_label].get("angle_z")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("angle_y")[:length],
                     self.data[node_label].get("angle_z")[:length],
                     label='yaw(pitch)',
                     color='black')
            plt.ylabel('yaw[deg]')
            plt.xlabel('pitch[deg]')
            plt.legend()            
            plt.grid()
            plt.suptitle('Global yaw as function of absolute pitch. Node: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["yaw(pitch)"] = node_label
                self.point_ani_ozoy, = plt.plot(self.data[node_label].get("angle_y")[0],
                                                self.data[node_label].get("angle_z")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ozoy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def O(self, node_label="1"):
        length = min(len(self.time), len(self.data[node_label].get("angle_x")))
        length = min(length, len(self.data[node_label].get("angle_y")))
        length = min(length, len(self.data[node_label].get("angle_z")))
        fig = plt.figure()
        plt.plot(self.time[:length],self.data[node_label].get("angle_x")[:length],label='roll(t)',color='red')
        plt.plot(self.time[:length],self.data[node_label].get("angle_y")[:length],label='pitch(t)',color='green')
        plt.plot(self.time[:length],self.data[node_label].get("angle_z")[:length],label='yaw(t)',color='blue')
        plt.ylabel('angle[deg]')
        plt.xlabel('t[s]')
        plt.legend()            
        plt.grid()
        plt.suptitle('Global orientation as function of time. Node: '+ node_label)
        xlim = plt.xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            plt.xlim(xmin = xlim[0] - 0.1)
            plt.xlim(xmax = xlim[1] + 0.1)  
        ylim = plt.ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            plt.ylim(ymin = ylim[0] - 0.1)
            plt.ylim(ymax = ylim[1] + 0.1) 
        if self.enableAnimation == True:
            self.animation_label["O(t)"] = node_label
            self.point_ani_otx, = plt.plot(self.time[0],
                                           self.data[node_label].get("angle_x")[0],
                                           "ro")
            self.point_ani_oty, = plt.plot(self.time[0],
                                           self.data[node_label].get("angle_y")[0],
                                           "ro")
            self.point_ani_otz, = plt.plot(self.time[0],
                                           self.data[node_label].get("angle_z")[0],
                                           "ro") 
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_ot,
                                          frames   = length,
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()

    def O3D(self, node_label="1"):
        x = self.data[node_label].get("angle_x")
        y = self.data[node_label].get("angle_y")
        z = self.data[node_label].get("angle_z")
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(x, y, z, label='roll,pitch,yaw')
        ax.legend()            
        ax.set_xlabel('roll[deg]')
        ax.set_ylabel('pitch[deg]')
        ax.set_zlabel('yaw[deg]')
        plt.legend()
        plt.grid()
        plt.suptitle('Absolute 3D orientation. Node: '+ node_label)
        xlim = plt.xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            plt.xlim(xmin = xlim[0] - 0.1)
            plt.xlim(xmax = xlim[1] + 0.1)  
        ylim = plt.ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            plt.ylim(ymin = ylim[0] - 0.1)
            plt.ylim(ymax = ylim[1] + 0.1)
        zlim = ax.get_zlim()
        if math.fabs(zlim[0]-zlim[1]) < 1e-3:
            ax.set_zlim(zlim[0] - 0.1,
                        zlim[1] + 0.1)
        if self.enableAnimation == True:
            self.animation_label["O3D"] = node_label
            self.point_ani_o3d, = ax.plot([x[0]], [y[0]], [z[0]], "ro")
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_o3d,
                                          frames   = len(self.time),
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()
               
    def ALL(self, node_label="1"):
        length = min(len(self.time), len(self.data[node_label].get("angle_x")))
        length = min(length, len(self.data[node_label].get("angle_y")))
        length = min(length, len(self.data[node_label].get("angle_z")))
        time= self.time[:length]
        x   = self.data[node_label].get("pos_x")[:length]
        y   = self.data[node_label].get("pos_y")[:length]
        z   = self.data[node_label].get("pos_z")[:length]
        Eux = self.data[node_label].get("angle_x")[:length]
        Euy = self.data[node_label].get("angle_y")[:length]
        Euz = self.data[node_label].get("angle_z")[:length]
        Vx  = self.data[node_label].get("vel_x")[:length]
        Vy  = self.data[node_label].get("vel_x")[:length]
        Vz  = self.data[node_label].get("vel_x")[:length]
        Wx  = self.data[node_label].get("angular_x")[:length]
        Wy  = self.data[node_label].get("angular_x")[:length]
        Wz  = self.data[node_label].get("angular_x")[:length]
        fig = plt.figure()
        ax1 = fig.add_subplot(341)
        ax2 = fig.add_subplot(342)
        ax3 = fig.add_subplot(343)
        ax4 = fig.add_subplot(344)
        ax5 = fig.add_subplot(345)
        ax6 = fig.add_subplot(346)
        ax7 = fig.add_subplot(347)
        ax8 = fig.add_subplot(348)
        ax9 = fig.add_subplot(349)
        ax10 = fig.add_subplot(3,4,10)
        ax11 = fig.add_subplot(3,4,11)
        ax12 = fig.add_subplot(3,4,12)            
        ax1.plot(time,x)
        ax5.plot(time,y)
        ax9.plot(time,z)
        ax1.set_ylabel('x[m]')
        ax1.set_xlabel('t[s]')
        ax5.set_ylabel('y[m]')
        ax5.set_xlabel('t[s]')
        ax9.set_ylabel('z[m]')
        ax9.set_xlabel('t[s]')        
        ax2.plot(time,Eux)
        xlim = ax2.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax2.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax2.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax2.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax6.plot(time,Euy)
        xlim = ax6.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax6.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax6.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax6.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax10.plot(time,Euz)
        xlim = ax10.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax10.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax10.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax10.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax2.set_ylabel('yaw[deg]')
        ax2.set_xlabel('t[s]')
        ax6.set_ylabel('pithc[deg]')
        ax6.set_xlabel('t[s]')
        ax10.set_ylabel('roll[deg]')
        ax10.set_xlabel('t[s]')
        ax3.plot(time,Vx)
        xlim = ax3.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax3.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax3.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax3.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax7.plot(time,Vy)
        xlim = ax7.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax7.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax7.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax7.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax11.plot(time,Vz)
        xlim = ax11.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax11.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax11.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax11.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax3.set_ylabel('Vx[m/s]')
        ax3.set_xlabel('t[s]')
        ax7.set_ylabel('Vy[m/s]')
        ax7.set_xlabel('t[s]')
        ax11.set_ylabel('Vz[m/s]')
        ax11.set_xlabel('t[s]')
        ax4.plot(time,Wx)
        xlim = ax4.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax4.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax4.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax4.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax8.plot(time,Wy)
        xlim = ax8.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax8.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax8.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax8.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax12.plot(time,Wz)
        xlim = ax12.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax12.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax12.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax12.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax4.set_ylabel('Wx[rad/s]')
        ax4.set_xlabel('t[s]')
        ax8.set_ylabel('Wy[rad/s]')
        ax8.set_xlabel('t[s]')
        ax12.set_ylabel('Wz[rad/s]')
        ax12.set_xlabel('t[s]')
        plt.legend()
        plt.suptitle('Simulation results. Node: '+ node_label)
        plt.show() 

def main():
    mbd = MBDynMovPlot("rigidbody.mbd")
    if mbd.getData():
        mbd.Wx(t="Wy")
    
if __name__ == '__main__':
    main()
    

