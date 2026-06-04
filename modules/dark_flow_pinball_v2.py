"""
Dark Flow — Pinball Universe Model
===================================
Filament squashing rule + φ-spaced void geometry + dark flow bulk motion.

Calibrated values from snail calibrator (φ=1.620 ratio):
  MEASURED sizes (as surveyed):          CORRECTED sizes (× n_void = 1.0831):
  Shell 0  Boötes     330 Mly            357.4 Mly
  Shell 1  Red-1      204 Mly            220.9 Mly
  Shell 2  Orange     126 Mly            136.4 Mly
  Shell 3  Yellow      78 Mly             84.5 Mly
  Shell 4  Green       48 Mly             52.0 Mly
  Shell 5  Blue        30 Mly             32.5 Mly
  Shell 6  Purple      18 Mly             19.5 Mly

PARALLAX / REFRACTIVE INDEX MODEL (June 2026):
  The void is a pool. Observer on near filament wall looks straight through
  the hot void interior to the far wall — no side-on reference available.
  Heat lens compresses apparent depth uniformly (like water refraction).

  n_void = H0_SH0ES / H0_Planck = 73.0 / 67.4 = 1.0831

  true_r = measured_r × n_void  — uniform correction, all shells
  φ-ratios already correct in measured data (1.620 across all pairs)
  Geometry was never wrong. Only the absolute distance scale was compressed.

  Planck looks through the pool → H0 = 67.4
  SH0ES looks around it (filament Cepheids) → H0 = 73.0
  Difference = n_void = 1.0831

Physics:
  - Void interiors are heat pressure centres, not empty space
  - Filaments form at contact surfaces between neighbouring voids
  - Flow velocity ∝ void radius (flux ∝ r from E=mc², volume/surface)
  - Galaxy discs form perpendicular to filament flow (squashing rule)
  - Dark flow = galaxies following filament toward next contact node
  - Andromeda: Bang t=0, first contact t=8.5 Gyr, NOW t=13.8 Gyr,
    Andromeda arrives t=18.3 Gyr = 4.5 Gyr from NOW (not 18.3 from now)
  - 1t = 13,800 Mly (fixed ruler — light year is absolute distance)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.gridspec import GridSpec
import math

# ============================================================
# PINBALL GEOMETRY — from snail calibrator
# ============================================================
PHI   = 1.618033988749895
T_MLY = 13800.0   # 1t = 13,800 Mly — fixed ruler

# PARALLAX CORRECTION
# n_void derived directly from Hubble tension — not a free parameter
N_VOID    = 73.0 / 67.4   # = 1.0831
H0_PLANCK = 67.4
H0_SHOES  = 73.0

# Measured shell sizes — φ-ratios already correct (1.620 ± 0.001)
BOOTES_R_MEASURED = 330.0
N_SHELLS  = 7
shell_r_measured = [BOOTES_R_MEASURED / (PHI ** i) for i in range(N_SHELLS)]

# Corrected sizes — uniform × n_void
shell_r_corrected = [r * N_VOID for r in shell_r_measured]

# Use corrected sizes as the working set
BOOTES_R = BOOTES_R_MEASURED * N_VOID   # 357.4 Mly
shell_r  = shell_r_corrected

SHELL_NAMES  = ['Boötes','Red-1','Orange','Yellow','Green','Blue','Purple']
SHELL_COLS   = ['#7f0000','#ef4444','#f97316','#eab308','#22c55e','#3b82f6','#9b30d9']
SHELL_LABELS = [f'{n}\n{r:.0f} Mly' for n, r in zip(SHELL_NAMES, shell_r)]

# Flow velocity scales with void radius (flux ∝ r)
flow_v = [r / BOOTES_R for r in shell_r]

# Contact distances (contacting condition)
contact_d = [0.0]
for i in range(1, N_SHELLS):
    contact_d.append(shell_r[i-1] + shell_r[i])

# In t-units
shell_r_t   = [r / T_MLY for r in shell_r]
contact_d_t = [d / T_MLY for d in contact_d]

# ============================================================
# FIGURE LAYOUT
# ============================================================
fig = plt.figure(figsize=(26, 16))
fig.patch.set_facecolor('#05050e')
gs = GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.35)

# ============================================================
# PANEL 1 — 3D Pinball Foam with Filaments and Flow
# ============================================================
ax1 = fig.add_subplot(gs[0:2, 0:2], projection='3d')
ax1.set_facecolor('#05050e')
ax1.set_title('Pinball Universe — Dark Flow & Filament Geometry\n'
              '(φ-spaced voids · flow velocity ∝ void radius · galaxy discs ⊥ flow)',
              fontsize=11, color='white', pad=15)

# Place 7 void spheres in φ-spaced positions along three axes
# Boötes at origin; shells radiate outward along ±x, ±y, ±z, ±diagonals
# Use a subset for clarity: place 6 neighbours around Boötes (contacting in 3D)
# 6 contacting positions along ±x, ±y, ±z
contact_dirs = np.array([
    [ 1, 0, 0], [-1, 0, 0],
    [ 0, 1, 0], [ 0,-1, 0],
    [ 0, 0, 1], [ 0, 0,-1],
])

def draw_void_sphere(ax, centre, radius, colour, alpha_fill=0.12, alpha_wire=0.35, n=20):
    """Draw a void sphere with wireframe and glow."""
    u = np.linspace(0, 2*np.pi, n)
    v = np.linspace(0, np.pi, n)
    x = centre[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = centre[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = centre[2] + radius * np.outer(np.ones(n), np.cos(v))
    ax.plot_surface(x, y, z, color=colour, alpha=alpha_fill, linewidth=0)
    # Equator ring
    eq = np.linspace(0, 2*np.pi, 60)
    ax.plot(centre[0]+radius*np.cos(eq), centre[1]+radius*np.sin(eq),
            centre[2]*np.ones(60), color=colour, alpha=alpha_wire, linewidth=0.8)

# Scale to plot units: Boötes = 1 unit
scale = 1.0 / BOOTES_R

# Boötes — centre
draw_void_sphere(ax1, [0,0,0], shell_r[0]*scale, SHELL_COLS[0], alpha_fill=0.08, alpha_wire=0.4)

# 6 Red-1 neighbours
r1_centres = []
for d in contact_dirs:
    centre = d * contact_d[1] * scale
    r1_centres.append(centre)
    draw_void_sphere(ax1, centre, shell_r[1]*scale, SHELL_COLS[1], alpha_fill=0.07, alpha_wire=0.3)

# Iron core dot
ax1.scatter([0],[0],[0], color='white', s=40, zorder=10)

# ── FILAMENTS ─────────────────────────────────────────────
# Filaments are the edges between void contact surfaces
# They run between the contact points of adjacent shells
# Draw filament lines connecting Red-1 centres (they form a cuboctahedron)
# Adjacent pairs (sharing a face): 12 edges of cuboctahedron
cubocta_edges = [
    (0,2),(0,3),(0,4),(0,5),   # +x neighbours
    (1,2),(1,3),(1,4),(1,5),   # -x neighbours
    (2,4),(2,5),(3,4),(3,5),   # y-z cross
]
fil_col = '#4fc3f7'
for i, j in cubocta_edges:
    p1, p2 = r1_centres[i], r1_centres[j]
    ax1.plot3D([p1[0],p2[0]], [p1[1],p2[1]], [p1[2],p2[2]],
               color=fil_col, linewidth=1.8, alpha=0.6)

# ── FLOW VECTORS ──────────────────────────────────────────
# Flow velocity ∝ void radius (flux = ρc²r/4π from E=mc², V/SA)
# Larger void pushes harder → faster flow at its wall
# Arrow length ∝ flow_v[shell_index]
for ci, centre in enumerate(r1_centres):
    direction = contact_dirs[ci]  # flow direction = outward from Boötes
    speed = flow_v[1]          # Red-1 flow speed
    arrow_len = 0.25 * speed
    mid = centre * 0.6         # place arrow midway along filament
    ax1.quiver(mid[0], mid[1], mid[2],
               direction[0]*arrow_len, direction[1]*arrow_len, direction[2]*arrow_len,
               color='#5de4a1', linewidth=1.5, arrow_length_ratio=0.4, alpha=0.8)

# ── ANDROMEDA TRAJECTORY ─────────────────────────────────
# Andromeda: ejected from a 3-way junction point like a squeezed pip.
# Three voids meet at a junction. Two dominant voids squeeze from their sides.
# Matter compressed at junction — ejected along the THIRD filament arm.
# That third arm points directly at us (Milky Way = far end of the same filament).
# NOT gravitational attraction — geometric ejection. Arrival = filament length / eject velocity.
# The junction point where it was ejected sits ~2.5 Mly from us along the +x filament.
andromeda_start = np.array([contact_d[1]*scale * 0.8, 0.1*scale, 0.05*scale])
andromeda_end   = np.array([0.05, 0.02*scale, 0.01*scale])
ax1.plot3D([andromeda_start[0], andromeda_end[0]],
           [andromeda_start[1], andromeda_end[1]],
           [andromeda_start[2], andromeda_end[2]],
           color='#fbbf24', linewidth=2.5, linestyle='--', alpha=0.9, label='Andromeda trajectory')
ax1.scatter(*andromeda_start, color='#fbbf24', s=60, zorder=10)
ax1.text(andromeda_start[0], andromeda_start[1], andromeda_start[2]+0.05,
         'Andromeda\n(ejected from\n3-way junction)', color='#fbbf24', fontsize=7, ha='center')

# ── GALAXY DISCS on filaments ─────────────────────────────
# Discs form perpendicular to local flow direction (squashing rule)
def draw_disc_3d(ax, centre, normal, r_maj, r_min, colour, alpha=0.6):
    normal = np.array(normal, dtype=float)
    normal /= np.linalg.norm(normal)
    if abs(normal[2]) < 0.9:
        u = np.cross(normal, [0,0,1]); u /= np.linalg.norm(u)
    else:
        u = np.cross(normal, [1,0,0]); u /= np.linalg.norm(u)
    v = np.cross(normal, u)
    t = np.linspace(0, 2*np.pi, 40)
    pts = np.array([r_maj*np.cos(a)*u + r_min*np.sin(a)*v for a in t]) + np.array(centre)
    ax.plot(pts[:,0], pts[:,1], pts[:,2], color=colour, alpha=alpha, linewidth=1.2)
    ax.plot_surface(pts[:,0].reshape(-1,1), pts[:,1].reshape(-1,1), pts[:,2].reshape(-1,1),
                    color=colour, alpha=alpha*0.4, linewidth=0)

disc_r = 0.06
for ci, centre in enumerate(r1_centres):
    flow_dir = contact_dirs[ci].astype(float)
    # Place 2 discs along each filament arm
    for frac in [0.35, 0.65]:
        pos = centre * frac
        draw_disc_3d(ax1, pos, flow_dir, disc_r*1.5, disc_r*0.5, '#eab308', alpha=0.7)

ax1.set_xlim([-1.8, 1.8]); ax1.set_ylim([-1.8, 1.8]); ax1.set_zlim([-1.8, 1.8])
ax1.set_xlabel('X (void units)', color='#aaa', fontsize=8)
ax1.set_ylabel('Y (void units)', color='#aaa', fontsize=8)
ax1.set_zlabel('Z (void units)', color='#aaa', fontsize=8)
ax1.tick_params(colors='#555', labelsize=7)
for pane in [ax1.xaxis.pane, ax1.yaxis.pane, ax1.zaxis.pane]:
    pane.fill = False
    pane.set_edgecolor('#1a1a2e')
ax1.legend(loc='upper left', fontsize=7, facecolor='#0a0a1a', labelcolor='white',
           edgecolor='#333')

# ============================================================
# PANEL 2 — Snail Shell Distance Map (1D projection)
# ============================================================
ax2 = fig.add_subplot(gs[0, 2])
ax2.set_facecolor('#05050e')
ax2.set_title('φ-Spaced Shell Distances\n(contacting condition, fixed Mly ruler)',
              fontsize=9, color='white')

y_base = 0.5
for i, (r, d, col, name) in enumerate(zip(shell_r, contact_d, SHELL_COLS, SHELL_NAMES)):
    # Bar showing shell extent
    bar_h = 0.06 + r/BOOTES_R * 0.25
    ax2.barh(y_base - i*0.13, r*2, left=-r, height=bar_h,
             color=col, alpha=0.7, edgecolor='white', linewidth=0.5)
    ax2.text(r+15, y_base - i*0.13, f'{name}\n{r:.0f} Mly', color=col,
             fontsize=7, va='center')
    # Centre dot
    ax2.scatter([0], [y_base - i*0.13], color='white', s=15, zorder=5)

ax2.axvline(0, color='#5de4a1', linewidth=1, alpha=0.5, linestyle='--')
ax2.set_xlim(-400, 650)
ax2.set_xlabel('Distance from Boötes centre (Mly)', color='#aaa', fontsize=8)
ax2.set_yticks([])
ax2.tick_params(colors='#888', labelsize=7)
ax2.spines[:].set_color('#1a1a2e')
ax2.text(-380, y_base + 0.05, '1t = 13,800 Mly (fixed ruler)', color='#5de4a1',
         fontsize=7, style='italic')

# ============================================================
# PANEL 3 — Flow Velocity vs Shell Radius
# ============================================================
ax3 = fig.add_subplot(gs[1, 2])
ax3.set_facecolor('#05050e')
ax3.set_title('Flow Velocity ∝ Void Radius\n(flux = ρc²r/4π from E=mc²)',
              fontsize=9, color='white')

ax3.plot(shell_r, flow_v, 'o-', color='#5de4a1', linewidth=2, markersize=8, zorder=5)
for i, (r, v, col, name) in enumerate(zip(shell_r, flow_v, SHELL_COLS, SHELL_NAMES)):
    ax3.scatter([r], [v], color=col, s=80, zorder=6, edgecolors='white', linewidth=0.5)
    ax3.annotate(name, (r, v), textcoords='offset points', xytext=(5, 5),
                color=col, fontsize=7)

ax3.set_xlabel('Void radius (Mly)', color='#aaa', fontsize=8)
ax3.set_ylabel('Flow velocity (normalised to Boötes)', color='#aaa', fontsize=8)
ax3.tick_params(colors='#888', labelsize=7)
ax3.spines[:].set_color('#1a1a2e')
ax3.set_facecolor('#05050e')
ax3.grid(True, color='#1a1a2e', linewidth=0.5)
ax3.text(50, 0.85, 'Bigger void → faster flow\n→ stronger dark flow signal',
         color='#fbbf24', fontsize=7, style='italic')
# Linear fit line
rr = np.linspace(0, BOOTES_R, 100)
ax3.plot(rr, rr/BOOTES_R, '--', color='white', alpha=0.3, linewidth=1, label='linear (theory)')
ax3.legend(fontsize=7, facecolor='#0a0a1a', labelcolor='white', edgecolor='#333')

# ============================================================
# PANEL 4 — Filament Squashing Rule (2D)
# ============================================================
ax4 = fig.add_subplot(gs[2, 0])
ax4.set_facecolor('#05050e')
ax4.set_title('Squashing Rule — Contact Zone\n(voids press inward → matter flows perpendicular)',
              fontsize=9, color='white')
ax4.set_xlim(-2.2, 2.2); ax4.set_ylim(-2.2, 2.2)
ax4.set_aspect('equal')

# Two voids pressing from left and right
for cx2 in [-1.6, 1.6]:
    circle = plt.Circle((cx2, 0), 0.9, color='#ef4444', alpha=0.15, fill=True)
    circle2 = plt.Circle((cx2, 0), 0.9, color='#ef4444', alpha=0.5, fill=False, linewidth=1.5)
    ax4.add_patch(circle); ax4.add_patch(circle2)
    ax4.scatter([cx2],[0], color='white', s=20, zorder=5)

# Filament in centre
ax4.axhline(0, color='#4fc3f7', linewidth=2.5, alpha=0.8, zorder=3)

# Void pressure arrows — pressing INWARD (horizontal, toward contact zone)
for cx3, dx3 in [(-1.6, 0.35), (1.6, -0.35)]:
    ax4.annotate('', xy=(cx3 + dx3, 0), xytext=(cx3 + dx3*0.3, 0),
                arrowprops=dict(arrowstyle='->', color='#ef4444', lw=2.0))

# Contact zone vertical line at x=0 (the pressure boundary)
ax4.axvline(0, color='#4fc3f7', linewidth=1.5, alpha=0.6, linestyle='--', zorder=3)

# CORRECT flow arrows — matter squirts OUT PERPENDICULAR to contact zone (upward + downward)
# The two voids press from left and right. Matter has nowhere to go except UP and DOWN.
for y_dir, y_arr in [(-0.3, -0.7), (0.3, 0.7)]:
    ax4.annotate('', xy=(0, y_arr), xytext=(0, y_dir),
                arrowprops=dict(arrowstyle='->', color='#4fc3f7', lw=2.5))

# Galaxy discs — HORIZONTAL (perpendicular to the vertical flow = disc plane ⊥ flow)
for y_pos in [-1.1, 0.0, 1.1]:
    disc = patches.Ellipse((0, y_pos), 0.55, 0.12, angle=0,
                            facecolor='#eab308', edgecolor='#fbbf24',
                            alpha=0.85, zorder=4)
    ax4.add_patch(disc)

# Contact node dots where matter collects
ax4.scatter([0],[0], color='#4fc3f7', s=40, zorder=6)

ax4.text(0, -2.0,
         'Voids press inward (→ ←) · Matter squirts OUT perpendicular (↑↓)\n'
         'Filament = contact zone · Galaxy disc forms ⊥ to flow (horizontal)',
         color='#aaa', fontsize=7.5, ha='center')
ax4.text(-1.6, 1.2, 'Void A', color='#ef4444', fontsize=8, ha='center')
ax4.text(1.6, 1.2, 'Void B', color='#ef4444', fontsize=8, ha='center')
ax4.text(0.15, 0.55, 'matter\nflows↑', color='#4fc3f7', fontsize=7, ha='left')
ax4.text(0.15,-0.55, 'matter\nflows↓', color='#4fc3f7', fontsize=7, ha='left')
ax4.text(0.28, 0.05, 'contact\nzone', color='#4fc3f7', fontsize=6.5, ha='left', alpha=0.7)
ax4.set_xticks([]); ax4.set_yticks([])
ax4.spines[:].set_color('#1a1a2e')

# ============================================================
# PANEL 5 — Andromeda / Dark Flow Timeline
# ============================================================
ax5 = fig.add_subplot(gs[2, 1])
ax5.set_facecolor('#05050e')
ax5.set_title('Contact Timeline — Shell Events & Dark Flow\n(inter-layer period = 5.3 Gyr)',
              fontsize=9, color='white')

# Timeline: ordered by Frank's sequence
# t=0      our Big Bang
# t=8.5    FIRST CONTACT — inner shell (closer to Boötes) locks
#          Sea RECEDES — infall begins — Andromeda starts moving toward us
#          Standard model: "dark matter gravity"
# t=13.8   FULL ENCLOSURE — outer shell contact — WE ARE HERE
#          The WAVE HITS — outward push begins
#          Standard model: "dark energy acceleration"
# t=18.3   ANDROMEDA ARRIVES — next contact event (+4.5 Gyr from now)
#          Filament rider, not gravitational fall — on schedule

events = [
    (0,    'our\nBig Bang',                   '#9b30d9', '◆', -0.3),
    (8.5,  '8.5 Gyrs\nFirst contact\n(inner shell locks\n— sea recedes)',
                                               '#ef4444', '★',  0.35),
    (13.8, '13.8 Gyr\nFull enclosure\nWE ARE HERE',
                                               '#5de4a1', '★', -0.35),
    (18.3, 'Andromeda\narrives\n+4.5 Gyr',  '#fbbf24', '◆',  0.35),
]

ax5.axhline(0, color='#333', linewidth=1.2)

for t, label, col, marker, y_off in events:
    s = 150 if marker == '★' else 100
    m = '*' if marker == '★' else 'D'
    ax5.scatter([t], [0], color=col, s=s, zorder=6, marker=m)
    ax5.plot([t,t], [0, y_off], color=col, alpha=0.5, linewidth=1.2, linestyle='-')
    va = 'bottom' if y_off > 0 else 'top'
    ax5.text(t, y_off + (0.04 if y_off>0 else -0.04), label,
             color=col, fontsize=6.8, ha='center', va=va, linespacing=1.3)

# Tidal wave phase labels
ax5.text(11.15, 0.07, 'TROUGH\n(infall / sea receding)', color='#ef4444',
         fontsize=6, ha='center', alpha=0.8, style='italic')
ax5.axvspan(8.5, 13.8, alpha=0.06, color='#ef4444')  # infall zone

ax5.text(16.05, 0.07, 'WAVE\narriving', color='#fbbf24',
         fontsize=6, ha='center', alpha=0.8, style='italic')
ax5.axvspan(13.8, 18.3, alpha=0.06, color='#fbbf24')  # wave zone

# Bracket: 5.3 Gyr trough
ax5.annotate('', xy=(13.8, -0.62), xytext=(8.5, -0.62),
            arrowprops=dict(arrowstyle='<->', color='#ef4444', lw=1.2))
ax5.text(11.15, -0.70, '5.3 Gyr\n(trough)', color='#ef4444', fontsize=6.5, ha='center')

# Bracket: 4.5 Gyr to Andromeda
ax5.annotate('', xy=(18.3, -0.62), xytext=(13.8, -0.62),
            arrowprops=dict(arrowstyle='<->', color='#fbbf24', lw=1.2))
ax5.text(16.05, -0.70, '4.5 Gyr\n(to arrival)', color='#fbbf24', fontsize=6.5, ha='center')

# WE ARE HERE dashed line
ax5.axvline(13.8, color='#5de4a1', linewidth=1.8, alpha=0.5, linestyle='--')

# Octant contact numbers
for contact_n, t_c, yc in [(4, 0.3,'below'), (7, 13.8,'above'), (8, 18.3,'below')]:
    ypos = 0.55 if yc=='above' else -0.80
    ax5.text(t_c, ypos, 'contact\n%d/8' % contact_n,
             color='#555', fontsize=5.5, ha='center', style='italic')
ax5.set_xlim(-2, 22); ax5.set_ylim(-0.9, 0.75)
ax5.set_xlabel('Time (Gyr)', color='#aaa', fontsize=8)
ax5.set_yticks([])
ax5.tick_params(colors='#888', labelsize=7)
ax5.spines[:].set_color('#1a1a2e')

# ============================================================
# PANEL 6 — Legend / Physics Summary
# ============================================================
ax6 = fig.add_subplot(gs[2, 2])
ax6.axis('off')
ax6.set_facecolor('#05050e')

lines = [
    ('PINBALL UNIVERSE — DARK FLOW', '#5de4a1', 11, True),
    ('', '#aaa', 8, False),
    ('FIXED RULER:', '#fff', 9, True),
    ('  1t = 13,800 Mly (light year = absolute distance)', '#aaa', 8, False),
    ('  Void sizes underestimated 15-25% by heat lensing', '#fbbf24', 8, False),
    ('', '#aaa', 8, False),
    ('FLOW PHYSICS (E=mc²):', '#fff', 9, True),
    ('  Flux at wall = ρc²r/4π  →  flow ∝ r', '#aaa', 8, False),
    ('  Bigger void pushes harder, flows faster', '#aaa', 8, False),
    ('  Contact point: r₀=r₁ — flux equality', '#5de4a1', 8, False),
    ('', '#aaa', 8, False),
    ('SQUASHING RULE:', '#fff', 9, True),
    ('  Voids press inward → matter exits perpendicular', '#aaa', 8, False),
    ('  Filament = contact zone · disc forms ⊥ to pressure', '#aaa', 8, False),
    ('  90% galaxy alignment observed ✓', '#22c55e', 8, False),
    ('', '#aaa', 8, False),
    ('DARK FLOW:', '#fff', 9, True),
    ('  Galaxies follow filaments to contact nodes', '#aaa', 8, False),
    ('  Andromeda: ejected from 3-way junction, NOT gravity', '#fbbf24', 8, False),
    ('  Arrives 18.3 Gyr = contact 8 of 8 octant sweep', '#fbbf24', 8, False),
    ('', '#aaa', 8, False),
    ('8 OCTANT CONTACTS (4.5 Gyr intervals):', '#fff', 9, True),
    ('  Full sphere sweep = 8 × 4.5 = 36 Gyr', '#aaa', 8, False),
    ('  Contact 4 ≈ 0.3 Gyr  — our Bang', '#9b30d9', 8, False),
    ('  Contact 7 = 13.8 Gyr — WE ARE HERE', '#5de4a1', 8, False),
    ('  Contact 8 = 18.3 Gyr — Andromeda (last octant)', '#fbbf24', 8, False),
    ('  Then new shell cycle begins', '#aaa', 8, False),
    ('  Arrival ~18 Gyr = one inter-layer period', '#fbbf24', 8, False),
    ('  Not a collision — a scheduled contact event', '#ef4444', 8, False),
    ('', '#aaa', 8, False),
    ('HUBBLE TENSION:', '#fff', 9, True),
    ('  Heat lensing bends light OUTWARD from voids', '#aaa', 8, False),
    ('  Gravity lensing bends light INWARD to mass', '#aaa', 8, False),
    ('  Standard model applies wrong correction →', '#aaa', 8, False),
    ('  All void sizes underestimated 15-25%', '#ef4444', 8, False),
    ('  Corrected sizes restore φ-ratio contacting ✓', '#22c55e', 8, False),
]

y = 0.97
for text, col, size, bold in lines:
    ax6.text(0.02, y, text, color=col, fontsize=size,
             weight='bold' if bold else 'normal',
             transform=ax6.transAxes, va='top')
    y -= 0.038

# ============================================================
fig.suptitle('Pinball Universe — Dark Flow, Filament Squashing & φ-Geometry',
             fontsize=14, color='white', y=0.98, weight='bold')

# ── ANDROMEDA EJECTION INSET (add to panel 4 — squashing rule) ────────────
# Show the 3-way junction mechanism as an inset on ax4
ax4_ins = ax4.inset_axes([0.55, 0.55, 0.45, 0.45])
ax4_ins.set_facecolor('#08080f')
ax4_ins.set_aspect('equal')
ax4_ins.set_title('3-junction ejection', color='#fbbf24', fontsize=6, pad=3)

# Three void circles meeting at a junction
import matplotlib.patches as mpatch
junction_voids = [
    (-0.7,  0.4, '#ef4444', 'Void 1'),   # upper left
    (-0.7, -0.4, '#f97316', 'Void 2'),   # lower left  — two dominant squeezers
    ( 0.5,  0.0, '#3b82f6', 'Void 3'),   # right — the third arm points left (toward us)
]
for vx, vy, vc, vn in junction_voids:
    circ = mpatch.Circle((vx, vy), 0.5, color=vc, alpha=0.15, fill=True)
    circ2 = mpatch.Circle((vx, vy), 0.5, color=vc, alpha=0.6, fill=False, linewidth=1)
    ax4_ins.add_patch(circ); ax4_ins.add_patch(circ2)

# Junction point at origin
ax4_ins.scatter([0],[0], color='white', s=30, zorder=6)

# Two squeeze arrows (from dominant voids)
ax4_ins.annotate('', xy=(0, 0), xytext=(-0.55, 0.28),
    arrowprops=dict(arrowstyle='->', color='#ef4444', lw=1.5))
ax4_ins.annotate('', xy=(0, 0), xytext=(-0.55, -0.28),
    arrowprops=dict(arrowstyle='->', color='#f97316', lw=1.5))

# Ejection arrow — third filament arm (pointing left = toward Milky Way)
ax4_ins.annotate('', xy=(-1.1, 0), xytext=(0, 0),
    arrowprops=dict(arrowstyle='->', color='#fbbf24', lw=2.0))
ax4_ins.text(-1.15, 0.12, 'Andromeda\nejected →', color='#fbbf24', fontsize=5.5, ha='right')

# Us at the end of the filament
ax4_ins.scatter([-1.15],[0], color='#5de4a1', s=25, zorder=6, marker='*')
ax4_ins.text(-1.15, -0.15, 'us', color='#5de4a1', fontsize=5.5, ha='center')

ax4_ins.set_xlim(-1.4, 1.1); ax4_ins.set_ylim(-0.9, 0.9)
ax4_ins.set_xticks([]); ax4_ins.set_yticks([])
ax4_ins.spines[:].set_color('#1a1a2e')

# ============================================================
# PANEL 7 — Parallax Correction & Hubble Tension (June 2026)
# ============================================================

ax7_top = fig.add_subplot(gs[0, 3])
ax7_top.set_facecolor('#05050e')
ax7_top.set_title('Parallax Correction — Measured vs True Radii\n(void = pool · heat lens compresses apparent depth)',
                   color='#ef4444', fontsize=9, pad=6)

# Measured vs corrected bars — uniform n_void scaling
y_pos = list(range(len(SHELL_NAMES)))[::-1]

bars_m = ax7_top.barh(y_pos, shell_r_measured, color=SHELL_COLS, alpha=0.45,
                       height=0.38, label=f'Measured (apparent)')
bars_t = ax7_top.barh(y_pos, shell_r_corrected, color=SHELL_COLS, alpha=0.2,
                       height=0.38, hatch='///', edgecolor=SHELL_COLS,
                       label=f'True (× n_void = {N_VOID:.4f})')

for i, (rm, rc, col) in enumerate(zip(shell_r_measured, shell_r_corrected, SHELL_COLS)):
    yi = y_pos[i]
    pct = (rc/rm - 1)*100
    ax7_top.annotate(f'+{pct:.1f}%',
                     xy=(rc, yi), xytext=(rc + 8, yi),
                     color='#ef4444', fontsize=7, va='center',
                     arrowprops=dict(arrowstyle='->', color='#ef4444', lw=0.8))
    ax7_top.text(-12, yi, SHELL_NAMES[i], color=col, fontsize=7,
                 va='center', ha='right', weight='bold')

ax7_top.axvline(0, color='#555', linewidth=0.8, linestyle='--')
ax7_top.set_xlim(-55, 430)
ax7_top.set_yticks([])
ax7_top.set_xlabel('Radius (Mly)', color='#aaa', fontsize=8)
ax7_top.tick_params(colors='#888', labelsize=7)
ax7_top.spines[:].set_color('#1a1a2e')
ax7_top.legend(loc='lower right', fontsize=6.5, facecolor='#0a0a1a',
               labelcolor='white', framealpha=0.7)

ax7_top.text(BOOTES_R_MEASURED, y_pos[0] + 0.28, f'{BOOTES_R_MEASURED:.0f} Mly measured',
             color='#888', fontsize=6.5, ha='center')
ax7_top.text(BOOTES_R, y_pos[0] + 0.28, f'{BOOTES_R:.1f} Mly true',
             color='#ef4444', fontsize=6.5, ha='center')

# φ-ratio annotation — all pairs already correct
ax7_top.text(0.98, 0.02,
             'φ-ratios: 1.620 across all pairs\nGeometry was never wrong',
             transform=ax7_top.transAxes, color='#5de4a1',
             fontsize=6.5, ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0a0a14',
                       edgecolor='#5de4a1', alpha=0.8))

# ── Hubble tension resolution panel ──
ax7_bot = fig.add_subplot(gs[1, 3])
ax7_bot.set_facecolor('#05050e')
ax7_bot.set_title('Hubble Tension Resolution\nn_void = H₀_SH0ES / H₀_Planck = 73.0 / 67.4',
                   color='#5de4a1', fontsize=9, pad=6)

h0_tension = H0_SHOES - H0_PLANCK

# Single uniform correction — one bar from Planck to SH0ES
ax7_bot.barh(0, h0_tension, left=H0_PLANCK,
             color='#ef4444', alpha=0.6, height=0.35,
             label=f'n_void correction (+{h0_tension:.1f})')

ax7_bot.axvline(H0_PLANCK, color='#4fc3f7', linewidth=2.0,
                linestyle='--', label=f'Planck H₀ = {H0_PLANCK} (through void)')
ax7_bot.axvline(H0_SHOES, color='#fbbf24', linewidth=2.0,
                linestyle='--', label=f'SH0ES H₀ = {H0_SHOES} (around void)')

ax7_bot.set_xlim(64, 76)
ax7_bot.set_ylim(-0.6, 0.6)
ax7_bot.set_xlabel('H₀ (km/s/Mpc)', color='#aaa', fontsize=8)
ax7_bot.set_yticks([])
ax7_bot.tick_params(colors='#888', labelsize=7)
ax7_bot.spines[:].set_color('#1a1a2e')
ax7_bot.legend(loc='upper left', fontsize=6.5, facecolor='#0a0a1a',
               labelcolor='white', framealpha=0.7)

ax7_bot.text(0.5, 0.12,
             f'n_void = {N_VOID:.4f}\n'
             f'Planck × n_void = {H0_PLANCK * N_VOID:.1f} = SH0ES  ✓\n'
             f'One number. No new physics.',
             transform=ax7_bot.transAxes, color='#5de4a1',
             fontsize=8, ha='center', va='bottom',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0a0a14',
                       edgecolor='#5de4a1', alpha=0.8))

# ── Text summary panel ──
ax7_txt = fig.add_subplot(gs[2, 3])
ax7_txt.axis('off')
ax7_txt.set_facecolor('#05050e')

lens_lines = [
    ('PARALLAX / REFRACTIVE INDEX MODEL', '#ef4444', 10, True),
    ('', '#aaa', 7, False),
    ('THE VOID IS A POOL:', '#fff', 8, True),
    ('  Observer on near wall looks through hot void', '#aaa', 7, False),
    ('  No side-on reference — cannot judge depth', '#aaa', 7, False),
    ('  Heat lens compresses apparent depth uniformly', '#ef4444', 7, False),
    ('  apparent_r = true_r / n_void', '#fbbf24', 7, False),
    ('', '#aaa', 7, False),
    ('THE TWO VIEWS:', '#fff', 8, True),
    ('  Planck: looks THROUGH the void to CMB', '#4fc3f7', 7, False),
    ('  SH0ES:  Cepheids on filaments — AROUND void', '#fbbf24', 7, False),
    ('  Difference = n_void = 73.0 / 67.4 = 1.0831', '#ef4444', 7, True),
    ('', '#aaa', 7, False),
    ('φ-RATIOS ALREADY CORRECT:', '#fff', 8, True),
    ('  All adjacent pairs: ratio = 1.620 ± 0.001', '#22c55e', 7, False),
    ('  Geometry was never wrong', '#22c55e', 7, False),
    ('  Only absolute scale was compressed', '#22c55e', 7, False),
    ('', '#aaa', 7, False),
    ('CORRECTED SIZES (× 1.0831):', '#fff', 8, True),
    (f'  Boötes  {BOOTES_R_MEASURED:.0f} → {BOOTES_R:.1f} Mly', '#7f0000', 7, False),
    (f'  Red-1   {shell_r_measured[1]:.0f} → {shell_r_corrected[1]:.1f} Mly', '#ef4444', 7, False),
    (f'  Orange  {shell_r_measured[2]:.0f} → {shell_r_corrected[2]:.1f} Mly', '#f97316', 7, False),
    (f'  Yellow   {shell_r_measured[3]:.0f} → {shell_r_corrected[3]:.1f} Mly', '#eab308', 7, False),
    (f'  Green    {shell_r_measured[4]:.0f} → {shell_r_corrected[4]:.1f} Mly', '#22c55e', 7, False),
    (f'  Blue     {shell_r_measured[5]:.0f} → {shell_r_corrected[5]:.1f} Mly', '#3b82f6', 7, False),
    (f'  Purple   {shell_r_measured[6]:.0f} → {shell_r_corrected[6]:.1f} Mly', '#9b30d9', 7, False),
    ('', '#aaa', 7, False),
    ('HUBBLE TENSION RESOLUTION:', '#5de4a1', 8, True),
    ('  Planck H₀ = 67.4  (through the pool)', '#4fc3f7', 7, False),
    ('  SH0ES H₀ = 73.0  (around the pool)', '#fbbf24', 7, False),
    ('  n_void × 67.4 = 73.0  ✓', '#5de4a1', 7, True),
    ('  No new physics. One number.', '#5de4a1', 7, False),
]

y = 0.98
for text, col, size, bold in lens_lines:
    ax7_txt.text(0.02, y, text, color=col, fontsize=size,
                 weight='bold' if bold else 'normal',
                 transform=ax7_txt.transAxes, va='top')
    y -= 0.040

plt.savefig('dark_flow_pinball_thermal.png'
, dpi=150, bbox_inches='tight',
            facecolor='#05050e', edgecolor='none')
plt.show()

# ── CALIBRATED VALUES OUTPUT ──────────────────────────────
print("\n" + "="*65)
print("PINBALL UNIVERSE — CALIBRATED GEOMETRY")
print("="*65)
print(f"n_void = {N_VOID:.4f}  (H0_SH0ES / H0_Planck = {H0_SHOES}/{H0_PLANCK})")
print(f"φ ratio: {PHI:.6f}  (measured φ-ratios: 1.620 across all pairs)")
print(f"1t = {T_MLY:.0f} Mly (fixed ruler)")
print()
print(f"{'Shell':<10} {'Measured':>10} {'Corrected':>12} {'Contact (corr)':>16} {'Flow v':>8}")
print("-"*60)
for i, (name, rm, rc, d, v) in enumerate(zip(
        SHELL_NAMES, shell_r_measured, shell_r_corrected, contact_d, flow_v)):
    print(f"{name:<10} {rm:>10.1f} {rc:>12.1f} {d:>16.1f} {v:>8.4f}")
print("="*65)
print(f"\nBoötes: {BOOTES_R_MEASURED:.0f} Mly measured → {BOOTES_R:.1f} Mly true (×{N_VOID:.4f})")
print(f"Timeline: Bang t=0 · First contact t=8.5 Gyr · NOW t=13.8 Gyr")
print(f"Andromeda: t=18.3 Gyr from Bang = 4.5 Gyr from NOW")
print(f"Inter-contact period: {13.8-8.5:.1f} Gyr")
print(f"Andromeda = last contact + {18.3-13.8:.1f} Gyr ≈ one period later")
print("="*65)
