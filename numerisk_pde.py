import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from matplotlib import cm

# Problembeskrivelse, randkrav og initialverdier
x_lengde = y_lengde = 40
totaltid = 20

romlige_antall_punkter = 20
tid_antall_punkter = 10000

x_skrittlengde_hx = x_lengde/romlige_antall_punkter
y_skrittlengde_hy = y_lengde/romlige_antall_punkter

tid_skrittlengde_k = totaltid/tid_antall_punkter

x_verdier = np.linspace(0, x_lengde, romlige_antall_punkter)
y_verdier = np.linspace(0, y_lengde, romlige_antall_punkter)
t_verdier = np.linspace(0, totaltid, tid_antall_punkter)

u_verdier = np.zeros((romlige_antall_punkter, romlige_antall_punkter, tid_antall_punkter))

start_varmefordeling = lambda x, y: np.cos(3*np.sqrt((x-1)**2 + (y-3)**2))

start_verdier = np.zeros((romlige_antall_punkter, romlige_antall_punkter))

for i in range(len(x_verdier)):
    for j in range(len(y_verdier)):
        start_verdier[i, j] = start_varmefordeling(x_verdier[i], y_verdier[j])

u_verdier[1:-1,1:-1,0] = start_verdier[1:-1, 1:-1]


# Euler eksplisitt

def u_next(u):
    u_next = np.zeros((romlige_antall_punkter, romlige_antall_punkter))
    for i in range(1, romlige_antall_punkter-1):
        for j in range(1, romlige_antall_punkter-1):
            u_next[i,j] = tid_skrittlengde_k/(x_skrittlengde_hx**2)*(u[i-1,j]-2*u[i,j]+u[i+1,j]) + tid_skrittlengde_k/(y_skrittlengde_hy**2)*(u[i,j-1] - 2*u[i,j] + u[i,j+1]) + u[i,j]
    return u_next

for i in range(tid_antall_punkter-1):
    u_verdier[:,:,i+1] = u_next(u_verdier[:,:,i])

# Animasjon

tid_ani = 2 #i sekunder
fps = 60 #frames per sekund
total_frames = tid_ani*fps

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
meshX, meshY = np.meshgrid(x_verdier, y_verdier)

def update(frame):
    ax.clear()
    surf = ax.plot_surface(meshX, meshY, u_verdier[:,:,frame], cmap = cm.coolwarm)
    ax.set_xlabel("$y$")
    ax.set_ylabel("$x$")
    ax.set_zlabel("$u$")
    ax.set_xlim((0,x_lengde))
    ax.set_ylim((0,y_lengde))
    ax.set_zlim((-1,1))
    return surf

ani = ani.FuncAnimation(fig, update, frames=np.linspace(0, tid_antall_punkter-1, total_frames).astype(int), interval = 1000/fps)
ani.save("animation2d.gif")
plt.show()