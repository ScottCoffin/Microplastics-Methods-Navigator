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
        from tabs.visual_tree_tab import render_decision_tree
        render_decision_tree(df, tree)
"""

import streamlit as st
import pandas as pd
import re
import html
import graphviz
import os
import shutil
from urllib.parse import urlencode
from streamlit.runtime.scriptrunner import get_script_run_ctx


# ── WORKFLOW STRUCTURES ─────────────────────────────────────

# Monitoring: linear core + auxiliary
MONITORING_CORE = [
    {"key": "sampling",    "label": "Sampling",    "icon": "📍", "column": "Sampling (Field Methods)"},
    {"key": "extraction",  "label": "Extraction",  "icon": "🧪", "column": "Sample Processing / Extraction"},
    {"key": "subsampling", "label": "Sub-sampling", "icon": "🔢", "column": "Sub-sampling"},
    {"key": "analysis",    "label": "Analysis",    "icon": "🔎", "column": "Analytical Methods (General)",
     "has_instruments": True},
    {"key": "data_stats",  "label": "Data Analysis & Statistics", "icon": "📊", "column": "Data Analysis & Statistics"},
    {"key": "reporting",   "label": "Reporting & Data Deposition", "icon": "📝", "column": "Reporting & Harmonization"},
]

MONITORING_AUXILIARY = [
    {"key": "ref_materials", "label": "Material Standards",             "icon": "📦",
     "columns": ["Material Standards - materials", "Material Standards - protocol"],
     "has_subtypes": True,
     "subtypes": {
         "materials": {"label": "Materials",            "column": "Material Standards - materials"},
         "protocols": {"label": "Generation Protocols", "column": "Material Standards - protocol"},
     }},
    {"key": "blanks",        "label": "Blanks & Contamination Control", "icon": "🧹",
     "column": "Blanks & Contamination Control"},
]

# Toxicology: linear core + auxiliary
TOX_CORE = [
    {"key": "particle_char",   "label": "Particle Characterization", "icon": "🔬",
     "column": "Toxicology: Study Design & Dosimetry"},
    {"key": "dosimetry",       "label": "Dosimetry",                 "icon": "💊",
     "column": "Toxicology: Study Design & Dosimetry"},
    {"key": "effects",         "label": "Effects Testing",           "icon": "🧬",
     "column": "Toxicology: Effects Testing Methods", "has_test_systems": True},
    {"key": "tox_reporting",   "label": "Reporting",                 "icon": "📝",
     "column": "Toxicology: Reporting & Harmonization"},
    {"key": "data_repository", "label": "Data Repository",           "icon": "🗃️",
     "column": "Toxicology: Databases & Data Sharing"},
]

TOX_AUXILIARY = [
    {"key": "ref_materials", "label": "Material Standards",             "icon": "📦",
     "columns": ["Material Standards - materials", "Material Standards - protocol"],
     "has_subtypes": True,
     "subtypes": {
         "materials": {"label": "Materials",            "column": "Material Standards - materials"},
         "protocols": {"label": "Generation Protocols", "column": "Material Standards - protocol"},
     }},
    {"key": "quality",       "label": "Study Quality & Scoring",        "icon": "✅",
     "column": "Toxicology: Study Design & Dosimetry",
     "keywords": "quality;QA;scoring;criteria;checklist;ToMEx"},
]

# Risk Assessment: linear
RA_CORE = [
    {"key": "frameworks", "label": "RA Frameworks",        "icon": "🏗️",
     "column": "Risk Assessment / Risk Char.", "primary_focus": "Risk Assessment"},
    {"key": "hazard",     "label": "Hazard Identification", "icon": "⚠️",
     "column": "Risk Assessment / Risk Char.",
     "keywords": "hazard identification;hazard characterization;toxicity database;ToMEx;SSD;species sensitivity;adverse effect;dose-response"},
    {"key": "exposure",   "label": "Exposure Assessment",   "icon": "📏",
     "column": "Risk Assessment / Risk Char.",
     "keywords": "exposure assessment;exposure scenario;PBK;PBPK;biokinetic;dietary exposure;inhalation exposure;internal dose;external dose"},
    {"key": "pbpk",       "label": "PBPK Modelling",         "icon": "🧮",
     "primary_focus": "PBPK Modelling", "receptors": ["human_health"]},
    {"key": "risk_char",  "label": "Risk Characterization", "icon": "📊",
     "column": "Risk Assessment / Risk Char.",
     "keywords": "risk quotient;threshold;management;stochastic;TRL"},
]

RA_AUXILIARY = []

# Matrices
MATRICES = {
    "drinking_water": {"label": "Drinking Water",  "icon": "🚰", "kw": "Drinking Water"},
    "surface_water":  {"label": "Surface Water",   "icon": "🌊", "kw": "Surface Water"},
    "wastewater":     {"label": "Wastewater",      "icon": "🏭", "kw": "Wastewater"},
    "biosolids":      {"label": "Biosolids / Sludge", "icon": "♻️", "kw": "Biosolids"},
    "sediment":       {"label": "Sediment",        "icon": "🪨", "kw": "Sediment"},
    "biota":          {"label": "Biota / Tissue",  "icon": "🐟", "kw": "Biota"},
    "air":            {"label": "Air",             "icon": "💨", "kw": "Air"},
    "food":           {"label": "Food / Dietary",  "icon": "🍽️", "kw": "Food"},
    "human_tissue":   {"label": "Human Tissue",    "icon": "🩸", "kw": "Human"},
    "soil":           {"label": "Soil",            "icon": "🌱", "kw": "Soil"},
}

RECEPTORS = {
    "human_health": {"label": "Human Health", "icon": "🧍", "kw": "Human Health"},
    "ecotoxicology": {"label": "Ecotoxicology", "icon": "🐟", "kw": "Ecotoxicology"},
    "in_vitro": {"label": "In Vitro", "icon": "🧫", "kw": "In Vitro"},
}

# Instruments (sub-branch of Analysis)
INSTRUMENTS = {
    "ftir":      {"label": "µFTIR / FPA-FTIR", "kw": "µFTIR"},
    "ldir":      {"label": "LDIR",              "kw": "LDIR"},
    "raman":     {"label": "µRaman",            "kw": "µRaman"},
    "pyrolysis": {"label": "Py-GC-MS",          "kw": "Py-GC-MS"},
    "ted":       {"label": "TED-GC-MS",         "kw": "TED-GC-MS"},
    "nile_red":  {"label": "Nile Red",           "kw": "Nile Red"},
    "imaging":   {"label": "Visual / SEM / Imaging", "kw": "Imaging;Visual;SEM"},
}

PARTICLE_TYPES = {
    "nanoplastics": {"label": "Nanoplastics", "kw": "Nanoplastics"},
    "microfibers": {"label": "Microfibers / Textiles", "kw": "Microfibers;Textiles;Textile fibers"},
    "tire_wear": {"label": "Tire Wear Particles", "kw": "Tire wear;Tire Wear Particles;TWP"},
    "ermp": {"label": "Environmentally Realistic Mixtures", "kw": "Environmentally Realistic Mixtures;ERMP"},
    "microbeads": {"label": "Microbeads", "kw": "Microbeads"},
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

# Matrix-conditional tier overrides.
# Format: {citation_substring: {matrix_keyword: tier, "default": tier}}
# Used when a reference carries a different authority level depending on the
# selected matrix (e.g., Sherrod et al. 2024 One4All is mandated by CA for
# drinking water [Tier 1] but is voluntary / best-practice for other matrices [Tier 3]).
MATRIX_TIER_OVERRIDES: dict[str, dict] = {
    "Sherrod": {"Drinking Water": 1, "default": 3},
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


def _filter_target_receptor(df, kw):
    col = _find_col(df, ["Target Receptor(s)", "Target Receptors"])
    if col is None:
        return df
    s = df[col].astype(str)
    return df[
        s.str.contains(kw, case=False, na=False)
        | s.str.contains(r"Cross[- ]?cutting|Both", case=False, na=False, regex=True)
        | s.isin(["", "nan", "None"])  # <-- pass through untagged entries
        | df[col].isna()               # <-- pass through NaN
    ]


def _filter_column(df, col_name):
    col = _find_col(df, [col_name])
    if col is None:
        return df
    return df[df[col].notna() & (df[col] != "") & (df[col] != 0)]


def _filter_primary_focus(df, value):
    col = _find_col(df, ["Primary Focus"])
    if col is None:
        return df
    return df[df[col].astype(str).str.contains(value, case=False, na=False)]


def _filter_instrument(df, kw):
    col = _find_col(df, ["Instrumentation Tags"])
    if col is None:
        return df
    mask = pd.Series(False, index=df.index)
    for term in str(kw).split(";"):
        term = term.strip()
        if term:
            mask = mask | df[col].astype(str).str.contains(term, case=False, na=False)
    return df[mask]


def _filter_particle_type(df, kw):
    col = _find_col(df, ["Particle/Polymer Type Tags"])
    if col is None:
        return df
    mask = pd.Series(False, index=df.index)
    for term in str(kw).split(";"):
        term = term.strip()
        if term:
            mask = mask | df[col].astype(str).str.contains(term, case=False, na=False)
    return df[mask]


def _filter_particle_types(df, selected_keys):
    if not selected_keys:
        return df
    mask = pd.Series(False, index=df.index)
    for key in selected_keys:
        info = PARTICLE_TYPES.get(key)
        if info:
            mask = mask | df.index.isin(_filter_particle_type(df, info["kw"]).index)
    return df[mask]


def _filter_problem_formulation(df):
    definition_col = _find_col(df, ["Definitions & Terminology"])
    problem_col = _find_col(df, ["Problem Formulation"])
    topic_mask = pd.Series(False, index=df.index)
    for col in [definition_col, problem_col]:
        if col:
            topic_mask = topic_mask | (
                df[col].notna() & (df[col] != "") & (df[col] != 0)
            )
    return df[topic_mask]


def _filter_doc_type(df, dt):
    col = _find_col(df, ["Document Type"])
    if col is None:
        return df
    return df[df[col].astype(str).str.contains(dt, case=False, na=False)]


def _doc_type_options(df):
    col = _find_col(df, ["Document Type"])
    if col is None:
        return []
    values = (
        df[col]
        .dropna()
        .astype(str)
        .map(str.strip)
    )
    return sorted(value for value in values.unique() if value and value.lower() != "nan")


def _filter_keywords(df, kws):
    col = _find_col(df, ["Key Notes"])
    if col is None:
        return df
    mask = pd.Series(False, index=df.index)
    for kw in kws.split(";"):
        mask = mask | df[col].astype(str).str.contains(kw.strip(), case=False, na=False)
    return df[mask]


def _apply_matrix_tier_overrides(df, matrix_kw):
    """Adjust tier_num for references with matrix-conditional authority levels."""
    if "tier_num" not in df.columns:
        return df
    citation_col = _find_col(df, ["Short Citation"])
    if citation_col is None:
        return df
    df = df.copy()
    for fragment, overrides in MATRIX_TIER_OVERRIDES.items():
        mask = df[citation_col].astype(str).str.contains(fragment, case=False, na=False)
        if not mask.any():
            continue
        if matrix_kw and matrix_kw in overrides:
            df.loc[mask, "tier_num"] = overrides[matrix_kw]
        elif "default" in overrides:
            df.loc[mask, "tier_num"] = overrides["default"]
    return df


def _filter_any_columns(df, col_names):
    """Return rows that have a non-empty score in ANY of the listed columns (OR logic)."""
    mask = pd.Series(False, index=df.index)
    for col_name in col_names:
        col = _find_col(df, [col_name])
        if col is not None:
            mask = mask | (df[col].notna() & (df[col] != "") & (df[col] != 0))
    return df[mask]


def _apply_step_filters(df, step_info):
    """Apply all filters defined in a step dict."""
    result = df
    if "doc_type" in step_info:
        result = _filter_doc_type(result, step_info["doc_type"])

    has_columns = "columns" in step_info
    has_column = "column" in step_info
    has_focus = "primary_focus" in step_info
    has_keywords = "keywords" in step_info

    if has_focus and (has_column or has_columns or has_keywords):
        matched_indexes = set(_filter_primary_focus(result, step_info["primary_focus"]).index)
        if has_column:
            matched_indexes.update(_filter_column(result, step_info["column"]).index)
        if has_columns:
            matched_indexes.update(_filter_any_columns(result, step_info["columns"]).index)
        if has_keywords:
            matched_indexes.update(_filter_keywords(result, step_info["keywords"]).index)
        return result.loc[result.index.isin(matched_indexes)]

    if has_column:
        result = _filter_column(result, step_info["column"])
    if has_columns:
        result = _filter_any_columns(result, step_info["columns"])
    if has_focus:
        result = _filter_primary_focus(result, step_info["primary_focus"])
    if has_keywords:
        result = _filter_keywords(result, step_info["keywords"])
    return result


def _sort_tier(df):
    yr = _find_col(df, ["Year"])
    if "tier_num" in df.columns:
        cols = ["tier_num"] + ([yr] if yr else [])
        asc = [True] + ([False] if yr else [])
        return df.sort_values(cols, ascending=asc)
    return df


def _year_series(df):
    year_col = _find_col(df, ["Year"])
    if year_col is None or year_col not in df.columns:
        return pd.Series(dtype="float64")
    return pd.to_numeric(df[year_col], errors="coerce")


def _tier_series(df):
    if "tier_num" not in df.columns:
        return pd.Series(dtype="float64")
    return pd.to_numeric(df["tier_num"], errors="coerce")


def _format_tier_counts(tier_counts):
    parts = [
        f"Tier {tier}: {tier_counts.get(tier, 0)}"
        for tier in [1, 2, 3, 4]
        if tier_counts.get(tier, 0) > 0
    ]
    return ", ".join(parts) if parts else "no tiered references"


def _state_choice(key, options, default_index=0):
    if not options:
        return None
    value = st.session_state.get(key)
    if value in options:
        return value
    fallback = options[min(default_index, len(options) - 1)]
    st.session_state[key] = fallback
    return fallback


def _ra_core_for_receptor(receptor_key):
    if not receptor_key:
        return [step for step in RA_CORE if "receptors" not in step]
    return [
        step
        for step in RA_CORE
        if "receptors" not in step or receptor_key in step["receptors"]
    ]


def _query_param_value(key):
    if get_script_run_ctx(suppress_warning=True) is None:
        return None
    value = st.query_params.get(key)
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _sync_tree_query_params():
    if get_script_run_ctx(suppress_warning=True) is None:
        return
    valid_values = {
        "tree_domain": ["Monitoring", "Toxicology", "Risk Assessment"],
        "tree_matrix": list(MATRICES.keys()),
        "tree_particle_type": list(PARTICLE_TYPES.keys()),
        "tree_receptor": list(RECEPTORS.keys()),
        "tree_problem": ["1"],
        "tree_core_step": [step["key"] for step in MONITORING_CORE],
        "tree_aux_step": [step["key"] for step in MONITORING_AUXILIARY],
        "tree_tox_core": [step["key"] for step in TOX_CORE],
        "tree_tox_aux": [step["key"] for step in TOX_AUXILIARY],
        "tree_ra_step": [step["key"] for step in RA_CORE],
        "tree_ra_aux": [step["key"] for step in RA_AUXILIARY],
        "tree_instrument": ["all", *INSTRUMENTS.keys()],
        "tree_test_sys": ["all", *TEST_SYSTEMS.keys()],
        "tree_aux_subtype": ["all", "materials", "protocols"],
    }
    last_synced = st.session_state.setdefault("_tree_synced_query_params", {})
    if _query_param_value("tree_problem") is None and last_synced.get("tree_problem") == "1":
        st.session_state.pop("tree_problem", None)
        last_synced.pop("tree_problem", None)
    for key, allowed in valid_values.items():
        value = _query_param_value(key)
        if value in allowed and last_synced.get(key) != value:
            st.session_state[key] = value
            last_synced[key] = value


def _tree_query_url(**updates):
    params = (
        dict(st.query_params)
        if get_script_run_ctx(suppress_warning=True) is not None
        else {}
    )
    for key, value in updates.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value
    return "?" + urlencode(params)


def _tree_query_values(key):
    if get_script_run_ctx(suppress_warning=True) is None:
        return []
    value = st.query_params.get_all(key)
    if value:
        return value
    single_value = st.query_params.get(key)
    if isinstance(single_value, list):
        return single_value
    return [single_value] if single_value else []


def _reference_context_messages(df):
    """Generate rules-based context from the selected Crosswalk rows."""
    if len(df) == 0:
        return []

    tier_values = _tier_series(df)
    valid_tier_mask = tier_values.notna()
    if not valid_tier_mask.any():
        return []

    tiers = tier_values.loc[valid_tier_mask].astype(int)
    best_tier = int(tiers.min())
    tier_counts = tiers.value_counts().sort_index().to_dict()
    best_tier_count = tier_counts.get(best_tier, 0)
    messages = []

    if best_tier > 2:
        messages.append(
            (
                "warning",
                f"No Tier 1/2 references match this selected path. "
                f"Highest available tier is Tier {best_tier} "
                f"({best_tier_count} reference"
                f"{'' if best_tier_count == 1 else 's'}); review all "
                f"Tier {best_tier} candidates rather than treating any "
                f"single citation as preferred.",
            )
        )

    messages.append(
        (
            "info",
            f"Current Crosswalk coverage for this path: "
            f"{_format_tier_counts(tier_counts)}.",
        )
    )

    years = _year_series(df)
    if years.empty:
        return messages

    best_mask = valid_tier_mask & (tier_values.astype("Int64") == best_tier)
    best_years = years.loc[best_mask].dropna()
    if best_years.empty:
        return messages

    newest_best_year = int(best_years.max())
    if newest_best_year < 2021:
        lower_mask = (
            valid_tier_mask
            & (tier_values > best_tier)
            & (years > newest_best_year)
        )
        lower_newer_years = years.loc[lower_mask].dropna()
        lower_tier_note = ""
        if not lower_newer_years.empty:
            lower_tier_note = (
                f" Newer lower-tier references are present through "
                f"{int(lower_newer_years.max())}."
            )
        messages.append(
            (
                "warning",
                f"Newest Tier {best_tier} reference is from {newest_best_year}. "
                f"Use caution and consider whether newer documents in lower "
                f"tiers update the approach.{lower_tier_note}",
            )
        )

    return messages


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


def _subtype_availability(base_df, step):
    """Compute availability for each sub-node of a has_subtypes step."""
    if not step.get("has_subtypes"):
        return {}
    return {
        f"AUXSUB_{step['key'].upper()}_{sub_key.upper()}": _availability(
            _filter_column(base_df, sub_info["column"])
        )
        for sub_key, sub_info in step["subtypes"].items()
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


def _n(nid, label, active=False, auxiliary=False, availability=None, url=None):
    """Generate a DOT node."""
    style, fill, border, text, penwidth = _node_style(
        active=active, auxiliary=auxiliary, availability=availability
    )
    label = _availability_label(label, availability)
    fontsize = 10 if auxiliary else 11
    return (f'    {nid} [label="{label}", style="{style}", '
            f'fillcolor="{fill}", color="{border}", '
            f'fontcolor="{text}", penwidth={penwidth}, '
            f'fontsize={fontsize}];')


def _e(src, dst, active=False, auxiliary=False, tier=None):
    """Generate a DOT edge."""
    color = TIER_COLORS.get(tier, _ACT_BORDER)
    if active:
        return f'    {src} -> {dst} [color="{color}", penwidth=2.0];'
    elif auxiliary:
        return f'    {src} -> {dst} [color="{_AUX_BORDER}", penwidth=0.8, style=dashed];'
    else:
        return f'    {src} -> {dst} [color="{_DIM_BORDER}", penwidth=0.8];'


def _summary_node(nid, label="..."):
    return (f'    {nid} [label="{label}", style="filled,dashed", '
            f'fillcolor="{_DIM_FILL}", color="{_DIM_BORDER}", '
            f'fontcolor="{_DIM_TEXT}", penwidth=1.0, fontsize=11];')


def build_graphviz(domain=None, matrix_key=None, receptor_key=None, core_step_key=None,
                   aux_step_key=None, instrument_key=None, aux_subtype_key=None,
                   availability=None):
    """Build a Graphviz DOT string showing the linear workflow with auxiliary branches."""
    availability = availability or {}

    lines = [
        "digraph Workflow {",
        '    rankdir=TB;',
        '    bgcolor="transparent";',
        '    size="5,8";',
        '    nodesep=0.25;',
        '    ranksep=0.35;',
        '    node [shape=box, style="filled,rounded", fontname="Helvetica", fontsize=11, margin="0.15,0.08"];',
        '    edge [arrowsize=0.7];',
        '    splines=polyline;',
        "",
    ]

    # ── Problem Formulation (always shown) ──────────────────
    pf_active = availability.get("PF", {}).get("active", False)
    lines.append(
        _n(
            "PF",
            "📋 Problem Formulation",
            active=pf_active,
            availability=availability.get("PF"),
            url=_tree_query_url(tree_problem="1"),
        )
    )
    # ── Definitions (auxiliary to Problem Formulation) ──────
    def_avail = availability.get("DEF")
    lines.append(
        _n("DEF", "📖 Definitions &\\nTerminology",
           auxiliary=True, availability=def_avail)
    )
    lines.append(_e("PF", "DEF", auxiliary=True,
                    tier=def_avail.get("tier") if def_avail else None))
    lines.append("")

    # ── Domain branch ───────────────────────────────────────
    for dk, lab in [("Monitoring", "🔬 Monitoring"), ("Toxicology", "🧫 Toxicology"), ("Risk Assessment", "⚖️ Risk Assessment")]:
        nid = dk.upper().replace(" ", "_")
        act = (domain == dk)
        lines.append(_n(nid, lab, active=act, url=_tree_query_url(tree_domain=dk, tree_problem=None)))
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
            lines.append(
                _n(
                    mat_id,
                    f'{mv["icon"]} {mv["label"]}',
                    active=True,
                    url=_tree_query_url(tree_matrix=matrix_key),
                )
            )
            lines.append(_e(parent, mat_id, active=True))
            chain_parent = mat_id
        else:
            chain_parent = parent

        collapse_monitoring_core = core_step_key == "analysis"

        # Linear core chain
        prev = chain_parent
        rendered_steps = (
            [step for step in core_steps if step["key"] == core_step_key]
            if collapse_monitoring_core
            else core_steps
        )
        if collapse_monitoring_core:
            lines.append(_summary_node("CORE_BEFORE", "..."))
            lines.append(_e(prev, "CORE_BEFORE"))
            prev = "CORE_BEFORE"

        for s in rendered_steps:
            sid = f"CORE_{s['key'].upper()}"
            node_availability = availability.get(sid)
            act = (core_step_key == s["key"])
            lines.append(
                _n(
                    sid,
                    f'{s["icon"]} {s["label"]}',
                    active=act,
                    availability=node_availability,
                    url=_tree_query_url(tree_core_step=s["key"]),
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
                            url=_tree_query_url(
                                tree_core_step="analysis",
                                tree_instrument=ik,
                            ),
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

        if collapse_monitoring_core:
            lines.append(_summary_node("CORE_AFTER", "..."))
            lines.append(_e(prev, "CORE_AFTER"))

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
                    url=_tree_query_url(tree_aux_step=a["key"]),
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
            if a.get("has_subtypes"):
                for sub_key, sub_info in a["subtypes"].items():
                    sub_id = f"AUXSUB_{a['key'].upper()}_{sub_key.upper()}"
                    sub_avail = availability.get(sub_id)
                    sub_act = (aux_subtype_key == sub_key)
                    lines.append(
                        _n(
                            sub_id,
                            sub_info["label"],
                            active=sub_act,
                            auxiliary=True,
                            availability=sub_avail,
                            url=_tree_query_url(tree_aux_step=a["key"], tree_aux_subtype=sub_key),
                        )
                    )
                    lines.append(
                        _e(aid, sub_id, active=sub_act, auxiliary=(not sub_act),
                           tier=sub_avail.get("tier") if sub_avail else None)
                    )

    elif domain == "Toxicology":
        core_steps = TOX_CORE
        aux_steps = TOX_AUXILIARY
        parent = "TOXICOLOGY"
        chain_parent = parent

        if receptor_key and receptor_key in RECEPTORS:
            rv = RECEPTORS[receptor_key]
            receptor_id = f"RECEPTOR_{receptor_key.upper()}"
            lines.append(
                _n(
                    receptor_id,
                    f'{rv["icon"]} {rv["label"]}',
                    active=True,
                    url=_tree_query_url(tree_receptor=receptor_key),
                )
            )
            lines.append(_e(parent, receptor_id, active=True))
            chain_parent = receptor_id

        prev = chain_parent
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
                    url=_tree_query_url(tree_tox_core=s["key"]),
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
                    url=_tree_query_url(tree_tox_aux=a["key"]),
                )
            )
            lines.append(
                _e(
                    chain_parent,
                    aid,
                    active=aact,
                    auxiliary=(not aact),
                    tier=node_availability.get("tier") if node_availability else None,
                )
            )
            if a.get("has_subtypes"):
                for sub_key, sub_info in a["subtypes"].items():
                    sub_id = f"AUXSUB_{a['key'].upper()}_{sub_key.upper()}"
                    sub_avail = availability.get(sub_id)
                    sub_act = (aux_subtype_key == sub_key)
                    lines.append(
                        _n(
                            sub_id,
                            sub_info["label"],
                            active=sub_act,
                            auxiliary=True,
                            availability=sub_avail,
                            url=_tree_query_url(tree_tox_aux=a["key"], tree_aux_subtype=sub_key),
                        )
                    )
                    lines.append(
                        _e(aid, sub_id, active=sub_act, auxiliary=(not sub_act),
                           tier=sub_avail.get("tier") if sub_avail else None)
                    )
        aux_ids = [f"AUX_{a['key'].upper()}" for a in aux_steps]
        if aux_ids:
            lines.append(f'    {{ rank=same; {"; ".join(aux_ids)} }}')

    elif domain == "Risk Assessment":
        core_steps = _ra_core_for_receptor(receptor_key)
        aux_steps = RA_AUXILIARY
        parent = "RISK_ASSESSMENT"
        chain_parent = parent

        if receptor_key and receptor_key in RECEPTORS:
            rv = RECEPTORS[receptor_key]
            receptor_id = f"RECEPTOR_{receptor_key.upper()}"
            lines.append(
                _n(
                    receptor_id,
                    f'{rv["icon"]} {rv["label"]}',
                    active=True,
                    url=_tree_query_url(tree_receptor=receptor_key),
                )
            )
            lines.append(_e(parent, receptor_id, active=True))
            chain_parent = receptor_id

        prev = chain_parent
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
                    url=_tree_query_url(tree_ra_step=s["key"]),
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
                    url=_tree_query_url(tree_ra_aux=a["key"]),
                )
            )
            lines.append(
                _e(
                    chain_parent,
                    aid,
                    active=aact,
                    auxiliary=(not aact),
                    tier=node_availability.get("tier") if node_availability else None,
                )
            )
        aux_ids = [f"AUX_{a['key'].upper()}" for a in aux_steps]
        if aux_ids:
            lines.append(f'    {{ rank=same; {"; ".join(aux_ids)} }}')

    lines.append("}")
    return "\n".join(lines)


def _prepare_svg_for_pan_zoom(svg):
    """Ensure the rendered SVG fills the pan/zoom container."""
    svg = re.sub(r"\s(width|height)=\"[^\"]*\"", "", svg, count=2)
    svg = re.sub(r"\sid=\"[^\"]*\"", "", svg, count=1)
    return re.sub(
        r"<svg\b",
        '<svg id="workflow-svg" width="100%" height="100%"',
        svg,
        count=1,
    )


def _zoomable_svg_html(svg, height):
    svg = _prepare_svg_for_pan_zoom(svg)
    return f"""
<!doctype html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
  <style>
    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #fafafa;
    }}
    #workflow-container {{
      width: 100%;
      height: 100%;
      border: 1px solid #ddd;
      background: #fafafa;
      box-sizing: border-box;
      overflow: hidden;
    }}
    #workflow-svg {{
      display: block;
      width: 100%;
      height: 100%;
    }}
  </style>
</head>
<body>
  <!-- diagram-height: {height}px -->
  <div id="workflow-container">
    {svg}
  </div>
  <script>
    const container = document.getElementById("workflow-container");
    const panZoom = svgPanZoom("#workflow-svg", {{
      controlIconsEnabled: true,
      fit: true,
      center: true,
      zoomScaleSensitivity: 0.3
    }});
    function refitDiagram() {{
      panZoom.resize();
      panZoom.fit();
      panZoom.center();
    }}
    window.addEventListener("resize", refitDiagram);
    if (window.ResizeObserver) {{
      new ResizeObserver(refitDiagram).observe(container);
    }}
    setTimeout(refitDiagram, 0);
  </script>
</body>
</html>
"""


def _ensure_graphviz_dot_on_path():
    if shutil.which("dot"):
        return True
    for path in [
        r"C:\Program Files\Graphviz\bin",
        r"C:\Program Files (x86)\Graphviz\bin",
    ]:
        dot_path = os.path.join(path, "dot.exe")
        if os.path.exists(dot_path):
            os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + path
            return True
    return False


@st.cache_data(show_spinner=False)
def _dot_to_svg(dot):
    return graphviz.Source(dot).pipe(format="svg").decode("utf-8")


def _render_zoomable_graphviz(dot, height):
    _ensure_graphviz_dot_on_path()
    try:
        svg = _dot_to_svg(dot)
    except graphviz.ExecutableNotFound:
        col, _ = st.columns([1, 1])
        with col:
            st.graphviz_chart(dot, use_container_width=True)
        return
    st.iframe(_zoomable_svg_html(svg, height), width="stretch", height=height)


# ── REFERENCE DISPLAY ───────────────────────────────────────

def _normalize_abstract_text(value):
    """Clean abstract text for display without modifying the source dataframe."""
    if value is None or pd.isna(value):
        return ""
    text = str(value)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s*[•●▪◦‣⁃]\s*", " ", text)
    text = re.sub(r"\s+(?:[-*])\s+", " ", text)
    text = re.sub(r"\s*\b(?:Abstract|Summary)\b\s*[:.-]?\s*", " ", text, count=1, flags=re.I)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _row_text(row, df, candidates):
    value = row.get(_find_col(df, candidates) or "", "")
    if pd.isna(value) or str(value).strip().lower() in ["nan", "none", ""]:
        return ""
    return str(value).strip()

def _compact_export_df(df):
    """Return a small, stable export table for filtered reference sets."""
    output = pd.DataFrame(index=df.index)
    column_map = {
        "Short Citation": ["Short Citation"],
        "Year": ["Year"],
        "Document Type": ["Document Type"],
        "Tier": ["Priority Tier", "Tier", "tier_num"],
        "DOI": ["DOI/URL", "DOI", "URL"],
        "Key Notes": ["Key Notes"],
    }
    for label, candidates in column_map.items():
        col = _find_col(df, candidates)
        output[label] = df[col] if col else ""
    return output.reset_index(drop=True)


def _display_compact_results(df, tier_expanders=True):
    df_sorted = _sort_tier(df)

    if len(df_sorted) == 0:
        st.info("No references found for this path.")
        return

    for level, message in _reference_context_messages(df_sorted):
        if level == "warning":
            st.warning(message)
        else:
            st.info(message)

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
                cite = _row_text(row, df, ["Short Citation"])
                year = _row_text(row, df, ["Year"]).replace(".0", "")
                dtype = _row_text(row, df, ["Document Type"])
                notes = _row_text(row, df, ["Key Notes"])
                doi = _row_text(row, df, ["DOI/URL", "DOI"])
                abstract = _row_text(row, df, ["Abstract"])
                metrics = _row_text(row, df, ["Key Metrics / Output", "Key Metrics", "Output"])
                size_range = _row_text(row, df, ["Particle Size Range"])
                scope = _row_text(row, df, ["Scope"])
                status = _row_text(row, df, ["Status"])
                cite_safe = html.escape(cite)
                year_safe = html.escape(year)
                dtype_safe = html.escape(dtype)
                notes_preview = notes[:200] + ("..." if len(notes) > 200 else "")
                notes_safe = html.escape(notes_preview)
                metrics_preview = metrics[:150] + ("..." if len(metrics) > 150 else "")
                metrics_safe = html.escape(metrics_preview)
                size_range_safe = html.escape(size_range)
                scope_safe = html.escape(scope)
                status_safe = html.escape(status)
                doi_safe = html.escape(doi, quote=True)
                doi_html = f" · <a href='{doi_safe}'>link</a>" if doi else ""
                tier_context = ""
                if tier_num <= 2:
                    if scope:
                        tier_context += f" · 🎯 {scope_safe}"
                    if status:
                        tier_context += f" · 📋 {status_safe}"
                metrics_html = (
                    f"<br/><span style='font-size:0.8em; color:#7a6b2e;'>"
                    f"📊 {metrics_safe}</span>"
                    if metrics and metrics != "0"
                    else ""
                )
                size_html = (
                    f"<br/><span style='font-size:0.8em; color:#555;'>📐 {size_range_safe}</span>"
                    if size_range and size_range not in ["0", "Not specified"]
                    else ""
                )

                st.markdown(
                    f"<div style='border-left:3px solid {color}; padding:4px 8px; "
                    f"margin-bottom:4px; font-size:0.9em;'>"
                    f"<strong>{icon} {cite_safe}</strong> ({year_safe}) "
                    f"<span style='color:{color};'>— {dtype_safe}</span>{doi_html}"
                    f"<span style='color:#555; font-size:0.8em;'>{tier_context}</span><br/>"
                    f"<span style='color:#555; font-size:0.85em;'>"
                    f"{notes_safe}</span>"
                    f"{metrics_html}"
                    f"{size_html}"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                if abstract:
                    with st.expander("Abstract", expanded=False):
                        st.write(_normalize_abstract_text(abstract))

    compact_csv = _compact_export_df(df_sorted).to_csv(index=False)
    full_csv = df_sorted.to_csv(index=False)
    export_cols = st.columns(2)
    key_base = hash(tuple(df_sorted.index.tolist()))
    with export_cols[0]:
        st.download_button(
            "📥 Export (compact)",
            compact_csv,
            "filtered_references_compact.csv",
            "text/csv",
            key=f"tree_export_compact_{key_base}",
        )
    with export_cols[1]:
        st.download_button(
            "📥 Export (full)",
            full_csv,
            "filtered_references_full.csv",
            "text/csv",
            key=f"tree_export_full_{key_base}",
        )


# ── MAIN RENDER ─────────────────────────────────────────────

def render_decision_tree(df, tree=None):
    """Render the workflow tree with separate core and auxiliary results."""
    _sync_tree_query_params()

    st.markdown("### 🌳 Study Design Workflow")
    st.markdown(
        "Follow the linear workflow below. **Core steps** (solid lines) proceed sequentially. "
        "**Auxiliary supports** (dashed lines) apply across the workflow."
    )

    matrix_key = None
    receptor_key = None
    instrument_key = None
    core_step_key = None
    aux_step_key = None
    aux_subtype_key = None
    core_label = ""
    aux_label = ""
    core_result_df = pd.DataFrame()
    aux_result_df = pd.DataFrame()
    core_selector_key = None
    aux_selector_key = None
    core_options = {}
    aux_options = {}
    detail_selector = None
    aux_info = {}
    availability = {}
    problem_selected = st.session_state.get("tree_problem") == "1"
    problem_result_df = _filter_problem_formulation(df)
    def_result_df = _filter_column(df, "Definitions & Terminology")
    availability["PF"] = _availability(problem_result_df) | {"active": problem_selected}
    availability["DEF"] = _availability(def_result_df)

    study_col, matrix_col = st.columns([1.1, 1.2])
    with study_col:
        domain = st.selectbox(
            "Study type",
            ["Monitoring", "Toxicology", "Risk Assessment"],
            key="tree_domain",
        )

    if domain == "Monitoring":
        df_domain = _filter_domain(df, "Monitoring")
        matrix_options = {
            key: f'{value["icon"]} {value["label"]}'
            for key, value in MATRICES.items()
        }
        core_options = {
            step["key"]: f'{step["icon"]} {step["label"]}'
            for step in MONITORING_CORE
        }
        aux_options = {
            step["key"]: f'{step["icon"]} {step["label"]}'
            for step in MONITORING_AUXILIARY
        }
        core_selector_key = "tree_core_step"
        aux_selector_key = "tree_aux_step"

        with matrix_col:
            matrix_key = st.selectbox(
                "Matrix",
                list(matrix_options.keys()),
                format_func=lambda key: matrix_options[key],
                key="tree_matrix",
            )
        particle_defaults = [
            key for key in _tree_query_values("tree_particle_type")
            if key in PARTICLE_TYPES
        ]
        particle_keys = st.multiselect(
            "Particle/polymer type",
            list(PARTICLE_TYPES.keys()),
            default=particle_defaults,
            format_func=lambda key: PARTICLE_TYPES[key]["label"],
            key="tree_particle_type",
        )
        st.caption("Showing references matching ANY selected type")
        core_step_key = _state_choice("tree_core_step", list(core_options.keys()))
        aux_step_key = _state_choice("tree_aux_step", list(aux_options.keys()))

        matrix_info = MATRICES[matrix_key]
        context_df = _filter_matrix(df_domain, matrix_info["kw"])
        context_df = _apply_matrix_tier_overrides(context_df, matrix_info["kw"])
        context_df = _filter_particle_types(context_df, particle_keys)
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
            detail_selector = {
                "label": "Technique",
                "key": "tree_instrument",
                "options": instrument_options,
            }
            instrument_key = _state_choice(
                "tree_instrument", list(instrument_options.keys())
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
        if aux_info.get("has_subtypes"):
            _sub_opts = {"all": "📋 Both"} | {
                k: v["label"] for k, v in aux_info["subtypes"].items()
            }
            _sel = _state_choice("tree_aux_subtype", list(_sub_opts.keys()))
            if _sel and _sel != "all":
                aux_subtype_key = _sel
                aux_result_df = _filter_column(
                    context_df, aux_info["subtypes"][_sel]["column"]
                )
                aux_label = f'{aux_info["icon"]} {aux_info["label"]} — {aux_info["subtypes"][_sel]["label"]}'

        availability.update(
            _workflow_availability(context_df, MONITORING_CORE, "CORE")
        )
        availability.update(
            _workflow_availability(context_df, MONITORING_AUXILIARY, "AUX")
        )
        availability.update(_instrument_availability(context_df))
        for _a in MONITORING_AUXILIARY:
            availability.update(_subtype_availability(context_df, _a))

    elif domain == "Toxicology":
        df_domain = _filter_domain(df, "Toxicology")
        receptor_options = {
            key: f'{value["icon"]} {value["label"]}'
            for key, value in RECEPTORS.items()
        }
        core_options = {
            step["key"]: f'{step["icon"]} {step["label"]}'
            for step in TOX_CORE
        }
        aux_options = {
            step["key"]: f'{step["icon"]} {step["label"]}'
            for step in TOX_AUXILIARY
        }
        core_selector_key = "tree_tox_core"
        aux_selector_key = "tree_tox_aux"

        with matrix_col:
            receptor_key = st.selectbox(
                "Target receptor",
                list(receptor_options.keys()),
                format_func=lambda key: receptor_options[key],
                key="tree_receptor",
            )
        receptor_info = RECEPTORS[receptor_key]
        context_df = _filter_target_receptor(df_domain, receptor_info["kw"])
        core_step_key = _state_choice("tree_tox_core", list(core_options.keys()))
        aux_step_key = _state_choice("tree_tox_aux", list(aux_options.keys()))

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
            detail_selector = {
                "label": "Test system",
                "key": "tree_test_sys",
                "options": system_options,
            }
            system_key = _state_choice(
                "tree_test_sys", list(system_options.keys())
            )
            if system_key != "all":
                core_result_df = _filter_keywords(
                    core_result_df, TEST_SYSTEMS[system_key]["keywords"]
                )
        aux_result_df = _apply_step_filters(context_df, aux_info)
        if aux_info.get("has_subtypes"):
            _sub_opts = {"all": "📋 Both"} | {
                k: v["label"] for k, v in aux_info["subtypes"].items()
            }
            _sel = _state_choice("tree_aux_subtype", list(_sub_opts.keys()))
            if _sel and _sel != "all":
                aux_subtype_key = _sel
                aux_result_df = _filter_column(
                    context_df, aux_info["subtypes"][_sel]["column"]
                )
                aux_label = f'{aux_info["icon"]} {aux_info["label"]} — {aux_info["subtypes"][_sel]["label"]}'

        availability.update(_workflow_availability(context_df, TOX_CORE, "CORE"))
        availability.update(
            _workflow_availability(context_df, TOX_AUXILIARY, "AUX")
        )
        for _a in TOX_AUXILIARY:
            availability.update(_subtype_availability(context_df, _a))

    elif domain == "Risk Assessment":
        df_domain = _filter_domain(df, "Risk Assessment")
        receptor_options = {
            key: f'{value["icon"]} {value["label"]}'
            for key, value in RECEPTORS.items()
        }
        core_selector_key = "tree_ra_step"

        with matrix_col:
            receptor_key = st.selectbox(
                "Target receptor",
                list(receptor_options.keys()),
                format_func=lambda key: receptor_options[key],
                key="tree_receptor",
            )
        receptor_info = RECEPTORS[receptor_key]
        context_df = _filter_target_receptor(df_domain, receptor_info["kw"])
        ra_core_steps = _ra_core_for_receptor(receptor_key)
        core_options = {
            step["key"]: f'{step["icon"]} {step["label"]}'
            for step in ra_core_steps
        }
        core_step_key = _state_choice("tree_ra_step", list(core_options.keys()))

        core_info = next(step for step in ra_core_steps if step["key"] == core_step_key)
        core_label = f'{core_info["icon"]} {core_info["label"]}'
        core_result_df = _apply_step_filters(context_df, core_info)

        availability.update(_workflow_availability(context_df, ra_core_steps, "CORE"))

    st.markdown("---")
    dot = build_graphviz(
        domain=domain,
        matrix_key=matrix_key,
        receptor_key=receptor_key,
        core_step_key=core_step_key,
        aux_step_key=aux_step_key,
        instrument_key=instrument_key,
        aux_subtype_key=aux_subtype_key,
        availability=availability,
    )
    _render_zoomable_graphviz(dot, 800)

    st.caption(
        "Node color shows best available tier: Tier 1 green, Tier 2 blue, "
        "Tier 3 gold, Tier 4 gray; red means no matching references."
    )

    st.markdown("**<span style='font-size:1.5em;'>Problem Formulation</span>**", unsafe_allow_html=True)
    problem_doc_types = _doc_type_options(problem_result_df)
    selected_problem_doc_types = st.multiselect(
        "Problem Formulation document type",
        problem_doc_types,
        default=problem_doc_types,
        key="tree_problem_doc_types",
    )
    if selected_problem_doc_types:
        doc_type_col = _find_col(problem_result_df, ["Document Type"])
        if doc_type_col:
            problem_display_df = problem_result_df[
                problem_result_df[doc_type_col].astype(str).isin(selected_problem_doc_types)
            ]
        else:
            problem_display_df = problem_result_df
    else:
        problem_display_df = problem_result_df.iloc[0:0]
    with st.expander(
        f"Problem Formulation references ({len(problem_display_df)})",
        expanded=problem_selected,
    ):
        _display_compact_results(problem_display_df, tier_expanders=False)

    with st.expander(
        f"📖 Definitions & Terminology ({len(def_result_df)})",
        expanded=False,
    ):
        _display_compact_results(def_result_df, tier_expanders=False)

    if core_selector_key:
        core_control_cols = st.columns([1.5, 1.2]) if detail_selector else [st.container()]
        with core_control_cols[0]:
            st.markdown("**<span style='font-size:1.5em;'>Core workflow</span>**", unsafe_allow_html=True)
            st.selectbox(
                "Core workflow",
                list(core_options.keys()),
                format_func=lambda key: core_options[key],
                key=core_selector_key,
                label_visibility="collapsed",
            )
        if detail_selector:
            with core_control_cols[1]:
                st.markdown(
                    f"**<span style='font-size:1.5em;'>{detail_selector['label']}</span>**",
                    unsafe_allow_html=True,
                )
                st.selectbox(
                    detail_selector["label"],
                    list(detail_selector["options"].keys()),
                    format_func=lambda key: detail_selector["options"][key],
                    key=detail_selector["key"],
                    label_visibility="collapsed",
                )

    with st.expander(
        f"Core Workflow references: {core_label} ({len(core_result_df)})",
        expanded=False,
    ):
        _display_compact_results(
            core_result_df,
            tier_expanders=False,
        )

    if aux_selector_key:
        st.markdown("**<span style='font-size:1.5em;'>Auxiliary Support</span>**", unsafe_allow_html=True)
        aux_has_subtypes = aux_info.get("has_subtypes", False)
        aux_ctrl_cols = st.columns([1.5, 1.2]) if aux_has_subtypes else [st.container()]
        with aux_ctrl_cols[0]:
            st.selectbox(
                "Auxiliary support",
                list(aux_options.keys()),
                format_func=lambda key: aux_options[key],
                key=aux_selector_key,
                label_visibility="collapsed",
            )
        if aux_has_subtypes:
            with aux_ctrl_cols[1]:
                st.markdown("**<span style='font-size:1.5em;'>Sub-type</span>**", unsafe_allow_html=True)
                _sub_opts = {"all": "📋 Both"} | {
                    k: v["label"]
                    for k, v in aux_info.get("subtypes", {}).items()  # type: ignore[union-attr]
                }
                st.selectbox(
                    "Sub-type",
                    list(_sub_opts.keys()),
                    format_func=lambda k: _sub_opts[k],
                    key="tree_aux_subtype",
                    label_visibility="collapsed",
                )

    with st.expander(
        f"Auxiliary Support references: {aux_label} ({len(aux_result_df)})",
        expanded=False,
    ):
        _display_compact_results(aux_result_df, tier_expanders=False)
