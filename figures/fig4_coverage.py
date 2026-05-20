"""
fig4_coverage.py
----------------
Three-panel stacked bar chart showing how many papers in the crosswalk collection
address each workflow step, broken down by priority tier.

Layout: 3 subplot rows — each group kept intact within a row.
  Row 1  Framing & Sampling     (Foundations + Sampling/Matrix)
  Row 2  Lab Processing & Analysis  (Processing + Spectroscopy/QC)
  Row 3  Data, Reporting & Toxicology

"Analytical Methods (General)" (col 19) is deliberately excluded:
  it is a broad catch-all that co-occurs with both specific spectroscopy
  columns (FTIR/Raman/Py-GC-MS) AND lab processing columns (Blanks,
  Sample Processing), creating visual double-counting. The specific
  method columns tell the story more clearly.

Data source: MNP Quality Standards Crosswalk v2.xlsx

Usage:
    python3 fig4_coverage.py
Output:
    fig4_coverage.html  (same directory)
"""

import json, pathlib
import openpyxl

HERE   = pathlib.Path(__file__).parent
OUTDIR = HERE
OUTDIR.mkdir(parents=True, exist_ok=True)

XLSX = HERE.parent / "methods_navigator/data/crosswalk.xlsx"
wb = openpyxl.load_workbook(XLSX)
ws = wb["Crosswalk Table"]
papers = [row for row in ws.iter_rows(min_row=3, values_only=True) if row[0] is not None]

def cell_tier(val):
    """Return integer tier if cell has a per-cell tier integer, else None."""
    try:
        t = int(val)
        return t if 1 <= t <= 4 else None
    except (TypeError, ValueError):
        return None

# ── Step definitions (col_idx, display_label, row, sub-group) ────────────────
# Col 19 "Analytical Methods (General)" intentionally omitted — see docstring.
STEPS = [
    # ROW 1 — Framing & Sampling
    # sub-group: Framing
    ( 7, "Definitions &\nTerminology",      1, "Framing"),
    ( 8, "Problem\nFormulation",            1, "Framing"),
    # sub-group: Sampling & Matrix
    ( 9, "Sampling\n(Field)",               1, "Sampling & Matrix"),
    (10, "Matrix:\nDrinking Water",         1, "Sampling & Matrix"),
    (11, "Matrix:\nSurface /\nWastewater",  1, "Sampling & Matrix"),
    (12, "Matrix:\nSediment",               1, "Sampling & Matrix"),
    (13, "Matrix:\nBiota / Tissue",         1, "Sampling & Matrix"),
    (14, "Matrix:\nAir / Atmos.",           1, "Sampling & Matrix"),
    (15, "Matrix:\nFood / Diet",            1, "Sampling & Matrix"),
    (16, "Matrix:\nHuman Tissue /\nBiomonit.",1, "Sampling & Matrix"),

    # ROW 2 — Lab Processing & Analysis
    # sub-group: Lab Processing
    (17, "Sample\nProcessing /\nExtraction", 2, "Lab Processing"),
    (18, "Sub-\nsampling",                   2, "Lab Processing"),
    (23, "Reference\nMaterials /\nControls", 2, "Lab Processing"),
    (24, "Blanks &\nContam. Control",        2, "Lab Processing"),
    # sub-group: Spectroscopic Analysis
    (20, "FTIR / IR",                        2, "Spectroscopic Analysis"),
    (21, "Raman /\nµRaman",                  2, "Spectroscopic Analysis"),
    (22, "Py-GC-MS",                         2, "Spectroscopic Analysis"),
    (30, "Interlaboratory\nValidation",           2, "Spectroscopic Analysis"),

    # ROW 3 — Data, Reporting & Toxicology
    # sub-group: Data & Reporting
    (25, "Data Analysis\n& Statistics",      3, "Data & Reporting"),
    (26, "Reporting &\nHarmonization",       3, "Data & Reporting"),
    (27, "Data\nDeposition",                 3, "Data & Reporting"),
    # sub-group: Toxicology
    (28, "Tox: Study\nDesign &\nDosimetry",  3, "Toxicology"),
    (29, "Tox: Effects\nTesting",            3, "Toxicology"),
    (31, "Risk\nAssessment /\nRisk Char.",   3, "Toxicology"),
]

TIER_COLORS = {
    1: "#6A0DAD",  # purple
    2: "#1565C0",  # blue
    3: "#2E7D32",  # green
    4: "#78909C",  # grey-blue
}
TIER_NAMES = {
    1: "Tier 1 — Regulatory / Accredited SOP",
    2: "Tier 2 — Authoritative Guidance",
    3: "Tier 3 — Peer-Reviewed Method",
    4: "Tier 4 — Supporting Science",
}

def get_tier(raw):
    s = str(raw) if raw else ""
    for i in [1, 2, 3, 4]:
        if f"Tier {i}" in s:
            return i
    return None

# ── Tally per step per tier ───────────────────────────────────────────────────
counts       = {t: [0]*len(STEPS) for t in [1,2,3,4]}
hover_detail = {t: [[] for _ in STEPS] for t in [1,2,3,4]}

for si, (ci, lbl, row, grp) in enumerate(STEPS):
    for p in papers:
        t = cell_tier(p[ci])
        if t in counts:
            counts[t][si] += 1
            hover_detail[t][si].append(str(p[1]))

totals = [sum(counts[t][si] for t in [1,2,3,4]) for si in range(len(STEPS))]

# ── Subplot domain layout ────────────────────────────────────────────────────
# 3 rows; proportional to step counts
row_sizes = {1: 10, 2: 8, 3: 5}
total_bars = sum(row_sizes.values())          # 23
gap        = 0.055                            # space between rows
available  = 1.0 - 2 * gap

def domain(row_num):
    """Return [y_bottom, y_top] for a given row (1=top, 3=bottom)."""
    fracs = {r: row_sizes[r] / total_bars * available for r in [1,2,3]}
    # layout bottom to top: row 3 first, then row 2, then row 1
    bot3 = 0.0
    top3 = bot3 + fracs[3]
    bot2 = top3 + gap
    top2 = bot2 + fracs[2]
    bot1 = top2 + gap
    top1 = bot1 + fracs[1]
    bounds = {3: [bot3, top3], 2: [bot2, top2], 1: [bot1, min(top1, 1.0)]}
    return bounds[row_num]

dom = {r: domain(r) for r in [1, 2, 3]}
ax_suffix = {1: "", 2: "2", 3: "3"}   # Plotly axis naming convention

# ── Build traces (one per tier per row) ──────────────────────────────────────
traces = []
legend_added = set()

for row_num in [1, 2, 3]:
    xs  = ax_suffix[row_num]
    row_steps = [(si, ci, lbl, grp)
                 for si, (ci, lbl, rn, grp) in enumerate(STEPS) if rn == row_num]
    step_labels = [lbl.replace("\n", "<br>") for _, _, lbl, _ in row_steps]

    for t in [1, 2, 3, 4]:
        ys, htexts, ttexts = [], [], []
        for si, ci, lbl, grp in row_steps:
            n = counts[t][si]
            ys.append(n)
            if n == 0:
                htexts.append("")
                ttexts.append("")
            else:
                cites = "<br>  ".join(hover_detail[t][si][:6])
                extra = f"<br>  ...+{len(hover_detail[t][si])-6} more" if len(hover_detail[t][si]) > 6 else ""
                htexts.append(
                    f"<b>{TIER_NAMES[t]}</b><br>"
                    f"Step: {lbl.replace(chr(10),' ')}<br>"
                    f"n = {n} papers:<br>  {cites}{extra}"
                )
                ttexts.append(str(n))

        show_legend = t not in legend_added
        if any(v > 0 for v in ys):
            legend_added.add(t)

        traces.append({
            "type": "bar",
            "name": TIER_NAMES[t],
            "legendgroup": TIER_NAMES[t],
            "showlegend": show_legend,
            "x": step_labels,
            "y": ys,
            "xaxis": f"x{xs}",
            "yaxis": f"y{xs}",
            "marker": {"color": TIER_COLORS[t]},
            "hovertext": htexts,
            "hovertemplate": "%{hovertext}<extra></extra>",
            "text": ttexts,
            "textposition": "inside",
            "textfont": {"size": 10, "color": "white"},
            "insidetextanchor": "middle",
        })

    # Totals as text above each bar group
    total_ys = [sum(counts[t][si] for t in [1,2,3,4]) for si, _, _, _ in row_steps]
    traces.append({
        "type": "scatter",
        "x": step_labels,
        "y": [v + 0.3 for v in total_ys],
        "mode": "text",
        "text": [f"<b>{v}</b>" if v > 0 else "" for v in total_ys],
        "textfont": {"size": 10, "color": "#333"},
        "xaxis": f"x{xs}",
        "yaxis": f"y{xs}",
        "hoverinfo": "skip",
        "showlegend": False,
    })

# ── Sub-group shading shapes ──────────────────────────────────────────────────
shapes = []
SUBGRP_COLORS = {
    "Framing":               "#E3F2FD",
    "Sampling & Matrix":     "#F3E5F5",
    "Lab Processing":        "#E8F5E9",
    "Spectroscopic Analysis":"#FFF3E0",
    "Data & Reporting":      "#E0F7FA",
    "Toxicology":            "#FCE4EC",
}

for row_num in [1, 2, 3]:
    xs = ax_suffix[row_num]
    row_steps = [(si, ci, lbl, grp)
                 for si, (ci, lbl, rn, grp) in enumerate(STEPS) if rn == row_num]

    # Identify sub-group spans within this row
    grp_spans = {}
    for local_i, (si, ci, lbl, grp) in enumerate(row_steps):
        if grp not in grp_spans:
            grp_spans[grp] = [local_i, local_i]
        else:
            grp_spans[grp][1] = local_i

    for grp, (start_i, end_i) in grp_spans.items():
        shapes.append({
            "type": "rect",
            "xref": f"x{xs}", "yref": "paper",
            "x0": start_i - 0.5, "x1": end_i + 0.5,
            "y0": dom[row_num][0], "y1": dom[row_num][1],
            "fillcolor": SUBGRP_COLORS.get(grp, "#FAFAFA"),
            "opacity": 0.3,
            "line": {"width": 0},
            "layer": "below",
        })

# ── Sub-group header annotations ──────────────────────────────────────────────
annotations = []
for row_num in [1, 2, 3]:
    xs = ax_suffix[row_num]
    ypos = dom[row_num][1] + 0.012   # just above each subplot
    row_steps = [(si, ci, lbl, grp)
                 for si, (ci, lbl, rn, grp) in enumerate(STEPS) if rn == row_num]
    grp_spans = {}
    for local_i, (si, ci, lbl, grp) in enumerate(row_steps):
        grp_spans.setdefault(grp, [local_i, local_i])[1] = local_i

    for grp, (start_i, end_i) in grp_spans.items():
        mid = (start_i + end_i) / 2
        annotations.append({
            "x": mid, "y": ypos,
            "xref": f"x{xs}", "yref": "paper",
            "text": f"<b>{grp}</b>",
            "showarrow": False,
            "font": {"size": 10, "color": "#444"},
            "align": "center",
        })

# ── Layout ────────────────────────────────────────────────────────────────────
max_y = max(totals) + 2

def axis_cfg(row_num, is_x=True):
    xs = ax_suffix[row_num]
    if is_x:
        return {
            "tickangle": -35,
            "tickfont": {"size": 10},
            "showgrid": False,
            "anchor": f"y{xs}",
            "domain": [0, 1],
        }
    else:
        return {
            "title": "Papers (n)",
            "showgrid": True, "gridcolor": "#EEEEEE",
            "zeroline": True, "zerolinecolor": "#CCC",
            "anchor": f"x{xs}",
            "domain": dom[row_num],
            "range": [0, max_y],
            "tickfont": {"size": 10},
            "titlefont": {"size": 10},
        }

layout = {
    "barmode": "stack",
    "title": {
        "text": (
            "<b>Coverage of MNP Research Workflow Steps by Priority Tier</b><br>"
            "<sup>n papers per step from 105-paper collection · per-cell tier ratings · "
            "'Analytical Methods (General)' excluded to avoid double-counting with FTIR/Raman/Py-GC-MS · "
            "hover bars for paper details</sup>"
        ),
        "x": 0.5, "font": {"size": 14},
    },
    "xaxis":  axis_cfg(1, is_x=True),
    "yaxis":  axis_cfg(1, is_x=False),
    "xaxis2": axis_cfg(2, is_x=True),
    "yaxis2": axis_cfg(2, is_x=False),
    "xaxis3": axis_cfg(3, is_x=True),
    "yaxis3": axis_cfg(3, is_x=False),
    "plot_bgcolor":  "#FFFFFF",
    "paper_bgcolor": "#FFFFFF",
    "legend": {
        "orientation": "h",
        "yanchor": "bottom", "y": -0.10,
        "xanchor": "center", "x": 0.5,
        "font": {"size": 11},
    },
    "shapes": shapes,
    "annotations": annotations,
    "margin": {"t": 100, "b": 120, "l": 55, "r": 20},
    "height": 780,
}

fig_json = json.dumps({"data": traces, "layout": layout})

HTML = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Fig 4 – MNP Guidance Coverage by Workflow Step</title>
  <script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>
  <style>body{{margin:0;font-family:sans-serif;}}</style>
</head>
<body>
  <div id="fig" style="width:100%;height:820px;"></div>
  <script>
    var fig = {fig_json};
    Plotly.newPlot('fig', fig.data, fig.layout, {{responsive:true, displayModeBar:true}});
  </script>
</body>
</html>"""

out_path = OUTDIR / "fig4_coverage.html"
out_path.write_text(HTML, encoding="utf-8")
print(f"Saved: {out_path}")
row_counts = {r: sum(1 for (_, _, rn, _) in STEPS if rn == r) for r in [1,2,3]}
print(f"  Rows: {row_counts}")
print(f"  Totals per step: {totals}")
