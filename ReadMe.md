Plot for MBDyn
---
* [about MBDyn click here](https://www.mbdyn.org/)

![](http://weipeng_su.gitee.io/img/30_MBDyn/ff_01.gif)

Example
---
```py
from MBDynMovPlot import MBDynMovPlot

mov = MBDynMovPlot("rigidbody.mbd")

if mov.getData():
    mov.P3D(node_label="1")
```

Plot Function
---
> Position

1. P3D()
2. P()
3. Px()
4. Px(t="Py")
5. Px(t="Pz")
6. Py()
7. Py(t="Px")
8. Py(t="Pz")
9. Pz()
10. Pz(t="Px")
11. Pz(t="Py")

> Orientation

1. O3D()
2. O()
3. roll()
4. roll(t="pitch")
5. roll(t="yaw")
6. pitch()
7. pitch(t="roll")
8. pitch(t="yaw")
9. yaw()
10. yaw(t="roll")
11. yaw(t="pitch")

> Velocity

1. V3D()
2. V()
3. Vx()
4. Vx(t="Vy")
5. Vx(t="Vz")
6. Vy()
7. Vy(t="Vx")
8. Vy(t="Vz")
9. Vz()
10. Vz(t="Vx")
11. Vz(t="Vy")

> Angular Velocity

1. W3D()
2. W()
3. Wx()
4. Wx(t="Wy")
5. Wx(t="Wz")
6. Wy()
7. Wy(t="Wx")
8. Wy(t="Wz")
9. Wz()
10. Wz(t="Wx")
11. Wz(t="Wy")
