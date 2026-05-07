"""
Microplastics Methods Navigator
Interactive decision-tree tool for researchers planning MP monitoring or toxicology studies.
Reads from the crosswalk Excel file and guides users to the best available references by tier.

Usage:
    pip install streamlit pandas openpyxl pyyaml
    streamlit run app.py

Expects:
    - crosswalk.xlsx  (your crosswalk workbook — Crosswalk Table sheet)
    - tree_structure.yaml  (decision tree configuration)
Both in the same directory as app.py.
"""

import streamlit as st
import pandas as pd
import yaml
import sys
import re
import html
from pathlib import Path

# ── CONFIG ──────────────────────────────────────────────────

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
CROSSWALK_FILE = APP_DIR / "crosswalk.xlsx"
CROSSWALK_SHEET = "Crosswalk Table"
TREE_FILE = APP_DIR / "tree_structure.yaml"
EXPECTED_CROSSWALK_COLUMNS = {
    "Short Citation",
    "Priority Tier",
    "Primary Domain",
    "Document Type",
    "Matrix Tags",
}

TIER_LABELS = {
    1: "★★★★ Tier 1 — Normative / Binding",
    2: "★★★☆ Tier 2 — Authoritative / Institutional",
    3: "★★☆☆ Tier 3 — Peer-Reviewed / Validated",
    4: "★☆☆☆ Tier 4 — Supporting / Contextual",
}

TIER_COLORS = {
    1: "#1a7a2e",  # dark green
    2: "#2e6b8a",  # steel blue
    3: "#6b5b2e",  # dark gold
    4: "#6b6b6b",  # gray
}

TIER_ICONS = {1: "🟢", 2: "🔵", 3: "🟡", 4: "⚪"}


# ── DATA LOADING ────────────────────────────────────────────

@st.cache_data
def load_crosswalk():
    """Load and clean the crosswalk spreadsheet."""
    if not CROSSWALK_FILE.exists():
        st.error(f"❌ Crosswalk file not found: {CROSSWALK_FILE}")
        st.stop()

    df = read_crosswalk_sheet()

    # Extract tier number from Priority Tier string (e.g., "★★★★ Tier 1 ..." → 1)
    if "Priority Tier" in df.columns:
        df["tier_num"] = (
            df["Priority Tier"]
            .astype(str)
            .str.extract(r"Tier\s*(\d)")
            .astype(float)
        )
    else:
        df["tier_num"] = 4  # default

    return df


def read_crosswalk_sheet():
    """Read the crosswalk using the row that best matches the app schema."""
    candidates = [
        normalize_crosswalk_columns(
            pd.read_excel(
                CROSSWALK_FILE, sheet_name=CROSSWALK_SHEET, header=header
            )
        )
        for header in (0, 1)
    ]
    return max(candidates, key=crosswalk_schema_score)


def normalize_crosswalk_columns(df):
    # Normalize column names: strip whitespace and newlines
    df.columns = [
        " ".join(str(c).strip().split()) for c in df.columns
    ]
    return df


def crosswalk_schema_score(df):
    cols = {c.lower().strip() for c in df.columns}
    return sum(
        1 for col in EXPECTED_CROSSWALK_COLUMNS if col.lower() in cols
    )


@st.cache_data
def load_tree():
    """Load the decision tree structure."""
    if not TREE_FILE.exists():
        st.warning(
            f"⚠️ Tree file not found: {TREE_FILE}. Using built-in defaults."
        )
        return None
    with open(TREE_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_column(df, candidates):
    """Find the first matching column name from a list of candidates."""
    df_cols_lower = {c.lower().strip(): c for c in df.columns}
    for candidate in candidates:
        candidate_clean = (
            candidate.lower().strip().replace("\n", " ").replace("  ", " ")
        )
        if candidate_clean in df_cols_lower:
            return df_cols_lower[candidate_clean]
        # Fuzzy: check if candidate is a substring
        for col_lower, col_orig in df_cols_lower.items():
            if candidate_clean in col_lower or col_lower in candidate_clean:
                return col_orig
    return None


# ── FILTERING LOGIC ─────────────────────────────────────────

def filter_by_domain(df, domain):
    """Filter to entries matching a Primary Domain."""
    col = find_column(df, ["Primary Domain"])
    if col is None:
        return df
    mask = df[col].astype(str).str.lower().isin(
        [domain.lower(), "both", "cross-cutting"]
    )
    return df[mask]


def filter_by_matrix(df, matrix_keyword):
    """Filter by Matrix Tags containing the keyword."""
    col = find_column(df, ["Matrix Tags"])
    if col is None:
        return df
    mask = (
        df[col]
        .astype(str)
        .str.contains(matrix_keyword, case=False, na=False)
        | df[col]
        .astype(str)
        .str.contains("Cross-cutting", case=False, na=False)
    )
    return df[mask]


def filter_by_topic_column(df, column_name):
    """Filter to entries that have a non-empty score in a topic column."""
    col = find_column(df, [column_name])
    if col is None:
        return df
    return df[df[col].notna() & (df[col] != "") & (df[col] != 0)]


def filter_by_instrument(df, instrument_keyword):
    """Filter by Instrumentation Tags containing the keyword."""
    col = find_column(df, ["Instrumentation Tags"])
    if col is None:
        return df
    return df[
        df[col]
        .astype(str)
        .str.contains(instrument_keyword, case=False, na=False)
    ]


def filter_by_doc_type(df, doc_type):
    """Filter by Document Type."""
    col = find_column(df, ["Document Type"])
    if col is None:
        return df
    return df[
        df[col].astype(str).str.contains(doc_type, case=False, na=False)
    ]


def filter_by_keyword(df, keywords):
    """Filter by keywords in Key Notes."""
    col = find_column(df, ["Key Notes"])
    if col is None:
        return df
    kw_list = [k.strip() for k in keywords.split(";")]
    mask = pd.Series([False] * len(df), index=df.index)
    for kw in kw_list:
        mask = mask | df[col].astype(str).str.contains(
            kw, case=False, na=False
        )
    return df[mask]


def sort_by_tier(df):
    """Sort by tier (1 first), then by year descending."""
    year_col = find_column(df, ["Year"])
    if "tier_num" in df.columns:
        sort_cols = ["tier_num"]
        ascending = [True]
        if year_col:
            sort_cols.append(year_col)
            ascending.append(False)
        return df.sort_values(sort_cols, ascending=ascending)
    return df


# ── DISPLAY FUNCTIONS ───────────────────────────────────────

def normalize_abstract_text(value):
    """Clean abstract text for display without changing the dataframe."""
    if value is None or pd.isna(value):
        return ""
    text = str(value)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s*[•●▪◦‣⁃]\s*", " ", text)
    text = re.sub(r"\s+(?:[-*])\s+", " ", text)
    text = re.sub(
        r"\s*\b(?:Abstract|Summary)\b\s*[:.-]?\s*",
        " ",
        text,
        count=1,
        flags=re.I,
    )
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def compact_export_df(df):
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
        col = find_column(df, candidates)
        output[label] = df[col] if col else ""
    return output.reset_index(drop=True)


def display_reference_card(row):
    """Display a single reference as a styled card."""
    tier = (
        int(row.get("tier_num", 4))
        if pd.notna(row.get("tier_num"))
        else 4
    )
    icon = TIER_ICONS.get(tier, "⚪")
    color = TIER_COLORS.get(tier, "#666")

    # Safely extract fields
    def get_field(row, candidates):
        col = find_column(pd.DataFrame([row]), candidates)
        if col and col in row.index:
            val = row[col]
            if pd.notna(val) and str(val).strip().lower() not in [
                "nan", "none", ""
            ]:
                return str(val)
        return ""

    citation = get_field(row, ["Short Citation"])
    year = get_field(row, ["Year"])
    doc_type = get_field(row, ["Document Type"])
    notes = get_field(row, ["Key Notes"])
    doi = get_field(row, ["DOI/URL", "DOI", "URL"])
    size_range = get_field(row, ["Particle Size Range", "Particle Size"])
    metrics = get_field(row, ["Key Metrics / Output", "Key Metrics", "Output"])
    scope = get_field(row, ["Scope"])
    status = get_field(row, ["Status"])
    abstract = normalize_abstract_text(get_field(row, ["Abstract"]))
    citation_safe = html.escape(citation)
    year_safe = html.escape(year)
    doc_type_safe = html.escape(doc_type)
    notes_safe = html.escape(notes)
    doi_safe = html.escape(doi, quote=True)
    size_range_safe = html.escape(size_range)
    metrics_preview = metrics[:150] + ("..." if len(metrics) > 150 else "")
    metrics_safe = html.escape(metrics_preview)
    scope_safe = html.escape(scope)
    status_safe = html.escape(status)

    # Build the card HTML
    parts = [
        f'<div style="border-left: 4px solid {color}; padding: 8px 12px; '
        f'margin-bottom: 8px; background-color: #f8f9fa; border-radius: 4px;">',
        f"<strong>{icon} {citation_safe}"
        + (f" ({year_safe})" if year else "")
        + "</strong>",
        f'<span style="color: {color}; font-size: 0.85em;"> — {doc_type_safe}</span>'
        if doc_type
        else "",
        "<br/>",
        f'<span style="font-size: 0.9em;">{notes_safe}</span>' if notes else "",
    ]

    if size_range:
        parts.append(
            f"<br/><span style='font-size: 0.8em; color: #555;'>"
            f"📐 Size range: {size_range_safe}</span>"
        )

    if metrics:
        parts.append(
            f"<br/><span style='font-size: 0.8em; color: #7a6b2e;'>"
            f"📊 {metrics_safe}</span>"
        )

    if tier <= 2 and (scope or status):
        parts.append("<br/><span style='font-size: 0.8em; color: #555;'>")
        if scope:
            parts.append(f"🎯 {scope_safe}")
        if status:
            parts.append(f"{' · ' if scope else ''}📋 {status_safe}")
        parts.append("</span>")

    if doi:
        parts.append(
            f"<br/><a href='{doi_safe}' style='font-size: 0.8em;'>"
            f"🔗 {doi_safe}</a>"
        )

    parts.append("</div>")

    st.markdown("".join(parts), unsafe_allow_html=True)
    if abstract:
        with st.expander("Abstract", expanded=False):
            st.write(abstract)


def display_results(df, title="References", gap_note=None):
    """Display filtered references grouped by tier."""
    df_sorted = sort_by_tier(df)

    if len(df_sorted) == 0:
        st.warning(
            "No references found for this combination. "
            "This may indicate a gap in the literature."
        )
        if gap_note:
            st.error(gap_note)
        return

    st.markdown(f"### {title}")
    st.caption(f"{len(df_sorted)} references found")

    if gap_note:
        st.warning(gap_note)

    # Group by tier
    for tier_num in [1, 2, 3, 4]:
        tier_df = df_sorted[df_sorted["tier_num"] == tier_num]
        if len(tier_df) == 0:
            continue

        tier_label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
        with st.expander(
            f"{tier_label} ({len(tier_df)} references)",
            expanded=(tier_num <= 2),
        ):
            for _, row in tier_df.iterrows():
                display_reference_card(row)

    export_cols = st.columns(2)
    with export_cols[0]:
        st.download_button(
            "📥 Export (compact)",
            compact_export_df(df_sorted).to_csv(index=False),
            file_name="filtered_references_compact.csv",
            mime="text/csv",
        )
    with export_cols[1]:
        st.download_button(
            "📥 Export (full)",
            df_sorted.to_csv(index=False),
            file_name="filtered_references_full.csv",
            mime="text/csv",
        )


def render_search_all_references(df):
    """Search across citation, notes, abstract, and metadata fields."""
    st.markdown("### Search All References")
    query = st.text_input(
        "Search references",
        placeholder="Search Short Citation, Key Notes, Abstract, DOI, metrics...",
        key="search_all_references_query",
    )
    searchable_cols = [
        find_column(df, [name])
        for name in [
            "Short Citation",
            "Full Title",
            "Key Notes",
            "Abstract",
            "Key Metrics / Output",
            "Particle Size Range",
            "DOI/URL",
        ]
    ]
    searchable_cols = [col for col in searchable_cols if col]
    result_df = df
    if query.strip() and searchable_cols:
        terms = [term for term in query.lower().split() if term]
        haystack = (
            df[searchable_cols]
            .fillna("")
            .astype(str)
            .agg(" ".join, axis=1)
            .str.lower()
        )
        mask = pd.Series(True, index=df.index)
        for term in terms:
            mask = mask & haystack.str.contains(term, regex=False, na=False)
        result_df = df[mask]

    st.caption(f"{len(result_df)} of {len(df)} references shown")
    display_results(result_df, "Search Results")


def get_gap_note(tree, matrix_key, step_key):
    """Look up a gap note from the tree structure."""
    if tree is None:
        return None
    gap_notes = tree.get("gap_notes", {})

    # Try specific matrix+step combination
    specific_key = f"{matrix_key}_{step_key}"
    if specific_key in gap_notes:
        return gap_notes[specific_key]

    # Try matrix-level catch-all
    matrix_all = f"{matrix_key}_all"
    if matrix_all in gap_notes:
        return gap_notes[matrix_all]

    return None


# ── MAIN APP ────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="MP Methods Navigator",
        page_icon="🔬",
        layout="wide",
    )

    st.title("🔬 Microplastics Methods Navigator")
    st.markdown(
        "*Interactive decision tree for planning microplastics "
        "monitoring and toxicology studies.*  \n"
        "Select your study type, matrix, and workflow step to find "
        "the best available methods ranked by authority tier."
    )

    # Load data
    df = load_crosswalk()
    tree = load_tree()

    # ── App tabs ────────────────────────────────────────────
    step_by_step_enabled = False
    if step_by_step_enabled:
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Step-by-Step Navigator", "Decision Tree", "Crosswalk", "Search All References"]
        )
    else:
        tab2, tab3, tab4 = st.tabs(["Decision Tree", "Crosswalk", "Search All References"])

    if step_by_step_enabled:
        with tab1:
    
            st.divider()
    
            # ── STEP 1: Study Domain ────────────────────────────────
            col1, col2 = st.columns([1, 2])
        
            with col1:
                st.markdown("### Step 1: Study Type")
                domain = st.radio(
                    "What are you designing?",
                    [
                        "🔬 Environmental Monitoring",
                        "🧫 Toxicology / Effects Testing",
                        "⚖️ Risk Assessment",
                    ],
                    label_visibility="collapsed",
                )
        
            domain_key = {
                "🔬 Environmental Monitoring": "Monitoring",
                "🧫 Toxicology / Effects Testing": "Toxicology",
                "⚖️ Risk Assessment": "Both",
            }[domain]
        
            df_domain = filter_by_domain(df, domain_key)
        
            # ── MONITORING PATH ─────────────────────────────────────
            if domain_key == "Monitoring":
                with col2:
                    st.markdown("### Step 2: Matrix")
                    matrix = st.selectbox(
                        "Which environmental matrix?",
                        [
                            "🚰 Drinking Water",
                            "🌊 Surface Water / Wastewater",
                            "🪨 Sediment",
                            "🐟 Biota / Tissue",
                            "💨 Air / Atmospheric Deposition",
                            "🍽️ Food / Dietary",
                            "🩸 Human Tissue / Biomonitoring",
                            "🌱 Soil / Terrestrial",
                        ],
                    )
        
                matrix_map = {
                    "🚰 Drinking Water": ("Drinking Water", "drinking_water"),
                    "🌊 Surface Water / Wastewater": (
                        "Surface Water",
                        "surface_water",
                    ),
                    "🪨 Sediment": ("Sediment", "sediment"),
                    "🐟 Biota / Tissue": ("Biota", "biota"),
                    "💨 Air / Atmospheric Deposition": ("Air", "air"),
                    "🍽️ Food / Dietary": ("Food", "food"),
                    "🩸 Human Tissue / Biomonitoring": (
                        "Human",
                        "human_tissue",
                    ),
                    "🌱 Soil / Terrestrial": ("Soil", "soil"),
                }
                matrix_filter, matrix_key = matrix_map[matrix]
                df_matrix = filter_by_matrix(df_domain, matrix_filter)
        
                st.divider()
                st.markdown("### Step 3: Workflow Step")
        
                workflow_step = st.selectbox(
                    "Which step of the monitoring workflow?",
                    [
                        "📖 Definitions & Terminology",
                        "📍 Sampling / Field Methods",
                        "🧪 Sample Processing / Extraction",
                        "🔎 Analytical Identification",
                        "📦 Reference Materials / Controls",
                        "🧹 Blanks & Contamination Control",
                        "📊 Data Analysis & Statistics",
                        "📝 Reporting & Data Deposition",
                        "🔄 Interlaboratory / Validation Studies",
                    ],
                )
        
                step_column_map = {
                    "📖 Definitions & Terminology": "Definitions & Terminology",
                    "📍 Sampling / Field Methods": "Sampling (Field Methods)",
                    "🧪 Sample Processing / Extraction": (
                        "Sample Processing / Extraction"
                    ),
                    "📦 Reference Materials / Controls": (
                        "Reference Materials / +Controls"
                    ),
                    "🧹 Blanks & Contamination Control": (
                        "Blanks & Contamination Control"
                    ),
                    "📊 Data Analysis & Statistics": "Data Analysis & Statistics",
                    "📝 Reporting & Data Deposition": "Reporting & Harmonization",
                    "🔄 Interlaboratory / Validation Studies": None,
                }
        
                step_key = (
                    workflow_step.split(" ", 1)[1]
                    .lower()
                    .replace(" ", "_")
                    .replace("/", "")
                )
        
                # ── Analytical: extra instrument filter ─────────────
                if workflow_step == "🔎 Analytical Identification":
                    instrument = st.selectbox(
                        "Which analytical technique?",
                        [
                            "📋 All Techniques (overview)",
                            "µFTIR / FPA-FTIR",
                            "LDIR (Laser Direct IR)",
                            "µRaman",
                            "Py-GC-MS",
                            "TED-GC-MS",
                            "Nile Red / Fluorescence",
                            "Visual / Stereomicroscopy",
                        ],
                    )
        
                    instrument_map = {
                        "µFTIR / FPA-FTIR": "µFTIR",
                        "LDIR (Laser Direct IR)": "LDIR",
                        "µRaman": "µRaman",
                        "Py-GC-MS": "Py-GC-MS",
                        "TED-GC-MS": "TED-GC-MS",
                        "Nile Red / Fluorescence": "Nile Red",
                        "Visual / Stereomicroscopy": "Stereomicroscopy",
                    }
        
                    if instrument == "📋 All Techniques (overview)":
                        df_result = filter_by_topic_column(
                            df_matrix, "Analytical Methods (General)"
                        )
                    else:
                        inst_key = instrument_map[instrument]
                        df_result = filter_by_instrument(df_matrix, inst_key)
        
                    gap_note = get_gap_note(tree, matrix_key, "analysis")
                    display_results(
                        df_result,
                        f"Analytical Methods — "
                        f"{matrix.split(' ', 1)[1]} — {instrument}",
                        gap_note,
                    )
        
                # ── Interlaboratory: filter by doc type ─────────────
                elif workflow_step == "🔄 Interlaboratory / Validation Studies":
                    df_result = filter_by_doc_type(df_matrix, "Interlaboratory")
                    gap_note = get_gap_note(
                        tree, matrix_key, "interlaboratory"
                    )
                    display_results(
                        df_result,
                        f"Interlaboratory Studies — "
                        f"{matrix.split(' ', 1)[1]}",
                        gap_note,
                    )
        
                # ── Standard workflow steps ─────────────────────────
                else:
                    col_name = step_column_map.get(workflow_step)
                    if col_name:
                        df_result = filter_by_topic_column(df_matrix, col_name)
                    else:
                        df_result = df_matrix
                    gap_note = get_gap_note(tree, matrix_key, step_key)
                    display_results(
                        df_result,
                        f"{workflow_step.split(' ', 1)[1]} — "
                        f"{matrix.split(' ', 1)[1]}",
                        gap_note,
                    )
        
            # ── TOXICOLOGY PATH ─────────────────────────────────────
            elif domain_key == "Toxicology":
                with col2:
                    st.markdown("### Step 2: Workflow Step")
                    tox_step = st.selectbox(
                        "Which toxicology workflow step?",
                        [
                            "🔬 Particle Characterization",
                            "📦 Reference / Test Particles",
                            "💊 Dosimetry (in vitro)",
                            "🧬 Effects Testing",
                            "✅ Study Quality / Scoring",
                            "📝 Reporting (Tox)",
                        ],
                    )
        
                tox_column_map = {
                    "🔬 Particle Characterization": (
                        "Toxicology: Study Design & Dosimetry"
                    ),
                    "📦 Reference / Test Particles": (
                        "Reference Materials / +Controls"
                    ),
                    "💊 Dosimetry (in vitro)": (
                        "Toxicology: Study Design & Dosimetry"
                    ),
                    "✅ Study Quality / Scoring": (
                        "Toxicology: Study Design & Dosimetry"
                    ),
                    "📝 Reporting (Tox)": "Reporting & Harmonization",
                }
        
                if tox_step == "🧬 Effects Testing":
                    st.divider()
                    st.markdown("### Step 3: Test System")
                    test_system = st.selectbox(
                        "Which test system?",
                        [
                            "🧫 In Vitro (cell-based)",
                            "🐠 Ecotox — Aquatic",
                            "🌱 Ecotox — Terrestrial / Soil",
                            "🐁 Mammalian In Vivo",
                            "👤 Human / Epidemiological",
                            "📋 All Effects Testing",
                        ],
                    )
        
                    keyword_map = {
                        "🧫 In Vitro (cell-based)": (
                            "in vitro;steroidogenesis;cell;H295R;Caco"
                        ),
                        "🐠 Ecotox — Aquatic": (
                            "ecotox;aquatic;benthic;fish;invertebrate;"
                            "Daphnia;bivalve;algae"
                        ),
                        "🌱 Ecotox — Terrestrial / Soil": (
                            "soil;terrestrial;earthworm"
                        ),
                        "🐁 Mammalian In Vivo": (
                            "mammalian;rodent;mouse;rat;oral exposure;organ"
                        ),
                        "👤 Human / Epidemiological": (
                            "human;blood;placenta;epidemiolog;clinical;lung"
                        ),
                    }
        
                    df_tox = filter_by_domain(df, "Toxicology")
                    df_result = filter_by_topic_column(
                        df_tox, "Toxicology: Effects Testing Methods"
                    )
        
                    if test_system != "📋 All Effects Testing":
                        kw = keyword_map[test_system]
                        df_result = filter_by_keyword(df_result, kw)
        
                    gap_note = get_gap_note(tree, "tox", "all")
                    display_results(
                        df_result,
                        f"Effects Testing — {test_system.split(' ', 1)[1]}",
                        gap_note,
                    )
        
                else:
                    col_name = tox_column_map.get(tox_step)
                    df_tox = filter_by_domain(df, "Toxicology")
        
                    if col_name:
                        df_result = filter_by_topic_column(df_tox, col_name)
                    else:
                        df_result = df_tox
        
                    # Additional keyword filtering
                    if tox_step == "💊 Dosimetry (in vitro)":
                        df_result = filter_by_keyword(
                            df_result,
                            "dosimetry;particokinetics;delivered dose;"
                            "ISDD;PBK;sedimentation",
                        )
                    elif tox_step == "✅ Study Quality / Scoring":
                        df_result = filter_by_keyword(
                            df_result,
                            "quality;QA;scoring;criteria;checklist;ToMEx",
                        )
        
                    gap_note = get_gap_note(tree, "tox", "all")
                    display_results(
                        df_result,
                        tox_step.split(" ", 1)[1],
                        gap_note,
                    )
        
            # ── RISK ASSESSMENT PATH ────────────────────────────────
            elif domain_key == "Both":  # Risk Assessment
                with col2:
                    st.markdown("### Step 2: RA Component")
                    ra_step = st.selectbox(
                        "Which risk assessment component?",
                        [
                            "🏗️ RA Frameworks & Approaches",
                            "⚠️ Hazard Identification",
                            "📏 Exposure Assessment",
                            "📊 Risk Characterization",
                            "📋 All RA References",
                        ],
                    )
        
                # Get all entries scored in the RA column
                ra_col = find_column(
                    df, ["Risk Assessment / Risk Char.", "Risk Assessment"]
                )
                if ra_col:
                    df_ra = df[
                        df[ra_col].notna()
                        & (df[ra_col] != "")
                        & (df[ra_col] != 0)
                    ]
                else:
                    df_ra = df
        
                if ra_step == "📋 All RA References":
                    df_result = df_ra
                elif ra_step == "🏗️ RA Frameworks & Approaches":
                    df_fw = filter_by_doc_type(df_ra, "Framework")
                    df_adopted = filter_by_doc_type(
                        df_ra, "Regulatory-Adopted"
                    )
                    df_result = pd.concat(
                        [df_fw, df_adopted]
                    ).drop_duplicates()
                elif ra_step == "⚠️ Hazard Identification":
                    df_result = filter_by_keyword(
                        df_ra,
                        "hazard;toxicity;effect;ToMEx;tox database;SSD",
                    )
                elif ra_step == "📏 Exposure Assessment":
                    df_result = filter_by_keyword(
                        df_ra,
                        "exposure;PBK;monitoring;scenario;"
                        "dietary;inhalation",
                    )
                elif ra_step == "📊 Risk Characterization":
                    df_result = filter_by_keyword(
                        df_ra,
                        "risk quotient;threshold;management;"
                        "stochastic;SSD;characterization;TRL",
                    )
                else:
                    df_result = df_ra
        
                display_results(
                    df_result, ra_step.split(" ", 1)[1]
                )
    
    with tab2:
        from visual_tree_tab import render_decision_tree
        render_decision_tree(df, tree)

    with tab3:
        from crosswalk_tab import render_crosswalk_tab
        render_crosswalk_tab(df)

    with tab4:
        render_search_all_references(df)

    # ── FOOTER ──────────────────────────────────────────────
    st.divider()
    st.markdown(
        "<div style='text-align: center; color: #888; "
        "font-size: 0.85em;'>"
        "<strong>Microplastics Methods Navigator</strong> · "
        "MIT License 2026<br/>"
        f"Crosswalk entries: {len(df)} · "
        f"Tier 1: {len(df[df['tier_num'] == 1])} · "
        f"Tier 2: {len(df[df['tier_num'] == 2])} · "
        f"Tier 3: {len(df[df['tier_num'] == 3])} · "
        f"Tier 4: {len(df[df['tier_num'] == 4])}"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
