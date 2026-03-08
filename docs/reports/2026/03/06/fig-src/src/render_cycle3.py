import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

cycle_labels = [
    "022","002","000","001","011","012","010","020","021",
    "121","101","111","112","122","102","100","110","120",
    "220","221","201","202","200","210","211","212","222",
    "022"
]
cycle = [(int(s[0]), int(s[1]), int(s[2])) for s in cycle_labels]

def wrap_axis(a, b):
    for ax in range(3):
        if a[ax] == 2 and b[ax] == 0:
            return ax
    return -1

def bezier_pts(p0, ctrl, p1, num=80):
    t = np.linspace(0, 1, num)
    p0, ctrl, p1 = np.array(p0,float), np.array(ctrl,float), np.array(p1,float)
    return ((1-t)**2)[:,None]*p0 + 2*(1-t)[:,None]*t[:,None]*ctrl + (t**2)[:,None]*p1

def control_point(p0, p1, wax):
    """
    Bow PERPENDICULAR to the arc direction, outward from the cube.
    The arc direction is along wax. We pick a perpendicular axis and
    bow outward (past +2 or past -0 face).
    """
    mid = (np.array(p0,float) + np.array(p1,float)) / 2
    # Pick perpendicular bow axis: use the non-wrap, non-varying axis if possible,
    # otherwise just the next axis. Bow direction: away from cube center (1,1,1).
    perp_axes = [a for a in range(3) if a != wax]
    # Choose the perp axis where mid coordinate is furthest from 1 (most extreme)
    best = max(perp_axes, key=lambda a: abs(mid[a] - 1.0))
    bow = np.zeros(3)
    # bow outward: if mid[best] >= 1, bow in + direction (past face=2), else - direction
    direction = 1.0 if mid[best] >= 1.0 else -1.0
    bow[best] = direction * 1.8
    return mid + bow

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 12), facecolor='#0a0c10')
ax = fig.add_subplot(111, projection='3d', facecolor='#0a0c10')

# Skeleton
for i in range(3):
    for j in range(3):
        for k in range(3):
            ax.plot([i,(i+1)%3],[j,j],[k,k], color='#1e2a40',lw=0.5,alpha=0.35,zorder=1)
            ax.plot([i,i],[j,(j+1)%3],[k,k], color='#1e2a40',lw=0.5,alpha=0.35,zorder=1)
            ax.plot([i,i],[j,j],[k,(k+1)%3], color='#1e2a40',lw=0.5,alpha=0.35,zorder=1)

n = 27
cmap = plt.cm.cool

for s in range(n):
    p0, p1 = cycle[s], cycle[s+1]
    t = s / n
    color = cmap(0.2 + 0.7 * t)
    wax = wrap_axis(p0, p1)

    if wax >= 0:
        ctrl = control_point(p0, p1, wax)
        pts = bezier_pts(p0, ctrl, p1)
        ax.plot(pts[:,0], pts[:,1], pts[:,2],
                color=color, lw=2.4, alpha=0.92, zorder=3, solid_capstyle='round')
        tang = pts[-1] - pts[-6]
        tang /= np.linalg.norm(tang) or 1
        tip = np.array(p1, float)
        ax.quiver(tip[0]-tang[0]*0.2, tip[1]-tang[1]*0.2, tip[2]-tang[2]*0.2,
                  tang[0]*0.18, tang[1]*0.18, tang[2]*0.18,
                  color=color, alpha=0.95, arrow_length_ratio=0.65,
                  linewidth=0, zorder=4)
    else:
        x0,y0,z0 = p0; x1,y1,z1 = p1
        dx,dy,dz = x1-x0,y1-y0,z1-z0
        ax.plot([x0,x1],[y0,y1],[z0,z1],
                color=color, lw=2.4, alpha=0.92, zorder=3, solid_capstyle='round')
        ax.quiver(x1-dx*0.22,y1-dy*0.22,z1-dz*0.22,
                  dx*0.18,dy*0.18,dz*0.18,
                  color=color, alpha=0.95, arrow_length_ratio=0.60,
                  linewidth=0, zorder=4)

# Vertices
all_verts = [(i,j,k) for i in range(3) for j in range(3) for k in range(3)]
xs=[v[0] for v in all_verts]; ys=[v[1] for v in all_verts]; zs=[v[2] for v in all_verts]
ax.scatter(xs,ys,zs, s=100, c='#c04040', edgecolors='#e08080',
           linewidths=1.2, zorder=5, depthshade=False)
for (i,j,k) in all_verts:
    ax.text(i,j,k+0.13,f"{i}{j}{k}", fontsize=6.5, color='#7a8cb0',
            ha='center', va='bottom', zorder=6, fontfamily='monospace')

# Step labels
for s in range(n):
    p0, p1 = cycle[s], cycle[s+1]
    t = s / n
    color = cmap(0.2 + 0.7 * t)
    wax = wrap_axis(p0, p1)
    if wax >= 0:
        ctrl = control_point(p0, p1, wax)
        pts = bezier_pts(p0, ctrl, p1)
        mx,my,mz = pts[40]
    else:
        mx=(p0[0]+p1[0])/2; my=(p0[1]+p1[1])/2; mz=(p0[2]+p1[2])/2
    ax.text(mx,my,mz,str(s+1), fontsize=5.5, color=color, alpha=0.78,
            ha='center', va='center', zorder=7, fontfamily='monospace')

# Colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0,26))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.45, pad=0.02, aspect=20)
cbar.set_label('Step in cycle (0 → 26)', color='#7a8cb0', fontsize=9, labelpad=8)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color='#7a8cb0', fontsize=8)
cbar.outline.set_edgecolor('#1e2230')

# Axes
ax.set_xlabel('i', color='#5a6480', labelpad=6)
ax.set_ylabel('j', color='#5a6480', labelpad=6)
ax.set_zlabel('k', color='#5a6480', labelpad=6)
ax.set_xticks([0,1,2]); ax.set_yticks([0,1,2]); ax.set_zticks([0,1,2])
ax.tick_params(colors='#3a4570', labelsize=8)
ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('#1a2030')
ax.yaxis.pane.set_edgecolor('#1a2030')
ax.zaxis.pane.set_edgecolor('#1a2030')
ax.grid(True, color='#1a2030', linewidth=0.5, alpha=0.5)
ax.set_xlim(-0.8, 3.8); ax.set_ylim(-0.8, 3.8); ax.set_zlim(-0.5, 3.0)
ax.view_init(elev=22, azim=38)

fig.text(0.5, 0.97, "Knuth's Hamiltonian Cycle on the 3×3×3 Cayley Digraph",
         ha='center', va='top', color='#7eb8f7', fontsize=13, fontfamily='serif', style='italic')
fig.text(0.5, 0.925, "27 vertices  ijk  ·  curved arcs = wraparound (coordinate 2→0 mod 3)  ·  cycle c=0",
         ha='center', va='top', color='#5a6480', fontsize=8, fontfamily='monospace')

plt.tight_layout(rect=[0,0,1,0.93])
plt.savefig('/mnt/user-data/outputs/hamiltonian_cycle_3d.png',
            dpi=180, bbox_inches='tight', facecolor='#0a0c10', edgecolor='none')

# Debug: print control points for wrap arcs
for s in range(n):
    p0, p1 = cycle[s], cycle[s+1]
    wax = wrap_axis(p0, p1)
    if wax >= 0:
        ctrl = control_point(p0, p1, wax)
        print(f"Step {s+1}: {cycle_labels[s]}->{cycle_labels[s+1]}  wax={wax}  ctrl={ctrl}")

print("Saved.")
