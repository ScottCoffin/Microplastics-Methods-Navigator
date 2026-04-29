"""
visual_tree_tab.py — Interactive Decision Tree with Linear Workflow Structure

Reflects how studies actually proceed:
    1. Problem Formulation (all studies)
    2. Branch: Monitoring / Toxicology / Risk Assessment
    3. Linear core workflow (e.g., Sampling → Extraction → Analysis → Reporting)
    4. Auxiliary supports shown alongside (Definitions, Ref Materials, Blanks/QC, Interlaboratory)

Integration in app.py:
    tab1, tab2 = st.tabs(["🔍 Step-by-Step Navigator", "🌳 Decision Tree"])
    with tab2:
        from visual_tree_tab import render_decision_tree
        render_decision_tree(df, tree)
"""

import streamlit as st
import pandas as pd


# ── WORKFLOW STRUCTURES ─────────────────────────────────────

# Monitoring: linear core + auxiliary
MONITORING_CORE = [
    {"key": "sampling",    "label": "Sampling",    "icon": "📍", "column": "Sampling (Field Methods)"},
    {"key": "extraction",  "label": "Extraction",  "icon": "🧪", "column": "Sample Processing / Extraction"},
    {"key": "analysis",    "label": "Analysis",    "icon": "🔎", "column": "Analytical Methods (General)",
     "has_instruments": True},
    {"key": "reporting",   "label": "Reporting & Data Deposition", "icon": "📝", "column": "Reporting & Harmonization"},
]

MONITORING_AUXILIARY = [
    {"key": "definitions",     "label": "Definitions & Terminology", "icon": "📖", "column": "Definitions & Terminology"},
    {"key": "ref_materials",   "label": "Reference Materials",       "icon": "📦", "column": "Reference Materials / +Controls"},
    {"key": "blanks",          "label": "Blanks & Contamination Control", "icon": "🧹", "column": "Blanks & Contamination Control"},
    {"key": "data_stats",      "label": "Data Analysis & Statistics", "icon": "📊", "column": "Data Analysis & Statistics"},
    {"key": "interlaboratory", "label": "Interlaboratory Studies",   "icon": "🔄", "doc_type": "Interlaboratory"},
]

# Toxicology: linear core + auxiliary
TOX_CORE = [
    {"key": "particle_char", "label": "Particle Characterization", "icon": "🔬",
     "column": "Toxicology: Study Design & Dosimetry"},
    {"key": "dosimetry",     "label": "Dosimetry",                 "icon": "💊",
     "column": "Toxicology: Study Design & Dosimetry",
     "keywords": "dosimetry;particokinetics;delivered dose;ISDD;PBK;sedimentation"},
    {"key": "effects",       "label": "Effects Testing",           "icon": "🧬",
     "column": "Toxicology: Effects Testing Methods", "has_test_systems": True},
    {"key": "tox_reporting", "label": "Reporting",                 "icon": "📝",
     "column": "Reporting & Harmonization"},
]

TOX_AUXILIARY = [
    {"key": "definitions",   "label": "Definitions & Terminology", "icon": "📖", "column": "Definitions & Terminology"},
    {"key": "ref_particles", "label": "Reference / Test Particles", "icon": "📦", "column": "Reference Materials / +Controls"},
    {"key": "quality",       "label": "Study Quality & Scoring",   "icon": "✅",
     "column": "Toxicology: Study Design & Dosimetry",
     "keywords": "quality;QA;scoring;criteria;checklist;ToMEx"},
]

# Risk Assessment: linear
RA_CORE = [
    {"key": "frameworks", "label": "RA Frameworks",        "icon": "🏗️",
     "column": "Risk Assessment / Risk Char.", "doc_type": "Framework"},
    {"key": "hazard",     "label": "Hazard Identification", "icon": "⚠️",
     "column": "Risk Assessment / Risk Char.",
     "keywords": "hazard;toxicity;effect;ToMEx;SSD"},
    {"key": "exposure",   "label": "Exposure Assessment",   "icon": "📏",
     "column": "Risk Assessment / Risk Char.",
     "keywords": "exposure;PBK;monitoring;scenario;dietary;inhalation"},
    {"key": "risk_char",  "label": "Risk Characterization", "icon": "📊",
     "column": "Risk Assessment / Risk Char.",
     "keywords": "risk quotient;threshold;management;stochastic;TRL"},
]

RA_AUXILIARY = [
    {"key": "definitions", "label": "Definitions & Terminology", "icon": "📖", "column": "Definitions & Terminology"},
]

# Matrices
MATRICES = {
    "drinking_water": {"label": "Drinking Water",  "icon": "🚰", "kw": "Drinking Water", "gap": None},
    "surface_water":  {"label": "Surface Water",   "icon": "🌊", "kw": "Surface Water",
                       "gap": "⚠️ No Tier 1 SOP. ASTM D8332 recommended. Brander et al. 2020 (Tier 3) best available."},
    "sediment":       {"label": "Sediment",        "icon": "🪨", "kw": "Sediment", "gap": None},
    "biota":          {"label": "Biota / Tissue",  "icon": "🐟", "kw": "Biota", "gap": None},
    "air":            {"label": "Air",             "icon": "💨", "kw": "Air",
                       "gap": "⚠️ No Tier 1/2 method. Ashta et al. 2026 (Tier 3) best available."},
    "food":           {"label": "Food / Dietary",  "icon": "🍽️", "kw": "Food",
                       "gap": "⚠️ No Tier 1/2 method. EFSA (2016) highlighted major gaps."},
    "human_tissue":   {"label": "Human Tissue",    "icon": "🩸", "kw": "Human",
                       "gap": "⚠️ No Tier 1/2 method. Rauert et al. 2025 (Tier 4) leads for blood."},
    "soil":           {"label": "Soil",            "icon": "🌱", "kw": "Soil",
                       "gap": "⚠️ No Tier 1/2 standard. Li 2019, Möller 2022, Ling 2026 (Tier 3) best available."},
}

# Instruments (sub-branch of Analysis)
INSTRUMENTS = {
    "ftir":      {"label": "µFTIR / FPA-FTIR", "kw": "µFTIR"},
    "ldir":      {"label": "LDIR",              "kw": "LDIR"},
    "raman":     {"label": "µRaman",            "kw": "µRaman"},
    "pyrolysis": {"label": "Py-GC-MS",          "kw": "Py-GC-MS"},
    "ted":       {"label": "TED-GC-MS",         "kw": "TED-GC-MS"},
    "nile_red":  {"label": "Nile Red",           "kw": "Nile Red"},
}

# Test systems (sub-branch of Effects Testing)
TEST_SYSTEMS = {
    "in_vitro":   {"label": "In Vitro (cell-based)",       "keywords": "in vitro;steroidogenesis;cell;H295R;Caco"},
    "eco_aquatic": {"label": "Ecotox — Aquatic",           "keywords": "ecotox;aquatic;benthic;fish;invertebrate;Daphnia;bivalve"},
    "eco_terr":   {"label": "Ecotox — Terrestrial / Soil", "keywords": "soil;terrestrial;earthworm"},
    "mammalian":  {"label": "Mammalian In Vivo",           "keywords": "mammalian;rodent;mouse;rat;oral"},
    "human":      {"label": "Human / Epidemiological",     "keywords": "human;blood;placenta;epidemiolog;clinical"},
}

# Display constants
TIER_COLORS = {1: "#1a7a2e", 2: "#2e6b8a", 3: "#6b5b2e", 4: "#6b6b6b"}
TIER_ICONS = {1: "🟢", 2: "🔵", 3: "🟡", 4: "⚪"}
TIER_LABELS = {
    1: "★★★★ Tier 1 — Normative / Binding",
    2: "★★★☆ Tier 2 — Authoritative / Institutional",
    3: "★★☆☆ Tier 3 — Peer-Reviewed / Validated",
    4: "★☆☆☆ Tier 4 — Supporting / Contextual",
}


# ── FILTER HELPERS ──────────────────────────────────────────

def _find_col(df, candidates):
    cols_lower = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        clean = cand.lower().strip().replace("\n", " ").replace("  ", " ")
        if clean in cols_lower:
            return cols_lower[clean]
        for cl, co in cols_lower.items():
            if clean in cl or cl in clean:
                return co
    return None


def _filter_domain(df, domain):
    col = _find_col(df, ["Primary Domain"])
    if col is None:
        return df
    return df[df[col].astype(str).str.lower().isin([domain.lower(), "both", "cross-cutting"])]


def _filter_matrix(df, kw):
    col = _find_col(df, ["Matrix Tags"])
    if col is None:
        return df
    s = df[col].astype(str)
    return df[s.str.contains(kw, case=False, na=False) | s.str.contains("Cross-cutting", case=False, na=False)]


def _filter_column(df, col_name):
    col = _find_col(df, [col_name])
    if col is None:
        return df
    return df[df[col].notna() & (df[col] != "") & (df[col] != 0)]


def _filter_instrument(df, kw):
    col = _find_col(df, ["Instrumentation Tags"])
    if col is None:
        return df
    return df[df[col].astype(str).str.contains(kw, case=False, na=False)]


def _filter_doc_type(df, dt):
    col = _find_col(df, ["Document Type"])
    if col is None:
        return df
    return df[df[col].astype(str).str.contains(dt, case=False, na=False)]


def _filter_keywords(df, kws):
    col = _find_col(df, ["Key Notes"])
    if col is None:
        return df
    mask = pd.Series(False, index=df.index)
    for kw in kws.split(";"):
        mask = mask | df[col].astype(str).str.contains(kw.strip(), case=False, na=False)
    return df[mask]


def _apply_step_filters(df, step_info):
    """Apply all filters defined in a step dict."""
    result = df
    if "column" in step_info:
        result = _filter_column(result, step_info["column"])
    if "doc_type" in step_info:
        result = _filter_doc_type(result, step_info["doc_type"])
    if "keywords" in step_info:
        result = _filter_keywords(result, step_info["keywords"])
    return result


def _sort_tier(df):
    yr = _find_col(df, ["Year"])
    if "tier_num" in df.columns:
        cols = ["tier_num"] + ([yr] if yr else [])
        asc = [True] + ([False] if yr else [])
        return df.sort_values(cols, ascending=asc)
    return df


# ── GRAPHVIZ BUILDER ────────────────────────────────────────

_ACT_FILL = "#e8f4f8"
_ACT_BORDER = "#2e6b8a"
_ACT_TEXT = "#1a3a4a"
_DIM_FILL = "#f5f5f5"
_DIM_BORDER = "#cccccc"
_DIM_TEXT = "#999999"
_AUX_FILL = "#fdf6e3"
_AUX_BORDER = "#b58900"
_NO_REF_FILL = "#f8e1e1"
_NO_REF_BORDER = "#b00020"
_NO_REF_TEXT = "#6b1b1b"
_TIER_NODE_STYLES = {
    1: ("#dff3e4", TIER_COLORS[1], "#134e22"),
    2: ("#dcecf4", TIER_COLORS[2], "#164760"),
    3: ("#f5edcf", TIER_COLORS[3], "#594814"),
    4: ("#eeeeee", TIER_COLORS[4], "#4f4f4f"),
}


def _best_tier(df):
    if len(df) == 0 or "tier_num" not in df.columns:
        return None
    tiers = pd.to_numeric(df["tier_num"], errors="coerce").dropna()
    if tiers.empty:
        return None
    return int(tiers.min())


def _availability(df):
    return {"count": len(df), "tier": _best_tier(df)}


def _availability_label(label, availability):
    if not availability:
        return label
    count = availability.get("count", 0)
    tier = availability.get("tier")
    tier_label = f"Tier {tier}" if tier else "No refs"
    return f"{label}\\n{tier_label}\\n{count} refs"


def _workflow_availability(base_df, steps, prefix):
    return {
        f"{prefix}_{step['key'].upper()}": _availability(
            _apply_step_filters(base_df, step)
        )
        for step in steps
    }


def _instrument_availability(base_df):
    return {
        f"INST_{key.upper()}": _availability(_filter_instrument(base_df, info["kw"]))
        for key, info in INSTRUMENTS.items()
    }


def _node_style(active=False, auxiliary=False, availability=None):
    style = "filled"
    if active:
        style += ",bold"
    if auxiliary:
        style += ",dashed"

    if availability:
        tier = availability.get("tier")
        if tier in _TIER_NODE_STYLES:
            fill, border, text = _TIER_NODE_STYLES[tier]
        else:
            fill, border, text = _NO_REF_FILL, _NO_REF_BORDER, _NO_REF_TEXT
    elif active:
        fill, border, text = _ACT_FILL, _ACT_BORDER, _ACT_TEXT
    elif auxiliary:
        fill, border, text = _AUX_FILL, _AUX_BORDER, "#665c00"
    else:
        fill, border, text = _DIM_FILL, _DIM_BORDER, _DIM_TEXT

    penwidth = 3.0 if active else 1.4 if availability else 1.0
    return style, fill, border, text, penwidth


def _n(nid, label, active=False, auxiliary=False, availability=None):
    """Generate a DOT node."""
    style, fill, border, text, penwidth = _node_style(
        active=active, auxiliary=auxiliary, availability=availability
    )
    label = _availability_label(label, availability)
    fontsize = 10 if auxiliary else 11
    return (f'    {nid} [label="{label}", style="{style}", '
            f'fillcolor="{fill}", color="{border}", '
            f'fontcolor="{text}", penwidth={penwidth}, fontsize={fontsize}];')


def _e(src, dst, active=False, auxiliary=False, tier=None):
    """Generate a DOT edge."""
    color = TIER_COLORS.get(tier, _ACT_BORDER)
    if active:
        return f'    {src} -> {dst} [color="{color}", penwidth=2.0];'
    elif auxiliary:
        return f'    {src} -> {dst} [color="{_AUX_BORDER}", penwidth=0.8, style=dashed];'
    else:
        return f'    {src} -> {dst} [color="{_DIM_BORDER}", penwidth=0.8];'


def build_graphviz(domain=None, matrix_key=None, core_step_key=None,
                   aux_step_key=None, instrument_key=None,
                   availability=None):
    """Build a Graphviz DOT string showing the linear workflow with auxiliary branches."""
    availability = availability or {}

    lines = [
        "digraph Workflow {",
        '    rankdir=TB;',
        '    bgcolor="transparent";',
        '    node [shape=box, style="filled,rounded", fontname="Helvetica", fontsize=11, margin="0.15,0.08"];',
        '    edge [arrowsize=0.7];',
        '    splines=ortho;',
        "",
    ]

    # ── Problem Formulation (always shown) ──────────────────
    lines.append(_n("PF", "📋 Problem Formulation", active=True))
    lines.append("")

    # ── Domain branch ───────────────────────────────────────
    for dk, lab in [("Monitoring", "🔬 Monitoring"), ("Toxicology", "🧫 Toxicology"), ("Risk Assessment", "⚖️ Risk Assessment")]:
        nid = dk.upper().replace(" ", "_")
        act = (domain == dk)
        lines.append(_n(nid, lab, active=act))
        lines.append(_e("PF", nid, active=act))
    lines.append("")

    # ── Build the selected domain's workflow ────────────────
    if domain == "Monitoring":
        core_steps = MONITORING_CORE
        aux_steps = MONITORING_AUXILIARY
        parent = "MONITORING"

        # Matrix node
        if matrix_key and matrix_key in MATRICES:
            mv = MATRICES[matrix_key]
            mat_id = f"MAT_{matrix_key.upper()}"
            lines.append(_n(mat_id, f'{mv["icon"]} {mv["label"]}', active=True))
            lines.append(_e(parent, mat_id, active=True))
            chain_parent = mat_id
        else:
            chain_parent = parent

        # Linear core chain
        prev = chain_parent
        for s in core_steps:
            sid = f"CORE_{s['key'].upper()}"
            node_availability = availability.get(sid)
            act = (core_step_key == s["key"])
            lines.append(
                _n(
                    sid,
                    f'{s["icon"]} {s["label"]}',
                    active=act,
                    availability=node_availability,
                )
            )
            lines.append(
                _e(prev, sid, active=act, tier=node_availability.get("tier") if node_availability else None)
            )
            prev = sid

            # Instrument sub-nodes under Analysis
            if s.get("has_instruments") and core_step_key == "analysis":
                lines.append("")
                for ik, iv in INSTRUMENTS.items():
                    iid = f"INST_{ik.upper()}"
                    iact = (instrument_key == ik)
                    node_availability = availability.get(iid)
                    lines.append(
                        _n(
                            iid,
                            iv["label"],
                            active=iact,
                            availability=node_availability,
                        )
                    )
                    lines.append(
                        _e(
                            sid,
                            iid,
                            active=iact,
                            tier=node_availability.get("tier") if node_availability else None,
                        )
                    )

        # Auxiliary branches (off the side of the chain)
        # Attach them to the chain parent (matrix node) with dashed edges
        lines.append("")
        lines.append("    // Auxiliary supports")
        aux_anchor = chain_parent
        for a in aux_steps:
            aid = f"AUX_{a['key'].upper()}"
            aact = (aux_step_key == a["key"])
            node_availability = availability.get(aid)
            lines.append(
                _n(
                    aid,
                    f'{a["icon"]} {a["label"]}',
                    active=aact,
                    auxiliary=True,
                    availability=node_availability,
                )
            )
            lines.append(
                _e(
                    aux_anchor,
                    aid,
                    active=aact,
                    auxiliary=(not aact),
                    tier=node_availability.get("tier") if node_availability else None,
                )
            )

        # Force auxiliary nodes to same rank (horizontal cluster)
        aux_ids = [f"AUX_{a['key'].upper()}" for a in aux_steps]
        lines.append(f'    {{ rank=same; {"; ".join(aux_ids)} }}')

    elif domain == "Toxicology":
        core_steps = TOX_CORE
        aux_steps = TOX_AUXILIARY
        parent = "TOXICOLOGY"

        prev = parent
        for s in core_steps:
            sid = f"CORE_{s['key'].upper()}"
            act = (core_step_key == s["key"])
            node_availability = availability.get(sid)
            lines.append(
                _n(
                    sid,
                    f'{s["icon"]} {s["label"]}',
                    active=act,
                    availability=node_availability,
                )
            )
            lines.append(
                _e(prev, sid, active=act, tier=node_availability.get("tier") if node_availability else None)
            )
            prev = sid

        lines.append("")
        lines.append("    // Auxiliary supports")
        for a in aux_steps:
            aid = f"AUX_{a['key'].upper()}"
            aact = (aux_step_key == a["key"])
            node_availability = availability.get(aid)
            lines.append(
                _n(
                    aid,
                    f'{a["icon"]} {a["label"]}',
                    active=aact,
                    auxiliary=True,
                    availability=node_availability,
                )
            )
            lines.append(
                _e(
                    parent,
                    aid,
                    active=aact,
                    auxiliary=(not aact),
                    tier=node_availability.get("tier") if node_availability else None,
                )
            )

        aux_ids = [f"AUX_{a['key'].upper()}" for a in aux_steps]
        lines.append(f'    {{ rank=same; {"; ".join(aux_ids)} }}')

    elif domain == "Risk Assessment":
        core_steps = RA_CORE
        aux_steps = RA_AUXILIARY
        parent = "RISK_ASSESSMENT"

        prev = parent
        for s in core_steps:
            sid = f"CORE_{s['key'].upper()}"
            act = (core_step_key == s["key"])
            node_availability = availability.get(sid)
            lines.append(
                _n(
                    sid,
                    f'{s["icon"]} {s["label"]}',
                    active=act,
                    availability=node_availability,
                )
            )
            lines.append(
                _e(prev, sid, active=act, tier=node_availability.get("tier") if node_availability else None)
            )
            prev = sid

        for a in aux_steps:
            aid = f"AUX_{a['key'].upper()}"
            aact = (aux_step_key == a["key"])
            node_availability = availability.get(aid)
            lines.append(
                _n(
                    aid,
                    f'{a["icon"]} {a["label"]}',
                    active=aact,
                    auxiliary=True,
                    availability=node_availability,
                )
            )
            lines.append(
                _e(
                    parent,
                    aid,
                    active=aact,
                    auxiliary=(not aact),
                    tier=node_availability.get("tier") if node_availability else None,
                )
            )

    lines.append("}")
    return "\n".join(lines)


# ── REFERENCE DISPLAY ───────────────────────────────────────

def _display_compact_results(df, gap_note=None, tier_expanders=True):
    df_sorted = _sort_tier(df)

    if len(df_sorted) == 0:
        st.info("No references found for this path.")
        if gap_note:
            st.error(gap_note)
        return

    if gap_note:
        st.warning(gap_note)

    st.caption(f"📚 {len(df_sorted)} references")

    for tier_num in [1, 2, 3, 4]:
        tier_df = df_sorted[df_sorted["tier_num"] == tier_num]
        if len(tier_df) == 0:
            continue

        icon = TIER_ICONS.get(tier_num, "⚪")
        color = TIER_COLORS.get(tier_num, "#666")
        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")

        if tier_expanders:
            tier_container = st.expander(
                f"{label} ({len(tier_df)})", expanded=(tier_num <= 2)
            )
        else:
            st.markdown(f"**{label} ({len(tier_df)})**")
            tier_container = st.container()

        with tier_container:
            for _, row in tier_df.iterrows():
                cite = row.get(_find_col(df, ["Short Citation"]) or "", "?")
                year = row.get(_find_col(df, ["Year"]) or "", "")
                dtype = row.get(_find_col(df, ["Document Type"]) or "", "")
                notes = row.get(_find_col(df, ["Key Notes"]) or "", "")
                doi = row.get(_find_col(df, ["DOI/URL", "DOI"]) or "", "")

                cite = "" if pd.isna(cite) else str(cite)
                year = "" if pd.isna(year) else str(year).replace(".0", "")
                dtype = "" if pd.isna(dtype) else str(dtype)
                notes = "" if pd.isna(notes) else str(notes)
                doi = "" if pd.isna(doi) or str(doi).strip().lower() in ["nan", ""] else str(doi)
                doi_html = f" · <a href='{doi}'>link</a>" if doi else ""

                st.markdown(
                    f"<div style='border-left:3px solid {color}; padding:4px 8px; "
                    f"margin-bottom:4px; font-size:0.9em;'>"
                    f"<strong>{icon} {cite}</strong> ({year}) "
                    f"<span style='color:{color};'>— {dtype}</span>{doi_html}<br/>"
                    f"<span style='color:#555; font-size:0.85em;'>"
                    f"{notes[:200]}{'...' if len(notes) > 200 else ''}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    csv = df_sorted.to_csv(index=False)
    st.download_button(
        "📥 Export", csv, "filtered_references.csv", "text/csv",
        key=f"tree_export_{hash(tuple(df_sorted.index.tolist()))}",
    )


# ── MAIN RENDER ─────────────────────────────────────────────

def render_decision_tree(df, tree=None):
    """Render the workflow tree with separate core and auxiliary results."""
    st.markdown("### 🌳 Study Design Workflow")
    st.markdown(
        "Follow the linear workflow below. **Core steps** (solid lines) proceed sequentially. "
        "**Auxiliary supports** (dashed lines) apply across the workflow."
    )

    col_tree, col_results = st.columns([1, 1])

    matrix_key = None
    instrument_key = None
    core_step_key = None
    aux_step_key = None
    core_label = ""
    aux_label = ""
    core_result_df = pd.DataFrame()
    aux_result_df = pd.DataFrame()
    core_gap_note = None
    availability = {}

    with col_tree:
        domain = st.radio(
            "**1. Study Type**",
            ["Monitoring", "Toxicology", "Risk Assessment"],
            horizontal=True,
            key="tree_domain",
        )

        if domain == "Monitoring":
            df_domain = _filter_domain(df, "Monitoring")
            matrix_options = {
                key: f'{value["icon"]} {value["label"]}'
                for key, value in MATRICES.items()
            }
            matrix_key = st.selectbox(
                "**2. Matrix**",
                list(matrix_options.keys()),
                format_func=lambda key: matrix_options[key],
                key="tree_matrix",
            )
            matrix_info = MATRICES[matrix_key]
            context_df = _filter_matrix(df_domain, matrix_info["kw"])
            core_gap_note = matrix_info.get("gap")

            st.markdown("**3. Workflow Step**")
            core_col, aux_col = st.columns(2)
            with core_col:
                core_options = {
                    step["key"]: f'{step["icon"]} {step["label"]}'
                    for step in MONITORING_CORE
                }
                core_step_key = st.radio(
                    "Core Workflow",
                    list(core_options.keys()),
                    format_func=lambda key: core_options[key],
                    key="tree_core_step",
                )
            with aux_col:
                aux_options = {
                    step["key"]: f'{step["icon"]} {step["label"]}'
                    for step in MONITORING_AUXILIARY
                }
                aux_step_key = st.radio(
                    "Auxiliary Supports",
                    list(aux_options.keys()),
                    format_func=lambda key: aux_options[key],
                    key="tree_aux_step",
                )

            core_info = next(
                step for step in MONITORING_CORE if step["key"] == core_step_key
            )
            aux_info = next(
                step for step in MONITORING_AUXILIARY if step["key"] == aux_step_key
            )
            core_label = f'{core_info["icon"]} {core_info["label"]}'
            aux_label = f'{aux_info["icon"]} {aux_info["label"]}'

            if core_info.get("has_instruments"):
                instrument_options = {"all": "📋 All Techniques"} | {
                    key: value["label"] for key, value in INSTRUMENTS.items()
                }
                instrument_key = st.selectbox(
                    "Analytical technique",
                    list(instrument_options.keys()),
                    format_func=lambda key: instrument_options[key],
                    key="tree_instrument",
                )
                if instrument_key == "all":
                    core_result_df = _filter_column(context_df, core_info["column"])
                    instrument_key = None
                else:
                    core_result_df = _filter_instrument(
                        context_df, INSTRUMENTS[instrument_key]["kw"]
                    )
            else:
                core_result_df = _apply_step_filters(context_df, core_info)
            aux_result_df = _apply_step_filters(context_df, aux_info)

            availability.update(
                _workflow_availability(context_df, MONITORING_CORE, "CORE")
            )
            availability.update(
                _workflow_availability(context_df, MONITORING_AUXILIARY, "AUX")
            )
            availability.update(_instrument_availability(context_df))

        elif domain == "Toxicology":
            context_df = _filter_domain(df, "Toxicology")
            core_gap_note = (
                "⚠️ No MP-specific test guidelines. OECD TGs applicable "
                "but not MP-validated."
            )

            st.markdown("**2. Workflow Step**")
            core_col, aux_col = st.columns(2)
            with core_col:
                core_options = {
                    step["key"]: f'{step["icon"]} {step["label"]}'
                    for step in TOX_CORE
                }
                core_step_key = st.radio(
                    "Core Workflow",
                    list(core_options.keys()),
                    format_func=lambda key: core_options[key],
                    key="tree_tox_core",
                )
            with aux_col:
                aux_options = {
                    step["key"]: f'{step["icon"]} {step["label"]}'
                    for step in TOX_AUXILIARY
                }
                aux_step_key = st.radio(
                    "Auxiliary Supports",
                    list(aux_options.keys()),
                    format_func=lambda key: aux_options[key],
                    key="tree_tox_aux",
                )

            core_info = next(step for step in TOX_CORE if step["key"] == core_step_key)
            aux_info = next(
                step for step in TOX_AUXILIARY if step["key"] == aux_step_key
            )
            core_label = f'{core_info["icon"]} {core_info["label"]}'
            aux_label = f'{aux_info["icon"]} {aux_info["label"]}'

            core_result_df = _apply_step_filters(context_df, core_info)
            if core_info.get("has_test_systems"):
                system_options = {"all": "📋 All Systems"} | {
                    key: value["label"] for key, value in TEST_SYSTEMS.items()
                }
                system_key = st.selectbox(
                    "Test system",
                    list(system_options.keys()),
                    format_func=lambda key: system_options[key],
                    key="tree_test_sys",
                )
                if system_key != "all":
                    core_result_df = _filter_keywords(
                        core_result_df, TEST_SYSTEMS[system_key]["keywords"]
                    )
            aux_result_df = _apply_step_filters(context_df, aux_info)

            availability.update(_workflow_availability(context_df, TOX_CORE, "CORE"))
            availability.update(
                _workflow_availability(context_df, TOX_AUXILIARY, "AUX")
            )

        elif domain == "Risk Assessment":
            context_df = df
            st.markdown("**2. Component**")
            core_col, aux_col = st.columns(2)
            with core_col:
                core_options = {
                    step["key"]: f'{step["icon"]} {step["label"]}'
                    for step in RA_CORE
                }
                core_step_key = st.radio(
                    "Core Workflow",
                    list(core_options.keys()),
                    format_func=lambda key: core_options[key],
                    key="tree_ra_step",
                )
            with aux_col:
                aux_options = {
                    step["key"]: f'{step["icon"]} {step["label"]}'
                    for step in RA_AUXILIARY
                }
                aux_step_key = st.radio(
                    "Auxiliary Supports",
                    list(aux_options.keys()),
                    format_func=lambda key: aux_options[key],
                    key="tree_ra_aux",
                )

            core_info = next(step for step in RA_CORE if step["key"] == core_step_key)
            aux_info = next(
                step for step in RA_AUXILIARY if step["key"] == aux_step_key
            )
            core_label = f'{core_info["icon"]} {core_info["label"]}'
            aux_label = f'{aux_info["icon"]} {aux_info["label"]}'
            core_result_df = _apply_step_filters(context_df, core_info)
            aux_result_df = _apply_step_filters(context_df, aux_info)

            availability.update(_workflow_availability(context_df, RA_CORE, "CORE"))
            availability.update(_workflow_availability(context_df, RA_AUXILIARY, "AUX"))

        st.markdown("---")
        dot = build_graphviz(
            domain=domain,
            matrix_key=matrix_key,
            core_step_key=core_step_key,
            aux_step_key=aux_step_key,
            instrument_key=instrument_key,
            availability=availability,
        )
        st.graphviz_chart(dot, width="stretch")

        st.caption(
            "Node color shows best available tier: Tier 1 green, Tier 2 blue, "
            "Tier 3 gold, Tier 4 gray; red means no matching references."
        )

    with col_results:
        path_parts = ["📋 Problem Formulation", domain]
        if matrix_key:
            matrix_info = MATRICES[matrix_key]
            path_parts.append(f'{matrix_info["icon"]} {matrix_info["label"]}')
        if core_label:
            path_parts.append(core_label)
        if instrument_key and instrument_key in INSTRUMENTS:
            path_parts.append(INSTRUMENTS[instrument_key]["label"])

        st.markdown(f"**📍 Core Path:** {' → '.join(path_parts)}")
        if aux_label:
            st.markdown(f"**🔧 Auxiliary Support:** {aux_label}")
        st.markdown("---")

        with st.expander(
            f"Core Workflow references: {core_label} ({len(core_result_df)})",
            expanded=True,
        ):
            _display_compact_results(
                core_result_df,
                gap_note=core_gap_note,
                tier_expanders=False,
            )

        with st.expander(
            f"Auxiliary Support references: {aux_label} ({len(aux_result_df)})",
            expanded=False,
        ):
            _display_compact_results(aux_result_df, tier_expanders=False)
