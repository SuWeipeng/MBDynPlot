import os, subprocess, re, math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from sys import platform

jnt_file_structure = {"node_label": 0,
                      "reaction_force_X_local"     : 1,
                      "reaction_force_Y_local"     : 2,
                      "reaction_force_Z_local"     : 3,
                      "reaction_couple_X_local"    : 4,
                      "reaction_couple_Y_local"    : 5,
                      "reaction_couple_Z_local"    : 6,
                      "reaction_force_X_global"    : 7,
                      "reaction_force_Y_global"    : 8,
                      "reaction_force_Z_global"    : 9,
                      "reaction_couple_X_global"   : 10,
                      "reaction_couple_Y_global"   : 11,
                      "reaction_couple_Z_global"   : 12}

class MBDynJntPlot:
    __ani_interval   = 10
    __ani_markersize = 10
    __ani_marker     = "o"
    def __init__(self, MBDynInPutFile=None):
        self.inputFile = MBDynInPutFile
        self.dataFile = {"input":None,
                         "jnt":None,
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
                if self.dataFile.get("jnt") is None:
                    self.notify(3)
                    self.run_mbdyn()
            else:
                self.notify(2)
        elif check_result is None:
            self.notify(1)

    def clear(self):
        dirName  = os.sep.join(os.getcwd().split("\\"))
        fileList = os.listdir(dirName)
        for fname in fileList:
            if ".ine" in fname:
                os.remove(fname)
            if ".log" in fname:
                os.remove(fname)
            if ".jnt" in fname:
                os.remove(fname)
            if ".mov" in fname:
                os.remove(fname)
            if ".out" in fname:
                os.remove(fname)

    def clear_run(self):
        self.clear()
        self.run_mbdyn()
        
    def run_mbdyn(self):
        if platform == "linux" or platform == "linux2": 
            mbdyn = subprocess.Popen(["mbdyn", "-f", self.dataFile.get("input")])
        if platform == "win32":
            mbdyn = subprocess.Popen(r'mbdyn.exe -f '+ self.dataFile.get("input"))
        try:
            mbdyn.wait(timeout = 100)
        except:
            print("===== process timeout =====")
            mbdyn.kill()
            
    def check_file(self, input_file = None):
        result    = None
        dirName  = os.sep.join(os.getcwd().split("\\"))
        fileList = os.listdir(dirName)
        for fname in fileList:
            suffix = fname.strip().split(".")[-1]
            if input_file == None:
                if "jnt" == suffix:
                    print("Find: "+fname)
                    if self.dataFile.get("jnt") == None:
                        if platform == "linux" or platform == "linux2": 
                            self.dataFile["jnt"] = dirName+"/"+fname
                        if platform == "win32":
                            self.dataFile["jnt"] = re.split('\\\\+$', dirName)[0]+"\\"+fname
                        print("--- " + fname + " is used now. ---")
                        result = True
            else:
                if input_file == fname:
                    result    = True
                    if platform == "linux" or platform == "linux2": 
                        self.dataFile["input"] = dirName+"/"+fname
                    if platform == "win32":
                        self.dataFile["input"] = re.split('\\\\+$', dirName)[0]+"\\"+fname
                if "jnt" == suffix:
                    if platform == "linux" or platform == "linux2": 
                        self.dataFile["jnt"] = dirName+"/"+input_file.strip().split(".")[0]+".jnt"
                    if platform == "win32":
                        self.dataFile["jnt"] = dirName+"\\"+input_file.strip().split(".")[0]+".jnt"
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
        if self.dataFile.get("jnt") == None:
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
        try:
            with open(self.dataFile.get("jnt"),"r") as file:
                for i, line in enumerate(file):
                    line_list = line.strip().split(" ")
                    
                    if i<2:
                        continue
                    
                    # get corresponding information
                    node                       = line_list[jnt_file_structure.get("node_label")]
                    reaction_force_X_local     = np.float64(line_list[jnt_file_structure.get("reaction_force_X_local")])
                    reaction_force_Y_local     = np.float64(line_list[jnt_file_structure.get("reaction_force_Y_local")])
                    reaction_force_Z_local     = np.float64(line_list[jnt_file_structure.get("reaction_force_Z_local")])
                    reaction_couple_X_local    = np.float64(line_list[jnt_file_structure.get("reaction_couple_X_local")])
                    reaction_couple_Y_local    = np.float64(line_list[jnt_file_structure.get("reaction_couple_Y_local")])
                    reaction_couple_Z_local    = np.float64(line_list[jnt_file_structure.get("reaction_couple_Z_local")])
                    reaction_force_X_global    = np.float64(line_list[jnt_file_structure.get("reaction_force_X_global")])
                    reaction_force_Y_global    = np.float64(line_list[jnt_file_structure.get("reaction_force_Y_global")])
                    reaction_force_Z_global    = np.float64(line_list[jnt_file_structure.get("reaction_force_Z_global")])
                    reaction_couple_X_global   = np.float64(line_list[jnt_file_structure.get("reaction_couple_X_global")])
                    reaction_couple_Y_global   = np.float64(line_list[jnt_file_structure.get("reaction_couple_Y_global")])
                    reaction_couple_Z_global   = np.float64(line_list[jnt_file_structure.get("reaction_couple_Z_global")])
                    
                    if self.data.get(node) == None:
                        self.data[node] = {"reaction_force_X_local"    :[reaction_force_X_local],
                                           "reaction_force_Y_local"    :[reaction_force_Y_local],
                                           "reaction_force_Z_local"    :[reaction_force_Z_local],
                                           "reaction_couple_X_local"   :[reaction_couple_X_local],
                                           "reaction_couple_Y_local"   :[reaction_couple_Y_local],
                                           "reaction_couple_Z_local"   :[reaction_couple_Z_local],
                                           "reaction_force_X_global"   :[reaction_force_X_global],
                                           "reaction_force_Y_global"   :[reaction_force_Y_global],
                                           "reaction_force_Z_global"   :[reaction_force_Z_global],
                                           "reaction_couple_X_global"  :[reaction_couple_X_global],
                                           "reaction_couple_Y_global"  :[reaction_couple_Y_global],
                                           "reaction_couple_Z_global"  :[reaction_couple_Z_global]}
                    else:
                        self.data[node].get("reaction_force_X_local").append(reaction_force_X_local)
                        self.data[node].get("reaction_force_Y_local").append(reaction_force_Y_local)
                        self.data[node].get("reaction_force_Z_local").append(reaction_force_Z_local)
                        self.data[node].get("reaction_couple_X_local").append(reaction_couple_X_local)
                        self.data[node].get("reaction_couple_Y_local").append(reaction_couple_Y_local)
                        self.data[node].get("reaction_couple_Z_local").append(reaction_couple_Z_local)
                        self.data[node].get("reaction_force_X_global").append(reaction_force_X_global)
                        self.data[node].get("reaction_force_Y_global").append(reaction_force_Y_global)
                        self.data[node].get("reaction_force_Z_global").append(reaction_force_Z_global)
                        self.data[node].get("reaction_couple_X_global").append(reaction_couple_X_global)
                        self.data[node].get("reaction_couple_Y_global").append(reaction_couple_Y_global)
                        self.data[node].get("reaction_couple_Z_global").append(reaction_couple_Z_global)
        except:
            if self.dataFile.get("input") is not None:
                self.run_mbdyn()
                return None   
        return True
    
# --- Animation Position ---
    def update_points_f3d(self, num):
        node_label = self.animation_label["F3D"]
        x = self.data[node_label].get("reaction_force_X_local")
        y = self.data[node_label].get("reaction_force_Y_local")
        z = self.data[node_label].get("reaction_force_Z_local")
        
        self.point_ani_f3d.set_marker(self.__ani_marker)
        self.point_ani_f3d.set_markersize(self.__ani_markersize)

        self.point_ani_f3d.set_xdata(x[num])
        self.point_ani_f3d.set_ydata(y[num])
        self.point_ani_f3d.set_3d_properties(z[num])
        return self.point_ani_f3d,
    
    def update_points_fxt(self, num):     
        node_label = self.animation_label["Fx(t)"]
        t = self.time
        x = self.data[node_label].get("reaction_force_X_local")

        self.point_ani_fxt.set_marker(self.__ani_marker)
        self.point_ani_fxt.set_markersize(self.__ani_markersize)

        self.point_ani_fxt.set_xdata(t[num])
        self.point_ani_fxt.set_ydata(x[num])
        return self.point_ani_fxt,

    def update_points_fyt(self, num):     
        node_label = self.animation_label["Fy(t)"]
        t = self.time
        y = self.data[node_label].get("reaction_force_Y_local")

        self.point_ani_fyt.set_marker(self.__ani_marker)
        self.point_ani_fyt.set_markersize(self.__ani_markersize)

        self.point_ani_fyt.set_xdata(t[num])
        self.point_ani_fyt.set_ydata(y[num])
        return self.point_ani_fyt,

    def update_points_fzt(self, num):     
        node_label = self.animation_label["Fz(t)"]
        t = self.time
        z = self.data[node_label].get("reaction_force_Z_local")

        self.point_ani_fzt.set_marker(self.__ani_marker)
        self.point_ani_fzt.set_markersize(self.__ani_markersize)

        self.point_ani_fzt.set_xdata(t[num])
        self.point_ani_fzt.set_ydata(z[num])
        return self.point_ani_fzt,
    
    def update_points_fxfy(self, num):     
        node_label = self.animation_label["Fx(Fy)"]
        x = self.data[node_label].get("reaction_force_X_local")
        y = self.data[node_label].get("reaction_force_Y_local")

        self.point_ani_fxfy.set_marker(self.__ani_marker)
        self.point_ani_fxfy.set_markersize(self.__ani_markersize)

        self.point_ani_fxfy.set_xdata(y[num])
        self.point_ani_fxfy.set_ydata(x[num])
        return self.point_ani_fxfy,
    
    def update_points_fxfz(self, num):     
        node_label = self.animation_label["Fx(Fz)"]
        x = self.data[node_label].get("reaction_force_X_local")
        z = self.data[node_label].get("reaction_force_Z_local")

        self.point_ani_fxfz.set_marker(self.__ani_marker)
        self.point_ani_fxfz.set_markersize(self.__ani_markersize)

        self.point_ani_fxfz.set_xdata(z[num])
        self.point_ani_fxfz.set_ydata(x[num])
        return self.point_ani_fxfz,

    def update_points_fyfx(self, num):     
        node_label = self.animation_label["Fy(Fx)"]
        x = self.data[node_label].get("reaction_force_X_local")
        y = self.data[node_label].get("reaction_force_Y_local")

        self.point_ani_fyfx.set_marker(self.__ani_marker)
        self.point_ani_fyfx.set_markersize(self.__ani_markersize)

        self.point_ani_fyfx.set_xdata(x[num])
        self.point_ani_fyfx.set_ydata(y[num])
        return self.point_ani_fyfx,
    
    def update_points_fyfz(self, num):     
        node_label = self.animation_label["Fy(Fz)"]
        y = self.data[node_label].get("reaction_force_Y_local")
        z = self.data[node_label].get("reaction_force_Z_local")

        self.point_ani_fyfz.set_marker(self.__ani_marker)
        self.point_ani_fyfz.set_markersize(self.__ani_markersize)

        self.point_ani_fyfz.set_xdata(z[num])
        self.point_ani_fyfz.set_ydata(y[num])
        return self.point_ani_fyfz,

    def update_points_fzfx(self, num):     
        node_label = self.animation_label["Fz(Fx)"]
        x = self.data[node_label].get("reaction_force_X_local")
        z = self.data[node_label].get("reaction_force_Z_local")

        self.point_ani_fzfx.set_marker(self.__ani_marker)
        self.point_ani_fzfx.set_markersize(self.__ani_markersize)

        self.point_ani_fzfx.set_xdata(x[num])
        self.point_ani_fzfx.set_ydata(z[num])
        return self.point_ani_fzfx,
    
    def update_points_fzfy(self, num):     
        node_label = self.animation_label["Fz(Fy)"]
        y = self.data[node_label].get("reaction_force_Y_local")
        z = self.data[node_label].get("reaction_force_Z_local")

        self.point_ani_fzfy.set_marker(self.__ani_marker)
        self.point_ani_fzfy.set_markersize(self.__ani_markersize)

        self.point_ani_fzfy.set_xdata(y[num])
        self.point_ani_fzfy.set_ydata(z[num])
        return self.point_ani_fzfy,
    
    def update_points_ft(self, num):     
        node_label = self.animation_label["F(t)"]
        t = self.time
        x = self.data[node_label].get("reaction_force_X_local")
        y = self.data[node_label].get("reaction_force_Y_local")
        z = self.data[node_label].get("reaction_force_Z_local")
        
        # Ftx
        self.point_ani_ftx.set_marker(self.__ani_marker)
        self.point_ani_ftx.set_markersize(self.__ani_markersize)

        self.point_ani_ftx.set_xdata(t[num])
        self.point_ani_ftx.set_ydata(x[num])
        
        #Fty
        self.point_ani_fty.set_marker(self.__ani_marker)
        self.point_ani_fty.set_markersize(self.__ani_markersize)

        self.point_ani_fty.set_xdata(t[num])
        self.point_ani_fty.set_ydata(y[num])

        #Ptz
        self.point_ani_ftz.set_marker(self.__ani_marker)
        self.point_ani_ftz.set_markersize(self.__ani_markersize)

        self.point_ani_ftz.set_xdata(t[num])
        self.point_ani_ftz.set_ydata(z[num])
        
        return self.point_ani_ftx, self.point_ani_fty, self.point_ani_ftz,
    
# --- Animation Velocity ---
    def update_points_ff3d(self, num):
        node_label = self.animation_label["FF3D"]
        x = self.data[node_label].get("reaction_force_X_global")
        y = self.data[node_label].get("reaction_force_Y_global")
        z = self.data[node_label].get("reaction_force_Z_global")
        
        self.point_ani_ff3d.set_marker(self.__ani_marker)
        self.point_ani_ff3d.set_markersize(self.__ani_markersize)

        self.point_ani_ff3d.set_xdata(x[num])
        self.point_ani_ff3d.set_ydata(y[num])
        self.point_ani_ff3d.set_3d_properties(z[num])
        return self.point_ani_ff3d,
    
    def update_points_ffxt(self, num):     
        node_label = self.animation_label["FFx(t)"]
        t = self.time
        x = self.data[node_label].get("reaction_force_X_global")

        self.point_ani_ffxt.set_marker(self.__ani_marker)
        self.point_ani_ffxt.set_markersize(self.__ani_markersize)

        self.point_ani_ffxt.set_xdata(t[num])
        self.point_ani_ffxt.set_ydata(x[num])
        return self.point_ani_ffxt,

    def update_points_ffyt(self, num):     
        node_label = self.animation_label["FFy(t)"]
        t = self.time
        y = self.data[node_label].get("reaction_force_Y_global")

        self.point_ani_ffyt.set_marker(self.__ani_marker)
        self.point_ani_ffyt.set_markersize(self.__ani_markersize)

        self.point_ani_ffyt.set_xdata(t[num])
        self.point_ani_ffyt.set_ydata(y[num])
        return self.point_ani_ffyt,

    def update_points_ffzt(self, num):     
        node_label = self.animation_label["FFz(t)"]
        t = self.time
        z = self.data[node_label].get("reaction_force_Z_global")

        self.point_ani_ffzt.set_marker(self.__ani_marker)
        self.point_ani_ffzt.set_markersize(self.__ani_markersize)

        self.point_ani_ffzt.set_xdata(t[num])
        self.point_ani_ffzt.set_ydata(z[num])
        return self.point_ani_ffzt,

    def update_points_ffxffy(self, num):     
        node_label = self.animation_label["FFx(FFy)"]
        x = self.data[node_label].get("reaction_force_X_global")
        y = self.data[node_label].get("reaction_force_Y_global")

        self.point_ani_ffxffy.set_marker(self.__ani_marker)
        self.point_ani_ffxffy.set_markersize(self.__ani_markersize)

        self.point_ani_ffxffy.set_xdata(y[num])
        self.point_ani_ffxffy.set_ydata(x[num])
        return self.point_ani_ffxffy,

    def update_points_ffxffz(self, num):     
        node_label = self.animation_label["FFx(Vz)"]
        x = self.data[node_label].get("reaction_force_X_global")
        z = self.data[node_label].get("reaction_force_Z_global")

        self.point_ani_ffxffz.set_marker(self.__ani_marker)
        self.point_ani_ffxffz.set_markersize(self.__ani_markersize)

        self.point_ani_ffxffz.set_xdata(z[num])
        self.point_ani_ffxffz.set_ydata(x[num])
        return self.point_ani_ffxffz,

    def update_points_ffyffx(self, num):     
        node_label = self.animation_label["FFy(FFx)"]
        x = self.data[node_label].get("reaction_force_X_global")
        y = self.data[node_label].get("reaction_force_Y_global")

        self.point_ani_ffyffx.set_marker(self.__ani_marker)
        self.point_ani_ffyffx.set_markersize(self.__ani_markersize)

        self.point_ani_ffyffx.set_xdata(x[num])
        self.point_ani_ffyffx.set_ydata(y[num])
        return self.point_ani_ffyffx,

    def update_points_ffyffz(self, num):     
        node_label = self.animation_label["FFy(FFz)"]
        y = self.data[node_label].get("reaction_force_Y_global")
        z = self.data[node_label].get("reaction_force_Z_global")

        self.point_ani_ffyffz.set_marker(self.__ani_marker)
        self.point_ani_ffyffz.set_markersize(self.__ani_markersize)

        self.point_ani_ffyffz.set_xdata(z[num])
        self.point_ani_ffyffz.set_ydata(y[num])
        return self.point_ani_ffyffz,

    def update_points_ffzffx(self, num):     
        node_label = self.animation_label["FFz(FFx)"]
        x = self.data[node_label].get("reaction_force_X_global")
        z = self.data[node_label].get("reaction_force_Z_global")

        self.point_ani_ffzffx.set_marker(self.__ani_marker)
        self.point_ani_ffzffx.set_markersize(self.__ani_markersize)

        self.point_ani_ffzffx.set_xdata(x[num])
        self.point_ani_ffzffx.set_ydata(z[num])
        return self.point_ani_ffzffx,

    def update_points_ffzffy(self, num):     
        node_label = self.animation_label["FFz(FFy)"]
        y = self.data[node_label].get("reaction_force_Y_global")
        z = self.data[node_label].get("reaction_force_Z_global")

        self.point_ani_ffzffy.set_marker(self.__ani_marker)
        self.point_ani_ffzffy.set_markersize(self.__ani_markersize)

        self.point_ani_ffzffy.set_xdata(y[num])
        self.point_ani_ffzffy.set_ydata(z[num])
        return self.point_ani_ffzffy,

    def update_points_FFt(self, num):     
        node_label = self.animation_label["FF(t)"]
        t = self.time
        x = self.data[node_label].get("reaction_force_X_global")
        y = self.data[node_label].get("reaction_force_Y_global")
        z = self.data[node_label].get("reaction_force_Z_global")
        
        # FFtx
        self.point_ani_fftx.set_marker(self.__ani_marker)
        self.point_ani_fftx.set_markersize(self.__ani_markersize)

        self.point_ani_fftx.set_xdata(t[num])
        self.point_ani_fftx.set_ydata(x[num])
        
        #FFty
        self.point_ani_ffty.set_marker(self.__ani_marker)
        self.point_ani_ffty.set_markersize(self.__ani_markersize)

        self.point_ani_ffty.set_xdata(t[num])
        self.point_ani_ffty.set_ydata(y[num])

        #FFtz
        self.point_ani_fftz.set_marker(self.__ani_marker)
        self.point_ani_fftz.set_markersize(self.__ani_markersize)

        self.point_ani_fftz.set_xdata(t[num])
        self.point_ani_fftz.set_ydata(z[num])
        
        return self.point_ani_fftx, self.point_ani_ffty, self.point_ani_fftz,
    
# --- Animation Torque ---
    def update_points_t3d(self, num):
        node_label = self.animation_label["T3D"]
        x = self.data[node_label].get("reaction_couple_X_local")
        y = self.data[node_label].get("reaction_couple_Y_local")
        z = self.data[node_label].get("reaction_couple_Z_local")
        
        self.point_ani_t3d.set_marker(self.__ani_marker)
        self.point_ani_t3d.set_markersize(self.__ani_markersize)

        self.point_ani_t3d.set_xdata(x[num])
        self.point_ani_t3d.set_ydata(y[num])
        self.point_ani_t3d.set_3d_properties(z[num])
        return self.point_ani_t3d,
    
    def update_points_txt(self, num):     
        node_label = self.animation_label["Tx(t)"]
        t = self.time
        x = self.data[node_label].get("reaction_couple_X_local")

        self.point_ani_txt.set_marker(self.__ani_marker)
        self.point_ani_txt.set_markersize(self.__ani_markersize)

        self.point_ani_txt.set_xdata(t[num])
        self.point_ani_txt.set_ydata(x[num])
        return self.point_ani_txt,

    def update_points_tyt(self, num):     
        node_label = self.animation_label["Ty(t)"]
        t = self.time
        y = self.data[node_label].get("reaction_couple_Y_local")

        self.point_ani_tyt.set_marker(self.__ani_marker)
        self.point_ani_tyt.set_markersize(self.__ani_markersize)

        self.point_ani_tyt.set_xdata(t[num])
        self.point_ani_tyt.set_ydata(y[num])
        return self.point_ani_tyt,

    def update_points_tzt(self, num):     
        node_label = self.animation_label["Tz(t)"]
        t = self.time
        z = self.data[node_label].get("reaction_couple_Z_local")

        self.point_ani_tzt.set_marker(self.__ani_marker)
        self.point_ani_tzt.set_markersize(self.__ani_markersize)

        self.point_ani_tzt.set_xdata(t[num])
        self.point_ani_tzt.set_ydata(z[num])
        return self.point_ani_tzt,

    def update_points_tt(self, num):     
        node_label = self.animation_label["T(t)"]
        t = self.time
        x = self.data[node_label].get("reaction_couple_X_local")
        y = self.data[node_label].get("reaction_couple_Y_local")
        z = self.data[node_label].get("reaction_couple_Z_local")
        
        # Tx
        self.point_ani_ttx.set_marker(self.__ani_marker)
        self.point_ani_ttx.set_markersize(self.__ani_markersize)

        self.point_ani_ttx.set_xdata(t[num])
        self.point_ani_ttx.set_ydata(x[num])
        
        # Ty
        self.point_ani_tty.set_marker(self.__ani_marker)
        self.point_ani_tty.set_markersize(self.__ani_markersize)

        self.point_ani_tty.set_xdata(t[num])
        self.point_ani_tty.set_ydata(y[num])

        # Tz
        self.point_ani_ttz.set_marker(self.__ani_marker)
        self.point_ani_ttz.set_markersize(self.__ani_markersize)

        self.point_ani_ttz.set_xdata(t[num])
        self.point_ani_ttz.set_ydata(z[num])
        
        return self.point_ani_ttx, self.point_ani_tty, self.point_ani_ttz,
    
# --- Plot reaction force in local frame ---        
    def Fx(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("reaction_force_X_local")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("reaction_force_X_local")[:length],
                     label='Fx(t)',
                     color='red')
            plt.ylabel('Fx[N]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('X component of local reaction force as function of time. Joint: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Fx(t)"] = node_label
                self.point_ani_fxt, = plt.plot(self.time[0],
                                               self.data[node_label].get("reaction_force_X_local")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_fxt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)           
            plt.show()
        if t == "Fy":
            length = min(len(self.data[node_label].get("reaction_force_X_local")), len(self.data[node_label].get("reaction_force_Y_local")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_Y_local")[:length],
                     self.data[node_label].get("reaction_force_X_local")[:length],
                     label='Fx(Fy)',
                     color='black')
            plt.ylabel('Fx[N]')
            plt.xlabel('Fy[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('X component of local reaction force as function of Y component of local reaction force. Joint: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Fx(Fy)"] = node_label
                self.point_ani_fxfy, = plt.plot(self.data[node_label].get("reaction_force_Y_local")[0],
                                                self.data[node_label].get("reaction_force_X_local")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_fxfy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Fz":
            length = min(len(self.data[node_label].get("reaction_force_X_local")), len(self.data[node_label].get("reaction_force_Z_local")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_Z_local")[:length],self.data[node_label].get("reaction_force_X_local")[:length],label='Fx(Fz)',color='black')
            plt.ylabel('Fx[N]')
            plt.xlabel('Fz[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('X component of local reaction force as function of Z component of local reaction force. Joint: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Fx(Fz)"] = node_label
                self.point_ani_fxfz, = plt.plot(self.data[node_label].get("reaction_force_Z_local")[0],
                                                self.data[node_label].get("reaction_force_X_local")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_fxfz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def Fy(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("reaction_force_Y_local")))
            fig = plt.figure()
            plt.plot(self.time[:length],self.data[node_label].get("reaction_force_Y_local")[:length],label='Py(t)',color='green')
            plt.ylabel('Fy[N]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Y component of local reaction force as function of time. Joint: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Fy(t)"] = node_label
                self.point_ani_fyt, = plt.plot(self.time[0],
                                               self.data[node_label].get("reaction_force_Y_local")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_fyt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Fx":
            length = min(len(self.data[node_label].get("reaction_force_X_local")), len(self.data[node_label].get("reaction_force_Y_local")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_X_local")[:length],self.data[node_label].get("reaction_force_Y_local")[:length],label='Fy(Fx)',color='black')
            plt.ylabel('Fy[N]')
            plt.xlabel('Fx[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Y component of local reaction force as function of X component of local reaction force. Joint: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Fy(Fx)"] = node_label
                self.point_ani_fyfx, = plt.plot(self.data[node_label].get("reaction_force_X_local")[0],
                                                self.data[node_label].get("reaction_force_Y_local")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_fyfx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Fz":
            length = min(len(self.data[node_label].get("reaction_force_Y_local")), len(self.data[node_label].get("reaction_force_Z_local")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_Z_local")[:length],self.data[node_label].get("reaction_force_Y_local")[:length],label='Py(Pz)',color='black')
            plt.ylabel('Fy[N]')
            plt.xlabel('Fz[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Y component of local reaction force as function of Z component of local reaction force. Joint: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Fy(Fz)"] = node_label
                self.point_ani_fyfz, = plt.plot(self.data[node_label].get("reaction_force_Z_local")[0],
                                                self.data[node_label].get("reaction_force_Y_local")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_fyfz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def Fz(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("reaction_force_Z_local")))
            fig = plt.figure()
            plt.plot(self.time[:length],self.data[node_label].get("reaction_force_Z_local")[:length],label='Pz(t)',color='blue')
            plt.ylabel('Fz[N]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Z component of local reaction force as function of time. Joint: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Fz(t)"] = node_label
                self.point_ani_fzt, = plt.plot(self.time[0],
                                               self.data[node_label].get("reaction_force_Z_local")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_fzt,
                                              frames   = len(self.time),
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Fx":
            length = min(len(self.data[node_label].get("reaction_force_X_local")), len(self.data[node_label].get("reaction_force_Z_local")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_X_local")[:length],self.data[node_label].get("reaction_force_Z_local")[:length],label='Fz(Fx)',color='black')
            plt.ylabel('Fz[N]')
            plt.xlabel('Fx[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Z component of local reaction force as function of X component of local reaction force. Joint: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Fz(Fx)"] = node_label
                self.point_ani_fzfx, = plt.plot(self.data[node_label].get("reaction_force_X_local")[0],
                                                self.data[node_label].get("reaction_force_Z_local")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_fzfx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "Fy":
            length = min(len(self.data[node_label].get("reaction_force_Y_local")), len(self.data[node_label].get("reaction_force_Z_local")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_Y_local")[:length],self.data[node_label].get("reaction_force_Z_local")[:length],label='Py(Pz)',color='black')
            plt.ylabel('Fz[N]')
            plt.xlabel('Fy[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Z component of local reaction force as function of Y component of local reaction force. Joint: '+ node_label)
            if self.enableAnimation == True:
                self.animation_label["Fz(Fy)"] = node_label
                self.point_ani_fzfy, = plt.plot(self.data[node_label].get("reaction_force_Y_local")[0],
                                                self.data[node_label].get("reaction_force_Z_local")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_fzfy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def F(self, node_label="1"):
        length = min(len(self.time), len(self.data[node_label].get("reaction_force_X_local")))
        length = min(length, len(self.data[node_label].get("reaction_force_Y_local")))
        length = min(length, len(self.data[node_label].get("reaction_force_Z_local")))
        fig = plt.figure()
        plt.plot(self.time[:length],self.data[node_label].get("reaction_force_X_local")[:length],label='Fx(t)',color='red')
        plt.plot(self.time[:length],self.data[node_label].get("reaction_force_Y_local")[:length],label='Fy(t)',color='green')
        plt.plot(self.time[:length],self.data[node_label].get("reaction_force_Z_local")[:length],label='Fz(t)',color='blue')
        plt.ylabel('F[N]')
        plt.xlabel('t[s]')
        plt.legend()            
        plt.grid()
        #plt.axis('equal')
        plt.suptitle('Local reaction force as function of time. Joint: '+ node_label)
        if self.enableAnimation == True:
            self.animation_label["F(t)"] = node_label
            self.point_ani_ftx, = plt.plot(self.time[0],
                                           self.data[node_label].get("reaction_force_X_local")[0],
                                           "ro")
            self.point_ani_fty, = plt.plot(self.time[0],
                                           self.data[node_label].get("reaction_force_Y_local")[0],
                                           "ro")
            self.point_ani_ftz, = plt.plot(self.time[0],
                                           self.data[node_label].get("reaction_force_Z_local")[0],
                                           "ro") 
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_ft,
                                          frames   = length,
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()

    def F3D(self, node_label="1"):
        x = self.data[node_label].get("reaction_force_X_local")
        y = self.data[node_label].get("reaction_force_Y_local")
        z = self.data[node_label].get("reaction_force_Z_local")
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(x, y, z, label='Fx,Fy,Fz')
        ax.legend()            
        ax.set_xlabel('Fx[N]')
        ax.set_ylabel('Fy[N]')
        ax.set_zlabel('Fz[N]')
        plt.legend()
        plt.grid()
        #plt.axis('equal')
        plt.suptitle('3D local reaction force. Joint: '+ node_label)
        if self.enableAnimation == True:
            self.animation_label["F3D"] = node_label
            self.point_ani_f3d, = ax.plot([x[0]], [y[0]], [z[0]], "ro")
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_f3d,
                                          frames   = len(x),
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()
        
# --- FORCE RELATIVE TO GLOBAL REFERENCE FRAME (FF) ---
    def FFx(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("reaction_force_X_global")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("reaction_force_X_global")[:length],
                     label='FFx(t)',
                     color='red')
            plt.ylabel('FFx[N]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('X component of global reaction force as function of time. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1)          
            if self.enableAnimation == True:
                self.animation_label["FFx(t)"] = node_label
                self.point_ani_ffxt, = plt.plot(self.time[0],
                                               self.data[node_label].get("reaction_force_X_global")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ffxt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)           
            plt.show()
        if t == "FFy":
            length = min(len(self.data[node_label].get("reaction_force_X_global")), len(self.data[node_label].get("reaction_force_Y_global")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_Y_global")[:length],
                     self.data[node_label].get("reaction_force_X_global")[:length],
                     label='FFx(FFy)',
                     color='black')
            plt.ylabel('FFx[N]')
            plt.xlabel('FFy[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('X component of global reaction force as function of Y component of global reaction force. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["FFx(FFy)"] = node_label
                self.point_ani_ffxffy, = plt.plot(self.data[node_label].get("reaction_force_Y_global")[0],
                                                  self.data[node_label].get("reaction_force_X_global")[0],
                                                  "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ffxffy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "FFz":
            length = min(len(self.data[node_label].get("reaction_force_X_global")), len(self.data[node_label].get("reaction_force_Z_global")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_Z_global")[:length],
                     self.data[node_label].get("reaction_force_X_global")[:length],
                     label='FFx(FFz)',
                     color='black')
            plt.ylabel('FFx[N]')
            plt.xlabel('FFz[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('X component of global reaction force as function of Z component of global reaction force. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["FFx(FFz)"] = node_label
                self.point_ani_ffxffz, = plt.plot(self.data[node_label].get("reaction_force_Z_global")[0],
                                                  self.data[node_label].get("reaction_force_X_global")[0],
                                                  "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ffxffz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def FFy(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("reaction_force_Y_global")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("reaction_force_Y_global")[:length],
                     label='FFy(t)',
                     color='green')
            plt.ylabel('FFy[N]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Y component of global reaction force as function of time. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["FFy(t)"] = node_label
                self.point_ani_ffyt, = plt.plot(self.time[0],
                                                self.data[node_label].get("reaction_force_Y_global")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ffyt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "FFx":
            length = min(len(self.data[node_label].get("reaction_force_X_global")), len(self.data[node_label].get("reaction_force_Y_global")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_X_global")[:length],
                     self.data[node_label].get("reaction_force_Y_global")[:length],
                     label='FFy(FFx)',
                     color='black')
            plt.ylabel('FFy[N]')
            plt.xlabel('FFx[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Y component of global reaction force as function of X component of global reaction force. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["FFy(FFx)"] = node_label
                self.point_ani_ffyffx, = plt.plot(self.data[node_label].get("reaction_force_X_global")[0],
                                                  self.data[node_label].get("reaction_force_Y_global")[0],
                                                  "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ffyffx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "FFz":
            length = min(len(self.data[node_label].get("reaction_force_Y_global")), len(self.data[node_label].get("reaction_force_Z_global")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_Z_global")[:length],
                     self.data[node_label].get("reaction_force_Y_global")[:length],
                     label='FFy(FFz)',
                     color='black')
            plt.ylabel('FFy[N]')
            plt.xlabel('FFz[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Y component of global reaction force as function of Z component of global reaction force. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["FFy(FFz)"] = node_label
                self.point_ani_ffyffz, = plt.plot(self.data[node_label].get("reaction_force_Z_global")[0],
                                                  self.data[node_label].get("reaction_force_Y_global")[0],
                                                  "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ffyffz,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def FFz(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("reaction_force_Z_global")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("reaction_force_Z_global")[:length],
                     label='FFz(t)',
                     color='blue')
            plt.ylabel('FFz[N]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Z component of global reaction force as function of time. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["FFz(t)"] = node_label
                self.point_ani_ffzt, = plt.plot(self.time[0],
                                                self.data[node_label].get("reaction_force_Z_global")[0],
                                                "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ffzt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "FFx":
            length = min(len(self.data[node_label].get("reaction_force_X_global")), len(self.data[node_label].get("reaction_force_Z_global")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_X_global")[:length],
                     self.data[node_label].get("reaction_force_Z_global")[:length],
                     label='FFz(FFx)',
                     color='black')
            plt.ylabel('FFz[N]')
            plt.xlabel('FFx[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Z component of global reaction force as function of X component of global reaction force. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["FFz(FFx)"] = node_label
                self.point_ani_ffzffx, = plt.plot(self.data[node_label].get("reaction_force_X_global")[0],
                                                  self.data[node_label].get("reaction_force_Z_global")[0],
                                                  "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ffzffx,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()
        if t == "FFy":
            length = min(len(self.data[node_label].get("reaction_force_Y_global")), len(self.data[node_label].get("reaction_force_Z_global")))
            fig = plt.figure()
            plt.plot(self.data[node_label].get("reaction_force_Y_global")[:length],
                     self.data[node_label].get("reaction_force_Z_global")[:length],
                     label='FFz(FFy)',
                     color='black')
            plt.ylabel('FFz[N]')
            plt.xlabel('FFy[N]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Z component of global reaction force as function of Y component of global reaction force. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["FFz(FFy)"] = node_label
                self.point_ani_ffzffy, = plt.plot(self.data[node_label].get("reaction_force_Y_global")[0],
                                                  self.data[node_label].get("reaction_force_Z_global")[0],
                                                  "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ffzffy,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def FF(self, node_label="1"):
        length = min(len(self.time), len(self.data[node_label].get("reaction_force_X_global")))
        length = min(length, len(self.data[node_label].get("reaction_force_Y_global")))
        length = min(length, len(self.data[node_label].get("reaction_force_Z_global")))
        fig = plt.figure()
        plt.plot(self.time[:length],self.data[node_label].get("reaction_force_X_global")[:length],label='Vx(t)',color='red')
        plt.plot(self.time[:length],self.data[node_label].get("reaction_force_Y_global")[:length],label='Vy(t)',color='green')
        plt.plot(self.time[:length],self.data[node_label].get("reaction_force_Z_global")[:length],label='Vz(t)',color='blue')
        plt.ylabel('FF[N]')
        plt.xlabel('t[s]')
        plt.legend()            
        plt.grid()
        #plt.axis('equal')
        plt.suptitle('Global reaction force as function of time. Joint: '+ node_label)
        if self.enableAnimation == True:
            self.animation_label["FF(t)"] = node_label
            self.point_ani_fftx, = plt.plot(self.time[0],
                                            self.data[node_label].get("reaction_force_X_global")[0],
                                            "ro")
            self.point_ani_ffty, = plt.plot(self.time[0],
                                            self.data[node_label].get("reaction_force_Y_global")[0],
                                            "ro")
            self.point_ani_fftz, = plt.plot(self.time[0],
                                            self.data[node_label].get("reaction_force_Z_global")[0],
                                            "ro") 
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_fft,
                                          frames   = length,
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()

    def FF3D(self, node_label="1"):
        x = self.data[node_label].get("reaction_force_X_global")
        y = self.data[node_label].get("reaction_force_Y_global")
        z = self.data[node_label].get("reaction_force_Z_global")
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(x, y, z, label='FFx,FFy,FFz')
        ax.legend()            
        ax.set_xlabel('FFx[N]')
        ax.set_ylabel('FFy[N]')
        ax.set_zlabel('FFz[N]')
        plt.legend()
        plt.grid()
        #plt.axis('equal')
        plt.suptitle('3D global reaction force. Joint: '+ node_label)
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
            self.animation_label["FF3D"] = node_label
            self.point_ani_ff3d, = ax.plot([x[0]], [y[0]], [z[0]], "ro")
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_ff3d,
                                          frames   = len(self.time),
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()
        
# --- TORQUE IN LOCAL FRAME ---
    def Tx(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("reaction_couple_X_local")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("reaction_couple_X_local")[:length],
                     label='Tx(t)',
                     color='red')
            plt.ylabel('Tx[N*m]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('X component of global torque as function of time. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1)          
            if self.enableAnimation == True:
                self.animation_label["Tx(t)"] = node_label
                self.point_ani_txt, = plt.plot(self.time[0],
                                               self.data[node_label].get("reaction_couple_X_local")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_txt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)           
            plt.show()

    def Ty(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("reaction_couple_Y_local")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("reaction_couple_Y_local")[:length],
                     label='Ty(t)',
                     color='green')
            plt.ylabel('Ty[N*m]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Y component of global torque as function of time. Joint: '+ node_label)
            xlim = plt.xlim()
            if math.fabs(xlim[0]-xlim[1]) < 1e-3:
                plt.xlim(xmin = xlim[0] - 0.1)
                plt.xlim(xmax = xlim[1] + 0.1)  
            ylim = plt.ylim()
            if math.fabs(ylim[0]-ylim[1]) < 1e-3:
                plt.ylim(ymin = ylim[0] - 0.1)
                plt.ylim(ymax = ylim[1] + 0.1) 
            if self.enableAnimation == True:
                self.animation_label["Ty(t)"] = node_label
                self.point_ani_tyt, = plt.plot(self.time[0],
                                               self.data[node_label].get("reaction_couple_Y_local")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_tyt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def Tz(self,t=None,node_label="1"):
        if t == None:
            length = min(len(self.time), len(self.data[node_label].get("reaction_couple_Z_local")))
            fig = plt.figure()
            plt.plot(self.time[:length],
                     self.data[node_label].get("reaction_couple_Z_local")[:length],
                     label='Tz(t)',
                     color='blue')
            plt.ylabel('Tz[N*m]')
            plt.xlabel('t[s]')
            plt.legend()            
            plt.grid()
            #plt.axis('equal')
            plt.suptitle('Z component of global torque as function of time. Joint: '+ node_label)
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
                                               self.data[node_label].get("reaction_couple_Z_local")[0],
                                               "ro")
                ani = animation.FuncAnimation(fig      = fig,
                                              func     = self.update_points_ozt,
                                              frames   = length,
                                              interval = self.__ani_interval,
                                              repeat   = True,
                                              blit     = True)
            plt.show()

    def T(self, node_label="1"):
        length = min(len(self.time), len(self.data[node_label].get("reaction_couple_X_local")))
        length = min(length, len(self.data[node_label].get("reaction_couple_Y_local")))
        length = min(length, len(self.data[node_label].get("reaction_couple_Z_local")))
        fig = plt.figure()
        plt.plot(self.time[:length],self.data[node_label].get("reaction_couple_X_local")[:length],label='Tx(t)',color='red')
        plt.plot(self.time[:length],self.data[node_label].get("reaction_couple_Y_local")[:length],label='Ty(t)',color='green')
        plt.plot(self.time[:length],self.data[node_label].get("reaction_couple_Z_local")[:length],label='Tz(t)',color='blue')
        plt.ylabel('T[N*m]')
        plt.xlabel('t[s]')
        plt.legend()            
        plt.grid()
        #plt.axis('equal')
        plt.suptitle('Local torque as function of time. Joint: '+ node_label)
        xlim = plt.xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            plt.xlim(xmin = xlim[0] - 0.1)
            plt.xlim(xmax = xlim[1] + 0.1)  
        ylim = plt.ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            plt.ylim(ymin = ylim[0] - 0.1)
            plt.ylim(ymax = ylim[1] + 0.1) 
        if self.enableAnimation == True:
            self.animation_label["T(t)"] = node_label
            self.point_ani_ttx, = plt.plot(self.time[0],
                                           self.data[node_label].get("reaction_couple_X_local")[0],
                                           "ro")
            self.point_ani_tty, = plt.plot(self.time[0],
                                           self.data[node_label].get("reaction_couple_Y_local")[0],
                                           "ro")
            self.point_ani_ttz, = plt.plot(self.time[0],
                                           self.data[node_label].get("reaction_couple_Z_local")[0],
                                           "ro") 
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_tt,
                                          frames   = length,
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()

    def T3D(self, node_label="1"):
        x = self.data[node_label].get("reaction_couple_X_local")
        y = self.data[node_label].get("reaction_couple_Y_local")
        z = self.data[node_label].get("reaction_couple_Z_local")
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(x, y, z, label='Tx,Ty,Tz')
        ax.legend()            
        ax.set_xlabel('Tx[N*m]')
        ax.set_ylabel('Ty[N*m]')
        ax.set_zlabel('Tz[N*m]')
        plt.legend()
        plt.grid()
        #plt.axis('equal')
        plt.suptitle('Local 3D torque. Joint: '+ node_label)
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
            self.point_ani_t3d, = ax.plot([x[0]], [y[0]], [z[0]], "ro")
            ani = animation.FuncAnimation(fig      = fig,
                                          func     = self.update_points_t3d,
                                          frames   = len(self.time),
                                          interval = 10,
                                          repeat   = True,
                                          blit     = True)
        plt.show()
               
    def ALL(self, node_label="1"):
        length = min(len(self.time), len(self.data[node_label].get("reaction_couple_X_local")))
        length = min(length, len(self.data[node_label].get("reaction_couple_Y_local")))
        length = min(length, len(self.data[node_label].get("reaction_couple_Z_local")))
        time= self.time[:length]
        fx   = self.data[node_label].get("reaction_force_X_local")[:length]
        fy   = self.data[node_label].get("reaction_force_Y_local")[:length]
        fz   = self.data[node_label].get("reaction_force_Z_local")[:length]
        tx   = self.data[node_label].get("reaction_couple_X_local")[:length]
        ty   = self.data[node_label].get("reaction_couple_Y_local")[:length]
        tz   = self.data[node_label].get("reaction_couple_Z_local")[:length]
        f1x  = self.data[node_label].get("reaction_force_X_global")[:length]
        f1y  = self.data[node_label].get("reaction_force_Y_global")[:length]
        f1z  = self.data[node_label].get("reaction_force_Z_global")[:length]
        t1x  = self.data[node_label].get("reaction_couple_X_global")[:length]
        t1y  = self.data[node_label].get("reaction_couple_Y_global")[:length]
        t1z  = self.data[node_label].get("reaction_couple_Z_global")[:length]
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
        ax1.plot(time,fx)
        xlim = ax1.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax1.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax1.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax1.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax5.plot(time,fy)
        xlim = ax5.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax5.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax5.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax5.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax9.plot(time,fz)
        xlim = ax9.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax9.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax9.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax9.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax1.set_ylabel('Fx[N]')
        ax1.set_xlabel('t[s]')
        ax5.set_ylabel('Fy[N]')
        ax5.set_xlabel('t[s]')
        ax9.set_ylabel('Fz[N]')
        ax9.set_xlabel('t[s]')        
        ax2.plot(time,tx)
        xlim = ax2.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax2.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax2.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax2.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax6.plot(time,ty)
        xlim = ax6.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax6.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax6.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax6.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax10.plot(time,tz)
        xlim = ax10.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax10.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax10.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax10.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax2.set_ylabel('local reaction torque x [N*m]')
        ax2.set_xlabel('t[s]')
        ax6.set_ylabel('local reaction torque y [N*m]')
        ax6.set_xlabel('t[s]')
        ax10.set_ylabel('local reaction torque z [N*m]')
        ax10.set_xlabel('t[s]')
        ax3.plot(time,f1x)
        xlim = ax3.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax3.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax3.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax3.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax7.plot(time,f1y)
        xlim = ax7.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax7.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax7.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax7.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax11.plot(time,f1z)
        xlim = ax11.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax11.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax11.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax11.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax3.set_ylabel('global reaction force x [N]')
        ax3.set_xlabel('t[s]')
        ax7.set_ylabel('global reaction force y [N]')
        ax7.set_xlabel('t[s]')
        ax11.set_ylabel('global reaction force z [N]')
        ax11.set_xlabel('t[s]')
        ax4.plot(time,t1x)
        xlim = ax4.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax4.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax4.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax4.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax8.plot(time,t1y)
        xlim = ax8.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax8.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax8.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax8.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax12.plot(time,t1z)
        xlim = ax12.get_xlim()
        if math.fabs(xlim[0]-xlim[1]) < 1e-3:
            ax12.set_xlim([xlim[0]-0.1, xlim[1]+0.1])
        ylim = ax12.get_ylim()
        if math.fabs(ylim[0]-ylim[1]) < 1e-3:
            ax12.set_ylim([ylim[0]-0.1, ylim[1]+0.1])
        ax4.set_ylabel('global reaction torque x [N*m]')
        ax4.set_xlabel('t[s]')
        ax8.set_ylabel('global reaction torque y [N*m]')
        ax8.set_xlabel('t[s]')
        ax12.set_ylabel('global reaction torque z [N*m]')
        ax12.set_xlabel('t[s]')
        plt.legend()
        plt.suptitle('Simulation results. Joint: '+ node_label)
        plt.show()
            
def main():
    mbd = MBDynJntPlot("pendulum")
    mbd.clear_run()
    if mbd.getData():
        mbd.Fy(t="Fx",node_label="1002")
    
if __name__ == '__main__':
    main()
    

