"""
fig3_quality_passrates.py
--------------------------
Bar chart comparing MNP study quality pass rates across major assessment frameworks
published 2020–2025. Illustrates that data quality has not meaningfully improved
over time despite the growth of the field.

Data: Hardcoded from extracted full-text readings of the relevant papers.
      See: Key Paper Content - Extracted from Full Text.md

Usage:
    python3 fig3_quality_passrates.py
Output:
    fig3_quality_passrates.html  (same directory)
"""

import json, pathlib

HERE   = pathlib.Path(__file__).parent
OUTDIR = HERE
OUTDIR.mkdir(parents=True, exist_ok=True)

# ── Data (from paper extractions) ───────────────────────────────────────────
# Each entry: (year, framework_short, pass_rate_pct, n_studies,
#              study_type, metric_description, color, reference)

FRAMEWORKS = [
    {
        "label":   "de Ruijter et al.<br>2020",
        "year":    2020,
        "type":    "Ecotoxicology",
        "metric":  "Avg score across 20 criteria",
        "pass_pct": 44.6,
        "range_lo": 20.0,
        "range_hi": 77.5,
        "n":       105,
        "note":    "No study scored positively on ALL 20 criteria. Average = 44.6% of max score (range 20–77.5%). "
                   "Most critical gap: background contamination control.",
        "ref":     "de Ruijter et al. (2020) Environ Sci Technol",
    },
    {
        "label":   "Gouin et al.<br>(NMP-TSAT)<br>2022",
        "year":    2022,
        "type":    "Human Health Toxicology",
        "metric":  "% studies passing all Tier 1 critical criteria",
        "pass_pct": 16.2,  # 12/74
        "range_lo": None,
        "range_hi": None,
        "n":       74,
        "note":    "Only 12/74 studies (10 oral + 2 inhalation) scored ≥1 on all critical criteria. "
                   "~60% of studies used monodisperse spheres; ~46% polystyrene. "
                   "Max possible TAS: 52 (in vivo), 46 (in vitro). Observed: 12–44 / 16–34.",
        "ref":     "Gouin et al. (2022) Microplastics and Nanoplastics 2:2",
    },
    {
        "label":   "ToMEx 1.0<br>(Hampton et al.)<br>2021",
        "year":    2021,
        "type":    "Ecotoxicology",
        "metric":  "% studies passing minimum screening\ncriteria for threshold derivation",
        "pass_pct": 13.0,
        "range_lo": None,
        "range_hi": None,
        "n":       162,
        "note":    "13% of aquatic toxicology studies passed minimum screening criteria for ecological threshold derivation.",
        "ref":     "Thornton Hampton et al. (2021) — ToMEx 1.0",
    },
    {
        "label":   "ToMEx 2.0<br>(Hampton et al.)<br>2025",
        "year":    2025,
        "type":    "Ecotoxicology",
        "metric":  "% studies passing minimum screening\ncriteria for threshold derivation",
        "pass_pct": 12.0,
        "range_lo": None,
        "range_hi": None,
        "n":       286,
        "note":    "89% of studies in ToMEx 2.0 failed minimum screening criteria. "
                   "Pass rate virtually unchanged from ToMEx 1.0 (13% → 12%). "
                   "Most common failure: <3 test concentrations (insufficient dose-response). "
                   "Only 12 new studies passed for threshold derivation.",
        "ref":     "Hampton et al. (2025) Microplastics and Nanoplastics 5:38",
    },
]

# Color by study type
TYPE_COLORS = {
    "Ecotoxicology":           "#1565C0",
    "Human Health Toxicology": "#8E24AA",
}

# ── Build traces ─────────────────────────────────────────────────────────────
bars = []
error_ys = []
for fw in FRAMEWORKS:
    c = TYPE_COLORS[fw["type"]]
    bars.append(fw["pass_pct"])
    error_ys.append(
        (fw["range_hi"] - fw["pass_pct"]) if fw["range_hi"] is not None else 0
    )

labels   = [fw["label"] for fw in FRAMEWORKS]
colors   = [TYPE_COLORS[fw["type"]] for fw in FRAMEWORKS]
hovers   = [
    f"<b>{fw['label'].replace('<br>',' ')}</b><br>"
    f"Study type: {fw['type']}<br>"
    f"n studies: {fw['n']}<br>"
    f"Metric: {fw['metric']}<br>"
    f"Pass rate: <b>{fw['pass_pct']:.1f}%</b>"
    + (f" (range {fw['range_lo']}–{fw['range_hi']}%)" if fw['range_lo'] else "")
    + f"<br><br>{fw['note']}<br><br><i>{fw['ref']}</i>"
    for fw in FRAMEWORKS
]

bar_trace = {
    "type": "bar",
    "x": labels,
    "y": [fw["pass_pct"] for fw in FRAMEWORKS],
    "marker": {"color": colors, "line": {"color": "white", "width": 1.5}},
    "text":  [f"<b>{fw['pass_pct']:.1f}%</b><br>(n={fw['n']})" for fw in FRAMEWORKS],
    "textposition": "outside",
    "textfont": {"size": 12},
    "hovertext": hovers,
    "hovertemplate": "%{hovertext}<extra></extra>",
    "error_y": {
        "type": "data",
        "array": [(fw["range_hi"] - fw["pass_pct"]) if fw["range_hi"] else 0 for fw in FRAMEWORKS],
        "arrayminus": [(fw["pass_pct"] - fw["range_lo"]) if fw["range_lo"] else 0 for fw in FRAMEWORKS],
        "visible": True,
        "color": "#555",
        "thickness": 2,
        "width": 6,
    },
    "showlegend": False,
}

# Threshold line at 100%
ref_line = {
    "type": "scatter",
    "x": [labels[0], labels[-1]],
    "y": [100, 100],
    "mode": "lines",
    "line": {"color": "#999", "dash": "dot", "width": 1},
    "name": "100% (all criteria met)",
    "hoverinfo": "skip",
}

# Annotation arrows for key insights
# Legend scatter traces for study type
legend_eco = {
    "type": "scatter", "x": [None], "y": [None],
    "mode": "markers",
    "marker": {"color": "#1565C0", "size": 14, "symbol": "square"},
    "name": "Ecotoxicology studies",
}
legend_hh = {
    "type": "scatter", "x": [None], "y": [None],
    "mode": "markers",
    "marker": {"color": "#8E24AA", "size": 14, "symbol": "square"},
    "name": "Human Health Toxicology studies",
}

layout = {
    "title": {
        "text": (
            "<b>MNP Study Quality: Pass Rates Across Assessment Frameworks (2020–2025)</b><br>"
            "<sup>Proportion of published studies meeting minimum quality criteria by framework</sup>"
        ),
        "x": 0.5, "font": {"size": 15},
    },
    "xaxis": {
        "title": "",
        "tickfont": {"size": 12},
        "showgrid": False,
    },
    "yaxis": {
        "title": "Studies meeting quality criteria (%)",
        "range": [0, 115],
        "tickfont": {"size": 12},
        "showgrid": True,
        "gridcolor": "#EEEEEE",
        "zeroline": True,
        "zerolinecolor": "#999",
    },
    "plot_bgcolor": "#FFFFFF",
    "paper_bgcolor": "#FFFFFF",
    "legend": {
        "orientation": "h",
        "yanchor": "bottom", "y": -0.22,
        "xanchor": "center", "x": 0.5,
        "font": {"size": 11},
    },
    "annotations": [
        {
            "x": 0, "y": 55,
            "xref": "x", "yref": "y",
            "text": "← Error bars show<br>score range<br>across studies",
            "showarrow": False,
            "font": {"size": 10, "color": "#555"},
            "align": "left",
        },
        {
            "x": 2.5, "y": 95,
            "xref": "x", "yref": "y",
            "text": "<i>Pass rate unchanged<br>2021 → 2025 despite<br>field growth</i>",
            "showarrow": True,
            "arrowhead": 2, "arrowsize": 1, "arrowwidth": 1.5,
            "arrowcolor": "#888",
            "ax": 50, "ay": -30,
            "font": {"size": 10, "color": "#888"},
        },
    ],
    "margin": {"t": 110, "b": 100, "l": 80, "r": 30},
    "height": 480,
    "bargap": 0.35,
}

fig_data = [bar_trace, ref_line, legend_eco, legend_hh]
fig_json = json.dumps({"data": fig_data, "layout": layout})

HTML = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Fig 3 – MNP Study Quality Pass Rates</title>
  <script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>
  <style>body{{margin:0;font-family:sans-serif;}}</style>
</head>
<body>
  <div id="fig" style="width:100%;height:520px;"></div>
  <script>
    var fig = {fig_json};
    Plotly.newPlot('fig', fig.data, fig.layout, {{responsive:true, displayModeBar:true}});
  </script>
</body>
</html>"""

out_path = OUTDIR / "fig3_quality_passrates.html"
out_path.write_text(HTML, encoding="utf-8")
print(f"Saved: {out_path}")
