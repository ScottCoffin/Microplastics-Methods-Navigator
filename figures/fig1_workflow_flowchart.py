"""
fig1_workflow_flowchart.py
---------------------------
Researcher decision flowchart showing the MNP research workflow,
with each step color-coded by the best available tier of guidance.
Two parallel tracks:
  Left  — Environmental Monitoring (all 7 matrices: DW, SW, Sed, Bio, Air, Food, HumTis)
  Right — Toxicology / Effects Testing

Tier color scheme (consistent with all other figures)
  Tier 1  |  #6A0DAD  purple     Regulatory / Accredited SOP
  Tier 2  |  #1565C0  blue       Authoritative Guidance
  Tier 3  |  #2E7D32  green      Peer-Reviewed Method
  Tier 4  |  #78909C  grey-blue  Supporting Science
  Gap     |  #FFCDD2  salmon     No specific guidance

Usage:
    python fig1_workflow_flowchart.py
Output:
    fig1_workflow_flowchart.html  (same directory)
"""

import json, pathlib

HERE   = pathlib.Path(__file__).parent
OUTDIR = HERE
OUTDIR.mkdir(parents=True, exist_ok=True)

# ── Color / styling helpers ───────────────────────────────────────────────────
T_COLORS = {
    1: {"bg": "#6A0DAD", "border": "#4A0080", "text": "white"},
    2: {"bg": "#1565C0", "border": "#0D47A1", "text": "white"},
    3: {"bg": "#2E7D32", "border": "#1B5E20", "text": "white"},
    4: {"bg": "#78909C", "border": "#546E7A", "text": "white"},
    0: {"bg": "#FFCDD2", "border": "#EF9A9A", "text": "#B71C1C"},  # Gap
}
T_LABELS = {1:"Tier 1", 2:"Tier 2", 3:"Tier 3", 4:"Tier 4", 0:"Gap"}

# Default box dimensions (normalized 0–1 canvas)
BOX_W = 0.072
BOX_H = 0.048
MAT_W = 0.062   # narrower boxes for the 7 matrix nodes

# ── Node definitions ──────────────────────────────────────────────────────────
# Each node: id, x, y, label, tier, shape, detail, box_w (opt), box_h (opt)
# x=0 left, x=1 right; y=0 bottom, y=1 top (y is NOT flipped — higher y = higher on canvas)
# Monitoring track: x=0.00–0.55;  Toxicology track: x=0.58–1.00

NODES = [

    # ── Shared start (diamond) ───────────────────────────────────────
    {
        "id": "start",
        "x": 0.50, "y": 0.97,
        "label": "Define Research Goal\n& Problem Formulation",
        "tier": 2,
        "shape": "diamond",
        "detail": (
            "Best practice (Tier 3): Brander et al. 2020, Cowger et al. 2020\n"
            "Framework (Tier 3): de Ruijter 2020, Gouin 2022\n"
            "Key questions: monitoring vs. effects? matrix? size range?\n"
            "Tier 2 guidance: WHO 2019 (DW context), Mehinto 2022 (SW risk framework)"
        ),
    },

    # ── Monitoring track header ──────────────────────────────────────
    {
        "id": "monitoring",
        "x": 0.27, "y": 0.88,
        "label": "Environmental\nMonitoring",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "Select matrix first — tier of available guidance varies substantially.\n"
            "Tier 1 available: Drinking Water, Sediment, Biota (sampling SOPs)\n"
            "Tier 2 available: Surface Water (Mehinto 2022 risk framework)\n"
            "Tier 3 only: Air, Food, Human Tissue\n"
            "Key decision: matrix selection drives method availability and rigor"
        ),
    },

    # ── 7 Matrix nodes (left → right in monitoring track) ────────────
    {
        "id": "matrix_dw",
        "x": 0.04, "y": 0.79,
        "label": "Drinking\nWater",
        "tier": 1,
        "shape": "rect",
        "box_w": MAT_W,
        "detail": (
            "COMPLETE Tier 1 workflow available:\n"
            "Sampling (T1): SWRCB/DDW 2025 (SWB-MP1-rev1) — 47mm SS in-line filters (20+5 µm series)\n"
            "  0.5–1 L source / 10–20 L treated; Class II BSC; field blanks 1 per event\n"
            "Lab Processing (T1): SWB-MP1/MP2-rev1 — density separation, enzymatic digestion\n"
            "FTIR (T1): SWB-MP1-rev1, ISO 16094-2:2025, EU Decision 2024/1441 — size ≥5 µm; HQI >70%\n"
            "Raman (T1): SWB-MP2-rev1, ISO 16094-2:2025 — size ≥1 µm; HQI >70%\n"
            "Py-GC-MS (T3): EU Decision 2024/1441, Dalmau-Soler 2025 — ≥1000 L sample; mass by polymer\n"
            "Only matrix with full regulatory SOP coverage across ALL workflow steps"
        ),
    },
    {
        "id": "matrix_sw",
        "x": 0.12, "y": 0.79,
        "label": "Surface Water /\nWastewater",
        "tier": 2,
        "shape": "rect",
        "box_w": MAT_W,
        "detail": (
            "Best: Tier 2 risk framework (Mehinto et al. 2022)\n"
            "Sampling (T3): Sutton 2019 (SF Bay multi-matrix); Mayer 2024 (tire wear particles)\n"
            "Lab Processing (T3): Vural 2025 (H\u2082O\u2082/NaClO-KOH digestion); Schymanski 2021\n"
            "FTIR/Raman (T3): Schymanski 2021 — 12-lab European consensus; same specs as DW\n"
            "Risk Framework (T2): Mehinto 2022 — CA SWRCB aquatic ecosystem action levels\n"
            "GAP: No Tier 1/2 SOP for sampling or extraction/lab processing"
        ),
    },
    {
        "id": "matrix_sed",
        "x": 0.20, "y": 0.79,
        "label": "Sediment /\nSoil",
        "tier": 1,
        "shape": "rect",
        "box_w": MAT_W,
        "detail": (
            "Tier 1 sampling SOP now available:\n"
            "Sampling (T1): SCCWRP 2025 (TR 1410.A) — surface sediment grab sampling; CA OPC Tier 1\n"
            "Lab Processing (T3): Langknecht 2023 (interlaboratory comparison); Vural 2025\n"
            "Analysis (T3): Raman — Vural 2025 (H\u2082O\u2082+KOH digestion + \u00b5-Raman ID)\n"
            "Method context: Waldschl\u00e4ger 2022 — sediment science applied to MPs (natural particle analogs)\n"
            "GAP: No Tier 1 lab processing or analytical SOP specific to sediment"
        ),
    },
    {
        "id": "matrix_bio",
        "x": 0.28, "y": 0.79,
        "label": "Biota /\nTissue",
        "tier": 1,
        "shape": "rect",
        "box_w": MAT_W,
        "detail": (
            "Tier 1 sampling SOP now available:\n"
            "Sampling (T1): SCCWRP 2025 (TR 1410.A) — mussels, oysters, fish tissue dissection; CA OPC\n"
            "QA Framework (T3): de Jourdan 2024 — biota biomonitoring quality scoring rubric\n"
            "Extraction (T3): Vural 2025 — H\u2082O\u2082/NaClO-KOH digestion validated for fish tissue\n"
            "Analysis (T3): \u00b5-Raman (Vural 2025); visual sort (Provencher 2019 marine bird protocol)\n"
            "Interlaboratory (T3): Tsangaris 2021 — biota tissue extraction ILC (Plastic Busters)\n"
            "TRL assessment: Vanavermaete 2024 — method maturity guide for biota matrices\n"
            "GAP: No Tier 1 analytical SOP for biota"
        ),
    },
    {
        "id": "matrix_air",
        "x": 0.36, "y": 0.79,
        "label": "Air /\nAtmos.",
        "tier": 3,
        "shape": "rect",
        "box_w": MAT_W,
        "detail": (
            "Best available: Tier 3 only\n"
            "Sampling (T3): Ashta 2026 — novel on-site wet deposition filtration; ~90% spike-recovery\n"
            "Sampling (T3): Wright 2021 — atmospheric deposition screening criteria\n"
            "Review (T4): Ren 2026 — passive vs. active air sampling; calls for standardization\n"
            "Analysis (T3): FPA-\u00b5FTIR (Ashta 2026) — particle count and type identification\n"
            "GAP: No Tier 1/2 SOP; active vs. passive sampler debate unresolved\n"
            "Key challenge: highly variable deposition; no consensus on collection period or volume"
        ),
    },
    {
        "id": "matrix_food",
        "x": 0.43, "y": 0.79,
        "label": "Food /\nDiet",
        "tier": 3,
        "shape": "rect",
        "box_w": MAT_W,
        "detail": (
            "Best available: Tier 3 (limited; no sampling-specific SOP)\n"
            "Exposure framework (T3): Gouin 2022 — dietary + inhalation route framework for human health\n"
            "Quantitative scenarios (T3): Lane 2025 — multi-route exposure (oral, inhalation, dermal)\n"
            "GAP: No standardized food sampling or matrix-specific extraction SOP\n"
            "No Tier 1/2 guidance for food-specific sample preparation\n"
            "Key challenge: highly variable food matrices (liquids, solids, processed foods)\n"
            "Recommended: adapt DW/biota principles; document all deviations"
        ),
    },
    {
        "id": "matrix_humtis",
        "x": 0.50, "y": 0.79,
        "label": "Human\nTissue",
        "tier": 3,
        "shape": "rect",
        "box_w": MAT_W,
        "detail": (
            "Best available: Tier 3 (growing area; no sampling SOP)\n"
            "Spectroscopic ID (T3): Wright 2025b — FTIR/Raman framework for pathological tissue (in situ)\n"
            "Py-GC-MS (T3): Rauert 2025 — validated for human blood; mass by polymer type\n"
            "PBK Modeling (T3): Wardani 2024 — physiologically-based kinetic model for NMP bioaccumulation\n"
            "Exposure (T3): Lane 2025 — quantitative scenarios across oral/inhalation/dermal routes\n"
            "Risk Integration: Coffin 2022 — DW monitoring \u2192 human health RA (used in CA regulation)\n"
            "GAP: No standardized clinical collection SOP; no consensus reference material for biomonitoring"
        ),
    },

    # ── Shared monitoring workflow steps ─────────────────────────────
    {
        "id": "sampling",
        "x": 0.27, "y": 0.67,
        "label": "Sampling\n(Field Collection)",
        "tier": 1,
        "shape": "rect",
        "detail": (
            "Tier by matrix:\n"
            "  Drinking Water (T1): SWRCB/DDW 2025 — 47mm SS in-line filters (20+5 \u00b5m); field blanks 1/event\n"
            "  Sediment & Biota (T1): SCCWRP 2025 (TR 1410.A) — grab sampling + biota dissection\n"
            "  Surface Water (T3): Sutton 2019, Mayer 2024 — manta nets, bulk collection; no regulatory SOP\n"
            "  Air / Atmos. (T3): Ashta 2026 (wet deposition device); Wright 2021 (passive deposition)\n"
            "  Food / Human Tissue (T3/Gap): No standardized SOP; adapt nearest matrix guidelines\n"
            "Universal: always record collection vessel, location, date/time, personnel"
        ),
    },
    {
        "id": "labproc",
        "x": 0.27, "y": 0.56,
        "label": "Lab Processing\n& Extraction",
        "tier": 1,
        "shape": "rect",
        "detail": (
            "Tier by matrix:\n"
            "  Drinking Water (T1): SWB-MP1/MP2-rev1 — density separation; enzymatic digestion option\n"
            "    LOD = mean(blanks) + 3 SD; min n=3; EPA recommends n=7 blanks\n"
            "  Sediment/Biota (T1 framework, T3 methods): SCCWRP 2025; KOH or H\u2082O\u2082/NaClO-KOH digestion\n"
            "  Surface Water (T3): Schymanski 2021 consensus; Vural 2025 (H\u2082O\u2082+KOH)\n"
            "  Air (T3): Ashta 2026 — on-site filter processing\n"
            "  Food/HumTis (T3/Gap): Adapt DW/biota principles; document deviations\n"
            "Universal contamination control: cotton lab coats, aluminum foil, glass/metal labware"
        ),
    },
    {
        "id": "subsample",
        "x": 0.27, "y": 0.46,
        "label": "Sub-sampling\n(if needed)",
        "tier": 4,
        "shape": "rect",
        "detail": (
            "Cowger et al. 2024 (Tier 4 supporting science):\n"
            "  Minimum 386 particles for polymer distribution at 5% error (95% CI)\n"
            "  Minimum 620 particles for polymer + color + size + morphology\n"
            "  Sample size formula: n = error\u207b\u00b2\n"
            "  Particles must be randomly selected from the full population\n"
            "Applies equally to ALL matrices where sub-sampling is performed\n"
            "GAP: No Tier 1/2/3 SOP for sub-sampling — supporting science only"
        ),
    },
    {
        "id": "analysis",
        "x": 0.27, "y": 0.35,
        "label": "Spectroscopic\nAnalysis",
        "tier": 1,
        "shape": "diamond",
        "detail": (
            "Choose method based on particle size and study goals:\n"
            "  FTIR: Best for \u226510 \u00b5m (DW Tier 1: \u22655 \u00b5m); wavenumber 1250\u20133600 cm\u207b\u00b9; HQI >70%\n"
            "  Raman: Best for 1\u201310 \u00b5m (DW Tier 1: \u22651 \u00b5m); wavenumber 200\u20132000 cm\u207b\u00b9; HQI >70%\n"
            "  Py-GC-MS: Mass-based; no size/shape data; all sizes; EU Decision 2024/1441 (DW/SW)\n"
            "Spectral matching: Open Specy 1.0 threshold = 0.7 (>40K spectra, 34 databases)\n"
            "Best tier by matrix: DW=T1; Sed/Bio/SW=T3; Air=T3; Food/HumTis=T3"
        ),
    },
    {
        "id": "ftir",
        "x": 0.14, "y": 0.24,
        "label": "FTIR / \u00b5FTIR",
        "tier": 1,
        "shape": "rect",
        "detail": (
            "Tier 1 SOPs (DW): SWB-MP1-rev1, ISO 16094-2:2025, EU Decision 2024/1441\n"
            "Tier 3 general: Schymanski 2021 (12-lab European consensus for clean water)\n"
            "Tier 3 air: Ashta 2026 (FPA-\u00b5FTIR for atmospheric wet deposition; ~90% recovery)\n"
            "Specifications:\n"
            "  Wavenumber range: 1250\u20133600 cm\u207b\u00b9 (minimum); full MID-IR best practice\n"
            "  Spectral resolution: \u22648 cm\u207b\u00b9; HQI threshold: >70%\n"
            "  Particle size: \u22655 \u00b5m (DW SOP); \u226510 \u00b5m typical FPA-\u00b5FTIR\n"
            "Reports: particle count, polymer type, size distribution, morphology"
        ),
    },
    {
        "id": "raman",
        "x": 0.27, "y": 0.24,
        "label": "Raman /\n\u00b5Raman",
        "tier": 1,
        "shape": "rect",
        "detail": (
            "Tier 1 SOPs (DW): SWB-MP2-rev1, ISO 16094-2:2025\n"
            "Tier 3 general: Schymanski 2021 (12-lab European consensus)\n"
            "Tier 3 multi-matrix: Vural 2025 (\u00b5-Raman after KOH/H\u2082O\u2082 digestion — SW/Sed/Bio)\n"
            "Specifications:\n"
            "  Wavenumber range: 200\u20132000 cm\u207b\u00b9; laser 532 nm or 785 nm\n"
            "  HQI threshold: >70%; human review recommended above threshold\n"
            "  Particle size: \u22651 \u00b5m; better sensitivity for submicron vs. FTIR\n"
            "Reports: particle count, polymer type, size distribution"
        ),
    },
    {
        "id": "pygcms",
        "x": 0.41, "y": 0.24,
        "label": "Py-GC-MS",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "Tier 3 (DW/SW): Dalmau-Soler 2025 — EU Decision 2024/1441 Py-GC-MS implementation\n"
            "  Glass-fiber filter + Py-GC-MS; applied to Llobregat river basin \u2192 Barcelona DW\n"
            "  92\u201399% removal demonstrated in drinking water treatment\n"
            "Tier 3 (Human Blood): Rauert 2025 — validated Py-GC-MS for blood biomonitoring\n"
            "No Tier 1/2 SOP in any matrix; no consensus calibration or reference material\n"
            "Reports: mass concentration by polymer type (NOT particle count or size)\n"
            "Key advantage: applicable to complex matrices; no particle isolation needed"
        ),
    },
    {
        "id": "qa",
        "x": 0.27, "y": 0.13,
        "label": "QA/QC &\nContamination Control",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "Universal requirements (all matrices):\n"
            "Brander et al. 2020 (T3): LOD = mean(blanks) + 3 SD; min 3 procedural blanks/study\n"
            "Cowger et al. 2020b (T3): 8 minimum reporting categories (all matrices)\n"
            "de Ruijter 2020 (T3): 20 QA/QC criteria for effects studies\n"
            "Key rules:\n"
            "  \u2022 Always subtract blank-corrected values; report before AND after correction\n"
            "  \u2022 Contamination control: cotton lab coats, Al foil, glass/metal labware\n"
            "  \u2022 Procedural blanks through all extraction steps\n"
            "  \u2022 Minimum 1 field + 1 procedural blank per 10 samples"
        ),
    },
    {
        "id": "report_env",
        "x": 0.44, "y": 0.07,
        "label": "Reporting &\nData Deposition",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "Cowger et al. 2020b (T3): 8 minimum reporting categories (applies to all matrices)\n"
            "Data deposition: One4All / Sherrod et al. 2024 (T3/4)\n"
            "  \u2192 openanalysis.org/one4all/ — 81 validation rules, FAIR principles\n"
            "  \u2192 Mandated for CA drinking water monitoring programs\n"
            "Spectral data: Open Specy 1.0 (Cowger 2025) — >40K spectra, 34 databases\n"
            "DW-specific: Annual reporting to CA DDW; standardized reporting template\n"
            "All matrices MUST report: polymer type, size bins, morphology, blank correction, LOD"
        ),
    },

    # ── Toxicology track ─────────────────────────────────────────────
    {
        "id": "toxicology",
        "x": 0.79, "y": 0.88,
        "label": "Toxicology /\nEffects Testing",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "de Ruijter 2020, Gouin 2022, Cowger 2020b (all Tier 3)\n"
            "Key: define study purpose first — mechanistic vs. hazard/risk vs. dose-response\n"
            "Quality pass rates extremely low:\n"
            "  ToMEx 2.0 (Hampton 2025): only 12% of 286 studies pass screening\n"
            "  NMP-TSAT (Gouin 2022): 16.2% of 74 human health studies pass Tier 1"
        ),
    },
    {
        "id": "tox_type",
        "x": 0.79, "y": 0.77,
        "label": "Study Type?",
        "tier": 3,
        "shape": "diamond",
        "detail": (
            "Ecological / Aquatic: de Ruijter 2020 (20 criteria), ToMEx 2.0 submission\n"
            "Human Health: Gouin 2022 NMP-TSAT (26 in vivo / 23 in vitro criteria), ToMEx-HH\n"
            "Mechanistic: flexible design; NMP-TSAT guidance still applicable\n"
            "Note: de Ruijter 2020 avg score 44.6%; NMP-TSAT 16.2% pass"
        ),
    },
    {
        "id": "tox_eco",
        "x": 0.67, "y": 0.66,
        "label": "Ecological\n(Aquatic)",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "de Ruijter 2020 (Tier 3): 20 criteria, 4 categories\n"
            "Average published score: 44.6% (0/105 studies scored on all criteria)\n"
            "ToMEx 2.0 (Hampton 2025): only 12% of 286 studies pass for threshold derivation\n"
            "Kennedy et al. 2025: same failures persist 2016\u20132024"
        ),
    },
    {
        "id": "tox_hh",
        "x": 0.91, "y": 0.66,
        "label": "Human Health\n(In vivo / In vitro)",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "Gouin 2022 NMP-TSAT (Tier 3): 26 criteria (in vivo), 23 (in vitro)\n"
            "Only 12/74 human health studies passed Tier 1 screening (16.2%)\n"
            "OECD test guidelines recommended where applicable\n"
            "Wardani 2024: PBK model for NMP bioaccumulation; Noventa 2021: bioavailability"
        ),
    },
    {
        "id": "particle_char",
        "x": 0.79, "y": 0.55,
        "label": "Particle\nCharacterization",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "Required by de Ruijter, Gouin, and Cowger 2020b (all Tier 3):\n"
            "  \u2022 Polymer type confirmed by spectroscopy (FTIR or Raman)\n"
            "  \u2022 Full size distribution (\u226510 bins if a range is used)\n"
            "  \u2022 Shape with high-resolution image\n"
            "  \u2022 Both mass AND number concentration\n"
            "Critical: wash particles with organic solvent (remove preservatives/additives)\n"
            "Avoid: unwashed PS spheres without explicit scientific justification"
        ),
    },
    {
        "id": "ref_materials",
        "x": 0.79, "y": 0.44,
        "label": "Reference Materials\n& Exposure Prep",
        "tier": 4,
        "shape": "rect",
        "detail": (
            "GAP: No consensus reference material for human health or ecotox exposure studies\n"
            "Available (limited): EURM\u00ae-060 (EU certified ~10 \u00b5m PET in water); commercial options\n"
            "Pegoraro 2025: nanoplastic reference materials (Tier 3 — limited)\n"
            "Arpa-H call for reference standards (ongoing as of 2025)\n"
            "Best practice: document particle source/lot#; verify via spectroscopy; wash with solvent\n"
            "Avoid: PS spheres alone (not environmentally representative)"
        ),
    },
    {
        "id": "exp_design",
        "x": 0.79, "y": 0.33,
        "label": "Experimental Design\n& Dosimetry",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "de Ruijter 2020 criteria:\n"
            "  Criterion 9: verify \u226580% of nominal concentration throughout test\n"
            "  Criterion 12: \u22653 replicates minimum\n"
            "  Criterion 16: \u22656 doses including control for dose-response curve\n"
            "  Criterion 17: >1 environmentally relevant concentration\n"
            "Gouin NMP-TSAT (CRITICAL): dose-response for POD (NOAEL/LOAEL/BMD)\n"
            "Noventa 2021: bioavailability / bioaccessibility must be considered"
        ),
    },
    {
        "id": "effects",
        "x": 0.79, "y": 0.22,
        "label": "Effects Testing\n& Endpoint Reporting",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "de Ruijter 2020:\n"
            "  Criterion 13: community-level or individual-level endpoints\n"
            "  Criterion 15: L(E)Cx WITH uncertainty intervals required\n"
            "  Criterion 18: aged/biofouled particles for environmental realism\n"
            "  Criterion 19: multiple polymer types; avoid PS sphere monoculture\n"
            "  Criterion 20: longer exposure durations; align with standard ecotox guidelines\n"
            "Gouin NMP-TSAT: highest-priority criteria include dose-response and POD derivation"
        ),
    },
    {
        "id": "report_tox",
        "x": 0.79, "y": 0.10,
        "label": "Reporting &\nData Deposition",
        "tier": 3,
        "shape": "rect",
        "detail": (
            "Reporting: Cowger 2020b 8 categories + de Ruijter/Gouin criteria\n"
            "Data deposition: ToMEx 2.0 (microplastics.sccwrp.org)\n"
            "  \u2192 Aquatic organisms database\n"
            "  \u2192 Human health database\n"
            "  \u2192 89% of current studies fail minimum ToMEx screening criteria\n"
            "Raw data deposition strongly encouraged (FAIR principles)"
        ),
    },
]

# ── Edges ─────────────────────────────────────────────────────────────────────
EDGES = [
    # Decision branch
    ("start",        "monitoring",     ""),
    ("start",        "toxicology",     ""),
    # Monitoring → 7 matrices
    ("monitoring",   "matrix_dw",      ""),
    ("monitoring",   "matrix_sw",      ""),
    ("monitoring",   "matrix_sed",     ""),
    ("monitoring",   "matrix_bio",     ""),
    ("monitoring",   "matrix_air",     ""),
    ("monitoring",   "matrix_food",    ""),
    ("monitoring",   "matrix_humtis",  ""),
    # All 7 matrices → shared workflow
    ("matrix_dw",    "sampling",       ""),
    ("matrix_sw",    "sampling",       ""),
    ("matrix_sed",   "sampling",       ""),
    ("matrix_bio",   "sampling",       ""),
    ("matrix_air",   "sampling",       ""),
    ("matrix_food",  "sampling",       ""),
    ("matrix_humtis","sampling",       ""),
    # Shared monitoring workflow
    ("sampling",     "labproc",        ""),
    ("labproc",      "subsample",      ""),
    ("subsample",    "analysis",       ""),
    ("analysis",     "ftir",           ""),
    ("analysis",     "raman",          ""),
    ("analysis",     "pygcms",         ""),
    ("ftir",         "qa",             ""),
    ("raman",        "qa",             ""),
    ("pygcms",       "qa",             ""),
    ("qa",           "report_env",     ""),
    # Toxicology workflow
    ("toxicology",   "tox_type",       ""),
    ("tox_type",     "tox_eco",        "Ecotox"),
    ("tox_type",     "tox_hh",         "Human Health"),
    ("tox_eco",      "particle_char",  ""),
    ("tox_hh",       "particle_char",  ""),
    ("particle_char","ref_materials",  ""),
    ("ref_materials","exp_design",     ""),
    ("exp_design",   "effects",        ""),
    ("effects",      "report_tox",     ""),
]

# ── Build figure geometry ─────────────────────────────────────────────────────
node_map = {n["id"]: n for n in NODES}

def box_bounds(n):
    cx, cy = n["x"], n["y"]
    bw = n.get("box_w", BOX_W)
    bh = n.get("box_h", BOX_H)
    return cx - bw/2, cy - bh/2, cx + bw/2, cy + bh/2

shapes = []
for n in NODES:
    tc = T_COLORS[n["tier"]]
    x0, y0, x1, y1 = box_bounds(n)
    if n["shape"] == "diamond":
        mx, my = (x0+x1)/2, (y0+y1)/2
        path = f"M {mx},{y1} L {x1},{my} L {mx},{y0} L {x0},{my} Z"
        shapes.append({
            "type": "path",
            "path": path,
            "fillcolor": tc["bg"],
            "line": {"color": tc["border"], "width": 1.5},
            "layer": "above",
        })
    else:
        shapes.append({
            "type": "rect",
            "x0": x0, "y0": y0, "x1": x1, "y1": y1,
            "fillcolor": tc["bg"],
            "line": {"color": tc["border"], "width": 1.5},
            "layer": "above",
        })

# Edge lines (straight arrows)
edge_traces = []
for (src, dst, lbl) in EDGES:
    ns = node_map[src]
    nd = node_map[dst]
    bh_s = ns.get("box_h", BOX_H)
    bh_d = nd.get("box_h", BOX_H)
    x0, y0 = ns["x"], ns["y"] - bh_s/2
    x1, y1 = nd["x"], nd["y"] + bh_d/2
    edge_traces.append({
        "type": "scatter",
        "x": [x0, x1],
        "y": [y0, y1],
        "mode": "lines",
        "line": {"color": "#BBBBBB", "width": 1.0},
        "hoverinfo": "skip",
        "showlegend": False,
    })
    edge_traces.append({
        "type": "scatter",
        "x": [x1],
        "y": [y1],
        "mode": "markers",
        "marker": {"symbol": "triangle-up", "size": 6, "color": "#AAAAAA"},
        "hoverinfo": "skip",
        "showlegend": False,
    })
    if lbl:
        edge_traces.append({
            "type": "scatter",
            "x": [(x0+x1)/2],
            "y": [(y0+y1)/2],
            "mode": "text",
            "text": [lbl],
            "textfont": {"size": 8, "color": "#666666"},
            "hoverinfo": "skip",
            "showlegend": False,
        })

# Node labels + hover
node_trace = {
    "type": "scatter",
    "x": [n["x"] for n in NODES],
    "y": [n["y"] for n in NODES],
    "mode": "text",
    "text": [n["label"].replace("\n", "<br>") for n in NODES],
    "hovertext": [
        (
            f"<b>{n['label'].replace(chr(10), ' ')}</b><br>"
            f"Best available guidance: <b>{T_LABELS[n['tier']]}</b><br><br>"
            f"{n['detail'].replace(chr(10), '<br>')}"
        )
        for n in NODES
    ],
    "hovertemplate": "%{hovertext}<extra></extra>",
    "hoverlabel": {"bgcolor": "white", "bordercolor": "#CCCCCC",
                   "font": {"size": 11}},
    "showlegend": False,
    "textfont": {
        "size": [7.5 if n.get("box_w", BOX_W) <= MAT_W else 8
                 for n in NODES],
        "color": [T_COLORS[n["tier"]]["text"] for n in NODES],
    },
}

# Track header annotations
header_annotations = [
    {"x": 0.27, "y": 1.015, "xref": "paper", "yref": "paper",
     "text": "<b>Environmental Monitoring Track</b>",
     "showarrow": False, "font": {"size": 13, "color": "#2E7D32"}, "align": "center"},
    {"x": 0.79, "y": 1.015, "xref": "paper", "yref": "paper",
     "text": "<b>Toxicology / Effects Testing Track</b>",
     "showarrow": False, "font": {"size": 13, "color": "#8E24AA"}, "align": "center"},
]

# Legend traces
legend_traces = []
for tier, color in [(1,"#6A0DAD"),(2,"#1565C0"),(3,"#2E7D32"),(4,"#78909C"),(0,"#FFCDD2")]:
    legend_traces.append({
        "type": "scatter", "x": [None], "y": [None],
        "mode": "markers",
        "marker": {"color": color, "size": 14, "symbol": "square"},
        "name": {
            1: "Tier 1 \u2014 Regulatory/Accredited SOP",
            2: "Tier 2 \u2014 Authoritative Guidance",
            3: "Tier 3 \u2014 Peer-Reviewed Method",
            4: "Tier 4 \u2014 Supporting Science",
            0: "Gap \u2014 No specific guidance",
        }[tier],
        "showlegend": True,
    })

# Background shading + divider
shapes = [
    {"type": "rect", "x0": 0, "y0": 0, "x1": 0.56, "y1": 1.0,
     "fillcolor": "#F8FFF8", "line": {"width": 0}, "layer": "below"},
    {"type": "rect", "x0": 0.58, "y0": 0, "x1": 1.0, "y1": 1.0,
     "fillcolor": "#FDF5FF", "line": {"width": 0}, "layer": "below"},
    {"type": "line", "x0": 0.57, "y0": 0, "x1": 0.57, "y1": 1.0,
     "line": {"color": "#DDDDDD", "width": 1.2, "dash": "dot"}},
] + shapes

layout = {
    "title": {
        "text": (
            "<b>MNP Research Workflow \u2014 Decision Guide</b><br>"
            "<sup>Hover over any step for tier details, specifications, and key citations. "
            "All 7 environmental matrices shown in monitoring track.</sup>"
        ),
        "x": 0.5, "font": {"size": 15},
    },
    "xaxis": {"visible": False, "range": [-0.02, 1.02]},
    "yaxis": {"visible": False, "range": [-0.03, 1.06]},
    "plot_bgcolor": "#FFFFFF",
    "paper_bgcolor": "#FFFFFF",
    "shapes": shapes,
    "annotations": header_annotations,
    "legend": {
        "orientation": "h",
        "yanchor": "bottom", "y": -0.07,
        "xanchor": "center", "x": 0.5,
        "font": {"size": 11},
    },
    "margin": {"t": 85, "b": 80, "l": 10, "r": 10},
    "height": 780,
}

all_traces = legend_traces + edge_traces + [node_trace]
fig_json = json.dumps({"data": all_traces, "layout": layout})

HTML = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Fig 1 \u2013 MNP Research Workflow Decision Guide</title>
  <script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>
  <style>body{{margin:0;font-family:sans-serif;}}</style>
</head>
<body>
  <div id="fig" style="width:100%;height:830px;"></div>
  <script>
    var fig = {fig_json};
    Plotly.newPlot('fig', fig.data, fig.layout, {{responsive:true, displayModeBar:true}});
  </script>
</body>
</html>"""

out_path = OUTDIR / "fig1_workflow_flowchart.html"
out_path.write_text(HTML, encoding="utf-8")
print(f"Saved: {out_path}")
print(f"  Nodes: {len(NODES)}, Edges: {len(EDGES)}")
