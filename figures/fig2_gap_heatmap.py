"""
fig2_gap_heatmap.py
-------------------
Generates a matrix × workflow-step heatmap showing the highest tier of available
guidance for each cell. Output is a self-contained interactive HTML file.

Data source: MNP Quality Standards Crosswalk v2.xlsx
             (relative path: ../MNP Quality Standards Crosswalk v2.xlsx)

Tier color scheme
  Tier 1  ▏ #6A0DAD  purple     Regulatory / Accredited SOP
  Tier 2  ▏ #1565C0  blue       Authoritative Guidance (WHO, ISO, etc.)
  Tier 3  ▏ #2E7D32  green      Peer-Reviewed Method / SOP
  Tier 4  ▏ #78909C  grey-blue  Supporting Science
  Gap     ▏ #FFCDD2  salmon     No specific guidance identified

Usage:
    python3 fig2_gap_heatmap.py
Output:
    fig2_gap_heatmap.html  (same directory)
"""

import json, os, pathlib
import openpyxl

# ── Paths ────────────────────────────────────────────────────────────────────
HERE   = pathlib.Path(__file__).parent
XLSX   = HERE.parent / "MNP Quality Standards Crosswalk v3.xlsx"
OUTDIR = HERE
OUTDIR.mkdir(parents=True, exist_ok=True)

# ── Load data ────────────────────────────────────────────────────────────────
wb = openpyxl.load_workbook(XLSX)
ws = wb["Crosswalk Table"]
papers = [row for row in ws.iter_rows(min_row=3, values_only=True) if row[0] is not None]

def cell_tier(val):
    """Return integer tier (1-4) if cell has a per-cell tier, else None."""
    try:
        t = int(val)
        return t if 1 <= t <= 4 else None
    except (TypeError, ValueError):
        return None

# Column index → readable label
MATRIX_COLS = [
    (10, "Drinking Water"),
    (11, "Surface Water /\nWastewater"),
    (12, "Sediment"),
    (13, "Biota / Tissue"),
    (14, "Air / Atmos."),
    (15, "Food / Diet"),
    (16, "Human Tissue /\nBiomonitoring"),
]

WORKFLOW_COLS = [
    ( 9, "Sampling"),
    (17, "Lab Processing\n/ Extraction"),
    (18, "Sub-sampling"),
    (20, "FTIR / IR"),
    (21, "Raman"),
    (22, "Py-GC-MS"),
    (23, "Reference\nMaterials"),
    (24, "Blanks &\nQC"),
    (25, "Data Analysis\n& Statistics"),
    (26, "Reporting &\nHarmonization"),
    (27, "Data\nDeposition"),
]

# Tox workflow — matrix-independent
TOX_COLS = [
    (28, "Tox Study\nDesign"),
    (29, "Tox Effects\nTesting"),
    (30, "Interlaboratory\nValidation"),  # p[30] = col 31 (1-based)
    (31, "Risk\nAssessment"),             # p[31] = col 32 (1-based)
]

def get_tier(tier_raw):
    s = str(tier_raw) if tier_raw else ""
    for i in [1, 2, 3, 4]:
        if f"Tier {i}" in s:
            return i
    return 5  # Gap / no coverage

TIER_LABELS = {1: "Tier 1", 2: "Tier 2", 3: "Tier 3", 4: "Tier 4", 5: "Gap"}
TIER_DESC   = {
    1: "Regulatory / Accredited SOP",
    2: "Authoritative Guidance",
    3: "Peer-Reviewed Method",
    4: "Supporting Science",
    5: "No specific guidance identified",
}

# ── Build heatmap arrays ─────────────────────────────────────────────────────
y_labels  = [m for _, m in MATRIX_COLS]
# Environmental workflow columns + a blank separator + Tox columns
x_labels_env = [w for _, w in WORKFLOW_COLS]
x_labels_tox = [w for _, w in TOX_COLS]
x_labels = x_labels_env + [""] + x_labels_tox   # empty string = visual spacer

n_rows = len(MATRIX_COLS)
n_cols = len(x_labels)

z        = [[None]*n_cols for _ in range(n_rows)]
hover    = [["" ]*n_cols for _ in range(n_rows)]
cell_txt = [[""  ]*n_cols for _ in range(n_rows)]

# Environmental monitoring cells
# Per-cell tier: use max(matrix_tier, workflow_tier) for the intersection quality
# Best available = minimum across relevant papers
for ri, (mci, mname) in enumerate(MATRIX_COLS):
    for ci, (wci, wname) in enumerate(WORKFLOW_COLS):
        plist = []
        for p in papers:
            tm = cell_tier(p[mci])
            tw = cell_tier(p[wci])
            if tm is not None and tw is not None:
                # Use worst (max) of the two per-cell tiers for this intersection
                plist.append((max(tm, tw), str(p[1])))
        plist.sort()
        if plist:
            bt = plist[0][0]
            z[ri][ci] = bt
            cites = "<br>".join(f"  {cite}" for _, cite in plist[:4])
            if len(plist) > 4:
                cites += f"<br>  ...+{len(plist)-4} more"
            hover[ri][ci] = (
                f"<b>{mname.replace(chr(10),' ')} × {wname.replace(chr(10),' ')}</b><br>"
                f"Best available: <b>{TIER_LABELS[bt]}</b> — {TIER_DESC[bt]}<br>"
                f"Papers (n={len(plist)}):<br>{cites}"
            )
            cell_txt[ri][ci] = TIER_LABELS[bt]
        else:
            z[ri][ci] = 5
            hover[ri][ci] = (
                f"<b>{mname.replace(chr(10),' ')} × {wname.replace(chr(10),' ')}</b><br>"
                "<b>Gap</b> — No specific guidance identified in this collection"
            )
            cell_txt[ri][ci] = "Gap"

# Spacer column
sep_ci = len(WORKFLOW_COLS)
for ri in range(n_rows):
    z[ri][sep_ci]     = None
    hover[ri][sep_ci] = ""
    cell_txt[ri][sep_ci] = ""

# Toxicology columns (matrix-independent — use per-cell tier directly)
for ti, (wci, wname) in enumerate(TOX_COLS):
    ci = sep_ci + 1 + ti
    plist = []
    for p in papers:
        t = cell_tier(p[wci])
        if t is not None:
            plist.append((t, str(p[1])))
    plist.sort()
    for ri in range(n_rows):
        if plist:
            bt = plist[0][0]
            z[ri][ci] = bt
            cites = "<br>".join(f"  {cite}" for _, cite in plist[:4])
            if len(plist) > 4:
                cites += f"<br>  ...+{len(plist)-4} more"
            hover[ri][ci] = (
                f"<b>Toxicology × {wname.replace(chr(10),' ')}</b><br>"
                f"(Matrix-independent guidance)<br>"
                f"Best available: <b>{TIER_LABELS[bt]}</b> — {TIER_DESC[bt]}<br>"
                f"Papers (n={len(plist)}):<br>{cites}"
            )
            cell_txt[ri][ci] = TIER_LABELS[bt]
        else:
            z[ri][ci] = 5
            hover[ri][ci] = f"<b>Toxicology × {wname}</b><br><b>Gap</b>"
            cell_txt[ri][ci] = "Gap"

# ── Plotly figure spec ───────────────────────────────────────────────────────
# Discrete colorscale: z range 1–5, centred at 1.5,2.5,3.5,4.5,5.5 → zmin=0.5,zmax=5.5
COLORSCALE = [
    [0.0,  "#6A0DAD"], [0.2,  "#6A0DAD"],  # Tier 1
    [0.2,  "#1565C0"], [0.4,  "#1565C0"],  # Tier 2
    [0.4,  "#2E7D32"], [0.6,  "#2E7D32"],  # Tier 3
    [0.6,  "#78909C"], [0.8,  "#78909C"],  # Tier 4
    [0.8,  "#FFCDD2"], [1.0,  "#FFCDD2"],  # Gap
]

# Clean x labels for display (replace \n with <br>)
x_display = [lbl.replace("\n", "<br>") for lbl in x_labels]
y_display = [lbl.replace("\n", "<br>") for lbl in y_labels]

trace = {
    "type": "heatmap",
    "z": z,
    "x": x_display,
    "y": y_display,
    "text": cell_txt,
    "hovertext": hover,
    "hovertemplate": "%{hovertext}<extra></extra>",
    "colorscale": COLORSCALE,
    "zmin": 0.5, "zmax": 5.5,
    "showscale": False,
    "xgap": 2, "ygap": 2,
}

# Annotation for cell text
annotations = []
for ri, row_z in enumerate(z):
    for ci, val in enumerate(row_z):
        if val is None or x_labels[ci] == "":
            continue
        txt_color = "white" if val in (1, 2) else ("black" if val == 5 else "white")
        short = cell_txt[ri][ci]
        annotations.append({
            "x": x_display[ci], "y": y_display[ri],
            "text": f"<b>{short}</b>",
            "font": {"size": 10, "color": txt_color},
            "showarrow": False,
            "xref": "x", "yref": "y",
        })

# Section header annotations
annotations += [
    {
        "x": 5, "y": n_rows - 0.52,
        "xref": "x", "yref": "y",
        "text": "<b>── Environmental Monitoring Workflow ──</b>",
        "showarrow": False,
        "font": {"size": 11, "color": "#333"},
        "align": "center",
    },
    {
        "x": sep_ci + 1.5, "y": n_rows - 0.52,
        "xref": "x", "yref": "y",
        "text": "<b>── Toxicology ──</b>",
        "showarrow": False,
        "font": {"size": 11, "color": "#333"},
        "align": "center",
    },
]

# Legend as invisible scatter traces
legend_traces = []
for tier, label, color in [
    (1, "Tier 1 — Regulatory/Accredited SOP",   "#6A0DAD"),
    (2, "Tier 2 — Authoritative Guidance",       "#1565C0"),
    (3, "Tier 3 — Peer-Reviewed Method",         "#2E7D32"),
    (4, "Tier 4 — Supporting Science",           "#78909C"),
    (5, "Gap — No specific guidance",            "#FFCDD2"),
]:
    legend_traces.append({
        "type": "scatter",
        "x": [None], "y": [None],
        "mode": "markers",
        "marker": {"color": color, "size": 14, "symbol": "square"},
        "name": label,
        "showlegend": True,
    })

layout = {
    "title": {
        "text": (
            "<b>Availability of Authoritative Guidance for MNP Research</b><br>"
            "<sup>By matrix and workflow step — highest tier paper identified in collection (n=105)</sup>"
        ),
        "x": 0.5, "font": {"size": 16},
    },
    "xaxis": {
        "side": "top",
        "tickangle": -30,
        "tickfont": {"size": 11},
        "showgrid": False,
        "zeroline": False,
    },
    "yaxis": {
        "autorange": "reversed",
        "tickfont": {"size": 11},
        "showgrid": False,
    },
    "plot_bgcolor": "#F5F5F5",
    "paper_bgcolor": "#FFFFFF",
    "annotations": annotations,
    "legend": {
        "orientation": "h",
        "yanchor": "bottom", "y": -0.25,
        "xanchor": "center", "x": 0.5,
        "title": {"text": "Best available guidance:  "},
        "font": {"size": 11},
    },
    "margin": {"t": 130, "b": 130, "l": 160, "r": 30},
    "height": 480,
}

fig_data = legend_traces + [trace]
fig_json = json.dumps({"data": fig_data, "layout": layout})

# ── Write HTML ───────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Fig 2 – MNP Guidance Gap Heatmap</title>
  <script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>
  <style>body{{margin:0;font-family:sans-serif;}}</style>
</head>
<body>
  <div id="fig" style="width:100%;height:580px;"></div>
  <script>
    var fig = {fig_json};
    Plotly.newPlot('fig', fig.data, fig.layout, {{responsive:true, displayModeBar:true}});
  </script>
</body>
</html>"""

out_path = OUTDIR / "fig2_gap_heatmap.html"
out_path.write_text(HTML, encoding="utf-8")
print(f"Saved: {out_path}")
print(f"  Rows: {n_rows} matrices × {n_cols} columns (incl. separator)")
