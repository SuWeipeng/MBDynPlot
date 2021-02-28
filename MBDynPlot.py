from MBDynMovPlot import MBDynMovPlot

mov = MBDynMovPlot("rigidbody.mbd")
mov.clear_run() # optional
if mov.getData():
    mov.P3D(node_label="1")
    
