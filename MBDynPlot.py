from MBDynMovPlot import MBDynMovPlot

mov = MBDynMovPlot("rigidbody.mbd")

if mov.getData():
    mov.P3D()