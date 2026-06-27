# Sphere Packing Experiments

**The Boötes void shape is not special. It is the standard output of φ-spiral bubble packing geometry.**

This folder contains experiments showing that the same scalloped void boundary — the shape observed in the real Boötes void — emerges from every φ-spiral packing run, at every density, at every scale. Different parameters. Same shape. Every time.

---

## What each experiment produces

Every experiment saves three files with the same base name:

```
experiment_name.html              — the interactive simulator (open in browser)
experiment_name.png               — screenshot of the settled packing at 74% fill
experiment_name_bootes_mask.png   — void mask of the most Boötes-like bubble
```

The void mask is:
- **512 × 512 pixels**
- **White = void interior** (hot, pressurised, the bang centre)
- **Black = matter wall** (filament boundary, scallops from neighbour pressure)
- Ready to load into the void inflator tool for inflation simulation

---

## What the masks show

Each mask is the boundary shape of one void bubble in the packing, as seen from outside. The black bites into the white interior are scallops — concave indentations carved by neighbouring void bubbles pressing inward.

**Scallop count** = number of immediate neighbours that pressed in
**Scallop depth** = how cramped the local packing was — how much pressure the neighbours applied
**Scallop asymmetry** = the neighbours were at unequal distances and angles (φ-spiral geometry ensures no two positions are identical)

The shape that emerges — 3 to 5 scallops, asymmetric, white interior with orange heat glow at centre — is the Boötes shape. Not because Boötes is special. Because this is what φ-spiral bubble packing geometry produces at every position in the hierarchy.

---

## The φ-spiral packing mechanism

Bubbles are placed at the golden angle (137.508°) from each other, with radius growing as √i from the centre. This is the same packing geometry as sunflower seeds, nautilus shells, and pine cone scales — nature's most efficient packing of objects in a growing spiral.

Because the golden angle is irrational, no two bubbles ever line up radially. Every bubble has a unique set of neighbours at unique distances and angles. This is why every void mask is slightly different — same process, different local geometry.

The neighbour counts follow Fibonacci numbers:
- Outer ring: 3–4 neighbours → 3–4 scallops → classic Boötes boot shape
- Middle ring: 5 neighbours → 5-petal flower shape
- Inner ring: 8 neighbours → dense petal pattern

---

## What this proves

The collection of masks in this folder is the proof.

Look at them. They are all the same kind of shape. Generated from different parameter settings, different random seeds, different positions in the spiral. The scallop count varies. The asymmetry varies. The depth varies. But the fundamental geometry — a white interior with dark concave bites from surrounding neighbours — is identical in every one.

This means:

**The Boötes void boundary shape is not a mystery.** It is not a statistical accident. It is not a property unique to Boötes. It is the inevitable output of φ-spiral bubble packing — the geometry that the golden angle forces on any system of expanding voids.

Every void in the universe has a Boötes shape. The scallop count tells you how many neighbours pressed in. The scallop depth tells you how dense the local packing was. The smoothness of the scallops tells you how old the void is — young voids have sharp scallops (the paper bag stage, still being compressed), old voids like Boötes have smooth gentle undulations (the expansion has stretched the creases smooth over billions of years).

**Age = smoothness. Count = neighbours. Depth = local density.**

Three measurements. One boundary. Readable from any void mask in any galaxy survey.

---

## The same process, the same shape

Newton said every force has an equal and opposite force. The scallop is the record of that equality. The neighbour void pressed inward. The Boötes void pressed outward. The scallop boundary is where they met and balanced. Its depth is the force ratio. Its position is the neighbour's angle. Its width is the contact area.

The universe is made of Boötes shapes at every scale. Inner bubbles, more cramped, more neighbours, deeper scallops. Outer bubbles, more space, fewer neighbours, shallower scallops and more asymmetric. But the same process. Always. Everywhere.

This folder shows that in a way that anyone can see.

---

## Tools

| Tool | Description |
|------|-------------|
| `spiral_void_masks.html` | φ-spiral packing simulator — void mask mode, save experiment button, click any bubble to extract its mask |
| `bootes_void_inflator.html` | Load any mask PNG, inflate it from compressed to expanded, watch scallops smooth over time |
| `pinball_cascade_timeline.html` | Sequential bang cascade — Boötes fires, Reds pushed out, Oranges reflected back, scallops carved over billions of years |

---

## File naming convention

```
sphere_packing_phi_spiral_D{density}_B{bootes_size}_sc{scallop_depth}_{timestamp}.png
sphere_packing_phi_spiral_D{density}_B{bootes_size}_sc{scallop_depth}_{timestamp}_bootes_mask.png
```

Example: `sphere_packing_phi_spiral_D8_B0.7_sc0.60_2026-06-05_0852_bootes_mask.png`
- D8 = density setting 8
- B0.7 = Boötes size 0.7×
- sc0.60 = scallop depth 0.60
- Timestamp for ordering experiments chronologically

---

*Pinball Universe — F. Burnham — June 2026*

*"The scallop is the fossil of the squeeze. The bang is the release. The pattern repeats."*
