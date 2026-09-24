# MNP Compass

This repository contains the Streamlit companion app and supporting materials for the manuscript:

> Learning from history instead of reinventing the wheel: A resource for coordinating microplastics research, reporting, and publication criteria across disciplines

The app helps researchers locate microplastics and nanoplastics methods, standards, guidance, and risk-assessment references by study domain, matrix, workflow step, instrumentation, particle type, and authority tier.

![Graphical Abstract](mnp_compass/www/graphical_abstract.png)

MNP Compass is an interactive decision-tree web tool for researchers designing microplastics monitoring, toxicology, or risk assessment studies. Users step through their study type, environmental matrix (drinking water, sediment, biota, air, food, soil, and others), and workflow step (sampling, extraction, analytical identification, QA/QC, reporting) to retrieve a curated, ranked list of methods, standards, and guidance documents drawn from a crosswalk of <!-- count sourced from crosswalk.xlsx row count as of 2026-08-27; the in-app count on the Crosswalk and About tabs is computed live from the same file and will not drift from it, but this README prose count is static and should be updated by hand if the workbook's row count changes -->190 seminal references in microplastics research. Results are grouped by a four-tier authority and validation framework — described below — and displayed with document type, key notes, and direct links, with the option to export filtered results to CSV. Worked examples (Quick Start), a live map of where authoritative methods exist and where they are missing (Coverage & Gaps), a full-text search across all references, and a domain glossary are also available.

### Authority and Validation Tier Framework

<!--
CANONICAL SOURCE: mnp_compass/tabs/citation_tab.py (TIER_FRAMEWORK_INTRO, TIER_FRAMEWORK_TIERS,
TIER_FRAMEWORK_OUTRO), rendered on the app's About tab. This section is a manual verbatim quote
of that constant. If you change the wording in one place, update the other to match — do not
retype tier definitions a third time anywhere else in the repo.
-->

To organize resources that differ substantially in their institutional status and degree of methodological validation, MNP Compass classifies each resource using a four-tier **authority and validation framework**. The tiers are intended to characterize the basis and strength of a resource's authority, rather than its overall scientific quality, utility, or currency; consequently, a lower-tier resource may be more current or more applicable to a particular research question than a higher-tier resource.

**🟢 Tier 1 — Normative / Binding** — Requirements, procedures, or methods that carry a formal legal, regulatory, or institutional mandate within a defined jurisdiction or program. Examples include legislation and regulations, regulatory decisions, and standardized methods or standard operating procedures required for regulatory compliance, accreditation, or official monitoring.

**🔵 Tier 2 — Authoritative / Institutional** — Standards, methods, guidance, and other resources formally issued or endorsed by recognized standards-development organizations, governmental or intergovernmental bodies, or comparable institutions, but that are not themselves mandatory in the relevant application. Examples include ISO and ASTM standards and formal guidance from organizations such as WHO, EFSA, GESAMP, NIST, and similar bodies.

**🟡 Tier 3 — Validated / Interlaboratory-Tested / Critical Guidance** — Resources supported by substantial empirical or evidence-synthesis-based evaluation but lacking the formal mandate or institutional status of Tiers 1 and 2. This category includes methods evaluated through interlaboratory comparison, proficiency testing, or quantitative validation, as well as critical or systematic reviews that establish evidence-based QA/QC criteria, performance criteria, or methodological recommendations.

**⚪ Tier 4 — Supporting / Contextual** — Resources that provide useful methodological, scientific, or interpretive context but have not undergone the level of validation or evidence synthesis represented by Tier 3 and do not carry the formal institutional authority of Tiers 1 or 2. Examples include emerging or single-laboratory methods, research tools and databases, narrative reviews, perspectives, frameworks, and other supporting literature.

The resulting classification therefore represents a gradient from formally binding requirements to supporting scientific context, rather than a numerical score of study or resource quality. MNP Compass presents resources across tiers so that users can consider formal authority alongside factors such as methodological relevance, recency, applicability, and available resources.

## Quick Start

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run mnp_compass/app.py
```

On Linux, macOS, Codespaces, or Streamlit Cloud, install Graphviz at the system level as well. This repo includes `packages.txt` with the `graphviz` package for environments that read apt package manifests.

Run the validation smoke test:

```powershell
python tests/smoke_test.py
```

## Repository Sitemap

```text
.
|-- README.md
|-- LICENSE
|-- requirements.txt
|-- requirements-metadata.txt
|-- packages.txt
|-- mnp_compass/
|   |-- app.py
|   |-- config/
|   |   `-- tree_structure.yaml
|   |-- data/
|   |   |-- crosswalk.xlsx
|   |   `-- metadata_cache/
|   `-- tabs/
|       |-- citation_tab.py
|       |-- coverage_tab.py
|       |-- crosswalk_tab.py
|       |-- glossary_tab.py
|       |-- quick_start_tab.py
|       `-- visual_tree_tab.py
|-- scripts/
|   `-- fill_crosswalk_metadata.py
|-- tests/
|   `-- smoke_test.py
|-- figures/
|   |-- manuscript_figures.R
|   |-- fig*_*.py
|   `-- generated figure outputs
|-- docs/
|   |-- key-paper-content.md
|   `-- letter-to-journals-and-funders.md
`-- archive/
    `-- historical_scripts/
```

## Core Files

`mnp_compass/app.py` is the Streamlit entry point.

`mnp_compass/data/crosswalk.xlsx` is the source workbook. The app reads the `Crosswalk Table` sheet and does not modify it.

`mnp_compass/config/tree_structure.yaml` stores a decision-tree structure and gap notes, loaded by `app.py`. **Note:** the live "Decision Tree" tab is currently rendered entirely by hardcoded Python dicts in `mnp_compass/tabs/visual_tree_tab.py` (matrices, instruments, particle types, workflow steps) and does not read this YAML — the YAML only feeds a "Step-by-Step Navigator" tab that is currently disabled (`step_by_step_enabled = False` in `app.py`). The two enumerations have drifted as a result; see `TODO(human)` in `visual_tree_tab.py` and `AUDIT_FINDINGS.md`.

`mnp_compass/tabs/` contains the app tab renderers, in tab order: Quick Start (a three-step guide plus worked examples that open pre-set Decision Tree paths), the visual decision tree, Coverage & Gaps (best available tier per matrix × monitoring step, matrix-specific or including cross-cutting documents), the crosswalk browser, search, glossary, and the About/citation page (tier framework, curation process, the exact filter and ordering rules, and the contribution process).

`scripts/fill_crosswalk_metadata.py` is the active maintenance script for filling selected workbook metadata fields from Zotero, PDFs, DOI/URL pages, and an Anthropic model.

`archive/historical_scripts/` contains older one-off workbook migration scripts. They are retained for provenance, but they are not part of the current app runtime or reproducible maintenance path.

## Crosswalk Data Fields

`mnp_compass/data/crosswalk.xlsx`'s "Crosswalk Table" sheet (header row 2) is the single source of truth for every reference the app surfaces — currently 190 rows. Column headers use embedded line breaks for readability in Excel; the app collapses them to single spaces at load time, and additionally renames `Priority Tier` to `Authority and Validation Tier` in memory (see [Authority and Validation Tier Framework](#authority-and-validation-tier-framework)) without touching the workbook itself.

**Bibliographic:** `#`, `Short Citation`, `Year`, `Full Title`, `DOI/URL`

**Classification & navigation:** `Document Type`, `Priority Tier`, `Primary Domain`, `Primary Focus`, `Instrumentation Tags`, `Matrix Tags`, `Particle/Polymer Type Tags`, `Target Receptor(s)`

**Topic-scoring columns** (hold a tier number 1–4 if the reference addresses that topic, blank otherwise): `Definitions & Terminology`, `Problem Formulation / Framework`, `Sampling (Field Methods)`, the `Matrix: *` columns (Drinking Water, Surface Water incl. Lacustrine/Riverine/Marine, Wastewater, Groundwater, Biosolids, Sediment, Soil, Biota/Tissue, Air/Atmos., Food/Dietary, Human Tissue/Biomonitor), `Sample Processing / Extraction`, `Sub-sampling`, `Analytical Methods (General)`, `FTIR / IR Spectroscopy`, `Raman Spectroscopy`, `Py-GC-MS`, `Imaging`, `Material Standards - materials`, `Material Standards - protocol`, `Blanks & Contamination Control`, `Data Analysis & Statistics`, `Reporting & Harmonization`, `Databases & Data Sharing`, the `Toxicology: *` columns (Study Design & Dosimetry, Effects Testing Methods, Reporting & Harmonization, Databases & Data Sharing), `Risk Assessment / Risk Char.`

**Narrative / metadata:** `Key Notes`, `Scope`, `Status`, `Particle Size Range`, `Key Metrics / Output`, `Abstract`

**Computed, not a workbook column:** `tier_num` — parsed from `Priority Tier` at load time (e.g., "★★★★ Tier 1 ..." → `1`); drives sorting, coloring, and expander grouping throughout the app.

**Curated by hand (always):** everything above except `Particle Size Range`, `Key Metrics / Output`, and `Abstract`.

**Optionally auto-filled:** `scripts/fill_crosswalk_metadata.py` can populate `Particle Size Range`, `Key Metrics / Output`, and `Abstract` from Zotero, PDFs, or DOI/URL landing pages (dry-run by default; see [Metadata Fill Workflow](#metadata-fill-workflow) below). On its first `--write` run it also creates its own `PDF Available in Zotero?` and `Reviewed` tracking columns — these are separate from the pre-existing, hand-curated `Status` column and are not required by the app or its smoke test.

## Dependencies

Runtime Python dependencies are listed in `requirements.txt`:

- `streamlit`
- `pandas`
- `openpyxl`
- `pyyaml`
- `graphviz`

The Python `graphviz` package also needs the Graphviz `dot` executable available on `PATH`.

Optional metadata-enrichment dependencies are listed in `requirements-metadata.txt`.

## Metadata Fill Workflow

The metadata workflow is dry-run by default. It can fill `Particle Size Range`, `Key Metrics / Output`, `Abstract`, `PDF Available in Zotero?`, and `Reviewed` in the `Crosswalk Table` sheet.

Install optional dependencies:

```powershell
python -m pip install -r requirements-metadata.txt
```

Set credentials for LLM-backed metadata extraction:

```powershell
$env:ANTHROPIC_API_KEY = "..."
# Optional model override:
$env:ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
```

Common commands:

```powershell
# Dry-run one DOI
python scripts/fill_crosswalk_metadata.py --doi 10.1016/j.chemosphere.2022.134282

# Write one DOI to a metadata-filled copy
python scripts/fill_crosswalk_metadata.py --doi 10.1016/j.chemosphere.2022.134282 --write

# Process all eligible rows into a metadata-filled copy
python scripts/fill_crosswalk_metadata.py --write

# Resume from the metadata-filled workbook in batches of 3
python scripts/fill_crosswalk_metadata.py --resume --batch-size 3

# Resume at a specific Excel row
python scripts/fill_crosswalk_metadata.py --resume --start-row 42 --batch-size 3

# Disable DOI/URL landing-page scraping for an offline Zotero/PDF-only run
python scripts/fill_crosswalk_metadata.py --resume --batch-size 3 --skip-url-scrape
```

The default cache and audit files live under `mnp_compass/data/metadata_cache/`. The audit CSV is append-only across runs; delete `mnp_compass/data/metadata_cache/crosswalk_metadata_audit.csv` before a new run if you want a fresh audit log.

## Reproducibility Notes

Use the root-level `requirements.txt` and `packages.txt` for app execution. Use `requirements-metadata.txt` only for the optional metadata fill workflow.

Keep `mnp_compass/data/crosswalk.xlsx` as the canonical data source for the app and figures. If you edit the workbook in Excel, close Excel before running scripts that read or write it.

Regenerate or check app behavior after structural changes with:

```powershell
python tests/smoke_test.py
```

Run the app locally with:

```powershell
streamlit run mnp_compass/app.py
```

Figure scripts in `figures/` read the same canonical workbook path: `mnp_compass/data/crosswalk.xlsx`.

## Deployment

For Streamlit Cloud or a dev container:

1. Install apt packages from `packages.txt`.
2. Install Python packages from `requirements.txt`.
3. Use `streamlit run mnp_compass/app.py` as the launch command.

The `.devcontainer/devcontainer.json` file follows this layout and auto-starts the app on port `8501`.

**Graphviz note:** `requirements.txt`'s `graphviz` package is only the Python binding — rendering the decision-tree diagram also requires the system `dot` executable, which `pip` does not install. `packages.txt` (apt package `graphviz`) supplies it on Streamlit Community Cloud; on other hosts, install Graphviz through the system package manager. If `dot` is unavailable at runtime, the decision-tree tab shows a warning explaining how to fix it instead of a stack trace.

## Contributing

The community can propose new references, corrections, or re-tierings through GitHub issues and pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow, including how to edit the canonical workbook, the tier schema to apply, and how to validate your change before opening a PR.

## License

This repository is licensed under the GNU Affero General Public License v3.0. See `LICENSE` for the full AGPL-3.0 text.

The app's citation/license tab states that the crosswalk data and decision-tree content are released under the same license.

## Citation

Suggested draft citation:

```text
Granek, E.F., Coffin, S., Brander, S.M., Seeley, M.E., Thornton Hampton, L.M., El Hayek, E., Walker, V.R., Wagner, M., Gouin, T., Gray, A.B., Harper, S.L., & Rooney, A.A. (in review). Learning from history instead of reinventing the wheel: A resource for coordinating microplastics research, reporting, and publication criteria across disciplines. [Journal TBD]. DOI: TBD
```

Update the citation once the manuscript has a final journal reference and DOI.

## Troubleshooting

If the decision-tree diagram fails, confirm the Graphviz `dot` executable is installed and on `PATH`.

If the workbook cannot be read or written, close Excel and rerun the command.

If app changes do not appear immediately, clear Streamlit's cache from the app menu or restart the Streamlit process.

If metadata extraction fails with `ANTHROPIC_API_KEY is not set`, set the environment variable or use `--skip-llm` for a non-LLM pass.
