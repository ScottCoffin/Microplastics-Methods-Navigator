# CLAUDE.md — Methods Navigator

## Purpose

This is an interactive Streamlit web app that helps researchers plan microplastics (MP) monitoring and toxicology studies by guiding them through a decision tree to find the most authoritative published methods, standards, and guidance documents for each step of their workflow.

It is the companion tool for a peer-reviewed publication: a crosswalk table summarizing \~150 seminal references in microplastics research harmonization, scored by authority tier and tagged by topic.

## Domain Context

Microplastics research is a rapidly growing field with a critical standardization problem: hundreds of methods exist, but very few are formally standardized. Researchers designing a new study face the question "which method should I use?" with no single authoritative answer for most matrices and workflow steps.

This tool solves that by organizing all known methods/standards into a decision tree: - **Study Type** → Monitoring vs. Toxicology vs. Risk Assessment - **Matrix** → Drinking Water, Surface Water, Sediment, Biota, Air, Food, Human Tissue, Soil - **Workflow Step** → Sampling → Extraction → Analysis → QA/QC → Reporting - **Instrumentation** → µFTIR, µRaman, Py-GC-MS, TED-GC-MS, LDIR, Nile Red, etc.

At each terminal node, the app displays matching references sorted by a 4-tier authority system: - **Tier 1 (Normative/Binding):** Laws, regulations, ISO/ASTM standards, government SOPs - **Tier 2 (Authoritative/Institutional):** WHO, GESAMP, EFSA, NOAA reports - **Tier 3 (Peer-Reviewed/Validated):** Published methods with quantitative validation data - **Tier 4 (Supporting/Contextual):** Reviews, frameworks, emerging methods, commentary

## Architecture

```         
root/
├── CLAUDE.md               # This file
└── README.md               # User-facing documentation
└──microplastics_navigator/
    ├── app.py                  # Streamlit app (main entry point)
    ├── tree_structure.yaml     # Decision tree config (nodes, branches, gap notes)
    ├── crosswalk.xlsx          # Data source (Excel workbook with ~150 references)
    ├── requirements.txt        # Python dependencies
```

### Data Flow

```         
crosswalk.xlsx ──read──► pandas DataFrame
                              │
tree_structure.yaml ──read──► dict (YAML)
                              │
User selections (Streamlit) ──► filter chain:
    1. filter_by_domain()      Primary Domain column
    2. filter_by_matrix()      Matrix Tags column
    3. filter_by_topic_column() Tier-scored topic columns
    4. filter_by_instrument()  Instrumentation Tags column (optional)
    5. filter_by_keyword()     Key Notes full-text search (optional)
    6. sort_by_tier()          Tier 1 first, then by year descending
                              │
                              ▼
                     display_results()  → grouped by tier, styled cards
```

### Key Design Decisions

1.  **Filtering is layered, not hardcoded.** Each filter narrows the DataFrame progressively. The tree_structure.yaml defines WHICH filters to apply at each node, but the filter functions themselves are generic. Adding a new branch means adding YAML, not Python.

2.  **Column name matching is fuzzy.** The `find_column()` function handles the fact that Excel column headers often contain line breaks, inconsistent spacing, etc. It does substring matching as a fallback. This makes the app resilient to minor spreadsheet reformatting.

3.  **The spreadsheet is the single source of truth.** All reference data lives in `crosswalk.xlsx`. The app never modifies it. The YAML file only defines navigation structure and gap notes.

4.  **Gap notes surface known blind spots.** When a matrix + workflow step combination has no Tier 1/2 coverage, the YAML file provides a contextual warning. These come from a formal gap analysis conducted during the crosswalk development.

## Crosswalk Data Schema

The Excel file (`methods_navigator/crosswalk.xlsx`, sheet "Crosswalk Table") has this structure:

### Bibliographic Columns

| Column           | Type | Description                 |
|------------------|------|-----------------------------|
| `#`              | int  | Unique entry ID             |
| `Short Citation` | str  | e.g., "Coffin et al., 2022" |
| `Year`           | int  | Publication year            |
| `Full Title`     | str  | Complete document title     |
| `DOI/URL`        | str  | Resolvable link             |

### Classification Columns

| Column | Type | Values |
|------------------------|------------------------|------------------------|
| `Document Type` | str | Legislation, Regulation/Regulatory Decision, Government SOP, Consensus Standard, Agency Technical Report, International Guidance, Scientific Advisory Report, Certified Reference Material, Regulatory-Adopted Method, Support Tool, Regulatory Definition, Method/Protocol, Interlaboratory Study, Framework, Guideline/Best Practice, Review, Tool/Database, Perspective/Commentary |
| `Priority Tier` | str | "★★★★ Tier 1 Normative / Binding", "★★★☆ Tier 2 Authoritative / Institutional", "★★☆☆ Tier 3 Peer-Reviewed / Validated", "★☆☆☆ Tier 4 Supporting / Contextual" |

### Navigation Columns (used by the decision tree)

| Column | Type | Description |
|------------------------|------------------------|------------------------|
| `Primary Domain` | str | `Monitoring`, `Toxicology`, `Both`, `Cross-cutting` |
| `Instrumentation Tags` | str (semicolon-separated) | e.g., "µFTIR; µRaman; Py-GC-MS" |
| `Matrix Tags` | str (semicolon-separated) | e.g., "Drinking Water; Surface Water" or "Cross-cutting" |

### Topic Scoring Columns

Each column holds a tier score (1, 2, 3, or 4) if the reference addresses that topic, or is blank/empty if it does not. The score matches the document's authority tier — it is NOT a quality rating.

Topic columns include: - `Definitions & Terminology` - `Sampling (Field Methods)` - `Matrix: Drinking Water`, `Matrix: Surface/Wastewater`, `Matrix: Sediment`, `Matrix: Biota/Tissue`, `Matrix: Air/Atmos.`, `Matrix: Food/Dietary`, `Matrix: Human Tissue/Biomonitor` - `Sample Processing / Extraction` - `Sub-sampling` - `Analytical Methods (General)`, `FTIR / IR Spectroscopy`, `Raman Spectroscopy`, `Py-GC-MS` - `Reference Materials / +Controls` - `Blanks & Contamination Control` - `Data Analysis & Statistics` - `Reporting & Harmonization` - `Databases & Data Sharing` - `Toxicology: Study Design & Dosimetry`, `Toxicology: Effects Testing Methods` - `Interlaboratory/Validation` - `Risk Assessment / Risk Char.`

### Metadata Columns

| Column | Type | Description |
|------------------------|------------------------|------------------------|
| `Key Notes` | str | Free-text summary of the reference's contribution. Used for keyword filtering. |
| `Particle Size Range` | str | Size range addressed by the method/document |

## tree_structure.yaml Schema

The YAML file defines: - **Decision nodes:** Each has a `question` and `options` (branches) - **Filter instructions:** Each terminal option specifies how to filter the crosswalk: - `crosswalk_column`: filter by non-empty values in a topic scoring column - `matrix_filter`: filter Matrix Tags containing this keyword - `instrument_filter`: filter Instrumentation Tags containing this keyword - `doc_type_filter`: filter Document Type containing this string - `keyword_filter`: semicolon-separated keywords to match against Key Notes - `domain_filter`: filter Primary Domain column - **Gap notes:** keyed by `{matrix_key}_{step_key}` or `{matrix_key}_all`, displayed as warnings

## Development Commands

``` bash
# Install dependencies
pip install -r methods_navigator/requirements.txt

# Run locally
streamlit run methods_navigator/app.py

# Run with auto-reload on file changes
streamlit run methods_navigator/app.py --server.runOnSave true

# Deploy to Streamlit Cloud
# Push to GitHub, connect at share.streamlit.io
```

## Common Tasks

### Adding a new reference to the crosswalk

1.  Add a row to `crosswalk.xlsx` with all required columns filled
2.  Score the relevant topic columns with the appropriate tier number
3.  Tag `Primary Domain`, `Instrumentation Tags`, and `Matrix Tags`
4.  The app will pick it up automatically on next load (clear Streamlit cache if needed)

### Adding a new matrix or workflow branch

1.  Add the new option to `tree_structure.yaml` under the appropriate parent node
2.  Specify the filter instructions (column name, matrix keyword, etc.)
3.  Add a gap note if the matrix has known coverage gaps
4.  No Python changes needed unless the filter type is entirely new

### Adding a new instrumentation option

1.  Add the instrument to the `instrumentation_select` node in YAML
2.  Ensure the corresponding references have the instrument tag in their `Instrumentation Tags` column
3.  Add to the `instrument_map` dict in the Analytical Identification section of `app.py`

### Changing the tier system

1.  Update `TIER_LABELS`, `TIER_COLORS`, `TIER_ICONS` dicts in `app.py`
2.  Update the `Priority Tier` strings in `crosswalk.xlsx`
3.  The tier number extraction regex (`Tier\s*(\d)`) must still match

## Known Limitations and TODOs

-   [ ] Column name matching via `find_column()` is fuzzy — works well in practice but could produce false matches if column names are very similar. Consider switching to exact match with a canonical column map after the spreadsheet schema stabilizes.
-   [ ] The app reads the entire Excel file on each session start. For \~150 entries this is instant; if the crosswalk grows to thousands of entries, consider converting to a SQLite database or Parquet file.
-   [ ] Keyword-based filtering (for tox test systems, RA subtopics) depends on the free-text Key Notes field. If Key Notes wording changes, keyword filters may miss entries. Consider adding structured tag columns for these if filtering precision becomes an issue.
-   [ ] The Particle Size Range column has some misaligned data (paste-shift errors from spreadsheet editing). Audit before using this field for filtering.
-   [ ] No authentication or user accounts. The app is read-only and intended for public use.
-   [ ] Gap notes are static (defined in YAML). A future version could auto-detect gaps by checking whether any Tier 1/2 entries exist for a given matrix + step combination.

## Glossary of Domain Terms

-   **Microplastics (MPs):** Plastic particles with dimensions typically between 1 µm and 5 mm, though definitions vary by jurisdiction (see the Definitions & Terminology branch of the decision tree).
-   **Nanoplastics (NPs):** Plastic particles smaller than 1 µm (ISO definition) or smaller than 100 nm (some agency definitions).
-   **µFTIR:** Micro–Fourier Transform Infrared spectroscopy. Identifies polymer type by IR absorption spectrum. Particle-counting method.
-   **µRaman:** Micro-Raman spectroscopy. Identifies polymer type by inelastic light scattering. Particle-counting method. Better spatial resolution than FTIR (\~1 µm vs. \~10–20 µm).
-   **Py-GC-MS:** Pyrolysis–Gas Chromatography–Mass Spectrometry. Thermally decomposes polymers and identifies them by their decomposition products. Mass-based method (no particle count).
-   **TED-GC-MS:** Thermal Extraction Desorption–GC-MS. Similar to Py-GC-MS but uses larger sample masses (up to 100 mg vs. \~0.5 mg), improving representativeness for heterogeneous samples.
-   **LDIR:** Laser Direct Infrared spectroscopy (Agilent 8700). Uses a quantum cascade laser for rapid automated particle-by-particle IR analysis. Particle-counting method.
-   **Nile Red:** A fluorescent dye that adsorbs onto plastic surfaces. Used as a rapid screening method; requires spectroscopic confirmation for polymer identification.
-   **Density separation:** The core sample processing technique for extracting MPs from solid matrices (soil, sediment, biota). Polymers float in dense salt solutions (NaCl, ZnCl₂, NaI, CaCl₂) while mineral/organic matrix sinks.
-   **SSD:** Species Sensitivity Distribution. A statistical method used in ecotoxicological risk assessment to derive protective thresholds.
-   **PBK/PBPK:** Physiologically-Based (Pharmaco)Kinetic modeling. Used to predict tissue-level exposure from external doses.
-   **ToMEx:** Toxicity of Microplastics Explorer. An open-access database of microplastic toxicity studies with quality scoring.
-   **SCCWRP:** Southern California Coastal Water Research Project. A public research agency that co-developed the California MP monitoring methods.
-   **SWB / SWRCB:** State Water (Resources Control) Board. California's regulatory agency for water quality; first agency worldwide to regulate MP monitoring in drinking water.