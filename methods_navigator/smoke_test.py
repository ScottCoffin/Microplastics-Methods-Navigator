"""
Headless smoke test for the Microplastics Methods Navigator.

Run from methods_navigator/:
    python smoke_test.py
"""

import py_compile
import sys
from pathlib import Path

import pandas as pd

from app import (
    filter_by_domain,
    filter_by_matrix,
    filter_by_topic_column,
    load_crosswalk,
    load_tree,
)
from visual_tree_tab import (
    MATRICES,
    MONITORING_AUXILIARY,
    MONITORING_CORE,
    _apply_step_filters,
    _filter_domain,
    _filter_matrix,
    _instrument_availability,
    _reference_context_messages,
    _workflow_availability,
    build_graphviz,
)


def check(condition, message, errors):
    if condition:
        print(f"OK: {message}")
    else:
        print(f"FAIL: {message}")
        errors.append(message)


def main():
    errors = []
    base_dir = Path(__file__).resolve().parent

    for filename in [
        "crosswalk.xlsx",
        "tree_structure.yaml",
        "app.py",
        "visual_tree_tab.py",
        "crosswalk_tab.py",
    ]:
        check((base_dir / filename).exists(), f"{filename} exists", errors)

    for filename in ["app.py", "visual_tree_tab.py", "crosswalk_tab.py"]:
        try:
            py_compile.compile(str(base_dir / filename), doraise=True)
            print(f"OK: {filename} compiles")
        except py_compile.PyCompileError as exc:
            print(f"FAIL: {filename} compile error: {exc.msg}")
            errors.append(f"{filename} compile error")

    try:
        tree = load_tree()
        check(isinstance(tree, dict), "tree_structure.yaml loads", errors)
        check("root" in tree, "tree has root node", errors)
        check("gap_notes" in tree, "tree has gap notes", errors)
    except Exception as exc:
        print(f"FAIL: tree load error: {exc}")
        errors.append("tree load error")
        tree = None

    try:
        df = load_crosswalk()
        print(f"OK: crosswalk loaded with {len(df)} entries and {len(df.columns)} columns")
    except Exception as exc:
        print(f"FAIL: crosswalk load error: {exc}")
        return 1

    required = [
        "Short Citation",
        "Document Type",
        "Priority Tier",
        "Key Notes",
        "Primary Domain",
        "Instrumentation Tags",
        "Matrix Tags",
        "tier_num",
    ]
    for column in required:
        check(column in df.columns, f"column present: {column}", errors)

    tier_counts = df["tier_num"].value_counts(dropna=False).sort_index()
    print(f"OK: tier distribution: {tier_counts.to_dict()}")
    check(tier_counts.sum() == len(df), "tier count covers all rows", errors)

    monitoring = filter_by_domain(df, "Monitoring")
    check(len(monitoring) > 0, "Monitoring domain filter returns rows", errors)

    drinking_water = filter_by_matrix(monitoring, "Drinking Water")
    check(len(drinking_water) > 0, "Drinking Water matrix filter returns rows", errors)

    sampling = filter_by_topic_column(drinking_water, "Sampling (Field Methods)")
    check(len(sampling) > 0, "Sampling topic filter returns rows", errors)

    try:
        nav_monitoring = _filter_domain(df, "Monitoring")
        matrix_df = _filter_matrix(
            nav_monitoring, MATRICES["drinking_water"]["kw"]
        )
        core_results = _apply_step_filters(matrix_df, MONITORING_CORE[0])
        aux_results = _apply_step_filters(matrix_df, MONITORING_AUXILIARY[0])
        availability = {}
        availability.update(
            _workflow_availability(matrix_df, MONITORING_CORE, "CORE")
        )
        availability.update(
            _workflow_availability(matrix_df, MONITORING_AUXILIARY, "AUX")
        )
        availability.update(_instrument_availability(matrix_df))
        dot = build_graphviz(
            domain="Monitoring",
            matrix_key="drinking_water",
            core_step_key="sampling",
            aux_step_key="definitions",
            availability=availability,
        )
        check(len(core_results) > 0, "Decision Tree core result returns rows", errors)
        check(len(aux_results) > 0, "Decision Tree auxiliary result returns rows", errors)
        check("Tier 1\\n" in dot, "Decision Tree node tier labels render on separate lines", errors)
        check("AUX_DEFINITIONS" in dot, "Decision Tree auxiliary node renders", errors)

        air_df = _filter_matrix(nav_monitoring, MATRICES["air"]["kw"])
        extraction_step = next(
            step for step in MONITORING_CORE if step["key"] == "extraction"
        )
        air_extraction = _apply_step_filters(air_df, extraction_step)
        context_messages = [
            text for _, text in _reference_context_messages(air_extraction)
        ]
        check(
            any(
                "No Tier 1/2 references match this selected path" in text
                for text in context_messages
            ),
            "Decision Tree detects no Tier 1/2 coverage dynamically",
            errors,
        )
        check(
            not any("Ashta" in text for text in context_messages),
            "Decision Tree context avoids single hardcoded best-available citation",
            errors,
        )

        age_test = _reference_context_messages(
            pd.DataFrame({"Year": [2020, 2024], "tier_num": [1, 3]})
        )
        check(
            any(
                "Newest Tier 1 reference is from 2020" in text
                for _, text in age_test
            ),
            "Decision Tree warns when top-tier coverage is older than 2021",
            errors,
        )
    except Exception as exc:
        print(f"FAIL: decision tree smoke error: {exc}")
        errors.append("decision tree smoke error")

    if tree:
        print(f"OK: gap notes loaded: {len(tree.get('gap_notes', {}))}")

    print("\n" + "=" * 50)
    if errors:
        print(f"SMOKE TEST FAILED: {len(errors)} error(s)")
        for error in errors:
            print(f" - {error}")
        return 1

    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
