# Microplastics Methods Navigator

This repository contains the Streamlit companion app and supporting materials for the manuscript:

> Learning from history instead of reinventing the wheel: A call for coordinating microplastics research, reporting, and publication criteria across disciplines

The app helps researchers locate microplastics and nanoplastics methods, standards, guidance, and risk-assessment references by study domain, matrix, workflow step, instrumentation, particle type, and authority tier.

The Microplastics Methods Navigator is an interactive decision-tree web tool for researchers designing microplastics monitoring, toxicology, or risk assessment studies. Users step through their study type, environmental matrix (drinking water, sediment, biota, air, food, soil, and others), and workflow step (sampling, extraction, analytical identification, QA/QC, reporting) to retrieve a curated, ranked list of methods, standards, and guidance documents drawn from a crosswalk of > 175 seminal references in microplastics research. Results are grouped by a four-tier authority hierarchy — from Tier 1 normative and binding standards (e.g., ISO, ASTM, government regulations and SOPs) to Tier 4 supporting literature (reviews and commentary) — and displayed with document type, key notes, and direct links, with the option to export filtered results to CSV. A full-text search across all references, an interactive visual decision tree, and a domain glossary are also available.

## Quick Start

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run methods_navigator/app.py
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
|-- methods_navigator/
|   |-- app.py
|   |-- config/
|   |   `-- tree_structure.yaml
|   |-- data/
|   |   |-- crosswalk.xlsx
|   |   `-- metadata_cache/
|   `-- tabs/
|       |-- citation_tab.py
|       |-- crosswalk_tab.py
|       |-- glossary_tab.py
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

`methods_navigator/app.py` is the Streamlit entry point.

`methods_navigator/data/crosswalk.xlsx` is the source workbook. The app reads the `Crosswalk Table` sheet and does not modify it.

`methods_navigator/config/tree_structure.yaml` stores the decision-tree structure and gap notes.

`methods_navigator/tabs/` contains the app tab renderers for the visual decision tree, crosswalk browser, glossary, and citation/license page.

`scripts/fill_crosswalk_metadata.py` is the active maintenance script for filling selected workbook metadata fields from Zotero, PDFs, DOI/URL pages, and an Anthropic model.

`archive/historical_scripts/` contains older one-off workbook migration scripts. They are retained for provenance, but they are not part of the current app runtime or reproducible maintenance path.

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

The default cache and audit files live under `methods_navigator/data/metadata_cache/`. The audit CSV is append-only across runs; delete `methods_navigator/data/metadata_cache/crosswalk_metadata_audit.csv` before a new run if you want a fresh audit log.

## Reproducibility Notes

Use the root-level `requirements.txt` and `packages.txt` for app execution. Use `requirements-metadata.txt` only for the optional metadata fill workflow.

Keep `methods_navigator/data/crosswalk.xlsx` as the canonical data source for the app and figures. If you edit the workbook in Excel, close Excel before running scripts that read or write it.

Regenerate or check app behavior after structural changes with:

```powershell
python tests/smoke_test.py
```

Run the app locally with:

```powershell
streamlit run methods_navigator/app.py
```

Figure scripts in `figures/` read the same canonical workbook path: `methods_navigator/data/crosswalk.xlsx`.

## Deployment

For Streamlit Cloud or a dev container:

1. Install apt packages from `packages.txt`.
2. Install Python packages from `requirements.txt`.
3. Use `streamlit run methods_navigator/app.py` as the launch command.

The `.devcontainer/devcontainer.json` file follows this layout and auto-starts the app on port `8501`.

## License

This repository is licensed under the GNU Affero General Public License v3.0. See `LICENSE` for the full AGPL-3.0 text.

The app's citation/license tab states that the crosswalk data and decision-tree content are released under the same license.

## Citation

Suggested draft citation:

```text
Granek, E.F., Brander, S.M., Coffin, S., El Hayek, E., Thornton Hampton, L.M., Seeley, M.E., Gray, A.B., & Harper, S.L. (in review). Learning from history instead of reinventing the wheel: A call for coordinating microplastics research, reporting, and publication criteria across disciplines. [Journal TBD]. DOI: TBD
```

Update the citation once the manuscript has a final journal reference and DOI.

## Troubleshooting

If the decision-tree diagram fails, confirm the Graphviz `dot` executable is installed and on `PATH`.

If the workbook cannot be read or written, close Excel and rerun the command.

If app changes do not appear immediately, clear Streamlit's cache from the app menu or restart the Streamlit process.

If metadata extraction fails with `ANTHROPIC_API_KEY is not set`, set the environment variable or use `--skip-llm` for a non-LLM pass.
