"""Drawing helpers for the CODE-M Day 2 toy reconstruction (Toybacter fermentans).

You do not need to read this file to follow the notebook. It provides:

* draw_network(model, fluxes=None) - a static picture of the toy network
  (works everywhere, no Jupyter extensions needed);
* write_escher_map(model, path) - writes an Escher map of the toy network,
  used to create toybacter_map.json.
"""
import json

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# Positions of the metabolites we draw (Escher pixel coordinates, y grows downwards).
# Cofactors (ATP/ADP, NAD+/NADH, CoA, H+, water, phosphate) are deliberately left out to keep the picture readable.
LAYOUT = {
    "glc__D_e": (190, 120), "glc__D_c": (460, 120),
    "pyr_c": (460, 340),
    "lac__L_c": (690, 340), "lac__L_e": (950, 340),
    "for_c": (690, 460), "for_e": (950, 460),
    "accoa_c": (460, 580),
    "ac_c": (690, 580), "ac_e": (950, 580),
    "etoh_c": (690, 720), "etoh_e": (950, 720),
    "nh4_e": (190, 460), "nh4_c": (360, 460),
    "ala__L_c": (360, 700),
}
# Where to put the centre of reactions that join more than two drawn metabolites,
# or that have no drawn product (biomass).
CENTRES = {
    "PFL": (460, 460),
    "ALAD": (400, 560),
    "BIOMASS": (460, 800),
}
CYTOSOL_BOX = (290, 40, 540, 830)  # x, y, width, height
BOUNDARY_SIDE = {"left": 30, "right": 1110}

TEAL, ORANGE, GREY, DARK = "#1B998B", "#B85C1E", "#C9D3D6", "#0E3B43"


def _drawn(reaction):
    return {m.id: c for m, c in reaction.metabolites.items() if m.id in LAYOUT}


def _geometry(reaction):
    """Return (reactant_points, product_points, centre) in layout coordinates."""
    mets = _drawn(reaction)
    if not mets:
        return None
    reac = [LAYOUT[m] for m, c in mets.items() if c < 0]
    prod = [LAYOUT[m] for m, c in mets.items() if c > 0]
    if reaction.boundary:  # exchange: draw towards the edge of the picture
        (x, y), = reac + prod
        edge = BOUNDARY_SIDE["left"] if x < 500 else BOUNDARY_SIDE["right"]
        return [(x, y)], [(edge, y)], None
    if reaction.id in CENTRES:
        return reac, prod, CENTRES[reaction.id]
    if len(reac) == 1 and len(prod) == 1:
        return reac, prod, None
    xs = [p[0] for p in reac + prod]
    ys = [p[1] for p in reac + prod]
    return reac, prod, (sum(xs) / len(xs), sum(ys) / len(ys))


def draw_network(model, fluxes=None, title=None, ax=None, max_width=7.0):
    """Draw the toy network. If `fluxes` (dict or pandas Series) is given,
    arrow thickness is proportional to |flux| and each reaction is labelled."""
    if ax is None:
        _, ax = plt.subplots(figsize=(11.5, 8.5))
    flux = dict(fluxes) if fluxes is not None else {}
    vmax = max([abs(v) for v in flux.values()] + [1e-9])

    x, y, w, h = CYTOSOL_BOX
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=6,rounding_size=30",
                                fc="#EAF4F1", ec=TEAL, lw=1.5, zorder=0))
    ax.text(x + 15, y + 25, "cytosol", color=TEAL, fontsize=11, style="italic")
    ax.text(30, 25, "extracellular", color="#5C7A82", fontsize=11, style="italic")

    for r in model.reactions:
        geom = _geometry(r)
        if geom is None:
            continue
        reac, prod, centre = geom
        v = flux.get(r.id, None)
        if v is not None and abs(v) < 1e-9:
            v = 0.0
        active = v is not None and abs(v) > 1e-6
        if v is not None and v < -1e-6:  # running backwards: swap the drawing direction
            reac, prod = prod, reac
        colour = (ORANGE if r.id in ("BIOMASS",) else TEAL) if active else GREY
        lw = 1.2 + (max_width - 1.2) * abs(v) / vmax if active else 1.0
        style = "-" if active or fluxes is None else (0, (4, 3))
        kw = dict(color=colour if fluxes is not None else DARK, lw=lw if fluxes is not None else 1.4,
                  linestyle=style, zorder=1, shrinkA=16, shrinkB=16)
        if centre is None:
            for a in reac:
                for b in prod:
                    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, **kw))
            lx, ly = (reac[0][0] + prod[0][0]) / 2, (reac[0][1] + prod[0][1]) / 2
        else:
            for a in reac:
                ax.add_patch(FancyArrowPatch(a, centre, arrowstyle="-", **{**kw, "shrinkB": 0}))
            for b in prod:
                ax.add_patch(FancyArrowPatch(centre, b, arrowstyle="-|>", mutation_scale=14, **{**kw, "shrinkA": 0}))
            if not prod:  # biomass: arrow pointing down to a label
                end = (centre[0], centre[1] + 45)
                ax.add_patch(FancyArrowPatch(centre, end, arrowstyle="-|>", mutation_scale=14, **{**kw, "shrinkA": 0, "shrinkB": 0}))
                ax.text(end[0], end[1] + 18, "biomass", ha="center", va="top", fontsize=11, color=DARK, weight="bold")
            lx, ly = centre
        label = r.id if v is None else f"{r.id}\n{v:.2f}"
        ax.text(lx, ly, label, ha="center", va="center", fontsize=8.5, zorder=3,
                color=DARK if (active or fluxes is None) else "#8A9BA0",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))

    for mid, (mx, my) in LAYOUT.items():
        if mid not in model.metabolites:
            continue
        ax.scatter([mx], [my], s=520, color="white", edgecolors=TEAL, linewidths=2, zorder=4)
        ax.text(mx, my, mid.rsplit("_", 1)[0].split("__")[0], ha="center", va="center", fontsize=8.5, zorder=5, color=DARK, weight="bold")

    ax.set_xlim(0, 1140)
    ax.set_ylim(900, 0)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=13, color=DARK, loc="left")
    return ax


def write_escher_map(model, path, map_name="Toybacter fermentans"):
    """Write an Escher (schema 1-0-0) map for the reactions of `model` that can be drawn."""
    nodes, reactions, nid = {}, {}, [0]

    def new_node(**kw):
        nid[0] += 1
        nodes[str(nid[0])] = kw
        return str(nid[0])

    met_nodes = {}
    for mid, (x, y) in LAYOUT.items():
        if mid in model.metabolites:
            m = model.metabolites.get_by_id(mid)
            met_nodes[mid] = new_node(node_type="metabolite", x=x, y=y, bigg_id=mid, name=m.name or mid,
                                      label_x=x - 20, label_y=y + 38, node_is_primary=True)

    for k, r in enumerate(model.reactions):
        geom = _geometry(r)
        if geom is None:
            continue
        reac, prod, centre = geom
        drawn = _drawn(r)
        if centre is None:
            a, b = (reac + prod)[0], (reac + prod)[-1] if not r.boundary else prod[0]
            centre = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        cx, cy = centre
        ax_, ay_ = reac[0] if reac else centre
        bx_, by_ = prod[0] if prod else (cx, cy + 40)
        def toward(p, q, d=20):
            dx, dy = q[0] - p[0], q[1] - p[1]
            n = max((dx * dx + dy * dy) ** 0.5, 1e-9)
            return p[0] + dx / n * d, p[1] + dy / n * d
        m1 = toward(centre, (ax_, ay_))
        m2 = toward(centre, (bx_, by_))
        mid_n = new_node(node_type="midmarker", x=cx, y=cy)
        mm1 = new_node(node_type="multimarker", x=m1[0], y=m1[1])
        mm2 = new_node(node_type="multimarker", x=m2[0], y=m2[1])
        segs, sid = {}, 0
        for f, t in [(mid_n, mm1), (mm2, mid_n)]:
            sid += 1
            segs[str(sid)] = {"from_node_id": f, "to_node_id": t, "b1": None, "b2": None}
        for met, coef in drawn.items():
            sid += 1
            if r.boundary:
                # exchanges: the drawn metabolite hangs off the inner multimarker
                segs[str(sid)] = {"from_node_id": met_nodes[met], "to_node_id": mm1, "b1": None, "b2": None}
            elif coef < 0:
                segs[str(sid)] = {"from_node_id": met_nodes[met], "to_node_id": mm1, "b1": None, "b2": None}
            else:
                segs[str(sid)] = {"from_node_id": mm2, "to_node_id": met_nodes[met], "b1": None, "b2": None}
        reactions[str(1000 + k)] = {
            "name": r.name or r.id, "bigg_id": r.id, "reversibility": r.reversibility,
            "label_x": cx + 12, "label_y": cy - 14,
            "gene_reaction_rule": r.gene_reaction_rule,
            "genes": [{"bigg_id": g.id, "name": g.name or ""} for g in r.genes],
            "metabolites": [{"bigg_id": m.id, "coefficient": c} for m, c in r.metabolites.items()],
            "segments": segs,
        }
    labels = {"t1": {"text": "cytosol", "x": 310, "y": 70}, "t2": {"text": "extracellular", "x": 30, "y": 40},
              "t3": {"text": "biomass", "x": 430, "y": 870}}
    header = {"map_name": map_name, "map_id": "toybacter_codem", "map_description": "CODE-M Day 2 toy reconstruction",
              "homepage": "https://escher.github.io", "schema": "https://escher.github.io/escher/jsonschema/1-0-0#"}
    body = {"reactions": reactions, "nodes": nodes, "text_labels": labels,
            "canvas": {"x": -40, "y": -40, "width": 1220, "height": 980}}
    with open(path, "w") as fh:
        json.dump([header, body], fh, indent=1)
    return path
