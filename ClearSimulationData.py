import os

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
    