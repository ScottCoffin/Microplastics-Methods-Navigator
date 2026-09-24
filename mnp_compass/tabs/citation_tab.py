"""Citation, license, and codebase information tab for MNP Compass."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

_WWW_DIR = Path(__file__).resolve().parent.parent / "www"
_GRAPHICAL_ABSTRACT = _WWW_DIR / "graphical_abstract.png"

try:
    from tabs.visual_tree_tab import (
        INSTRUMENTS, MATRICES, MATRIX_TIER_OVERRIDES, MONITORING_AUXILIARY,
        MONITORING_CORE, PARTICLE_TYPES, RA_CORE, TEST_SYSTEMS, TOX_AUXILIARY,
        TOX_CORE,
    )
except ImportError:  # imported as mnp_compass.tabs.citation_tab (tests)
    from mnp_compass.tabs.visual_tree_tab import (
        INSTRUMENTS, MATRICES, MATRIX_TIER_OVERRIDES, MONITORING_AUXILIARY,
        MONITORING_CORE, PARTICLE_TYPES, RA_CORE, TEST_SYSTEMS, TOX_AUXILIARY,
        TOX_CORE,
    )

# PAPER_TITLE is the single constant used both for the "Companion Publication"
# info box and the "Suggested Citation" text below — do not retype the title
# in a second place. Source: NanoImpact decision letter for IMPACT-D-26-00454
# (major revision, 2026). Update PAPER_STATUS / PAPER_JOURNAL / DOI on acceptance.
PAPER_TITLE = (
    "MNP Compass: a resource for coordinating micro-/nano-plastics research, "
    "reporting, and publication criteria across disciplines"
)
PAPER_JOURNAL = "NanoImpact"
PAPER_STATUS = "in revision"

AUTHORS = [
    {
        "name": "Granek, Elise F.",
        "affiliation": "Environmental Science & Management, Portland State University, Oregon, USA",
    },
    {
        "name": "Coffin, Scott",
        "affiliation": (
            "Office of Environmental Health Hazard Assessment, "
            "1001 I. St., Sacramento, California, 95814, United States of America"
        ),
    },
    {
        "name": "Brander, Susanne M.",
        "affiliation": (
            "Oregon State University, College of Agricultural Sciences, "
            "Corvallis, Oregon, 97331, USA"
        ),
    },
    {
        "name": "Seeley, Meredith Evans",
        "affiliation": (
            "Virginia Institute of Marine Science, William & Mary, "
            "Gloucester Point, VA 23062, USA"
        ),
    },
    {
        "name": "Thornton Hampton, Leah M.",
        "affiliation": (
            "Toxicology Department, Southern California Coastal Water Research Project, "
            "3535 Harbor Blvd. Suite 110, Costa Mesa, CA, 92626-1437, USA"
        ),
    },
    {
        "name": "El Hayek, Eliane",
        "affiliation": (
            "Department of Pharmaceutical Sciences, University of New Mexico, "
            "College of Pharmacy, MSC09 5360, Albuquerque, New Mexico 87131, USA"
        ),
    },
    {
        "name": "Walker, Vickie R.",
        "affiliation": "",
    },
    {
        "name": "Wagner, Martin",
        "affiliation": "",
    },
    {
        "name": "Gouin, Todd",
        "affiliation": "",
    },
    {
        "name": "Gray, Andrew B.",
        "affiliation": (
            "Department of Environmental Sciences, University of California, Riverside, "
            "Riverside, California, 92521, USA"
        ),
    },
    {
        "name": "Harper, Stacey L.",
        "affiliation": (
            "Oregon State University, College of Agricultural Sciences / College of Engineering, "
            "Corvallis, Oregon, 97331, USA"
        ),
    },
    {
        "name": "Rooney, Andrew A.",
        "affiliation": "",
    },
]

GITHUB_URL = "https://github.com/ScottCoffin/MNP-Compass"

GITHUB_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
     fill="currentColor" style="vertical-align:middle; margin-right:6px;">
  <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577
           v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756
           -1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237
           1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604
           -2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221
           -.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23
           A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404
           2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176
           .77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921
           .43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576
           C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
</svg>"""

AGPL_TEXT = """\
This tool is released under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

The AGPL-3.0 is a copyleft license that requires anyone who runs a modified version of this
software over a network to make the complete corresponding source code available.

Key conditions:
- **Use** — Free to use for any purpose.
- **Distribute** — May distribute copies of the original or modified software.
- **Modify** — May modify the source code, but modifications must also be released under AGPL-3.0.
- **Network use** — If you deploy a modified version as a web service, you must provide the
  source code to users of that service.
- **Attribution** — The original copyright notice and license must be preserved.

Full license text: https://www.gnu.org/licenses/agpl-3.0.html
"""


def _about_text(reference_count):
    """Build the About-tab intro paragraph.

    The reference count is computed at runtime from the loaded crosswalk
    dataframe (same source the Crosswalk tab's live count uses) so this text
    can never drift from the actual data the way a hardcoded number would.
    """
    count_phrase = str(reference_count) if reference_count is not None else "150+"
    return (
        "MNP Compass is an interactive decision-tree web tool for "
        "researchers designing microplastics monitoring, toxicology, or risk assessment studies. "
        "Users step through their study type, environmental matrix (drinking water, sediment, "
        "biota, air, food, soil, and others), and workflow step (sampling, extraction, analytical "
        "identification, QA/QC, reporting) to retrieve a curated, ranked list of methods, "
        f"standards, and guidance documents drawn from a crosswalk of {count_phrase} seminal "
        "references in microplastics research. Results are grouped by a four-tier authority and "
        "validation framework — described in detail below — and displayed with document type, "
        "key notes, and direct links, with the option to export filtered results to CSV. "
        "Worked examples (Quick Start), a live map of where authoritative methods exist and "
        "where they are missing (Coverage & Gaps), a full-text search across all references, "
        "and a domain glossary are also available."
    )

# Canonical tier definitions for the whole app. README.md's tier section is a manual
# verbatim quote of TIER_FRAMEWORK_INTRO / TIER_FRAMEWORK_TIERS / TIER_FRAMEWORK_OUTRO —
# if you change the wording here, update README.md's "Authority and Validation Tier
# Framework" section to match, and vice versa. Do not retype tier definitions elsewhere.
TIER_FRAMEWORK_INTRO = (
    "To organize resources that differ substantially in their institutional status and degree "
    "of methodological validation, MNP Compass classifies each resource using a four-tier "
    "**authority and validation framework**. The tiers are intended to characterize the basis "
    "and strength of a resource's authority, rather than its overall scientific quality, "
    "utility, or currency; consequently, a lower-tier resource may be more current or more "
    "applicable to a particular research question than a higher-tier resource."
)

TIER_FRAMEWORK_TIERS = [
    (
        "🟢 Tier 1 — Normative / Binding",
        "Requirements, procedures, or methods that carry a formal legal, regulatory, or "
        "institutional mandate within a defined jurisdiction or program. Examples include "
        "legislation and regulations, regulatory decisions, and standardized methods or "
        "standard operating procedures required for regulatory compliance, accreditation, "
        "or official monitoring.",
    ),
    (
        "🔵 Tier 2 — Authoritative / Institutional",
        "Standards, methods, guidance, and other resources formally issued or endorsed by "
        "recognized standards-development organizations, governmental or intergovernmental "
        "bodies, or comparable institutions, but that are not themselves mandatory in the "
        "relevant application. Examples include ISO and ASTM standards and formal guidance "
        "from organizations such as WHO, EFSA, GESAMP, NIST, and similar bodies.",
    ),
    (
        "🟡 Tier 3 — Validated / Interlaboratory-Tested / Critical Guidance",
        "Resources supported by substantial empirical or evidence-synthesis-based evaluation "
        "but lacking the formal mandate or institutional status of Tiers 1 and 2. This category "
        "includes methods evaluated through interlaboratory comparison, proficiency testing, or "
        "quantitative validation, as well as critical or systematic reviews that establish "
        "evidence-based QA/QC criteria, performance criteria, or methodological recommendations.",
    ),
    (
        "⚪ Tier 4 — Supporting / Contextual",
        "Resources that provide useful methodological, scientific, or interpretive context but "
        "have not undergone the level of validation or evidence synthesis represented by Tier 3 "
        "and do not carry the formal institutional authority of Tiers 1 or 2. Examples include "
        "emerging or single-laboratory methods, research tools and databases, narrative reviews, "
        "perspectives, frameworks, and other supporting literature.",
    ),
]

TIER_FRAMEWORK_OUTRO = (
    "The resulting classification therefore represents a gradient from formally binding "
    "requirements to supporting scientific context, rather than a numerical score of study or "
    "resource quality. MNP Compass presents resources across tiers so that users can consider "
    "formal authority alongside factors such as methodological relevance, recency, "
    "applicability, and available resources."
)

# Concrete cases where a lower-tier resource fits a study better than a higher-tier one.
# Named references and tiers are checked against crosswalk.xlsx by tests/smoke_test.py
# (LOWER_TIER_EXAMPLE_TIERS) — update both together.
LOWER_TIER_EXAMPLES = [
    (
        "Particle size outside the higher-tier method's scope",
        "The Tier 1 drinking-water methods (California SWB-MP2, Wong & Coffin, 2022b; EU "
        "Delegated Decision 2024/1441, European Commission, 2024) cover 20 µm–5 mm. A study of "
        "smaller particles needs a method whose validated range extends lower, such as "
        "ISO 16094-2:2025 (Tier 2; 1 µm–5 mm in low-turbidity water). Below that range, and "
        "for nanoplastics, only Tier 3–4 resources exist.",
    ),
    (
        "Matrix outside the higher-tier method's scope",
        "Tier 1–2 spectroscopy methods were developed for drinking water and other "
        "low-turbidity waters. For human blood, the most applicable resources are Tier 4 "
        "single-laboratory studies. Rauert et al. (2025) found that Py-GC-MS is currently "
        "unsuitable for polyethylene and PVC in biological matrices because of matrix "
        "interferences, a finding that should shape any blood study even though it carries "
        "less formal authority than a drinking-water SOP.",
    ),
    (
        "Study purpose",
        "The Tier 2 certified reference material EURM-060 (JRC, 2025; ~10 µm PET in water) "
        "suits recovery checks for drinking-water methods. A toxicity test intended to reflect "
        "environmental exposure is better served by Tier 3 protocols for environmentally "
        "relevant particle mixtures (De Ruijter et al., 2025a), and Tier 4 commentary explains "
        "why polystyrene spheres are of limited relevance (Gouin et al., 2024).",
    ),
    (
        "Jurisdiction",
        "Tier 1 status applies only within a jurisdiction and program. A method binding for "
        "California or EU drinking water is not binding for a different matrix or country. "
        "MNP Compass records this where it matters: Sherrod et al. (2024) is ranked Tier 1 "
        "under Monitoring → Drinking Water and Tier 3 under the other monitoring matrices.",
    ),
    (
        "Currency",
        "Standards take years to revise. When the newest reference at the best available "
        "tier predates 2021, the app warns that newer lower-tier work may update the approach.",
    ),
    (
        "Resources and instrumentation",
        "A Tier 1 SOP presumes specific instruments, sample volumes, and staff time. A "
        "laboratory without them may reasonably adopt a validated Tier 3 method it can run "
        "well, provided the choice and its validation data are reported transparently.",
    ),
]
LOWER_TIER_EXAMPLE_TIERS = {
    "Wong & Coffin, 2022b": 1,
    "European Commission, 2024": 1,
    "ISO 16094-2:2025": 2,
    "Rauert et al., 2025": 4,
    "JRC, 2025 (EURM-060)": 2,
    "De Ruijter et al., 2025a": 3,
    "Gouin et al., 2024": 4,
    "Sherrod et al., 2024": 1,
}

CURATION_TEXT = (
    "References were assembled from the best-practice and QA/QC syntheses that underpin the "
    "companion manuscript, together with the author team's expertise across ecotoxicology, "
    "human-health toxicology, analytical chemistry, environmental monitoring, and risk "
    "assessment. A resource was included if it can serve as a method, standard, guidance "
    "document, reference material, database, or critical or evidence-synthesis review for a "
    "specific step of an MNP study. The crosswalk is a curated map of that literature, "
    "**not an exhaustive systematic review**.\n\n"
    "Each reference was assigned one authority tier by a single author applying the "
    "framework above. Tier boundaries are interpretive, so some assignments are open to "
    "debate. Each reference was then tagged by domain, matrix, instrumentation, particle "
    "type, and target receptor, and scored in every topic column (workflow step, matrix, "
    "analytical technique) it addresses. A topic score normally equals the document's tier; "
    "it can differ by matrix where authority is matrix- or jurisdiction-specific."
)


def _describe_step_filter(step):
    """Plain-language description of a Decision Tree step's filter, built from its config."""
    parts = []
    if "column" in step:
        parts.append(f"scored in `{step['column']}`")
    if "columns" in step:
        parts.append("scored in any of " + ", ".join(f"`{c}`" for c in step["columns"]))
    if "keywords" in step:
        parts.append(
            "Key Notes mention any of: " + ", ".join(k.strip() for k in step["keywords"].split(";"))
        )
    joiner = " **or** " if "primary_focus" in step and parts else " **and** "
    if "primary_focus" in step:
        parts.insert(0, f"Primary Focus contains \"{step['primary_focus']}\"")
    return joiner.join(parts)


def _render_ranking_method():
    st.markdown(
        "Every Decision Tree result list is produced by the same deterministic filter chain. "
        "There is no relevance score, weighting, or machine learning, so any result can be "
        "traced to the columns of `crosswalk.xlsx`.\n\n"
        "1. **Study type:** keep references whose Primary Domain is the selected study type, "
        "`Both`, or `Cross-cutting`.\n"
        "2. **Context.** *Monitoring:* keep references tagged with the selected matrix, scored "
        "in its `Matrix: …` column, or tagged `Cross-cutting`; the last group is marked "
        "🌐 cross-cutting in results. An optional particle/polymer-type filter keeps "
        "references matching **any** selected type. *Toxicology and Risk Assessment:* keep "
        "references whose Target Receptor(s) include the selected receptor, are "
        "`Cross-cutting`/`Both`, or are blank (untagged references are kept rather than "
        "hidden).\n"
        "3. **Workflow step:** keep references scored in the step's topic column(s). "
        "Analytical techniques match Instrumentation Tags; some steps also use Key Notes "
        "keywords or Primary Focus (exact rules below).\n"
        "4. **Matrix-conditional tiers (Monitoring only):** a small number of references carry "
        "a different tier depending on the selected matrix (listed below).\n"
        "5. **Ordering:** sort by tier (Tier 1 first), then by publication year (newest "
        "first). Nothing else affects order within a tier.\n"
        "6. **Automated context messages:** the app warns when no Tier 1/2 reference matches, "
        "when the newest reference at the best available tier predates 2021, and when the "
        "best tier comes only from cross-cutting documents rather than matrix-specific ones.\n\n"
        "Diagram node colors show the best (lowest-numbered) tier among a node's references. "
        "The **Search All References** tab keeps references containing **all** search terms "
        "and applies the same ordering."
    )

    with st.expander("Exact filter rules for every Decision Tree step"):
        groups = [
            ("Monitoring — core workflow", MONITORING_CORE),
            ("Monitoring — auxiliary support", MONITORING_AUXILIARY),
            ("Toxicology — core workflow", TOX_CORE),
            ("Toxicology — auxiliary support", TOX_AUXILIARY),
            ("Risk Assessment", RA_CORE),
        ]
        for heading, steps in groups:
            st.markdown(f"**{heading}**")
            st.markdown(
                "\n".join(f"- {s['label']}: {_describe_step_filter(s)}" for s in steps)
            )
        st.markdown("**Matrices** (Matrix Tags keyword · matrix column)")
        st.markdown(
            "\n".join(f"- {m['label']}: \"{m['kw']}\" · `{m['column']}`" for m in MATRICES.values())
        )
        st.markdown("**Analytical techniques** (Instrumentation Tags contain any of)")
        st.markdown(
            "\n".join(f"- {i['label']}: {i['kw'].replace(';', ', ')}" for i in INSTRUMENTS.values())
        )
        st.markdown("**Toxicology test systems** (Key Notes mention any of)")
        st.markdown(
            "\n".join(
                f"- {t['label']}: {t['keywords'].replace(';', ', ')}" for t in TEST_SYSTEMS.values()
            )
        )
        st.markdown("**Particle/polymer types** (Particle/Polymer Type Tags contain any of)")
        st.markdown(
            "\n".join(f"- {p['label']}: {p['kw'].replace(';', ', ')}" for p in PARTICLE_TYPES.values())
        )

    st.markdown("**Matrix-conditional tier assignments**")
    st.markdown(
        "\n".join(
            f"- References matching \"{fragment}\": "
            + ", ".join(
                f"Tier {tier} for {'all other matrices' if matrix == 'default' else matrix}"
                for matrix, tier in overrides.items()
            )
            for fragment, overrides in MATRIX_TIER_OVERRIDES.items()
        )
    )


def _render_growth_section(reference_count):
    st.markdown(
        "MNP Compass is designed to change as the field does. All "
        + (f"{reference_count} " if reference_count else "")
        + "references live in one openly licensed, version-controlled spreadsheet "
        "(`mnp_compass/data/crosswalk.xlsx`). Result lists, diagram colors, the Coverage & "
        "Gaps table, and all counts are recalculated from it on every load, so adding or "
        "re-tiering a reference needs no code changes.\n\n"
        f"- **Suggest a reference, correction, or re-tiering:** open an issue at "
        f"[{GITHUB_URL}/issues]({GITHUB_URL}/issues), or submit a pull request that edits "
        "the spreadsheet (see `CONTRIBUTING.md`). Maintainers review every tier assignment "
        "before merging and ask contributors to cite the tier criterion a resource meets.\n"
        "- **New categories** (a new matrix, technique, particle type, or workflow step) are "
        "added in the app configuration and discussed in an issue first.\n"
        "- **History:** every change to the data and code is recorded in the repository's "
        "commit history, so earlier versions of any result list can be reproduced."
    )


def render_citation_tab(df=None):
    """Render the citation, codebase, and license tab.

    `df` is the loaded crosswalk dataframe (same one the Crosswalk tab
    displays), passed in so the reference count in the About text is
    computed live rather than hardcoded.
    """

    # ── About ────────────────────────────────────────────────────────────────
    st.markdown("### About This Tool")
    if _GRAPHICAL_ABSTRACT.exists():
        _img_col, _ = st.columns([1, 2])
        with _img_col:
            st.image(str(_GRAPHICAL_ABSTRACT), caption=f"Granek et al. ({PAPER_STATUS}). Graphical Abstract", width="stretch")
    reference_count = len(df) if df is not None else None
    st.markdown(_about_text(reference_count))

    st.divider()

    # ── Authority and Validation Tier Framework ────────────────────────────────
    st.markdown("### Authority and Validation Tier Framework")
    st.markdown(TIER_FRAMEWORK_INTRO)
    for title, description in TIER_FRAMEWORK_TIERS:
        st.markdown(f"**{title}**")
        st.markdown(description)
    st.markdown(TIER_FRAMEWORK_OUTRO)

    st.markdown("#### When a lower-tier resource may be the better choice")
    for heading, body in LOWER_TIER_EXAMPLES:
        st.markdown(f"- **{heading}.** {body}")

    st.divider()

    st.markdown("### How the Crosswalk Was Compiled and Tiered")
    st.markdown(CURATION_TEXT)

    st.divider()

    st.markdown("### How Results Are Selected and Ordered")
    _render_ranking_method()

    st.divider()

    st.markdown("### How MNP Compass Grows")
    _render_growth_section(reference_count)

    st.divider()

    # ── Paper citation ───────────────────────────────────────────────────────
    st.markdown("### Companion Publication")
    st.markdown(
        f"This tool accompanies the following manuscript *({PAPER_STATUS}, {PAPER_JOURNAL})*:"
    )

    st.info(f"**{PAPER_TITLE}**", icon="📄")

    # Author list
    st.markdown("#### Authors")
    for i, author in enumerate(AUTHORS, start=1):
        st.markdown(
            f"<div style='margin-bottom:4px;'>"
            f"<strong>{i}. {author['name']}</strong>"
            f"<br/><span style='color:#555; font-size:0.88em;'>{author['affiliation']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Formatted draft citation block
    st.markdown("#### Suggested Citation *(draft — update with journal/DOI when published)*")
    author_short = (
        "Granek, E.F., Coffin, S., Brander, S.M., Seeley, M.E., "
        "Thornton Hampton, L.M., El Hayek, E., Walker, V.R., Wagner, M., "
        "Gouin, T., Gray, A.B., Harper, S.L., & Rooney, A.A."
    )
    citation_text = (
        f"{author_short} ({PAPER_STATUS}). {PAPER_TITLE}. "
        f"{PAPER_JOURNAL}. DOI: TBD"
    )
    st.code(citation_text, language=None)

    st.divider()

    # ── Codebase ─────────────────────────────────────────────────────────────
    st.markdown("### Codebase")
    st.markdown(
        f"{GITHUB_LOGO_SVG}"
        f"<a href='{GITHUB_URL}' target='_blank' style='font-size:1.05em; font-weight:600;'>"
        f"ScottCoffin/MNP-Compass</a>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"The source code for this tool — including the decision tree configuration, "
        f"crosswalk data, and Streamlit application — is publicly available at:"
    )
    st.markdown(
        f"<a href='{GITHUB_URL}' target='_blank'>{GITHUB_URL}</a>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── License ──────────────────────────────────────────────────────────────
    st.markdown("### License")
    st.markdown(AGPL_TEXT)

    st.markdown(
        "<div style='font-size:0.82em; color:#888; margin-top:8px;'>"
        "Copyright © 2026 the authors listed above. "
        "Crosswalk data and decision tree content are released under the same license."
        "</div>",
        unsafe_allow_html=True,
    )
