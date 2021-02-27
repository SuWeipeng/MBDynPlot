from MBDynMovPlot import MBDynMovPlot

mov = MBDynMovPlot("doublependulum")

if mov.getData():
    mov.Py(t="Pz",node_label="6")
