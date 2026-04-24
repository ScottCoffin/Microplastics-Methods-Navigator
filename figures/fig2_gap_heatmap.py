"""
fig2_gap_heatmap.py
-------------------
Two-facet interactive heatmap showing availability of authoritative guidance for MNP research.

Facet 1 (top)  — Environmental Monitoring Workflow
  Axes: matrix (y) × workflow step (x)
  Color: best tier of guidance at that intersection

Facet 2 (bottom) — Toxicology Workflow
  Axes: workflow step (x); matrix-independent
  Color: best tier of guidance for each tox step

Hover shows per-paper details: analytical method(s), particle size range covered,
key metrics reported (mass vs. count vs. full characterization), and contextual notes.

Data source: MNP Quality Standards Crosswalk v3.xlsx

Tier color scheme
  Tier 1  |  #6A0DAD  purple     Regulatory / Accredited SOP
  Tier 2  |  #1565C0  blue       Authoritative Guidance
  Tier 3  |  #2E7D32  green      Peer-Reviewed Method / SOP
  Tier 4  |  #78909C  grey-blue  Supporting Science
  Gap     |  #FFCDD2  salmon     No specific guidance identified

Usage:
    python fig2_gap_heatmap.py
Output:
    fig2_gap_heatmap.html  (same directory)
"""

import json, pathlib
import openpyxl

HERE   = pathlib.Path(__file__).parent
XLSX   = HERE.parent / "MNP Quality Standards Crosswalk v3.xlsx"
OUTDIR = HERE
OUTDIR.mkdir(parents=True, exist_ok=True)

# ── Load data ────────────────────────────────────────────────────────────────
wb = openpyxl.load_workbook(XLSX)
ws = wb["Crosswalk Table"]
papers = [row for row in ws.iter_rows(min_row=3, values_only=True) if row[0] is not None]

def cell_tier(val):
    """Return integer tier (1-4) if cell has a per-cell tier value, else None."""
    try:
        t = int(val)
        return t if 1 <= t <= 4 else None
    except (TypeError, ValueError):
        return None

# ── Column definitions (0-based Python indices) ──────────────────────────────
MATRIX_COLS = [
    (10, "Drinking Water"),
    (11, "Surface Water /\nWastewater"),
    (12, "Sediment"),
    (13, "Biota / Tissue"),
    (14, "Air / Atmos."),
    (15, "Food / Diet"),
    (16, "Human Tissue /\nBiomonitor"),
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

TOX_COLS = [
    (28, "Tox Study\nDesign"),
    (29, "Tox Effects\nTesting"),
    (30, "Interlaboratory\nValidation"),
    (31, "Risk\nAssessment"),
]

# Method column indices → display name (for inferring methods from crosswalk)
METHOD_COLS = {20: "\u00b5FTIR", 21: "\u00b5Raman", 22: "Py-GC-MS"}

TIER_LABELS = {1: "Tier 1", 2: "Tier 2", 3: "Tier 3", 4: "Tier 4", 5: "Gap"}
TIER_DESC   = {
    1: "Regulatory / Accredited SOP",
    2: "Authoritative Guidance",
    3: "Peer-Reviewed Method",
    4: "Supporting Science",
    5: "No specific guidance identified",
}

# ── Per-paper metadata for enriched hover text ────────────────────────────────
# Keyed by row ID (p[0]) from crosswalk. Provides size ranges and key metrics
# not fully captured in the Key Notes column.
PAPER_METADATA = {
    # --- Drinking Water ---
    82: {  # SWRCB/DDW 2025 (SWB-MP1-rev1 sampling SOP)
        "size_range": "\u22655 \u00b5m (FTIR); \u22651 \u00b5m (Raman)",
        "key_metrics": "Particle count by polymer type, size bin, morphology; blank-corrected values",
    },
    85: {  # Wong & Coffin 2022 (SWB-MP1 extraction + FTIR)
        "size_range": "\u22655 \u00b5m (\u00b5FTIR); California DW matrix",
        "key_metrics": "Count by polymer/size/morphology; blank-corrected; LOD reported",
    },
    89: {  # ISO 16094-2:2025
        "size_range": "\u226520 \u00b5m (\u00b5FTIR); \u22651 \u00b5m (\u00b5Raman) for DW/low-turbidity",
        "key_metrics": "Count, polymer type, size distribution; spectral quality (HQI); library requirements",
    },
    102: {  # EU Decision 2024/1441
        "size_range": "20\u20135000 \u00b5m (particles, area-equivalent diameter); 20\u201315000 \u00b5m (fibres, length); 5 size bins",
        "key_metrics": "Count/m\u00b3 by polymer type (10 priority + other synthetics); \u22651000 L sample; 10 procedural blanks; spike recovery 100%\u00b140%",
    },
    23: {  # De Frond 2022 (DW interlaboratory, 22 labs)
        "size_range": "1\u201320, 20\u2013212, 212\u2013500, >500 \u00b5m (4 size fractions spiked)",
        "key_metrics": "Recovery 76\u00b110% SE (\u226520 \u00b5m: 92\u00b112%); FTIR accuracy 95%, Raman 91%; 4 polymers; 22 labs; blank 91\u00b1141 particles",
    },
    77: {  # WHO 2019 (DW risk)
        "size_range": "Not specified (risk assessment framework; no analytical SOP)",
        "key_metrics": "Qualitative risk characterization; exposure and hazard assessment framework",
    },
    56: {  # Ponti 2025 (JRC density separation validation)
        "size_range": ">20 \u00b5m (density separation validation, DW matrix)",
        "key_metrics": "Extraction efficiency (spike-recovery); reference material EURM-060 validation",
    },
    88: {  # JRC 2025 (EURM-060)
        "size_range": "~10 \u00b5m PET particles in water matrix (certified reference material)",
        "key_metrics": "Certified reference material for method validation; count-based certification",
    },
    68: {  # Thornton Hampton 2023 (matrix effects DW/SW)
        "size_range": "Multiple size fractions tested across DW and SW matrices",
        "key_metrics": "Extraction efficiency by matrix; method comparison; background particle levels",
    },
    16: {  # Coffin 2022 (DW risk integration)
        "size_range": "\u22655 \u00b5m (DW monitoring context; CA SOP-based)",
        "key_metrics": "Risk characterization; integrated monitoring + RA framework for CA DW regulation",
    },
    # --- Surface Water / Wastewater ---
    64: {  # Sutton 2019 (SF Bay multi-matrix)
        "size_range": ">0.3 mm (manta net); <0.3 mm (pump sampling)",
        "key_metrics": "Count and polymer type in water column; multi-matrix comparison across SF Bay",
    },
    46: {  # Mayer 2024 (tire wear particles)
        "size_range": ">10 \u00b5m (tire wear particle focus; estimated)",
        "key_metrics": "Tire wear particle count/identification; morphology-specific criteria",
    },
    47: {  # Mehinto 2022 (SW risk framework)
        "size_range": "Not specified (risk framework based on monitoring data)",
        "key_metrics": "Action levels for aquatic MPs; risk quotient framework; monitoring data integration",
    },
    1: {   # Dalmau-Soler 2025 (DW/SW Py-GC-MS)
        "size_range": "Any (bulk pyrolysis \u2014 no particle size threshold)",
        "key_metrics": "Mass by polymer type (\u00b5g/L); 92\u201399% removal in DWT documented",
    },
    62: {  # Schymanski 2021 (DW/SW FTIR + Raman)
        "size_range": "\u22651 \u00b5m (Raman); \u226510 \u00b5m (FTIR) for clean/surface water",
        "key_metrics": "Count by polymer/size; spectral quality (HQI >70%); library \u226510 polymer types, \u22657 size bins",
    },
    # --- Sediment ---
    76: {  # Waldschläger 2022 (sediment)
        "size_range": "Various (sediment transport theory applied to MPs; size-dependent settling)",
        "key_metrics": "Settling velocity; density-based fractionation; methodological context for MP behavior",
    },
    41: {  # Langknecht 2023 (sediment interlaboratory)
        "size_range": "\u2265100 \u00b5m (visual sort); \u226510 \u00b5m (spectroscopic subset, estimated)",
        "key_metrics": "Interlaboratory variability in sediment extraction; count and polymer type comparison",
    },
    # --- Sediment + Biota (SCCWRP 2025) ---
    103: { # SCCWRP 2025 (TR 1410.A) sediment/biota sampling
        "size_range": "\u22651 \u00b5m (operationally defined by filter pore size); density separation + digestion prior to spectroscopic ID",
        "key_metrics": "Count/kg dw (sediment); count/g ww (biota tissue); Tier 1 field collection SOP; MDA blank-correction (Lao 2025 framework)",
    },
    104: { # Vural 2025 STAR Protocols (multi-matrix Raman)
        "size_range": "\u2265330 \u00b5m (manta net, SW); \u22651.2 \u00b5m (GF/C filter, sediment & fish GIT); 5 size bins up to >5 mm",
        "key_metrics": "Count by polymer (12-type library) via \u00b5Raman 785 nm; recovery \u226580%; CV <11% target; particles/m\u00b3 (water), /g dw (sediment), /fish",
    },
    # --- Biota ---
    58: {  # Provencher 2019 (marine bird biota)
        "size_range": "\u22650.3 mm (storm-petrels); \u22651 mm (most species); \u22655 mm (mesoplastics); sieve stack 0.3/1/5 mm",
        "key_metrics": "Frequency of occurrence (% birds); count and mass (mg) per individual; GIT compartment-specific; count by size class, shape, color",
    },
    69: {  # Tsangaris 2021 (biota ILC, 4 labs)
        "size_range": "PE/PP/PET spike particles (µm range); fish GIT and mussel tissue",
        "key_metrics": "KOH recovery 96.7%; H\u2082O\u2082 recovery 88.8%; interlaboratory CV <11%; 3 polymers; 2 tissue types; 4 labs",
    },
    24: {  # de Jourdan 2024 (biota QA framework)
        "size_range": "Not specified (QA framework for biota biomonitoring; method-agnostic)",
        "key_metrics": "Quality score rubric (0\u2013100 scale); 18 criteria for biota biomonitoring studies",
    },
    73: {  # Vanavermaete 2024 (TRL biota)
        "size_range": "Not specified (TRL assessment \u2014 methodology readiness evaluation)",
        "key_metrics": "Technology readiness levels (TRL 1\u20139) for biota monitoring methods",
    },
    # --- Air / Atmospheric ---
    79: {  # Wright 2021 (air deposition review)
        "size_range": ">10 \u00b5m (majority of reviewed studies); recommends prioritizing <10 \u00b5m (PM10) for health",
        "key_metrics": "Count (particles/m\u00b3 or particles/m\u00b2/day); polymer type; 11-criterion QA/QC score (mean 48.6% across 27 studies)",
    },
    100: { # Ashta 2026 (FPA-µFTIR air)
        "size_range": "\u226510 \u00b5m (FPA-\u00b5FTIR; wet deposition samples)",
        "key_metrics": "Particle count and type; ~90% spike-recovery; deposition flux (particles/m\u00b2/event)",
    },
    101: { # Ren 2026 (air review)
        "size_range": "Various (review paper; passive and active sampling methods compared)",
        "key_metrics": "Count, flux, and mass metrics across atmospheric studies; standardization gaps identified",
    },
    # --- Food / Diet ---
    29: {  # Gouin 2022a (food + air exposure)
        "size_range": "0.001\u20135000 \u00b5m (NMP range; dietary + inhalation framework)",
        "key_metrics": "Daily intake estimates (particles/day, \u00b5g/day) by route; hazard quotient for human health",
    },
    94: {  # Lane 2025 (exposure scenarios)
        "size_range": "0.1\u20135000 \u00b5m (NMPs; multi-route exposure scenarios)",
        "key_metrics": "Estimated daily intake by route and matrix; exposure distributions across populations",
    },
    # --- Human Tissue / Biomonitoring ---
    60: {  # Rauert 2025 (human blood Py-GC-MS)
        "size_range": "Any (bulk pyrolysis \u2014 validated for blood; no particle size threshold)",
        "key_metrics": "Mass concentration (\u00b5g/mL) by polymer type in human blood; validation data provided",
    },
    98: {  # Wright 2025b (tissue spectroscopic ID)
        "size_range": "\u22655 \u00b5m (\u00b5FTIR/\u00b5Raman for in situ tissue identification)",
        "key_metrics": "In situ particle identification; polymer confirmation in pathological tissue sections",
    },
    96: {  # Wardani 2024 (PBK)
        "size_range": "0.1\u201310 \u00b5m (NMPs; nano-range bioaccumulation focus)",
        "key_metrics": "Tissue concentration estimates; bioaccumulation factors; clearance rates from PBK model",
    },
    16: {  # Coffin 2022 (also HumTis via RA)
        "size_range": "\u22655 \u00b5m (DW monitoring context; tied to CA SOP)",
        "key_metrics": "Integrated monitoring + human health RA framework used in California regulation",
    },
}

# ── Helper functions ──────────────────────────────────────────────────────────
def get_paper_methods(p):
    """Return list of method display names this paper addresses (from method columns)."""
    return [name for ci, name in METHOD_COLS.items() if cell_tier(p[ci]) is not None]

def fmt(s):
    """Replace newlines with <br> for display."""
    return s.replace("\n", "<br>")

def build_mon_hover(mname, wname, plist):
    """Rich hover text for a monitoring matrix x workflow cell."""
    if not plist:
        return (
            f"<b>{fmt(mname)} \u00d7 {fmt(wname)}</b><br>"
            "<b>Gap</b> \u2014 No specific guidance identified in this collection<br>"
            "Consider adapting nearest matrix guidelines; document all deviations"
        )
    bt = plist[0][0]
    lines = [
        f"<b>{fmt(mname)} \u00d7 {fmt(wname)}</b>",
        f"Best available: <b>{TIER_LABELS[bt]}</b> \u2014 {TIER_DESC[bt]}",
        f"Papers with guidance (n={len(plist)}):",
    ]
    for tier, pid, cite, notes, methods in plist[:5]:
        meta = PAPER_METADATA.get(pid, {})
        method_str = ", ".join(methods) if methods else "see paper"
        size_str   = meta.get("size_range",   "see paper")
        metric_str = meta.get("key_metrics",  "see paper")
        note_str   = (notes or "")[:130]
        lines.append(f"<br>\u2022 <b>{cite}</b> [{TIER_LABELS[tier]}]")
        lines.append(f"\u00a0\u00a0Method(s): {method_str}")
        lines.append(f"\u00a0\u00a0Size range: {size_str}")
        lines.append(f"\u00a0\u00a0Key metrics: {metric_str}")
        if note_str:
            lines.append(f"\u00a0\u00a0Note: {note_str}")
    if len(plist) > 5:
        lines.append(f"<br>\u00a0\u00a0...+{len(plist)-5} additional papers in collection")
    return "<br>".join(lines)

def build_tox_hover(wname, plist):
    """Rich hover text for a toxicology workflow cell."""
    if not plist:
        return (
            f"<b>Toxicology \u00d7 {fmt(wname)}</b><br>"
            "<b>Gap</b> \u2014 No specific guidance identified"
        )
    bt = plist[0][0]
    lines = [
        f"<b>Toxicology \u00d7 {fmt(wname)}</b>",
        "(Matrix-independent guidance)",
        f"Best available: <b>{TIER_LABELS[bt]}</b> \u2014 {TIER_DESC[bt]}",
        f"Papers (n={len(plist)}):",
    ]
    for tier, pid, cite, notes, methods in plist[:7]:
        meta     = PAPER_METADATA.get(pid, {})
        note_str = (notes or "")[:150]
        method_str = ", ".join(methods) if methods else None
        lines.append(f"<br>\u2022 <b>{cite}</b> [{TIER_LABELS[tier]}]")
        if method_str:
            lines.append(f"\u00a0\u00a0Method(s): {method_str}")
        if meta.get("size_range"):
            lines.append(f"\u00a0\u00a0Particle size: {meta['size_range']}")
        if meta.get("key_metrics"):
            lines.append(f"\u00a0\u00a0Key metrics: {meta['key_metrics']}")
        if note_str:
            lines.append(f"\u00a0\u00a0Note: {note_str}")
    if len(plist) > 7:
        lines.append(f"<br>\u00a0\u00a0...+{len(plist)-7} additional papers")
    return "<br>".join(lines)

# ── Build monitoring heatmap ──────────────────────────────────────────────────
y_mon = [m for _, m in MATRIX_COLS]
x_mon = [w for _, w in WORKFLOW_COLS]
n_mrows, n_mcols = len(MATRIX_COLS), len(WORKFLOW_COLS)

z_mon     = [[None]*n_mcols for _ in range(n_mrows)]
hover_mon = [[""  ]*n_mcols for _ in range(n_mrows)]
txt_mon   = [[""  ]*n_mcols for _ in range(n_mrows)]

for ri, (mci, mname) in enumerate(MATRIX_COLS):
    for ci, (wci, wname) in enumerate(WORKFLOW_COLS):
        plist = []
        for p in papers:
            tm = cell_tier(p[mci])
            tw = cell_tier(p[wci])
            if tm is not None and tw is not None:
                plist.append((
                    max(tm, tw),       # intersection tier (worst of the two)
                    int(p[0]),         # paper ID
                    str(p[1]),         # citation
                    str(p[32]) if p[32] else "",  # Key Notes
                    get_paper_methods(p),          # method list
                ))
        plist.sort()
        if plist:
            bt = plist[0][0]
            z_mon[ri][ci]     = bt
            hover_mon[ri][ci] = build_mon_hover(mname, wname, plist)
            txt_mon[ri][ci]   = TIER_LABELS[bt]
        else:
            z_mon[ri][ci]     = 5
            hover_mon[ri][ci] = build_mon_hover(mname, wname, [])
            txt_mon[ri][ci]   = "Gap"

# ── Build toxicology heatmap ──────────────────────────────────────────────────
y_tox = ["Toxicology"]
x_tox = [w for _, w in TOX_COLS]
n_tcols = len(TOX_COLS)

z_tox     = [[None]*n_tcols]
hover_tox = [[""  ]*n_tcols]
txt_tox   = [[""  ]*n_tcols]

for ti, (wci, wname) in enumerate(TOX_COLS):
    plist = []
    for p in papers:
        tw = cell_tier(p[wci])
        if tw is not None:
            plist.append((
                tw,
                int(p[0]),
                str(p[1]),
                str(p[32]) if p[32] else "",
                get_paper_methods(p),
            ))
    plist.sort()
    if plist:
        bt = plist[0][0]
        z_tox[0][ti]     = bt
        hover_tox[0][ti] = build_tox_hover(wname, plist)
        txt_tox[0][ti]   = TIER_LABELS[bt]
    else:
        z_tox[0][ti]     = 5
        hover_tox[0][ti] = build_tox_hover(wname, [])
        txt_tox[0][ti]   = "Gap"

# ── Display labels ────────────────────────────────────────────────────────────
x_mon_d = [fmt(l) for l in x_mon]
y_mon_d = [fmt(l) for l in y_mon]
x_tox_d = [fmt(l) for l in x_tox]
y_tox_d = [fmt(l) for l in y_tox]

# ── Discrete colorscale ───────────────────────────────────────────────────────
COLORSCALE = [
    [0.0, "#6A0DAD"], [0.2, "#6A0DAD"],  # Tier 1
    [0.2, "#1565C0"], [0.4, "#1565C0"],  # Tier 2
    [0.4, "#2E7D32"], [0.6, "#2E7D32"],  # Tier 3
    [0.6, "#78909C"], [0.8, "#78909C"],  # Tier 4
    [0.8, "#FFCDD2"], [1.0, "#FFCDD2"],  # Gap
]

# ── Heatmap traces ────────────────────────────────────────────────────────────
mon_trace = {
    "type": "heatmap",
    "z": z_mon,
    "x": x_mon_d,
    "y": y_mon_d,
    "text": txt_mon,
    "hovertext": hover_mon,
    "hovertemplate": "%{hovertext}<extra></extra>",
    "colorscale": COLORSCALE,
    "zmin": 0.5, "zmax": 5.5,
    "showscale": False,
    "xgap": 2, "ygap": 2,
    "xaxis": "x", "yaxis": "y",
}

tox_trace = {
    "type": "heatmap",
    "z": z_tox,
    "x": x_tox_d,
    "y": y_tox_d,
    "text": txt_tox,
    "hovertext": hover_tox,
    "hovertemplate": "%{hovertext}<extra></extra>",
    "colorscale": COLORSCALE,
    "zmin": 0.5, "zmax": 5.5,
    "showscale": False,
    "xgap": 3, "ygap": 4,
    "xaxis": "x2", "yaxis": "y2",
}

# ── Cell text annotations ─────────────────────────────────────────────────────
def txt_color(val):
    return "white" if val in (1, 2) else ("#B71C1C" if val == 5 else "white")

mon_annotations = []
for ri, row in enumerate(z_mon):
    for ci, val in enumerate(row):
        if val is None:
            continue
        mon_annotations.append({
            "x": x_mon_d[ci], "y": y_mon_d[ri],
            "text": f"<b>{txt_mon[ri][ci]}</b>",
            "font": {"size": 9, "color": txt_color(val)},
            "showarrow": False,
            "xref": "x", "yref": "y",
        })

tox_annotations = []
for ci, val in enumerate(z_tox[0]):
    if val is None:
        continue
    tox_annotations.append({
        "x": x_tox_d[ci], "y": y_tox_d[0],
        "text": f"<b>{txt_tox[0][ci]}</b>",
        "font": {"size": 10, "color": txt_color(val)},
        "showarrow": False,
        "xref": "x2", "yref": "y2",
    })

# ── Subplot title annotations (paper-relative coordinates) ───────────────────
# yaxis domain: [0.30, 1.0]   xaxis domain: [0, 1]
# yaxis2 domain: [0.0, 0.22]  xaxis2 domain: [0, 0.45]
subplot_annots = [
    {
        "x": 0.5, "y": 1.03,
        "xref": "paper", "yref": "paper",
        "text": "<b>\u25a0 Environmental Monitoring Workflow</b>",
        "showarrow": False,
        "font": {"size": 14, "color": "#2E7D32"},
        "align": "center",
    },
    {
        "x": 0.225, "y": 0.245,
        "xref": "paper", "yref": "paper",
        "text": "<b>\u25a0 Toxicology Workflow</b>",
        "showarrow": False,
        "font": {"size": 14, "color": "#8E24AA"},
        "align": "center",
    },
    {
        "x": 0.225, "y": 0.225,
        "xref": "paper", "yref": "paper",
        "text": "<i>(matrix-independent)</i>",
        "showarrow": False,
        "font": {"size": 10, "color": "#666666"},
        "align": "center",
    },
]

all_annotations = mon_annotations + tox_annotations + subplot_annots

# ── Legend scatter traces ─────────────────────────────────────────────────────
legend_traces = []
for tier, label, color in [
    (1, "Tier 1 \u2014 Regulatory/Accredited SOP",  "#6A0DAD"),
    (2, "Tier 2 \u2014 Authoritative Guidance",      "#1565C0"),
    (3, "Tier 3 \u2014 Peer-Reviewed Method",        "#2E7D32"),
    (4, "Tier 4 \u2014 Supporting Science",          "#78909C"),
    (5, "Gap \u2014 No specific guidance",           "#FFCDD2"),
]:
    legend_traces.append({
        "type": "scatter",
        "x": [None], "y": [None],
        "mode": "markers",
        "marker": {"color": color, "size": 14, "symbol": "square"},
        "name": label,
        "showlegend": True,
    })

# ── Layout ────────────────────────────────────────────────────────────────────
layout = {
    "title": {
        "text": (
            "<b>Availability of Authoritative Guidance for MNP Research</b><br>"
            "<sup>Hover over any cell for paper details, analytical methods, "
            "particle size ranges, and key metrics (n=105 papers in collection)</sup>"
        ),
        "x": 0.5,
        "font": {"size": 15},
    },
    # Monitoring subplot (top, larger)
    "xaxis": {
        "side": "top",
        "tickangle": -30,
        "tickfont": {"size": 10},
        "showgrid": False,
        "zeroline": False,
        "domain": [0, 1],
        "anchor": "y",
    },
    "yaxis": {
        "autorange": "reversed",
        "tickfont": {"size": 11},
        "showgrid": False,
        "domain": [0.28, 1.0],
        "anchor": "x",
    },
    # Toxicology subplot (bottom, smaller — 4 cols ~ 36% of width)
    "xaxis2": {
        "side": "top",
        "tickangle": -30,
        "tickfont": {"size": 10},
        "showgrid": False,
        "zeroline": False,
        "domain": [0, 0.44],
        "anchor": "y2",
    },
    "yaxis2": {
        "tickfont": {"size": 12},
        "showgrid": False,
        "domain": [0.0, 0.20],
        "anchor": "x2",
    },
    "plot_bgcolor": "#F5F5F5",
    "paper_bgcolor": "#FFFFFF",
    "annotations": all_annotations,
    "legend": {
        "orientation": "h",
        "yanchor": "bottom", "y": -0.08,
        "xanchor": "center", "x": 0.5,
        "title": {"text": "Best available guidance:  "},
        "font": {"size": 11},
    },
    "margin": {"t": 140, "b": 90, "l": 170, "r": 30},
    "height": 880,
    "hoverlabel": {
        "bgcolor": "white",
        "bordercolor": "#CCCCCC",
        "font": {"size": 11},
        "namelength": -1,
    },
}

# ── Assemble and write ────────────────────────────────────────────────────────
fig_data = legend_traces + [mon_trace, tox_trace]
fig_json = json.dumps({"data": fig_data, "layout": layout})

HTML = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Fig 2 \u2013 MNP Guidance Gap Heatmap</title>
  <script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>
  <style>
    body{{margin:0;font-family:sans-serif;}}
    .plotly-graph-div .hoverlayer .hovertext {{
      max-width: 500px !important;
      white-space: normal !important;
    }}
  </style>
</head>
<body>
  <div id="fig" style="width:100%;height:960px;"></div>
  <script>
    var fig = {fig_json};
    var config = {{
      responsive: true,
      displayModeBar: true,
      toImageButtonOptions: {{format: 'svg', width: 1400, height: 960}}
    }};
    Plotly.newPlot('fig', fig.data, fig.layout, config);
  </script>
</body>
</html>"""

out_path = OUTDIR / "fig2_gap_heatmap.html"
out_path.write_text(HTML, encoding="utf-8")
print(f"Saved: {out_path}")
print(f"  Monitoring: {n_mrows} matrices \u00d7 {n_mcols} workflow steps")
print(f"  Toxicology: 1 row \u00d7 {n_tcols} tox steps")
# Report cells with gaps
gaps_mon = sum(1 for row in z_mon for v in row if v == 5)
tot_mon  = n_mrows * n_mcols
print(f"  Monitoring gaps: {gaps_mon}/{tot_mon} cells ({100*gaps_mon//tot_mon}%)")
