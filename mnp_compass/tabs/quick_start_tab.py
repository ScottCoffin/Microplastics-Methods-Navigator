"""Quick Start tab: a short guide plus worked examples that open pre-set Decision Tree paths.

Each worked example names specific crosswalk references and their tiers. Those
claims are checked against crosswalk.xlsx by tests/smoke_test.py (the
`expected_tiers` field), so if a reference is re-tiered or renamed the test
fails and the example text below must be updated to match.
"""

from __future__ import annotations

import streamlit as st

try:
    from tabs.visual_tree_tab import (
        resolve_tree_path, render_static_graphviz, path_dot_for_state,
        _format_tier_counts, _best_tier,
    )
except ImportError:  # imported as mnp_compass.tabs.quick_start_tab (tests)
    from mnp_compass.tabs.visual_tree_tab import (
        resolve_tree_path, render_static_graphviz, path_dot_for_state,
        _format_tier_counts, _best_tier,
    )

# Main tab labels, shared with app.py so examples can switch tabs programmatically.
MAIN_TABS_KEY = "main_tabs"
TAB_QUICK_START = "Quick Start"
TAB_DECISION_TREE = "Decision Tree"
TAB_COVERAGE = "Coverage & Gaps"
TAB_CROSSWALK = "Crosswalk"
TAB_SEARCH = "Search All References"
TAB_GLOSSARY = "Glossary"
TAB_ABOUT = "About"
MAIN_TABS = [
    TAB_QUICK_START,
    TAB_DECISION_TREE,
    TAB_COVERAGE,
    TAB_CROSSWALK,
    TAB_SEARCH,
    TAB_GLOSSARY,
    TAB_ABOUT,
]

# Decision Tree session-state keys cleared before an example applies its own.
_TREE_STATE_KEYS = [
    "tree_domain", "tree_matrix", "tree_receptor", "tree_particle_type",
    "tree_problem", "tree_core_step", "tree_aux_step", "tree_tox_core",
    "tree_tox_aux", "tree_ra_step", "tree_instrument", "tree_test_sys",
    "tree_aux_subtype",
]
EXPAND_RESULTS_KEY = "tree_expand_results"

WORKED_EXAMPLES = [
    {
        "key": "dw_raman",
        "title": "Drinking-water monitoring by µRaman",
        "who": "A water utility or contract laboratory planning regulatory monitoring.",
        "path": "Monitoring → Drinking Water → Analysis → µRaman",
        "state": {
            "tree_domain": "Monitoring",
            "tree_matrix": "drinking_water",
            "tree_core_step": "analysis",
            "tree_instrument": "raman",
        },
        "expand": "core",
        "shows": (
            "Drinking water is one of the few matrices with binding methods. Tier 1 results "
            "include the California SWB-MP2 Raman SOP (Wong & Coffin, 2022b) and the EU "
            "methodology for water intended for human consumption (European Commission, 2024), "
            "followed by ISO 16094-2:2025 (Tier 2) and interlaboratory studies (Tier 3) that "
            "document recovery and between-laboratory variability."
        ),
        "plan": (
            "Where one of these methods is legally required, follow it as written; the Tier 3 "
            "interlaboratory studies help set realistic recovery targets, QC acceptance criteria, "
            "and staff time. Check the size range on each card: both Tier 1 methods cover "
            "20 µm–5 mm, so a study targeting smaller particles must add a method whose scope "
            "extends lower (e.g., ISO 16094-2 covers 1 µm–5 mm in low-turbidity water) and report "
            "the size ranges of each method separately."
        ),
        "expected_tiers": {
            "Wong & Coffin, 2022b": 1,
            "European Commission, 2024": 1,
            "ISO 16094-2:2025": 2,
            "De Frond et al., 2022": 3,
        },
    },
    {
        "key": "blood_pygcms",
        "title": "Plastics in human blood by Py-GC-MS",
        "who": "A biomedical research group new to microplastics analysis.",
        "path": "Monitoring → Human Tissue → Analysis → Py-GC-MS",
        "state": {
            "tree_domain": "Monitoring",
            "tree_matrix": "human_tissue",
            "tree_core_step": "analysis",
            "tree_instrument": "pyrolysis",
        },
        "expand": "core",
        "shows": (
            "No Tier 1–3 reference exists for this combination. The best available, "
            "matrix-specific resources are Tier 4 single-laboratory methods (Leslie et al., 2022; "
            "Rauert et al., 2025), and the app warns that no Tier 1/2 reference matches the path."
        ),
        "plan": (
            "Here a lower-tier resource is the right choice: a higher-tier drinking-water method "
            "has more authority but does not apply to blood. The Tier 4 study changes the design "
            "directly: Rauert et al. (2025) concluded that Py-GC-MS is currently unsuitable for "
            "polyethylene and PVC in biological matrices because of matrix interferences. Plan "
            "to exclude or separately confirm those polymers, add matrix-matched spike-recovery "
            "tests and procedural blanks, and report confidence in polymer identification "
            "explicitly (search \"Communicating Confidence\" in Search All References)."
        ),
        "expected_tiers": {
            "Rauert et al., 2025": 4,
            "Leslie et al., 2022": 4,
        },
    },
    {
        "key": "air_sampling",
        "title": "Atmospheric deposition sampling",
        "who": "An environmental monitoring team adding air to an existing water program.",
        "path": "Monitoring → Air → Sampling",
        "state": {
            "tree_domain": "Monitoring",
            "tree_matrix": "air",
            "tree_core_step": "sampling",
            "tree_aux_step": "blanks",
        },
        "expand": "core",
        "shows": (
            "No Tier 1/2 sampling method exists for air. The highest tier is Tier 3, with several "
            "candidates (e.g., Wright et al., 2021 screening criteria; Ren et al., 2026 critical "
            "review of passive and active samplers)."
        ),
        "plan": (
            "With no authoritative method to defer to, compare all the Tier 3 candidates rather "
            "than picking one citation. Justify the sampler choice in the methods section and "
            "report the sampling parameters these reviews identify as necessary for comparing "
            "studies. Open Blanks & Contamination Control under Auxiliary Support as well: "
            "airborne fibres in the laboratory are a common source of procedural contamination, "
            "which matters most when the sample is itself air."
        ),
        "expected_tiers": {
            "Wright et al., 2021": 3,
            "Ren et al., 2026": 3,
        },
    },
    {
        "key": "aquatic_tox",
        "title": "Aquatic effects study (e.g., fish larvae)",
        "who": "An ecotoxicologist designing a dose-response exposure study.",
        "path": "Toxicology → Ecotoxicology → Study Quality & Scoring (Auxiliary Support)",
        "state": {
            "tree_domain": "Toxicology",
            "tree_receptor": "ecotoxicology",
            "tree_tox_core": "effects",
            "tree_test_sys": "eco_aquatic",
            "tree_tox_aux": "quality",
        },
        "expand": "aux",
        "shows": (
            "There are no microplastic-specific test guidelines (Tier 1/2) for effects testing. "
            "The strongest guidance consists of Tier 3 quality-criteria frameworks: "
            "de Ruijter et al., 2020; Kokalj et al., 2021 (nanoplastics); and SciRAPplastic / "
            "plasticCRED (Due et al., 2026). These are the criteria used to screen studies "
            "before they are admitted into risk assessments."
        ),
        "plan": (
            "Design against these criteria from the start: characterize the test particles, "
            "use at least three concentrations to support effect metrics, and include "
            "contamination and particle-only controls. That keeps the finished study eligible "
            "for threshold derivation. Also check Material Standards under Auxiliary Support "
            "when choosing test particles (next example)."
        ),
        "expected_tiers": {
            "de Ruijter et al., 2020": 3,
            "Kokalj et al., 2021": 3,
            "Due et al. 2026": 3,
        },
    },
    {
        "key": "test_particles",
        "title": "Choosing test particles for an exposure study",
        "who": "A toxicologist deciding between commercial spheres, reference materials, and "
               "lab-generated particles.",
        "path": "Toxicology → Ecotoxicology → Material Standards → Generation Protocols",
        "state": {
            "tree_domain": "Toxicology",
            "tree_receptor": "ecotoxicology",
            "tree_tox_aux": "ref_materials",
            "tree_aux_subtype": "protocols",
        },
        "expand": "aux",
        "shows": (
            "The Tier 2 results address specific particle classes (e.g., tyre and road wear "
            "particle generation, ISO 22638:2024) or nanoplastics (OECD, 2026). Tier 3 protocols "
            "describe how to create environmentally relevant particle mixtures "
            "(De Ruijter et al., 2025a), and Tier 4 commentary explains the limited relevance "
            "of polystyrene spheres (Gouin et al., 2024)."
        ),
        "plan": (
            "Let the study goal pick the tier. For a mechanistic study of tyre wear particles, the "
            "Tier 2 ISO protocol is the obvious choice. For a dose-response study intended to "
            "inform risk thresholds, a Tier 3 protocol for environmentally relevant mixtures is "
            "more appropriate than any higher-tier material with a narrower scope. Switch "
            "Sub-type to Materials to see purchasable reference materials."
        ),
        "expected_tiers": {
            "ISO 22638:2024": 2,
            "OECD, 2026": 2,
            "De Ruijter et al., 2025a": 3,
            "Gouin et al., 2024": 4,
        },
    },
    {
        "key": "editor_review",
        "title": "Editor, reviewer, or funder checking expected practice",
        "who": "A journal editor, peer reviewer, or program officer.",
        "path": "Crosswalk tab → filter by Primary Domain, Matrix Tags, Instrumentation Tags, "
                "and Authority Tier",
        "state": None,
        "tab": TAB_CROSSWALK,
        "shows": (
            "The Crosswalk tab shows every reference in one filterable table, which is faster "
            "than stepping through the tree. Filter to the submission's domain, matrix, and "
            "instrument, then to Tiers 1–3 to see the established methods and QA/QC criteria "
            "a study of that kind would be expected to cite or follow."
        ),
        "plan": (
            "Use the filtered list as a checklist in review or in a call for proposals. Where "
            "the Coverage & Gaps tab shows no Tier 1/2 method for a matrix, expect authors to "
            "justify their method choice and report validation data rather than cite a "
            "standard that does not exist."
        ),
        "expected_tiers": {},
    },
]


def _open_example(example):
    for key in _TREE_STATE_KEYS:
        st.session_state.pop(key, None)
    if example.get("state"):
        st.session_state.update(example["state"])
        st.session_state[EXPAND_RESULTS_KEY] = example.get("expand")
    st.session_state[MAIN_TABS_KEY] = example.get("tab", TAB_DECISION_TREE)


def _live_summary(df, example):
    """One-line live count for an example's path, computed with the tree's own filters."""
    if not example.get("state"):
        return None
    path = resolve_tree_path(df, example["state"])
    result_df = path["aux"] if example.get("expand") == "aux" else path["core"]
    if len(result_df) == 0:
        return "Live result: no matching references."
    tiers = result_df["tier_num"].dropna().astype(int).value_counts().to_dict()
    summary = f"Live result: {len(result_df)} references ({_format_tier_counts(tiers)})"
    matrix_info = path.get("matrix_info")
    if matrix_info:
        specific = path["core_specific"] if example.get("expand") != "aux" else path["aux_specific"]
        specific_tier = _best_tier(specific)
        summary += (
            f"; best {matrix_info['label']}-specific tier: "
            + (f"Tier {specific_tier}" if specific_tier else "none")
        )
    return summary + "."


def render_quick_start_tab(df):
    st.markdown("### Quick Start")
    st.markdown(
        "MNP Compass points you to the methods, standards, and guidance that apply to one "
        "step of a micro-/nanoplastics study, and shows how authoritative each one is."
    )

    guide_cols = st.columns(3)
    guide_steps = [
        (
            "1 · Describe your study",
            "In **Decision Tree**, pick a study type (Monitoring, Toxicology, or Risk "
            "Assessment), then a matrix (monitoring) or target receptor (toxicology and risk "
            "assessment). Optionally filter by particle type.",
        ),
        (
            "2 · Pick a workflow step",
            "Choose a **Core workflow** step (e.g., Sampling → Extraction → Analysis) and, if "
            "needed, an **Auxiliary Support** (Material Standards, Blanks & Contamination "
            "Control). Node colors in the diagram show the best tier available at each step.",
        ),
        (
            "3 · Read the results as evidence",
            "Results are grouped Tier 1 → Tier 4. The tier describes a document's **authority**, "
            "not its quality: check the size range, matrix, and date on each card, and note "
            "the 🌐 cross-cutting badge on documents not written for your matrix. Export to CSV "
            "for a study plan.",
        ),
    ]
    for col, (heading, body) in zip(guide_cols, guide_steps):
        with col:
            with st.container(border=True):
                st.markdown(f"**{heading}**")
                st.markdown(body)

    st.caption(
        "Other tabs: **Coverage & Gaps** maps where authoritative methods exist; **Crosswalk** "
        "and **Search All References** browse all references; **About** explains how references "
        "were compiled, tiered, and ranked."
    )

    st.markdown("#### Worked examples")
    st.markdown(
        "Each example opens a pre-set path in the Decision Tree. Several show cases where a "
        "lower-tier resource is the better choice for a given study."
    )

    for example in WORKED_EXAMPLES:
        with st.container(border=True):
            if example.get("state"):
                text_col, tree_col = st.columns([3, 2], gap="medium")
            else:
                text_col, tree_col = st.container(), None
            with text_col:
                st.markdown(f"**{example['title']}**")
                st.caption(f"{example['who']}  \nPath: {example['path']}")
                st.markdown(f"**What MNP Compass shows:** {example['shows']}")
                live = _live_summary(df, example)
                if live:
                    st.caption(live)
                st.markdown(f"**How it shapes the study plan:** {example['plan']}")
                target_tab = example.get("tab", TAB_DECISION_TREE)
                st.button(
                    f"Open in {target_tab} →",
                    key=f"quick_start_{example['key']}",
                    on_click=_open_example,
                    args=(example,),
                )
            if tree_col is not None:
                with tree_col:
                    if render_static_graphviz(path_dot_for_state(df, example["state"])):
                        st.caption(
                            "Highlighted path: bold outlines. Node color: best available tier."
                        )
