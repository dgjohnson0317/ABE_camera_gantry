'''
import numpy as np
import matplotlib.pyplot as plt

import numpy as np

data = np.loadtxt('tf_data_fine.csv', delimiter=',', skiprows=0)

t = data[:, 0]
x = data[:, 1]
y = data[:, 2]
z = data[:, 3]

# keep only strictly increasing time steps
mask = np.diff(t, prepend=t[0] - 1e-9) > 0

t = t[mask]
x = x[mask]
y = y[mask]
z = z[mask]


vx, vy, vz = np.gradient(x, t), np.gradient(y, t), np.gradient(z, t)
ax, ay, az = np.gradient(vx, t), np.gradient(vy, t), np.gradient(vz, t)
#jx, jy, jz = np.gradient(ax, t), np.gradient(ay, t), np.gradient(az, t)


#plt.plot(t, vx, label='vx'); plt.plot(t, vy, label='vy'); plt.plot(t, vz, label='vz')
plt.plot(t, ax, label='ax'); plt.plot(t, ay, label='ay'); plt.plot(t, az, label='az')

#plt.plot(t, np.linalg.norm([vx,vy,vz], axis=0), label='velocity')
plt.plot(t, np.linalg.norm([ax,ay,az], axis=0), label='acceleration')
#plt.plot(t, np.linalg.norm([jx,jy,jz], axis=0), label='jerk')
plt.title('Tensile Fine Acceleration')
plt.legend(); plt.show()
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -----------------------
# LOAD + PROCESS (UNCHANGED)
# -----------------------
data = np.loadtxt('tf_data.csv', delimiter=',', skiprows=0)

t = data[:, 0]
x = data[:, 1]
y = data[:, 2]
z = data[:, 3]

# keep only strictly increasing time steps
mask = np.diff(t, prepend=t[0] - 1e-9) > 0

t = t[mask]
x = x[mask]
y = y[mask]
z = z[mask]

vx, vy, vz = np.gradient(x, t), np.gradient(y, t), np.gradient(z, t)
ax_data, ay_data, az_data = np.gradient(vx, t), np.gradient(vy, t), np.gradient(vz, t)

acc = np.vstack((ax_data, ay_data, az_data)).T

# -----------------------
# OPTIONAL: SMOOTHING (VERY IMPORTANT)
# -----------------------
#alpha = 0.2
#acc_smooth = np.zeros_like(acc)

#for i in range(1, len(acc)):
#    acc_smooth[i] = alpha * acc[i] + (1 - alpha) * acc_smooth[i-1]
 #convert to Gs
#acc_smooth /= 9.81


# -----------------------
# 3D LIVE G-METER SETUP
# -----------------------
plt.ion()

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# fixed limits (critical)
ax.set_xlim([-6, 6])
ax.set_ylim([-6, 6])
ax.set_zlim([-6, 6])

ax.set_xlabel("Forward")
ax.set_ylabel("Left")
ax.set_zlabel("Up")
ax.set_title("3D G-Meter (TCP Acceleration)")

# lock camera
#ax.view_init(elev=20, azim=45)

# ---- unit sphere (1g reference)
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
sx = np.cos(u)*np.sin(v)
sy = np.sin(u)*np.sin(v)
sz = np.cos(v)

ax.plot_wireframe(sx, sy, sz, alpha=0.15)

# ---- initial arrow + trail
quiver = ax.quiver(0, 0, 0, 0, 0, 0)

trail_len = 50
trail = np.zeros((trail_len, 3))
line, = ax.plot([], [], [])

# -----------------------
# LIVE UPDATE LOOP
# -----------------------
for i in range(len(acc)):

    a = acc[i]

    # update arrow
    quiver.remove()
    mag = np.linalg.norm(a)
    color = plt.cm.jet(min(mag / 2, 1))

    quiver = ax.quiver(0, 0, 0, a[0], a[1], a[2], color=color)

    # update trail
    trail = np.roll(trail, -1, axis=0)
    trail[-1] = a

    line.set_data(trail[:, 0], trail[:, 1])
    line.set_3d_properties(trail[:, 2])

    plt.draw()
    
    # real-time pause
    if i > 0:
        dt = t[i] - t[i-1]
    else:
        dt = 0.01

    plt.pause(dt)

plt.ioff()
plt.show()
