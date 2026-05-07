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
    INSTRUMENTS,
    MATRICES,
    MONITORING_AUXILIARY,
    MONITORING_CORE,
    PARTICLE_TYPES,
    RA_AUXILIARY,
    RA_CORE,
    RECEPTORS,
    TOX_AUXILIARY,
    TOX_CORE,
    _apply_step_filters,
    _doc_type_options,
    _filter_domain,
    _filter_matrix,
    _filter_particle_types,
    _filter_primary_focus,
    _filter_problem_formulation,
    _filter_target_receptor,
    _instrument_availability,
    _normalize_abstract_text,
    _ra_core_for_receptor,
    _reference_context_messages,
    _ensure_graphviz_dot_on_path,
    _zoomable_svg_html,
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
        "Primary Focus",
        "Target Receptor(s)",
        "Particle/Polymer Type Tags",
        "Scope",
        "Status",
        "Key Metrics / Output",
        "Abstract",
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
        check("splines=polyline" in dot, "Decision Tree uses polyline graph routing", errors)
        check("URL=" not in dot, "Decision Tree graph nodes are not clickable", errors)
        check("target=" not in dot, "Decision Tree graph nodes do not navigate iframes", errors)
        analysis_dot = build_graphviz(
            domain="Monitoring",
            matrix_key="drinking_water",
            core_step_key="analysis",
            aux_step_key="definitions",
            availability=availability,
        )
        check(
            "CORE_BEFORE" in analysis_dot and "CORE_AFTER" in analysis_dot,
            "Monitoring Analysis graph collapses non-selected core steps",
            errors,
        )
        check(
            "CORE_SAMPLING" not in analysis_dot and "CORE_REPORTING" not in analysis_dot,
            "Monitoring Analysis graph hides individual non-selected core nodes",
            errors,
        )
        zoom_html = _zoomable_svg_html(
            '<svg width="100pt" height="50pt" viewBox="0 0 100 50"></svg>',
            450,
        )
        check(
            "svg-pan-zoom@3.6.1" in zoom_html,
            "Zoomable diagram loads svg-pan-zoom from CDN",
            errors,
        )
        check(
            'width="100%"' in zoom_html and 'height="100%"' in zoom_html,
            "Zoomable diagram SVG fills its container",
            errors,
        )
        check(
            "ResizeObserver" in zoom_html and "diagram-height: 450px" in zoom_html,
            "Zoomable diagram reacts to component height changes",
            errors,
        )
        check(
            _ensure_graphviz_dot_on_path(),
            "Graphviz dot executable is discoverable for zoomable rendering",
            errors,
        )
        check(
            "controlIconsEnabled: true" in zoom_html
            and "fit: true" in zoom_html
            and "center: true" in zoom_html
            and "zoomScaleSensitivity: 0.3" in zoom_html,
            "Zoomable diagram enables requested pan/zoom settings",
            errors,
        )
        visual_tree_source = (base_dir / "visual_tree_tab.py").read_text(encoding="utf-8")
        check(
            "components.html" not in visual_tree_source,
            "Zoomable diagram avoids deprecated HTML component API",
            errors,
        )

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

        check(
            "interlaboratory" not in {step["key"] for step in MONITORING_AUXILIARY},
            "Monitoring interlaboratory studies are not an auxiliary workflow box",
            errors,
        )
        check(
            [step["key"] for step in MONITORING_CORE][-2:] == ["data_stats", "reporting"],
            "Monitoring workflow places Data Analysis before Reporting",
            errors,
        )
        check(
            "subsampling" in [step["key"] for step in MONITORING_CORE],
            "Monitoring workflow includes Sub-sampling",
            errors,
        )
        check(
            {"wastewater", "biosolids"}.issubset(MATRICES),
            "Decision Tree includes Wastewater and Biosolids matrix options",
            errors,
        )
        check(
            "imaging" in INSTRUMENTS,
            "Decision Tree includes Visual / SEM / Imaging instrument option",
            errors,
        )
        particle_filtered = _filter_particle_types(
            nav_monitoring, list(PARTICLE_TYPES.keys())[:1]
        )
        check(
            len(particle_filtered) <= len(nav_monitoring),
            "Decision Tree particle/polymer type filter is bounded",
            errors,
        )

        tox_keys = [step["key"] for step in TOX_CORE]
        check(
            tox_keys[:3] == ["ref_particles", "particle_char", "dosimetry"],
            "Toxicology workflow orders reference particles before characterization and dosimetry",
            errors,
        )
        check(
            tox_keys[-2:] == ["tox_reporting", "data_repository"],
            "Toxicology workflow places Data Repository after Reporting",
            errors,
        )

        tox_df = _filter_domain(df, "Toxicology")
        human_tox = _filter_target_receptor(
            tox_df, RECEPTORS["human_health"]["kw"]
        )
        eco_tox = _filter_target_receptor(
            tox_df, RECEPTORS["ecotoxicology"]["kw"]
        )
        in_vitro_tox = _filter_target_receptor(
            tox_df, RECEPTORS["in_vitro"]["kw"]
        )
        check(len(human_tox) > 0, "Toxicology Human Health receptor filter returns rows", errors)
        check(len(eco_tox) > 0, "Toxicology Ecotoxicology receptor filter returns rows", errors)
        check(len(in_vitro_tox) > 0, "Toxicology In Vitro receptor filter returns rows", errors)
        ref_particles_step = next(
            step for step in TOX_CORE if step["key"] == "ref_particles"
        )
        ref_particles = _apply_step_filters(human_tox, ref_particles_step)
        ref_particles_primary = _filter_primary_focus(
            human_tox, "Reference Materials"
        )
        ref_particle_citations = set(
            ref_particles["Short Citation"].astype(str).str.strip()
        )
        check(
            len(ref_particles) > len(ref_particles_primary),
            "Toxicology reference particle selection uses column/keyword fallback",
            errors,
        )
        check(
            "Gouin et al., 2024" in ref_particle_citations,
            "Toxicology reference particle selection includes quality critiques of PS spheres",
            errors,
        )
        check(
            "interlaboratory" not in {step["key"] for step in TOX_AUXILIARY},
            "Toxicology interlaboratory studies are not a workflow box",
            errors,
        )
        check(
            "interlaboratory" not in {step["key"] for step in RA_AUXILIARY},
            "Risk Assessment interlaboratory studies are not a workflow box",
            errors,
        )
        tox_dot = build_graphviz(
            domain="Toxicology",
            receptor_key="human_health",
            core_step_key="effects",
            aux_step_key="definitions",
        )
        ra_dot = build_graphviz(
            domain="Risk Assessment",
            receptor_key="human_health",
            core_step_key="hazard",
            aux_step_key="definitions",
        )
        check(
            "{ rank=same; AUX_DEFINITIONS; AUX_QUALITY }" in tox_dot,
            "Toxicology auxiliary nodes are constrained to the same rank",
            errors,
        )
        check(
            "{ rank=same; AUX_DEFINITIONS }" in ra_dot,
            "Risk Assessment auxiliary nodes are constrained to the same rank",
            errors,
        )
        ra_df = _filter_domain(df, "Risk Assessment")
        human_ra = _filter_target_receptor(
            ra_df, RECEPTORS["human_health"]["kw"]
        )
        eco_ra = _filter_target_receptor(
            ra_df, RECEPTORS["ecotoxicology"]["kw"]
        )
        human_ra_keys = [step["key"] for step in _ra_core_for_receptor("human_health")]
        eco_ra_keys = [step["key"] for step in _ra_core_for_receptor("ecotoxicology")]
        check(
            human_ra_keys[human_ra_keys.index("exposure") + 1] == "pbpk",
            "Human Health Risk Assessment places PBPK after exposure",
            errors,
        )
        check(
            human_ra_keys[human_ra_keys.index("pbpk") + 1] == "risk_char",
            "Human Health Risk Assessment places PBPK before risk characterization",
            errors,
        )
        check(
            "pbpk" not in eco_ra_keys,
            "Ecotoxicology Risk Assessment does not show PBPK workflow step",
            errors,
        )
        pbpk_step = next(step for step in RA_CORE if step["key"] == "pbpk")
        pbpk_refs = _apply_step_filters(human_ra, pbpk_step)
        check(
            "Wardani et al., 2024" in set(pbpk_refs["Short Citation"].astype(str)),
            "Human Health PBPK step filters Primary Focus == PBPK Modelling",
            errors,
        )
        check(
            len(_apply_step_filters(eco_ra, pbpk_step)) == 0,
            "Ecotoxicology PBPK filter has no receptor-matched rows",
            errors,
        )
        data_repo_step = next(
            step for step in TOX_CORE if step["key"] == "data_repository"
        )
        data_repo_short_citations = set(
            _apply_step_filters(human_tox, data_repo_step)["Short Citation"]
            .astype(str)
            .str.strip()
        )
        check(
            {
                "Thornton Hampton et al., 2022a",
                "Thornton Hampton et al., 2025",
            }.issubset(data_repo_short_citations),
            "Toxicology Data Repository includes Thornton Hampton repository entries",
            errors,
        )
        normalized_abstract = _normalize_abstract_text(
            "Abstract\n • First point\n - Second point\t with spacing"
        )
        check(
            normalized_abstract == "First point Second point with spacing",
            "Decision Tree abstract display normalizes whitespace and bullets",
            errors,
        )
        check(
            len(_filter_problem_formulation(df)) > 0,
            "Problem Formulation interactive node returns cross-cutting rows",
            errors,
        )
        problem_doc_types = _doc_type_options(_filter_problem_formulation(df))
        check(
            "Method / Protocol" in problem_doc_types
            and "Guideline / Best Practice" in problem_doc_types,
            "Problem Formulation document type selector has expected options",
            errors,
        )
        dot_with_problem = build_graphviz(
            domain="Monitoring",
            matrix_key="drinking_water",
            core_step_key="sampling",
            aux_step_key="definitions",
            availability={"PF": {"count": 1, "tier": 1, "active": False}},
        )
        check(
            'URL="?tree_problem=1"' not in dot_with_problem,
            "Problem Formulation node is display-only in graph",
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
