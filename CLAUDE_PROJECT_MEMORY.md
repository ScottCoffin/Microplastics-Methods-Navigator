# Claude Project Memory — MNP Quality Standards Manuscript

*Last updated: 2026-04-22* *Project owner: Scott Coffin (scott.l.coffin\@gmail.com)*

------------------------------------------------------------------------

## Project Overview

**Goal:** Develop a manuscript synthesizing quality standards and guidance for micro- and nanoplastic (MNP) research, with a focus on regulatory applicability. The manuscript uses a systematic crosswalk of \~100 papers mapped to workflow steps, tier levels, and knowledge gaps.

**Working folder:** `C:\Users\Scott.Coffin\Documents\Claude\Projects\Quality Manuscript\` (Mounted at `/sessions/eloquent-inspiring-gauss/mnt/Quality Manuscript/`)

------------------------------------------------------------------------

## Key Files in Workspace

| File | Purpose |
|-----------------------------|-------------------------------------------|
| `MNP Quality Standards Crosswalk v2.xlsx` | Master Excel crosswalk — **do not write while Excel is open** (file corrupts in transit) |
| `crosswalk_append_new_papers.py` | Run after closing Excel to safely append \~18 new papers |
| `Key Paper Content - Extracted from Full Text.md` | Full extractions from priority papers (sections 1–12) |
| `Letter to journals and funders.md` | Manuscript cover letter draft |
| `figures/fig1_workflow_flowchart.py` + `.html` | Researcher decision flowchart (interactive Plotly) |
| `figures/fig2_gap_heatmap.py` + `.html` | Guidance gap heatmap by matrix × workflow step |
| `figures/fig3_quality_passrates.py` + `.html` | Quality pass-rate comparison across frameworks |
| `figures/fig4_coverage.py` + `.html` | Paper coverage by workflow step, 3-panel stacked bar |

------------------------------------------------------------------------

## Zotero Collection

-   **Collection name:** Quality Standards for MNPs
-   **Collection key:** `AKNE8BJL`
-   **Library user ID:** `5485228`
-   **Current count:** \~100 items (was 86 → Scott added 6 → we added 8 more from Regulatory Readiness citations)

### MCP Tool Notes

-   `zotero_get_collection_items` with `detail="summary"` and `limit=120` is the reliable way to get all items
-   `zotero_search_items` frequently times out — prefer collection retrieval
-   `zotero_get_item_fulltext` returns large files saved to tool-results path; read strategically (find sections first, then extract)
-   After `zotero_add_by_doi`, metadata 404s are common for a few minutes — normal sync delay

------------------------------------------------------------------------

## Crosswalk Structure (MNP Quality Standards Crosswalk v2.xlsx)

**Sheet:** `Crosswalk Table` **Rows:** 1 = section header, 2 = column headers, 3+ = paper data (86 original rows → growing)

| Col (Excel) | Col (Python 0-idx) | Content |
|----------------------|--------------------------------|------------------|
| A | 0 | Row ID (integer) |
| B | 1 | Short citation (e.g., "Koelmans et al. 2025") |
| C | 2 | Year (integer) |
| D | 3 | Full title |
| E | 4 | Primary Focus ("Environmental", "Toxicology", "Both", "Framework") |
| F | 5 | Document Type |
| G | 6 | Priority Tier string (see below) |
| H–Q | 7–16 | Per-cell tier integers: Definitions, Problem Formulation, Sampling, DW, SW, Sediment, Biota, Air, Food, Human Tissue |
| R–W | 17–22 | Per-cell tier: SampProc, Subsamp, AnlGen (General), FTIR, Raman, Py-GC-MS |
| X–AB | 23–27 | Per-cell tier: RefMat/Controls, Blanks/QC, Data Analysis, Reporting, Data Deposition |
| AC–AE | 28–30 | Per-cell tier: Tox Study Design, Tox Effects, Interlaboratory/Validation |
| AF | 31 | Per-cell tier: Risk Assessment / Risk Char. |
| AG | 32 | Key Notes |

**⚠️ SCHEMA CHANGE (2026-04-22): Per-cell tier integers replaced binary ✓ checkmarks**
- Cells now contain integer 1, 2, 3, or 4 (the tier of guidance for THAT specific workflow step)
- **NOT** `"✓"` anymore — don't look for checkmark character
- Figure scripts now use: `cell_tier(p[ci])` helper that returns int or None
- Detection: `isinstance(p[ci], (int, float)) and 1 <= p[ci] <= 4`
- Cell background = light tier color; font = tier color (bold)
- Tier 4 papers: ALL their cells = 4 (uniform, no per-cell assessment needed)
- Tier 1-3 papers: per-cell tiers based on whether the paper provides specific guidance for that step (Haiku-assessed, Apr 2026)
- Known overrides: ID 16 cols 18+25 → 4; ID 105 cols 8+9 → 4

**Tier strings** (col G, must contain "Tier N" for Python scripts to detect):
- `"★★★★ Tier 1\nRegulatory/\nAccredited SOP"` 
- `"★★★☆ Tier 2\nAuthoritative\nGuidance"` 
- `"★★☆☆ Tier 3\nPeer-Reviewed\nMethod/SOP"` 
- `"★☆☆☆ Tier 4\nSupporting\nScience"`

**Excel file locking / corruption:** macOS FUSE mount can corrupt xlsx central directory when saved in Excel; result is `BadZipFile` error. Recovery: use `update_crosswalk_ra.py` from `/sessions/.../` local directory (recovers from `crosswalk_v2.xlsx`). If xlsx appears valid via `file` command but openpyxl fails, the zip central directory is likely missing — see session d486f554 for repair approach.

------------------------------------------------------------------------

## 4-Tier Priority System

| Tier | Color | Description | Examples |
|----------------|----------------|------------------------|-----------------|
| 1 | Purple `#6A0DAD` | Regulatory / Accredited SOP | ISO standards, EPA methods, CA SWRCB SOPs |
| 2 | Blue `#1565C0` | Authoritative Guidance | WHO, EFSA, ISO guidance docs, JRC reference materials |
| 3 | Green `#2E7D32` | Peer-Reviewed Method / SOP | Published papers establishing specific methods |
| 4 | Grey `#78909C` | Supporting Science | Other peer-reviewed literature, conference abstracts |
| Gap | Salmon `#FFCDD2` | No guidance identified | Used in heatmap only |

------------------------------------------------------------------------

## Figures — Technical Notes

All figures are standalone interactive Plotly HTML files. Plotly loaded from CDN (`plotly-2.35.0.min.js`) — **no local network access needed at render time, only at open time.**

### Fig 1 — Workflow Flowchart (`fig1_workflow_flowchart.py`)

-   24 nodes, 29 edges; two-track (Environmental Monitoring left, Toxicology right)
-   Custom Plotly shapes (rectangles/diamonds) + scatter for edges/labels
-   Background shading: green=monitoring, purple=toxicology track

### Fig 2 — Gap Heatmap (`fig2_gap_heatmap.py`)

-   7 matrix rows × 11 env workflow cols + separator + 3 tox cols
-   Discrete colorscale: z=1–5 mapped to tier colors + salmon gap
-   Key finding visible: only Drinking Water row has Tier 1 (purple) coverage

### Fig 3 — Quality Pass Rates (`fig3_quality_passrates.py`)

-   Hardcoded data (4 frameworks, small dataset)
-   Error bars show score range where available
-   Data points: de Ruijter 2020 (44.6%), Gouin NMP-TSAT 2022 (16.2%), ToMEx 1.0 2021 (13%), ToMEx 2.0 2025 (12%)

### Fig 4 — Coverage by Workflow Step (`fig4_coverage.py`)

-   3-row Plotly subplot layout (proportional domains: 10/8/5 steps per row)
-   **Col 19 "Analytical Methods (General)" excluded** — documented in docstring; causes double-counting with FTIR/Raman/Py-GC-MS columns
-   Row 1: Framing (Def, PF) + Sampling & Matrix (Samp, DW, SW, Sed, Bio, Air, Food, HumTis)
-   Row 2: Lab Processing (SampProc, Subsamp, RefMat, Blanks) + Spectroscopic (FTIR, Raman, PyGCMS, InterLab)
-   Row 3: Data & Reporting (DataAnal, Report, DataDep) + Toxicology (ToxDesign, ToxEffects)
-   Sub-group shading via `yref="paper"` shapes using domain coordinates

**Subplot axis naming (Plotly convention):** - Row 1: `xaxis` / `yaxis` (no number suffix) - Row 2: `xaxis2` / `yaxis2` - Row 3: `xaxis3` / `yaxis3`

------------------------------------------------------------------------

## Key Paper Content Extracted (sections in Key Paper Content - Extracted from Full Text.md)

| § | Paper | Key Quantitative Finding |
|-------------|-------------|----------------------------------------------|
| 1 | Brander et al. 2020 | No standard methods for drinking water (as of 2020); now superseded by CA SOPs |
| 2 | Cowger et al. 2020 (reporting guidelines) | Guidelines are "proposed minimum," not regulatory standard |
| 3 | SWRCB/DDW 2025 (SWB-MP1/2 SOPs) | CA Tier 1 SOPs; drinking water sampling + FTIR/Raman measurement |
| 4 | Koelmans et al. 2019 | Sub-sampling threshold: ≥386 particles for polymer distribution alone |
| 5 | de Ruijter et al. 2020 | No study of 105 scored positively on all 20 QA/QC criteria; avg = 44.6% |
| 6 | WHO 2019/2022 | Authoritative guidance; QA/QC criteria now implemented by WHO |
| 7 | Schymanski et al. 2021 | Minimum requirements: HQI \>70%, IR 1250–3600 cm⁻¹, Raman 200–2000 cm⁻¹, ≤8 cm⁻¹ resolution, 1 blank/10 samples, 10 polymer types, 7 size bins |
| 8 | Hampton et al. 2025 (ToMEx 2.0) | 89% fail screening; 12% pass (unchanged from ToMEx 1.0 = 13%) |
| 9 | Cowger et al. 2025 (Open Specy 1.0) | \>40K spectra, 34 databases; 96% recovery with smoothing (CV=38% ✓); 86% without (CV=83% ✗) |
| 10 | Gouin et al. 2022 (NMP-TSAT) | Only 12/74 studies pass Tier 1 critical criteria; max TAS 52 (in vivo) / 46 (in vitro) |
| 11 | Koelmans et al. 2025 (Reg. Readiness) | TRL: SCCWRP=7, MICROPLASTICLAB=6, POLYRISK/MOMENTUM=5, AURORA=3-4, PLASTICHEAL=3 |
| 12 | De Ruijter et al. 2025 (Brief History) | Same 2016 QA/QC failures persist in 2024; ERMP protocol provided; no freshwater benthic risk at current concentrations |

------------------------------------------------------------------------

## Crosswalk Status

**Current row count:** 105 data rows (IDs 1–105) as of 2026-04-21 (updated session).
**Current column count:** 33 columns (A–AG); 32=Risk Assessment (new), 33=Key Notes.

- IDs 1–86: Original papers (ID 8 renamed → "De Ruijter et al., 2025a")
- IDs 87–98: Added by crosswalk_append_new_papers.py + fixed by fix_crosswalk_v3.py
- IDs 99–104: Added by append_literature_search_papers.py (literature search 2026-04-21)
- ID 105: De Ruijter et al., 2025b — Brief History (added 2026-04-21 update session)

**Resolved citations:**
- ID 104 = "Vural et al., 2025" (STAR Protocols, Zotero: 3EMHDUUP) ← was [TBD]
- ID 105 = "De Ruijter et al., 2025b" (Brief History ecotox review, Zotero: HJRW7S45) ← new row
- Old ID 105 (Dalmau-Soler duplicate) deleted; checkmarks merged into ID 1

**ID disambiguation:**
- ID 1 = Dalmau-Soler et al., 2025 — Implementation plan Py-GC-MS per EU 2024/1441 (Zotero: 56WC834M)
- ID 8 = De Ruijter et al., 2025a — Natural mineral particles for tox testing (Zotero: H97HMUJP)
- ID 105 = De Ruijter et al., 2025b — Brief history of MP effect testing (Zotero: HJRW7S45)

**Column 31 (AE): "Interlaboratory / Validation"** — p[30] (0-based)
**Column 32 (AF): "Risk Assessment / Risk Char."** — p[31] (0-based)
**Column 33 (AG): "Key Notes"** — p[32] (0-based)

- RA column: 23 papers with tier values; tier distribution: {1:2, 2:1, 3:8, 4:12}
- Interlaboratory: 8 papers with tier values; tier dist: {3:7, 4:1}
- Figure scripts updated for per-cell tiers AND correct column indices (2026-04-22)
  - fig2: cell_tier() helper + max(tm,tw) for matrix×workflow intersection
  - fig4: cell_tier(p[ci]) replaces p[ci]=="✓" checks

**IMPORTANT index note:** STEPS and WORKFLOW_COLS/TOX_COLS use 0-BASED Python indices (not 1-based Excel column numbers):
- p[30] = Interlaboratory (col 31 Excel)
- p[31] = Risk Assessment (col 32 Excel)

**Primary Focus updates:**
- ID 16 (Coffin 2022): Framework → Both (DW monitoring + human health RA)
- ID 47 (Mehinto 2022): Framework → Both (aquatic monitoring + ecological RA)

---

## Literature Search Strategy (for future sessions)

**Goal:** Find peer-reviewed methods, SOPs, standards, and frameworks for MNP quality standards that may not yet be in the crosswalk.

**Search tool:** WebSearch (via Cowork agent). Zotero semantic search unavailable (requires `pip install zotero-mcp-server[semantic]`).

**Evaluated & added (2026-04-21):**

| Topic area | Search query used | Papers found |
|---|---|---|
| QA/QC analytical methods | "microplastics QA/QC analytical methods standards 2024 2025" | ITRC field manual, Anal. Bioanal. Chem ref materials, MNP method validation |
| Human tissue biomonitoring | "microplastics human tissue biomonitoring methods 2024 2025" | Human Plastiphere (EST), quantitative biomonitoring review |
| Food/dietary methods | "microplastics food dietary exposure methods standard 2024 2025" | EU Decision 2024/1441, several reviews |
| Sediment/biota methods | "microplastics sediment biota sampling methods SOP 2024 2025" | SCCWRP TR 1410.A, STAR Protocols Vural 2025 |
| Atmospheric methods | "microplastics atmospheric air deposition sampling methods 2024 2025" | Ashta 2026 (AMT), Ren 2026 review |
| Interlaboratory / ring trials | "microplastics interlaboratory ring trial 2024 2025" | Lenz 2024, Ciornii 2025 |
| Py-GC-MS / EU regulation | "microplastics Py-GC-MS EU 2024/1441 implementation method" | Dalmau-Soler 2025 |

**Inclusion criteria:**
1. Must provide specific methodological guidance (not just ecological/toxicological data)
2. Must be applicable to ≥1 workflow step in the crosswalk
3. Should be published 2019–2026 (or be a foundational older paper not yet captured)
4. Tier 1/2 only if from regulatory body (ISO, EPA, CA SWRCB, EU Commission, WHO)
5. Exclude purely narrative reviews with no method-specific guidance

**Future search areas to explore:**
- AURORA framework papers (conceptual only, TRL 3-4 per Koelmans 2025)
- POLYRISK/MOMENTUM-specific publications (may be mostly project reports)
- Sediment extraction validation studies (Langknecht 2023 already in crosswalk)
- Microplastics in food matrices — specific preparation methods
- Nanoplastics specific detection methods (below 1 µm)

---

## New Papers from Literature Search 2026-04-21

All 8 added to Zotero (collection AKNE8BJL) and crosswalk. Ciornii et al. 2025 already existed (ID 15) — skipped.

| Citation | Zotero Key | Crosswalk ID | Tier | Key Columns |
|----------|------------|-------------|------|-------------|
| Ciornii et al., 2025 (ILC Anal. Chem.) | JSCS5RFD | 15 (pre-existing) | T3 | FTIR, Raman, PyGCMS, RefMat, InterLab |
| Lenz et al., 2024 (ring trials EST) | TRB5U5TE | 99 | T3 | FTIR, Raman, RefMat, Blanks, InterLab |
| Ashta et al., 2026 (atm. deposition AMT) | QXH62ZSF | 100 | T3 | Air, SampProc, FTIR, Blanks, DataAnal |
| Ren et al., 2026 (atm. review Springer) | RXPEWSMR | 101 | T4 | Samp, Air, SampProc, Report |
| European Commission, 2024 (Decision EU 2024/1441) | PSTRUFWX | 102 | T1 | DW, SampProc, FTIR, Raman |
| SCCWRP, 2025 (TR 1410.A sediment/biota) | BP397VWH | 103 | T1 | Samp, Sediment, Biota, SampProc, Subsamp, Blanks |
| [TBD] et al., 2025 (STAR Protocols freshwater/sed/fish) | ZVFB976N | 104 | T3 | SW, Sed, Bio, SampProc, Subsamp, Raman, RefMat, Blanks |
| [TBD] et al., 2025 (Py-GC-MS + EU 2024/1441, Environ. Pollut.) | HTI2VRRF | 105 | T3 | DW, SW, SampProc, PyGCMS, DataAnal |

### Key regulatory documents newly added (both Tier 1):
- **EU Commission Delegated Decision (EU) 2024/1441** (11 March 2024): EU-wide methodology for measuring MPs in drinking water. Requires ≥1000 L sample, filter cascade (100+20 µm), IR or Raman micro-spectroscopy. Supplements Directive (EU) 2020/2184.
- **SCCWRP Technical Report 1410.A** (April 2025, CA OPC): SOPs for surface sediment and aquatic biota (mussels, oysters, fish) sample collection. Companion to drinking water SOPs (SWB-MP1/2). Extends California Tier 1 coverage beyond DW.

---

## Papers Added to Zotero Previously (crosswalk rows already created)

### From Regulatory Readiness cited references (added via DOI):

| Citation | Zotero Key | Tier | Primary Columns |
|----------------|-----------------|----------------|-------------------------|
| Vogel et al. 2024 | A9IPX8JW | T3 | PF, Def, ToxDesign, ToxEffects, Report |
| Foss Hansen et al. 2024 (PlasticRiskCat) | 22DT35FU | T4 | PF, ToxDesign, ToxEffects |
| Koelmans et al. 2023 (TrAC) | 8AMTU2FB | T3 | Def, PF, DataAnal, Report, ToxDesign |
| Lane et al. 2025 (Exposure scenarios) | NIH492ZS | T3 | Def, PF, Samp, DW, Air, Food, HumTis |
| Qiu et al. 2025 (AI quality) | ERS2Z529 | T3 | PF, DataAnal, Report |
| Wardani et al. 2024 (PBK) | RHF3EK8P | T3 | PF, HumTis, ToxDesign, ToxEffects |
| Noventa et al. 2021 | XKCA572S | T3 | Def, PF, ToxDesign, ToxEffects |
| Wright et al. 2025 (tissue screening) | PUDABW95 | T3 | FTIR, Raman, SampProc, RefMat, HumTis, DataAnal |

### Candidate Scott additions (may already be in crosswalk — script will check):

| Citation | Zotero Key | Tier | Primary Columns |
|----------------|-----------------|----------------|-------------------------|
| Koelmans et al. 2025a (Reg. Readiness preprint) | IMZAL8Y8 | T4 | Def, PF, ToxDesign, ToxEffects, DataAnal, Report |
| De Ruijter et al. 2025 (Brief History) | HJRW7S45 | T3 | Def, PF, RefMat, Blanks, DataAnal, Report, ToxDesign, ToxEffects |
| JRC 2025 EURM-060 | DVWNDVSE | T2 | DW, SampProc, RefMat |
| ISO 16094-2:2025 | K8JP8LP7 | T1 | Samp, DW, SampProc, FTIR, Raman, RefMat, Blanks |
| Thomas et al. 2026 (Communicating Confidence) | 5BAU3XQM | T3 | Def, PF, FTIR, Raman, PyGCMS, DataAnal, Report, HumTis |
| Wright et al. 2024b (MNP concepts) | 8WEGWFBC | T3 | Def, PF, ToxDesign, ToxEffects |
| Xu et al. 2025 (Are MPs bad?) | WPVFAJZN | T3 | PF, DataAnal, Report, ToxDesign, ToxEffects |
| Kennedy et al. 2025 (Trends in Quality) | ESLWHWEW | T3 | PF, RefMat, Blanks, DataAnal, Report, ToxDesign, ToxEffects |
| Hagelskjær et al. 2025 (EasyMP) | YDLUDXK7 | T3 | Samp, SampProc, RefMat |
| Pegoraro et al. 2025 (Nanoplastic RefMat) | DB7ZYKBF | T3 | SampProc, RefMat, FTIR, Raman |

------------------------------------------------------------------------

## Key Scientific Facts for Manuscript

### Quality Pass Rates (cross-framework)

-   **de Ruijter 2020:** 0/105 studies scored on all 20 criteria; average = 44.6% of max score (range 20–77.5%)
-   **ToMEx 1.0 (Hampton 2021):** 13% of 162 aquatic tox studies pass minimum screening criteria
-   **ToMEx 2.0 (Hampton 2025):** 12% of 286 studies pass — **virtually unchanged despite field growth**
-   **NMP-TSAT (Gouin 2022):** 16.2% of 74 human health studies pass Tier 1 critical criteria (12/74)
-   **Kennedy et al. 2025:** Longitudinal trend confirms same failures persist 2016–2024

### Spectral Analysis Minimums (Schymanski 2021)

-   HQI threshold: \>70% (same as Open Specy 0.7 match score)
-   FTIR range: 1250–3600 cm⁻¹
-   Raman range: 200–2000 cm⁻¹
-   Spectral resolution: ≤8 cm⁻¹
-   Blanks: minimum 1 per 10 samples
-   Library: minimum 10 polymer types, 7 size bins

### Regulatory Readiness (Koelmans et al. 2025)

-   SCCWRP (Coffin et al. 2022) = TRL 7 — only framework in operational regulatory use
-   MICROPLASTICLAB = TRL 6 — most scientifically complete
-   California's approach is globally the most implementation-ready

### Sub-sampling (Koelmans et al. 2019)

-   Minimum 386 particles needed for polymer distribution alone
-   Many environmental studies fall below this threshold

------------------------------------------------------------------------

## Python Environment Notes

-   Python 3.10 in sandbox
-   `openpyxl` installed; use `pip install PACKAGE --b