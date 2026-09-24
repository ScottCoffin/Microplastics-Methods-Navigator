"""Coverage & Gaps tab: best available tier per matrix × monitoring workflow step.

Computed live from crosswalk.xlsx with the same filters the Decision Tree uses
(visual_tree_tab.monitoring_coverage), so it updates automatically as
references are added or re-tiered.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

try:
    from tabs.visual_tree_tab import (
        MATRICES, MONITORING_AUXILIARY, MONITORING_CORE, PARTICLE_TYPES,
        TIER_COLORS, monitoring_coverage,
    )
except ImportError:  # imported as mnp_compass.tabs.coverage_tab (tests)
    from mnp_compass.tabs.visual_tree_tab import (
        MATRICES, MONITORING_AUXILIARY, MONITORING_CORE, PARTICLE_TYPES,
        TIER_COLORS, monitoring_coverage,
    )

_NONE_COLOR = "#b00020"


def coverage_table(coverage, specific_only=True):
    """Pivot monitoring_coverage() output into matrix × step cells like 'T1 · 7'."""
    tier_col, count_col = (
        ("specific_tier", "specific_count") if specific_only else ("tier", "count")
    )
    steps = [s["label"] for s in MONITORING_CORE + MONITORING_AUXILIARY]
    matrices = [m["label"] for m in MATRICES.values()]
    tiers = coverage.pivot(index="matrix", columns="step", values=tier_col).reindex(
        index=matrices, columns=steps
    )
    counts = coverage.pivot(index="matrix", columns="step", values=count_col).reindex(
        index=matrices, columns=steps
    )
    labels = tiers.copy().astype(object)
    for matrix in matrices:
        for step in steps:
            tier = tiers.loc[matrix, step]
            labels.loc[matrix, step] = (
                "none" if pd.isna(tier) else f"T{int(tier)} · {int(counts.loc[matrix, step])}"
            )
    return tiers, labels


def _cell_style(tier):
    color = _NONE_COLOR if pd.isna(tier) else TIER_COLORS[int(tier)]
    return f"background-color: {color}; color: white;"


def render_coverage_tab(df):
    st.markdown("### Coverage & Gaps")
    st.markdown(
        "Where do authoritative methods exist? Each cell shows the **best (lowest-numbered) "
        "tier** available for a matrix and monitoring workflow step, followed by the number "
        "of references. Red cells have no matching reference. Coverage describes the "
        "**authority** of available resources, not their scientific quality, and a cell's "
        "best tier may not match your particle size range or instrument. Open the path in "
        "the Decision Tree to check."
    )

    control_cols = st.columns([1.2, 1])
    with control_cols[0]:
        scope = st.radio(
            "References counted",
            ["Matrix-specific only", "Include cross-cutting documents"],
            horizontal=True,
            key="coverage_scope",
            help=(
                "Matrix-specific: tagged with the matrix or scored in its matrix column by the "
                "curators. Cross-cutting documents apply across matrices (e.g., general "
                "terminology or QA/QC standards) and are also shown in the Decision Tree."
            ),
        )
    with control_cols[1]:
        particle_keys = st.multiselect(
            "Restrict to particle/polymer type",
            list(PARTICLE_TYPES.keys()),
            format_func=lambda key: PARTICLE_TYPES[key]["label"],
            key="coverage_particle_type",
        )

    specific_only = scope == "Matrix-specific only"
    coverage = monitoring_coverage(df, particle_keys)
    tiers, labels = coverage_table(coverage, specific_only=specific_only)

    styled = labels.style.apply(
        lambda column: [_cell_style(t) for t in tiers[column.name]], axis=0
    )
    st.dataframe(styled, width="stretch")

    tier_col = "specific_tier" if specific_only else "tier"
    total = len(coverage)
    strong = int(coverage[tier_col].isin([1, 2]).sum())
    missing = int(coverage[tier_col].isna().sum())
    lacking = (
        coverage.groupby("matrix")[tier_col]
        .apply(lambda s: not s.isin([1, 2]).any())
    )
    lacking_matrices = [m["label"] for m in MATRICES.values() if lacking.get(m["label"], False)]

    summary = (
        f"{strong} of {total} matrix × step combinations have a Tier 1 or 2 reference; "
        f"{missing} have no matching reference"
        + (f" for the selected particle type(s)" if particle_keys else "")
        + "."
    )
    st.info(summary)
    if lacking_matrices:
        st.warning(
            "No Tier 1/2 reference at any monitoring step: " + ", ".join(lacking_matrices) + "."
        )

    with st.expander("How this table is computed"):
        st.markdown(
            "- References are filtered exactly as in the Decision Tree's Monitoring branch: "
            "Primary Domain is Monitoring, Both, or Cross-cutting; the matrix filter keeps "
            "references tagged with the matrix, scored in its `Matrix: …` column, or tagged "
            "Cross-cutting; each step keeps references scored in that step's topic column(s).\n"
            "- **Matrix-specific only** drops references that entered only through a "
            "Cross-cutting tag. This is the closer analogue of the manuscript's Figure 2, "
            "which counts references scored in each matrix column.\n"
            "- Matrix-conditional tier adjustments (see About → How results are selected and "
            "ordered) are applied before the best tier is taken.\n"
            "- The table recalculates from `crosswalk.xlsx` on every load, so it changes as "
            "references are added or re-tiered."
        )

    csv = coverage.to_csv(index=False)
    st.download_button(
        "📥 Export coverage table",
        csv,
        file_name="mnp_compass_coverage.csv",
        mime="text/csv",
    )
