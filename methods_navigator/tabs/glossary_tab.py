"""Glossary tab for the MP Methods Navigator."""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Glossary data
# Each entry: term, category, definition, decision_tree_relevance
# ---------------------------------------------------------------------------

GLOSSARY: list[dict] = [
    # ── Particle Terminology ────────────────────────────────────────────────
    {
        "term": "Microplastics (MPs)",
        "category": "Particle Terminology",
        "definition": (
            "Plastic particles with a longest dimension of 1 µm–5 mm. "
            "The 5 mm upper bound is broadly agreed; the lower bound varies: "
            "ISO 21994 uses 1 µm; NOAA's original definition (≤5 mm) specifies no lower bound; "
            "ECHA's REACH restriction and some EU legislation use 1 nm. "
            "Definitions also differ on whether semi-synthetic and coated materials are included."
        ),
        "decision_tree_relevance": (
            "The size definition adopted determines which particles are counted and which methods are appropriate. "
            "Navigate to Definitions & Terminology in any matrix branch to compare regulatory and scientific definitions."
        ),
    },
    {
        "term": "Nanoplastics (NPs)",
        "category": "Particle Terminology",
        "definition": (
            "Plastic particles smaller than 1 µm (ISO/TR 21960) or <100 nm (EU nanomaterial definition). "
            "No internationally harmonized definition exists. "
            "Colloidal behavior dominates at this scale, making conventional MP methods inapplicable."
        ),
        "decision_tree_relevance": (
            "CRITICAL GAP: No standardized detection or quantification method exists for NPs. "
            "ISO 16094-2 specifies a 20 µm practical minimum for most FTIR approaches. "
            "The gap note in the decision tree flags this as the most significant unresolved standardization challenge."
        ),
    },
    {
        "term": "Primary Microplastics",
        "category": "Particle Terminology",
        "definition": (
            "Intentionally manufactured plastic particles at the micro scale: microbeads in personal care products, "
            "pre-production pellets/nurdles, industrial powders, and plastic abrasives. "
            "Released directly into the environment without further fragmentation."
        ),
        "decision_tree_relevance": (
            "Relevant to source investigation studies and regulatory scope (ECHA's restriction targets intentionally added MPs). "
            "Morphologically uniform — generally easier to spike and recover than secondary MPs."
        ),
    },
    {
        "term": "Secondary Microplastics",
        "category": "Particle Terminology",
        "definition": (
            "Particles produced by fragmentation of larger plastic items via UV photodegradation, "
            "mechanical abrasion (tire wear, washing of synthetic textiles), or biological processes. "
            "The dominant source of environmental MPs. Highly irregular in morphology and surface chemistry."
        ),
        "decision_tree_relevance": (
            "Irregular shapes and heterogeneous surfaces complicate spectral library matching and size measurement. "
            "Monitoring studies must account for the morphological diversity of secondary MPs in their reporting."
        ),
    },
    {
        "term": "Particle Morphology / Shape",
        "category": "Particle Terminology",
        "definition": (
            "The physical form of a microplastic: fragment (irregular, angular), fiber (elongated, aspect ratio >3:1), "
            "film (thin flat sheet), pellet/nurdle (pre-production spheroid), foam, or bead (spherical). "
            "Shape must be defined and recorded consistently. Fibers present special challenges for size measurement "
            "(length vs. width) and for spectral analysis due to orientation effects."
        ),
        "decision_tree_relevance": (
            "Morphology must be reported under Reporting & Harmonization guidelines. "
            "Some methods (µRaman) better resolve fine fibers than FTIR. "
            "Fiber aspect ratios affect toxicological mode of action in in vitro and in vivo studies."
        ),
    },
    {
        "term": "Weathered / Environmentally Aged Polymers",
        "category": "Particle Terminology",
        "definition": (
            "Plastics subjected to UV irradiation, thermal stress, chemical oxidation, or mechanical abrasion — "
            "simulating environmental aging. Weathering increases surface oxygen content (carbonyl groups, hydroxyl groups), "
            "alters crystallinity, increases brittleness and fragmentation rate, and changes leachate/additive release profiles. "
            "Also called 'field-collected' or 'environmentally relevant' MPs when derived from aged natural samples."
        ),
        "decision_tree_relevance": (
            "Toxicology: pristine commercial beads are not environmentally representative; weathered particles are preferred "
            "for ecological relevance but lack standardized preparation protocols. "
            "Navigate to Reference / Test Particles for guidance on particle selection."
        ),
    },
    {
        "term": "Polymer Type",
        "category": "Particle Terminology",
        "definition": (
            "The chemical identity of the plastic: polyethylene (PE), polypropylene (PP), polystyrene (PS), "
            "polyethylene terephthalate (PET), polyamide (PA/Nylon), polyvinyl chloride (PVC), "
            "polycarbonate (PC), and others. Determined by IR or Raman spectral library matching (particle-counting methods) "
            "or by pyrolysis product fingerprinting (mass-based methods)."
        ),
        "decision_tree_relevance": (
            "Polymer type determines density (affecting density separation efficiency — PET and PVC sink in NaCl solutions), "
            "spectral signature (affecting analytical identification), and toxicological relevance. "
            "All spectroscopic methods provide polymer identification; Py-GC-MS and TED-GC-MS provide mass-based polymer quantification."
        ),
    },
    {
        "term": "Synthetic vs. Semi-Synthetic Particles",
        "category": "Particle Terminology",
        "definition": (
            "Synthetic particles are virgin petroleum-derived polymers (e.g., polystyrene beads, PE pellets). "
            "Semi-synthetic particles derive from natural polymers modified with synthetic chemistry "
            "(cellulose acetate, rayon/viscose, lyocell). Regulatory scope varies: "
            "ECHA's restriction and ISO 11097 include synthetic polymers only and generally exclude semi-synthetics."
        ),
        "decision_tree_relevance": (
            "Critical for scope decisions in monitoring and toxicology — whether cellulose acetate fibers (cigarette filter waste) "
            "are counted depends on the definition adopted. "
            "Navigate to Definitions & Terminology to see how different standards handle this boundary."
        ),
    },
    {
        "term": "Lower Limit of Detection (LLOD) / Minimum Reportable Size",
        "category": "Particle Terminology",
        "definition": (
            "The smallest particle size that can be reliably detected AND polymer-identified by the method under routine conditions. "
            "Distinct from instrument spatial resolution (the smallest feature physically resolvable). "
            "Approximate LLODs: µFTIR/LDIR ~20–50 µm; µRaman ~1 µm; Py-GC-MS and TED-GC-MS have no particle-level LLOD (bulk method)."
        ),
        "decision_tree_relevance": (
            "Must be reported in all monitoring studies. Studies with different LLODs cannot be directly compared — "
            "a study reporting ≥20 µm captures far fewer particles than one reporting ≥1 µm. "
            "Size limit selection is covered under Definitions & Terminology and Analytical Identification branches."
        ),
    },
    {
        "term": "Upper Size Limit / Mesh Size",
        "category": "Particle Terminology",
        "definition": (
            "The largest particle captured by the sampling device: manta trawl mesh (~330 µm), "
            "filter pore size, or sieve aperture. Particles larger than the collection aperture are excluded. "
            "Together with LLOD, defines the size window of the study."
        ),
        "decision_tree_relevance": (
            "Must be reported alongside LLOD in Reporting & Harmonization. "
            "Manta trawls (330 µm mesh) capture only a fraction of environmental MPs; "
            "pump-based sampling with smaller filters is preferred for comprehensive size coverage."
        ),
    },

    # ── Study Types & Design ────────────────────────────────────────────────
    {
        "term": "Problem Formulation",
        "category": "Study Design",
        "definition": (
            "The foundational step of any study or risk assessment that explicitly defines: "
            "(1) the assessment endpoint (what is being protected?), "
            "(2) the exposure scenario (who is exposed, to what, by which route?), "
            "(3) the study scope (geographic extent, chemicals of concern, matrix, species), and "
            "(4) the policy question being addressed. "
            "Problem formulation determines which data and methods are relevant and prevents scope creep."
        ),
        "decision_tree_relevance": (
            "The first step BEFORE navigating the decision tree. "
            "Your problem formulation determines which study type (Monitoring / Toxicology / Risk Assessment), "
            "matrix, and workflow step are relevant to your question."
        ),
    },
    {
        "term": "Environmental Monitoring",
        "category": "Study Design",
        "definition": (
            "Systematic collection and analysis of environmental, food, or human samples to detect, "
            "quantify, and characterize MPs. Generates occurrence data describing what is present and at what concentrations. "
            "Does not establish causation. Subtypes include ambient characterization, change detection, flux studies, "
            "and source investigation."
        ),
        "decision_tree_relevance": (
            "Primary domain in the decision tree. References tagged 'Monitoring' or 'Both' in Primary Domain. "
            "Navigate via Study Type → Environmental Monitoring."
        ),
    },
    {
        "term": "Ambient Characterization / Occurrence Study",
        "category": "Study Design",
        "definition": (
            "A monitoring study designed to describe the baseline presence, concentrations, size distributions, "
            "and polymer composition of MPs in a specific environment — without a change detection or source attribution objective. "
            "Most published MP monitoring studies fall into this category."
        ),
        "decision_tree_relevance": (
            "Standard monitoring objective. Method standardization is essential for comparability across studies. "
            "Navigate: Monitoring → select matrix → Sampling through Reporting steps."
        ),
    },
    {
        "term": "Change Detection / Temporal Trend",
        "category": "Study Design",
        "definition": (
            "A monitoring study designed to detect a statistically significant change in MP concentrations "
            "or characteristics over time or across a spatial gradient. "
            "Requires a priori power analysis, replicated sampling, and strictly standardized methods across time points."
        ),
        "decision_tree_relevance": (
            "Drives requirements for Data Analysis & Statistics (sub-sampling, uncertainty quantification, statistical power). "
            "Method changes between sampling rounds invalidate trend detection."
        ),
    },
    {
        "term": "Source Investigation / Fingerprinting",
        "category": "Study Design",
        "definition": (
            "A monitoring study aimed at identifying the origin(s) of MPs (e.g., tire wear vs. textile fibers vs. agricultural plastic). "
            "Uses polymer type profiling, additive fingerprinting (GC-MS), morphological distribution, or isotopic analysis."
        ),
        "decision_tree_relevance": (
            "Mass-based methods (Py-GC-MS, TED-GC-MS) are often preferred over particle-counting for bulk source attribution. "
            "Navigate: Monitoring → matrix → Analytical Identification → Py-GC-MS or TED-GC-MS."
        ),
    },
    {
        "term": "Proof of Concept (Method Development)",
        "category": "Study Design",
        "definition": (
            "A study demonstrating that a new method can detect or quantify MPs under idealized, controlled conditions "
            "before full matrix validation. Typically uses pristine reference particles in a clean or simplified matrix."
        ),
        "decision_tree_relevance": (
            "Relevant to Reference Materials & Controls and Interlaboratory / Validation branches. "
            "Proof-of-concept results should be followed by matrix-matched validation before adoption."
        ),
    },

    # ── Environmental Matrices ──────────────────────────────────────────────
    {
        "term": "Drinking Water",
        "category": "Environmental Matrix",
        "definition": (
            "Treated or untreated water intended for human consumption: tap water, bottled water, and groundwater supplies. "
            "The most-regulated matrix: California SB 1422 (2018) mandated the world's first MP monitoring program for drinking water. "
            "Typically analyzed after large-volume filtration (e.g., 50–1,000 L through stainless steel filters)."
        ),
        "decision_tree_relevance": (
            "Most Tier 1 and 2 references exist for this matrix. "
            "Navigate: Monitoring → Drinking Water for the most complete method coverage."
        ),
    },
    {
        "term": "Surface Water / Wastewater",
        "category": "Environmental Matrix",
        "definition": (
            "Rivers, lakes, estuaries, coastal marine waters, and treated/untreated wastewater effluents. "
            "The most historically studied environmental matrix for MPs globally. "
            "Collection methods include manta trawls, pump sampling, and continuous flow centrifugation."
        ),
        "decision_tree_relevance": (
            "No Tier 1 regulatory SOP exists; ASTM D8332-20 is recommended. "
            "Gap notes in the decision tree identify Tier 1/2 coverage gaps for sampling and extraction steps."
        ),
    },
    {
        "term": "Sediment",
        "category": "Environmental Matrix",
        "definition": (
            "Unconsolidated material on freshwater, marine, or estuarine bed surfaces, or deposited on land. "
            "MPs accumulate in sediments due to density-driven settling and are considered a major environmental sink. "
            "Bulk density and organic content vary widely and affect extraction efficiency."
        ),
        "decision_tree_relevance": (
            "Density separation is the primary extraction technique; NaI or ZnCl₂ is required for denser polymers (PET, PVC). "
            "Carbonate and organic matter digestion is commonly needed before density separation."
        ),
    },
    {
        "term": "Biota / Tissue",
        "category": "Environmental Matrix",
        "definition": (
            "Biological organisms or dissected tissues sampled to determine internal MP burdens. "
            "Whole-organism analysis is used for invertebrates; gastrointestinal tract, gills, or muscle dissection for vertebrates. "
            "Bivalves (mussels, oysters) are widely used as biomonitors due to filter feeding."
        ),
        "decision_tree_relevance": (
            "Requires chemical or enzymatic digestion of organic matter before analysis. "
            "KOH digestion is common; enzymatic digestion (proteinase K) is gentler for sensitive polymers."
        ),
    },
    {
        "term": "Air / Atmospheric Deposition",
        "category": "Environmental Matrix",
        "definition": (
            "MPs transported through the atmosphere, collected by bulk deposition collectors, passive samplers, "
            "or active air pumps. Includes atmospheric fallout (deposition flux) and inhalable airborne particles. "
            "Contamination control is extremely challenging (ambient fiber contamination)."
        ),
        "decision_tree_relevance": (
            "CRITICAL GAP: No Tier 1 or 2 method exists for any air workflow step. "
            "Ashta et al. (2026, Tier 3) is currently the best available method (~90% recovery)."
        ),
    },
    {
        "term": "Food / Dietary",
        "category": "Environmental Matrix",
        "definition": (
            "MPs detected in food items intended for human consumption: seafood, salt, honey, beer, bottled beverages, "
            "and other commodities. Dietary intake is a major human exposure pathway. "
            "Matrix complexity (fats, proteins, starches) requires tailored digestion protocols."
        ),
        "decision_tree_relevance": (
            "No Tier 1 or 2 method exists. EFSA (2016) identified major standardization gaps. "
            "Navigate: Monitoring → Food / Dietary to see available Tier 3–4 references."
        ),
    },
    {
        "term": "Human Tissue / Biomonitoring",
        "category": "Environmental Matrix",
        "definition": (
            "Detection and quantification of MPs in human biological samples: blood, lung tissue, placenta, "
            "stool, urine, and breast milk. Human biomonitoring bridges environmental exposure assessment "
            "and internal dose for health risk assessment. MP detection in human blood (Leslie et al. 2022; "
            "Rauert et al. 2025) has driven significant recent interest."
        ),
        "decision_tree_relevance": (
            "No Tier 1 or 2 method exists. Py-GC-MS is the leading technique for blood and tissue. "
            "Navigate: Monitoring → Human Tissue / Biomonitoring for the most current references."
        ),
    },
    {
        "term": "Soil / Terrestrial",
        "category": "Environmental Matrix",
        "definition": (
            "Agricultural, urban, and natural soils. MP inputs include sewage sludge (biosolids) application, "
            "atmospheric deposition, irrigation with reclaimed water, and plastic mulch degradation. "
            "Organic content, clay fraction, and mineral density complicate extraction."
        ),
        "decision_tree_relevance": (
            "No Tier 1 or 2 standard. High-density salt solutions (ZnCl₂ ~1.6–1.8 g/cm³, NaI) are required "
            "to float denser polymers. Peer-reviewed protocols (Li 2019; Möller 2022; Ling 2026) are best available."
        ),
    },

    # ── Monitoring Workflow ─────────────────────────────────────────────────
    {
        "term": "Sampling / Field Methods",
        "category": "Monitoring Workflow",
        "definition": (
            "Procedures for physically collecting representative environmental samples in the field: "
            "equipment selection (manta trawls, pump systems, passive samplers, grab samplers), "
            "sampling volume/area, replicate strategy, field blank collection, and chain-of-custody protocols. "
            "Sampling bias propagates irreversibly through all downstream analyses."
        ),
        "decision_tree_relevance": (
            "Navigate: Monitoring → matrix → Sampling / Field Methods. "
            "No matrix has universal Tier 1 sampling guidance except drinking water."
        ),
    },
    {
        "term": "Sample Processing / Extraction",
        "category": "Monitoring Workflow",
        "definition": (
            "Laboratory procedures to isolate MPs from the sample matrix before analysis: "
            "chemical or enzymatic digestion of organic matter, density separation, filtration, and sub-sampling. "
            "Also called 'sample preparation.' Matrix-specific: drinking water uses direct filtration; "
            "sediment and biota require digestion followed by density separation."
        ),
        "decision_tree_relevance": (
            "Navigate: Monitoring → matrix → Sample Processing / Extraction. "
            "Extraction efficiency (% recovery of spiked particles) must be measured and reported."
        ),
    },
    {
        "term": "Density Separation",
        "category": "Monitoring Workflow",
        "definition": (
            "Core extraction technique for solid matrices: polymers (density 0.9–1.5 g/cm³ for most common types) "
            "are floated in a concentrated salt solution while mineral particles and organic matter sink. "
            "Common media: NaCl (~1.2 g/cm³, low cost but misses PET/PVC/PC), "
            "ZnCl₂ (~1.5–1.8 g/cm³), NaI (~1.6–1.8 g/cm³), CaCl₂."
        ),
        "decision_tree_relevance": (
            "NaCl-based density separation systematically under-recovers denser polymers (PET ρ≈1.38, PVC ρ≈1.4). "
            "For comprehensive extraction, NaI or ZnCl₂ is recommended. "
            "Recovery of each target polymer type should be validated with spike experiments."
        ),
    },
    {
        "term": "Digestion (Chemical / Enzymatic)",
        "category": "Monitoring Workflow",
        "definition": (
            "Treatment to destroy biological organic matter without degrading plastic polymers. "
            "Common agents: KOH (potassium hydroxide — gentle, widely used for biota), "
            "H₂O₂ (hydrogen peroxide — can oxidize some polymers), "
            "HNO₃ (nitric acid — aggressive, may degrade polymers), "
            "proteinase K or other proteases (enzymatic — very gentle but slow). "
            "Digestion efficiency and polymer compatibility must both be validated."
        ),
        "decision_tree_relevance": (
            "Required for biota, food, and human tissue matrices. "
            "Navigate: Monitoring → Biota or Human Tissue → Sample Processing / Extraction for digestion guidance."
        ),
    },
    {
        "term": "Sub-sampling",
        "category": "Monitoring Workflow",
        "definition": (
            "Analyzing a known fraction of a processed sample when the total particle load exceeds instrument throughput. "
            "Statistical sub-sampling (e.g., Gyssel device, random grid selection) introduces additional uncertainty "
            "that must be quantified and propagated to the final count estimate."
        ),
        "decision_tree_relevance": (
            "Addressed in Data Analysis & Statistics branch. "
            "Sub-sampling uncertainty is a major source of imprecision in high-concentration matrices "
            "(stormwater, estuarine sediments)."
        ),
    },
    {
        "term": "Blanks & Contamination Control",
        "category": "Monitoring Workflow",
        "definition": (
            "Procedural blanks (field blanks, lab blanks, filter blanks, equipment blanks) are processed identically "
            "to real samples but contain no sample material. They quantify background contamination introduced during "
            "collection, transport, and analysis. Contamination control protocols include cotton or non-synthetic labware, "
            "filtered air systems, wet covers, and enclosed processing workspaces."
        ),
        "decision_tree_relevance": (
            "Contamination control and blank-corrected reporting are mandatory in Tier 1–2 methods "
            "and should be standard in all published studies. "
            "Navigate: Blanks & Contamination Control branch for specific protocols."
        ),
    },
    {
        "term": "Interlaboratory Study / Ring Trial",
        "category": "Monitoring Workflow",
        "definition": (
            "An exercise in which multiple laboratories analyze matched samples using their own protocols "
            "to assess inter-laboratory reproducibility and identify systematic method-specific biases. "
            "Also called proficiency testing or collaborative study. "
            "Results establish precision requirements for formal standards and identify outlier methods."
        ),
        "decision_tree_relevance": (
            "Navigate: Interlaboratory / Validation branch for ring trial references by matrix. "
            "Inter-laboratory variability in MP analysis is currently large (orders of magnitude between labs) — "
            "a major driver for standardization efforts."
        ),
    },
    {
        "term": "Reporting & Data Deposition",
        "category": "Monitoring Workflow",
        "definition": (
            "Structured documentation and sharing of monitoring results. Minimum reporting elements include: "
            "sample volume/area, size fraction analyzed (LLOD + upper size limit), matrix, polymer identification method, "
            "contamination control measures, blank results, extraction recovery, and uncertainty estimate. "
            "Open data repositories include LITTERBASE, SEAPLEX, national databases."
        ),
        "decision_tree_relevance": (
            "Navigate: Reporting & Data Deposition branch for harmonization guidance. "
            "Inadequate reporting is the primary reason MP datasets cannot be compared or combined in meta-analyses."
        ),
    },

    # ── Analytical Methods ──────────────────────────────────────────────────
    {
        "term": "µFTIR / FPA-FTIR (Micro-Fourier Transform Infrared)",
        "category": "Analytical Method",
        "definition": (
            "Identifies polymer type by measuring infrared absorption across individual particles, "
            "matched against a spectral library. Focal Plane Array (FPA) FTIR images an entire filter in one acquisition, "
            "enabling automated particle-by-particle mapping. "
            "Spatial resolution: typically 5–20 µm (transmission mode) or ~5 µm (ATR mode). "
            "Covered by ISO 24187 and California SWRCB SOP."
        ),
        "decision_tree_relevance": (
            "Most widely used particle-counting method in monitoring. "
            "Navigate: Analytical Identification → µFTIR / FPA-FTIR / LDIR."
        ),
    },
    {
        "term": "LDIR (Laser Direct Infrared Imaging)",
        "category": "Analytical Method",
        "definition": (
            "Automated particle analysis system (Agilent 8700 LDIR) using a tunable quantum cascade laser "
            "to acquire IR spectra across a filter at automated stage positions. "
            "Higher throughput than FPA-FTIR; spatial resolution ~20 µm. "
            "Requires specialized consumables and filter substrates."
        ),
        "decision_tree_relevance": (
            "Grouped with FTIR methods in most standards. "
            "Navigate: Analytical Identification → µFTIR / FPA-FTIR / LDIR."
        ),
    },
    {
        "term": "µRaman (Micro-Raman Spectroscopy)",
        "category": "Analytical Method",
        "definition": (
            "Identifies polymer molecular structure via laser-excited inelastic (Raman) light scattering. "
            "Spatial resolution ~1 µm — finer than FTIR, enabling detection of particles down to ~1 µm. "
            "Fluorescence from organic matter can interfere (mitigated by photobleaching or shifted excitation). "
            "Generally slower throughput than FPA-FTIR for whole-filter analysis."
        ),
        "decision_tree_relevance": (
            "Preferred for particles <20 µm and for matrices containing fluorescent organic matter. "
            "Navigate: Analytical Identification → µRaman."
        ),
    },
    {
        "term": "Py-GC-MS (Pyrolysis Gas Chromatography–Mass Spectrometry)",
        "category": "Analytical Method",
        "definition": (
            "Thermally decomposes (pyrolyzes) a bulk sample (~0.5 mg) and identifies polymer type by "
            "the characteristic volatile breakdown products detected by GC-MS. "
            "Provides mass-based quantification (µg/g or µg/L), not particle count, size, or morphology. "
            "Sample size is a major limitation — risks non-representative sub-sampling in heterogeneous matrices."
        ),
        "decision_tree_relevance": (
            "Best for human tissue, blood, and complex matrices where particle isolation is impractical. "
            "Also used for source attribution. Navigate: Analytical Identification → Py-GC-MS."
        ),
    },
    {
        "term": "TED-GC-MS (Thermal Extraction Desorption GC-MS)",
        "category": "Analytical Method",
        "definition": (
            "Similar to Py-GC-MS but uses larger sample masses (up to 100 mg) and a two-step process "
            "(thermal desorption of additives + flash pyrolysis of polymers), enabling simultaneous quantification "
            "of plastics and associated chemical additives. Better representativeness for heterogeneous samples."
        ),
        "decision_tree_relevance": (
            "Preferred over Py-GC-MS for sediment, sewage sludge, and other heterogeneous environmental matrices. "
            "Instrument less widely available. Navigate: Analytical Identification → TED-GC-MS."
        ),
    },
    {
        "term": "Nile Red / Fluorescence Screening",
        "category": "Analytical Method",
        "definition": (
            "Nile Red is a lipophilic fluorescent dye that preferentially stains plastic particle surfaces, "
            "enabling rapid enumeration under fluorescence microscopy. A SCREENING method only — "
            "polymer identity cannot be confirmed by fluorescence alone. "
            "Staining efficiency varies by polymer type, surface fouling, and weathering state."
        ),
        "decision_tree_relevance": (
            "Fast, low-cost first-pass screening for hotspot detection. "
            "Spectroscopic confirmation required before reporting polymer-specific data. "
            "Navigate: Analytical Identification → Nile Red / Fluorescence Screening."
        ),
    },
    {
        "term": "Visual / Stereomicroscopy",
        "category": "Analytical Method",
        "definition": (
            "Optical identification of suspected MPs under a dissecting or stereomicroscope, "
            "classified by color, morphology, and transparency. Lowest cost but highest false-positive rate "
            "(organic matter, diatoms, and natural fibers are commonly misidentified as MPs). "
            "WHO (2019) and GESAMP (2016) consider visual-only identification insufficient."
        ),
        "decision_tree_relevance": (
            "Acceptable for initial sorting before spectroscopic analysis, but not a standalone identification method. "
            "Navigate: Analytical Identification → Visual / Stereomicroscopy for relevant guidance."
        ),
    },

    # ── Quality Assurance / Quality Control ─────────────────────────────────
    {
        "term": "QA/QC (Quality Assurance / Quality Control)",
        "category": "QA/QC",
        "definition": (
            "Quality Assurance (QA): the systematic organizational program ensuring study design and execution meet "
            "defined quality standards — SOPs, training, equipment calibration, data review. "
            "Quality Control (QC): the specific technical measures during analysis — blanks, spikes, duplicates, "
            "reference material checks — used to monitor and verify data quality in real time."
        ),
        "decision_tree_relevance": (
            "Central to all branches. No MP study should be published without documented QA/QC. "
            "Minimum requirements: blank reporting, spike recovery, method detection limit, and uncertainty estimate. "
            "Navigate: Blanks & Contamination Control and Reference Materials / Controls branches."
        ),
    },
    {
        "term": "Controls (Positive / Negative / Matrix Spike)",
        "category": "QA/QC",
        "definition": (
            "Positive controls contain known amounts of target material (verify the method can detect MPs). "
            "Negative controls / blanks contain no target material (quantify background contamination). "
            "Matrix spikes add known particles to real samples before processing "
            "(measure combined extraction + detection efficiency in the actual sample matrix)."
        ),
        "decision_tree_relevance": (
            "Essential for all analytical methods. Navigate: Reference Materials / Positive Controls branch "
            "for guidance on what types of controls are appropriate for each workflow step."
        ),
    },
    {
        "term": "Spike Recovery / Recovery Rate",
        "category": "QA/QC",
        "definition": (
            "Known quantities of reference particles added to samples before or during processing "
            "to measure the efficiency of the entire analytical workflow. "
            "Recovery (%) = (particles detected / particles added) × 100. "
            "Typical acceptance criteria: ≥70% recovery (ISO, SWRCB SOPs). "
            "Low recovery indicates particle loss; high variability indicates inconsistent processing."
        ),
        "decision_tree_relevance": (
            "Required for method validation and routine QC. Results must be reported with monitoring data. "
            "Recovery varies by particle size, shape, polymer type, and matrix — "
            "validate with particles representative of those expected in samples."
        ),
    },
    {
        "term": "Certified Reference Material (CRM)",
        "category": "QA/QC",
        "definition": (
            "A reference material with certified values established by a metrologically traceable procedure "
            "and issued by a national metrology institute (NIST, JRC/IRMM, BAM, etc.). "
            "Provides an external benchmark for instrument calibration and inter-laboratory comparability. "
            "Only one CRM currently exists for MPs: EURM-060 (PET particles in water, European Commission JRC). "
            "NIST and JRC are developing CRMs for sediment and biological matrices."
        ),
        "decision_tree_relevance": (
            "CRITICAL GAP: the near-absence of CRMs is a major barrier to harmonization. "
            "Navigate: Reference Materials / Positive Controls for available CRM and near-CRM materials."
        ),
    },
    {
        "term": "Source Material / Test Particles",
        "category": "QA/QC",
        "definition": (
            "The plastic particles used as the test substance in toxicology or method development studies. "
            "Must be characterized for: size distribution (number- or volume-weighted), "
            "polymer identity, particle morphology, surface chemistry, purity (contaminants, additives), "
            "and preparation method. Characterization data must be reported alongside study results."
        ),
        "decision_tree_relevance": (
            "Navigate: Toxicology → Reference / Test Particles for guidance on particle selection and characterization. "
            "Use of poorly characterized source material is a common quality deficiency identified by ToMEx scoring."
        ),
    },
    {
        "term": "Spiked Standards",
        "category": "QA/QC",
        "definition": (
            "Reference particles of known size, polymer type, and concentration added to a sample or blank "
            "to evaluate extraction efficiency (matrix spike) or instrument response (instrument spike). "
            "Distinct from certified reference materials: spiked standards are laboratory-prepared "
            "and do not carry metrological traceability, but are widely used due to the lack of CRMs."
        ),
        "decision_tree_relevance": (
            "Used throughout sampling (field spikes), extraction (matrix spikes), and analysis (instrument calibration). "
            "Spike particle type should match expected environmental particles where possible."
        ),
    },

    # ── Toxicology ──────────────────────────────────────────────────────────
    {
        "term": "In Vitro",
        "category": "Toxicology",
        "definition": (
            "Experiments conducted in cell cultures, tissue cultures, or cell-free systems (Latin: 'in glass'). "
            "Highly controlled and reproducible; enables mechanistic investigation of cellular responses. "
            "May not replicate in vivo physiology (missing systemic factors, metabolism, immune context). "
            "Common MP in vitro models: Caco-2 (gut), A549 (lung), H295R (steroidogenesis), "
            "macrophage lines (RAW264.7), barrier co-culture models."
        ),
        "decision_tree_relevance": (
            "Navigate: Toxicology → Effects Testing → In Vitro (cell-based). "
            "Dosimetry (ISDD modeling) is required to determine the delivered dose at the cell layer."
        ),
    },
    {
        "term": "In Vivo",
        "category": "Toxicology",
        "definition": (
            "Experiments conducted in living organisms (Latin: 'in life'). "
            "More physiologically relevant than in vitro; captures systemic distribution, metabolism, "
            "elimination (ADME), and organism-level effects (growth, reproduction, behavior). "
            "Higher biological complexity, cost, and ethical considerations than in vitro."
        ),
        "decision_tree_relevance": (
            "Navigate: Toxicology → Effects Testing → Mammalian In Vivo (rodent studies) "
            "or Ecotox — Aquatic/Terrestrial for environmentally relevant species."
        ),
    },
    {
        "term": "Ex Vivo",
        "category": "Toxicology",
        "definition": (
            "Experiments using tissues or organs removed from a living organism but maintained under "
            "conditions that preserve physiological function (perfusion, oxygenated media). "
            "Intermediate between in vitro and in vivo — retains tissue architecture without whole-animal confounders."
        ),
        "decision_tree_relevance": (
            "Less common in MP toxicology but relevant for gut permeability studies (everted gut sac) "
            "and respiratory models. Classify under In Vitro in most guidance frameworks."
        ),
    },
    {
        "term": "Dosimetry",
        "category": "Toxicology",
        "definition": (
            "The science of quantifying the biologically effective dose of MPs delivered to a target tissue or cell. "
            "Distinguishes: nominal concentration (added to test medium) → administered dose → "
            "delivered dose (what reaches the target cell or tissue). "
            "Bridging nominal and delivered dose is especially critical in in vitro studies "
            "where particle sedimentation and diffusion differ from in vivo conditions."
        ),
        "decision_tree_relevance": (
            "Navigate: Toxicology → Dosimetry (in vitro). "
            "Without dosimetry correction, studies using different particle sizes and densities "
            "cannot be meaningfully compared — a key source of inconsistency in the MP tox literature."
        ),
    },
    {
        "term": "Particokinetics / ISDD Model",
        "category": "Toxicology",
        "definition": (
            "Particokinetics describes the time-dependent transport of particles in a cell culture medium: "
            "sedimentation, diffusion, and agglomeration. The In vitro Sedimentation, Diffusion, "
            "and Dosimetry (ISDD) model (Hinderliter et al. 2010) calculates the fraction of particles "
            "that reaches the cell monolayer over time, based on particle size, density, "
            "medium viscosity, and well geometry."
        ),
        "decision_tree_relevance": (
            "Required for rigorous in vitro dosimetry (keyword: 'particokinetics; ISDD; delivered dose'). "
            "Navigate: Toxicology → Dosimetry (in vitro)."
        ),
    },
    {
        "term": "PBK / PBPK Modeling",
        "category": "Toxicology",
        "definition": (
            "Physiologically-Based (Pharmaco)Kinetic modeling uses mathematical representations of "
            "physiological processes (organ blood flow, tissue volumes, partition coefficients) "
            "to predict MP distribution among body compartments over time. "
            "Used to extrapolate from administered dose to internal tissue concentration, "
            "and to scale across species or exposure routes."
        ),
        "decision_tree_relevance": (
            "Navigate: Risk Assessment → Exposure Assessment. "
            "PBK is also referenced in the Toxicology → Dosimetry branch (keyword: 'PBK')."
        ),
    },
    {
        "term": "Ecotoxicology (Ecotox)",
        "category": "Toxicology",
        "definition": (
            "The study of toxic effects of environmental contaminants on non-human organisms in their natural "
            "or simulated habitat. Encompasses aquatic (fish, Daphnia, algae, bivalves, benthic invertebrates), "
            "terrestrial (earthworms, plants, soil invertebrates), and avian toxicology. "
            "OECD test guidelines provide standardized protocols for most standard test species and endpoints."
        ),
        "decision_tree_relevance": (
            "Navigate: Toxicology → Effects Testing → Ecotox — Aquatic or Terrestrial. "
            "No OECD test guidelines are currently MP-specific; standard TGs are applicable but require adaptation."
        ),
    },
    {
        "term": "Study Endpoints",
        "category": "Toxicology",
        "definition": (
            "Specific biological parameters measured in a toxicology study, defined a priori. "
            "Common endpoints: mortality (LC50), reproduction (EC50 for reproductive output), "
            "growth inhibition, oxidative stress (ROS, antioxidant enzymes), genotoxicity (comet assay), "
            "endocrine disruption (steroidogenesis, vitellogenin), behavior, and histopathology. "
            "Choice of endpoint determines which OECD test guideline applies."
        ),
        "decision_tree_relevance": (
            "Endpoint selection is part of problem formulation and study design. "
            "Navigate: Toxicology → Effects Testing for endpoint-specific method guidance."
        ),
    },
    {
        "term": "ToMEx (Toxicity of Microplastics Explorer)",
        "category": "Toxicology",
        "definition": (
            "An open-access database (toxmex.org) that compiles and quality-scores published MP toxicity studies. "
            "Includes effect concentrations (LC50, EC50, NOEC), species, endpoints, particle characteristics, "
            "and study quality scores based on defined criteria. "
            "Developed by SCCWRP and collaborators for use in California MP risk assessment."
        ),
        "decision_tree_relevance": (
            "Primary resource for hazard identification in risk assessment. "
            "Navigate: Risk Assessment → Hazard Identification (keyword: 'ToMEx')."
        ),
    },
    {
        "term": "Study Quality / Quality Scoring",
        "category": "Toxicology",
        "definition": (
            "Systematic evaluation of toxicology study design, conduct, and reporting quality using "
            "defined criteria or checklists (e.g., ToMEx quality criteria, CREDO or PEPPER scoring). "
            "Key quality indicators: particle characterization completeness, dosimetry documentation, "
            "appropriate controls, statistical power, and reporting transparency."
        ),
        "decision_tree_relevance": (
            "Navigate: Toxicology → Study Quality / Scoring (keywords: 'quality; QA; scoring; criteria'). "
            "Low-quality tox studies cannot be reliably used in SSD-based risk assessment."
        ),
    },

    # ── Risk Assessment ─────────────────────────────────────────────────────
    {
        "term": "Hazard Identification",
        "category": "Risk Assessment",
        "definition": (
            "First phase of risk assessment: systematically evaluating whether MPs can cause harm, "
            "to which biological receptors, via which mechanisms, and under what conditions. "
            "Draws on toxicological databases (ToMEx), systematic reviews, and evidence synthesis "
            "(weight-of-evidence, mechanistic plausibility)."
        ),
        "decision_tree_relevance": (
            "Navigate: Risk Assessment → Hazard Identification."
        ),
    },
    {
        "term": "Exposure Assessment",
        "category": "Risk Assessment",
        "definition": (
            "Quantification of the amount, frequency, and duration of contact between an organism (or population) "
            "and MPs. For humans: dietary intake (ingestion), inhalation, and dermal contact are major routes. "
            "Uses monitoring occurrence data, consumption surveys, and PBK/PBPK models to estimate internal dose."
        ),
        "decision_tree_relevance": (
            "Navigate: Risk Assessment → Exposure Assessment (keywords: 'exposure; PBK; monitoring; scenario'). "
            "Requires harmonized monitoring data — another driver for method standardization."
        ),
    },
    {
        "term": "Risk Characterization",
        "category": "Risk Assessment",
        "definition": (
            "The integrative phase of risk assessment that combines hazard and exposure data to estimate "
            "the probability and magnitude of adverse effects. "
            "Products: risk quotients (RQ = exposure / threshold), SSD-derived hazard concentrations (HC5), "
            "probability distributions of risk (stochastic RA), and uncertainty analyses."
        ),
        "decision_tree_relevance": (
            "Navigate: Risk Assessment → Risk Characterization (keywords: 'risk quotient; threshold; SSD; stochastic')."
        ),
    },
    {
        "term": "Risk Quotient (RQ)",
        "category": "Risk Assessment",
        "definition": (
            "A deterministic risk metric: RQ = measured environmental concentration (MEC) / no-effect threshold (PNEC or HC5). "
            "RQ > 1 indicates potential risk. Can be calculated for individual exposure scenarios or aggregated. "
            "Simple but does not capture uncertainty or variability distributions."
        ),
        "decision_tree_relevance": (
            "Key output of Risk Characterization step. Keyword 'risk quotient' in RA branch."
        ),
    },
    {
        "term": "Species Sensitivity Distribution (SSD)",
        "category": "Risk Assessment",
        "definition": (
            "A statistical model fitted to effect concentrations from multiple species (LC50, EC50, or chronic NOEC) "
            "to derive a Hazardous Concentration (HC5) protective of 95% of species. "
            "Used to set environmental quality criteria and Predicted No-Effect Concentrations (PNECs). "
            "Multiple SSD analyses of MP toxicity data have been published (Burns & Boxall; Adam et al.; Mehinto et al.)."
        ),
        "decision_tree_relevance": (
            "Key method for deriving regulatory thresholds. Navigate: Risk Assessment → Risk Characterization. "
            "SSD quality depends critically on the quality and consistency of underlying tox studies."
        ),
    },
    {
        "term": "Technology Readiness Level (TRL)",
        "category": "Risk Assessment",
        "definition": (
            "A 1–9 scale assessing the maturity of a risk assessment method or tool: "
            "TRL 1–3 (basic research), TRL 4–6 (laboratory validation), TRL 7–9 (operational validation). "
            "Originally developed by NASA; adopted by ECHA and regulatory science to evaluate whether a method "
            "is ready for regulatory application."
        ),
        "decision_tree_relevance": (
            "Referenced in Risk Characterization branch (keyword: 'TRL'). "
            "Mehinto et al. used the TRL framework to evaluate MP risk assessment methods for California SWRCB."
        ),
    },

    # ── Authority & Document Types ──────────────────────────────────────────
    {
        "term": "Tier 1 — Normative / Binding",
        "category": "Authority Tier System",
        "definition": (
            "Documents with legal or regulatory force: statutes (legislation), enforceable regulations, "
            "government-issued SOPs with regulatory backing (e.g., California SWRCB methods), "
            "or consensus standards formally adopted by regulators (e.g., ISO standards cited in law). "
            "Compliance is required in the relevant jurisdiction."
        ),
        "decision_tree_relevance": (
            "Highest authority in the decision tree. When a Tier 1 document exists, it should be the primary reference. "
            "Tier 1 references are expanded by default in results."
        ),
    },
    {
        "term": "Tier 2 — Authoritative / Institutional",
        "category": "Authority Tier System",
        "definition": (
            "Documents from recognized international bodies (WHO, GESAMP, EFSA, NOAA) or consensus standards "
            "not yet formally adopted by regulators (ISO, ASTM), and major agency technical reports. "
            "Not legally binding but carry substantial scientific and policy authority."
        ),
        "decision_tree_relevance": (
            "Primary reference when no Tier 1 document exists for a matrix/step combination. "
            "Tier 2 references are expanded by default in results."
        ),
    },
    {
        "term": "Tier 3 — Peer-Reviewed / Validated",
        "category": "Authority Tier System",
        "definition": (
            "Published methods with quantitative validation data (recovery experiments, method detection limits, "
            "interlaboratory comparisons) that have passed peer review. The best available option when "
            "no Tier 1 or 2 document exists — which is the case for most matrices outside drinking water."
        ),
        "decision_tree_relevance": (
            "Most commonly cited references for matrices with standardization gaps (Air, Food, Soil, Human Tissue)."
        ),
    },
    {
        "term": "Tier 4 — Supporting / Contextual",
        "category": "Authority Tier System",
        "definition": (
            "Reviews, frameworks, commentary, and emerging methods that inform study design but do not provide "
            "primary methodological guidance. Useful for background, context, and identifying areas of scientific debate."
        ),
        "decision_tree_relevance": (
            "Lowest authority tier. Not recommended as standalone primary references for regulatory or standardization purposes."
        ),
    },
    {
        "term": "Consensus Standard",
        "category": "Authority Tier System",
        "definition": (
            "A technical standard developed through a formal multi-stakeholder process by a recognized standards body "
            "(ISO, ASTM, CEN, DIN) with public comment periods and ballot approval. "
            "Examples: ISO 24187 (FTIR for MPs in water), ASTM D8332-20 (surface water sampling). "
            "Key ISO committees: TC 147/SC 2 (water quality methods) and TC 61/SC 14 (environmental aspects of plastics)."
        ),
        "decision_tree_relevance": (
            "Typically Tier 1 or 2 in the crosswalk. The most important standards for MPs are still under development."
        ),
    },
    {
        "term": "Government SOP",
        "category": "Authority Tier System",
        "definition": (
            "A Standard Operating Procedure issued by a regulatory or government agency with specific, "
            "step-by-step analytical instructions that analysts can follow directly. "
            "Example: California SWRCB Microplastics in Drinking Water SOP (Tier 1). "
            "SOPs may reference or adapt consensus standards but often include matrix-specific modifications."
        ),
        "decision_tree_relevance": (
            "Typically Tier 1. Navigate to Drinking Water matrix for the most complete SOP coverage."
        ),
    },

    # ── Key Organizations ───────────────────────────────────────────────────
    {
        "term": "ISO (International Organization for Standardization)",
        "category": "Key Organization",
        "definition": (
            "The world's largest independent standards body. Relevant committees for MPs: "
            "ISO TC 147/SC 2 (physical, chemical, and biochemical water quality methods — including drinking water MPs), "
            "ISO TC 61/SC 14 (environmental aspects of plastics — definitions, fate, and effects). "
            "Key published standards: ISO/TR 21960, ISO 24187, ISO 11097."
        ),
        "decision_tree_relevance": (
            "ISO standards are Tier 1–2 in the crosswalk. "
            "Filter Document Type = 'Consensus Standard' in the Crosswalk tab to see ISO entries."
        ),
    },
    {
        "term": "ASTM International",
        "category": "Key Organization",
        "definition": (
            "American standards development organization. "
            "MP-relevant standards under Committee D34 (Waste Management): "
            "D8332-20 (surface water sampling), D8333-20 (sample preparation), "
            "and several in development for other matrices."
        ),
        "decision_tree_relevance": (
            "Tier 2 references widely used in North American monitoring programs."
        ),
    },
    {
        "term": "NOAA (National Oceanic and Atmospheric Administration)",
        "category": "Key Organization",
        "definition": (
            "U.S. federal agency; NOAA's Marine Debris Program co-developed widely used protocols "
            "for monitoring MPs in ocean and Great Lakes environments. "
            "NOAA's ≤5 mm size definition (no lower bound specified) is the most widely adopted globally, "
            "differing from ISO's 1 µm lower bound."
        ),
        "decision_tree_relevance": (
            "NOAA laboratory methods are Tier 2 references in surface water and sediment branches. "
            "NOAA size definition vs. ISO 1 µm lower bound is a key definitional conflict."
        ),
    },
    {
        "term": "WHO (World Health Organization)",
        "category": "Key Organization",
        "definition": (
            "U.N. public health agency. WHO (2019) published a landmark Tier 2 assessment of MP risks "
            "in drinking water, concluding that current evidence does not indicate a health risk "
            "at present levels but calling for further research and standardized methods."
        ),
        "decision_tree_relevance": (
            "WHO (2019) is a key Tier 2 reference in the Drinking Water matrix branch."
        ),
    },
    {
        "term": "GESAMP (Joint Group of Experts on Scientific Aspects of Marine Environmental Protection)",
        "category": "Key Organization",
        "definition": (
            "A joint U.N. expert body. Published 'Sources, Fate and Effects of Microplastics in the Marine Environment' "
            "(2016), among the most-cited Tier 2 guidance documents on marine MP monitoring methodology."
        ),
        "decision_tree_relevance": (
            "Tier 2 reference in marine/surface water monitoring branches."
        ),
    },
    {
        "term": "EFSA (European Food Safety Authority)",
        "category": "Key Organization",
        "definition": (
            "EU agency for food safety risk assessment. Published key opinions on MPs in seafood (2016) "
            "and a comprehensive re-evaluation incorporating new occurrence and toxicity data (2023)."
        ),
        "decision_tree_relevance": (
            "Key Tier 2 reference in the Food / Dietary matrix branch. Identified major standardization gaps."
        ),
    },
    {
        "term": "ECHA (European Chemicals Agency)",
        "category": "Key Organization",
        "definition": (
            "EU agency responsible for chemical regulation under REACH. Drafted the EU restriction on "
            "intentionally added microplastics (REACH Annex XVII, Entry 78), defining MPs as "
            "synthetic polymer particles <5 mm. The restriction assessment contains an extensive "
            "methodology review and MP definition analysis."
        ),
        "decision_tree_relevance": (
            "ECHA restriction documents are Tier 1 references for definitions and intentional-additive scope. "
            "ECHA's definition explicitly excludes natural polymers and semi-synthetics."
        ),
    },
    {
        "term": "SCCWRP (Southern California Coastal Water Research Project)",
        "category": "Key Organization",
        "definition": (
            "California-based public research agency that co-developed the California drinking water "
            "MP monitoring methodology with SWRCB. Published extensive Tier 3 protocols for "
            "surface water, sediment, and biota monitoring. Hosts the ToMEx database."
        ),
        "decision_tree_relevance": (
            "Tier 2–3 references throughout multiple monitoring branches."
        ),
    },
    {
        "term": "SWRCB / State Water Board (California)",
        "category": "Key Organization",
        "definition": (
            "California's primary water quality regulatory agency. Issued the world's first enforceable "
            "regulation requiring MP monitoring in drinking water (SB 1422, 2018). "
            "The SWRCB SOP for drinking water analysis is a Tier 1 regulatory reference."
        ),
        "decision_tree_relevance": (
            "Tier 1 reference in the Drinking Water matrix branch. "
            "The California framework is the leading model for drinking water MP regulation globally."
        ),
    },

    # ── Plastic Material Types ───────────────────────────────────────────────
    {
        "term": "Semi-Synthetic Plastics / Bioplastics",
        "category": "Plastic Material Types",
        "definition": (
            "Semi-synthetic plastics are synthesized from polymers derived from non-fossil-fuel-based sources, "
            "including biological materials such as corn starch or bacteria. "
            "Rayon (viscose), for example, is a semi-synthetic fiber produced from plant cellulose. "
            "The term 'bioplastic' is commonly used interchangeably with semi-synthetic and also — confusingly — "
            "with biodegradable plastic, although not all bioplastics are biodegradable or compostable. "
            "Most conventional plastics are synthetic (derived from fossil fuels)."
        ),
        "decision_tree_relevance": (
            "Scope decisions in monitoring and toxicology depend on whether semi-synthetics are included. "
            "ECHA's REACH restriction and ISO 11097 generally exclude semi-synthetic polymers. "
            "Navigate to Definitions & Terminology to see how different standards handle this boundary."
        ),
    },
    {
        "term": "Biodegradable Plastics",
        "category": "Plastic Material Types",
        "definition": (
            "Plastics that break down into natural components (CO₂, water, biomass) in the environment "
            "through microbial degradation. Currently there is no universal regulatory standard defining "
            "what constitutes biodegradability — timescales, conditions, and required end products vary widely "
            "across jurisdictions and standards bodies. Many materials marketed as biodegradable "
            "do not degrade meaningfully under real environmental conditions."
        ),
        "decision_tree_relevance": (
            "Biodegradable polymers may or may not be in scope for MP monitoring depending on the regulatory definition used. "
            "Their intermediate degradation products (micro-sized fragments) may behave like conventional MPs "
            "before complete mineralization. Navigate to Definitions & Terminology for regulatory scope guidance."
        ),
    },
    {
        "term": "Compostable Plastics",
        "category": "Plastic Material Types",
        "definition": (
            "Plastics certified to biodegrade under controlled composting conditions — typically requiring "
            "elevated temperatures (55–60 °C), humidity, and microbial activity found in industrial composting facilities. "
            "Compostable plastics may be either bioplastics or fossil-fuel-derived (e.g., PBAT). "
            "Most do not degrade in home compost bins or in open environmental conditions at the required rate. "
            "Not synonymous with biodegradable, recyclable, or bioplastic."
        ),
        "decision_tree_relevance": (
            "Compostable plastics in the environment may generate MP fragments if industrial composting conditions are absent. "
            "Their inclusion or exclusion from MP monitoring scope depends on the working definition adopted."
        ),
    },
    {
        "term": "Weathered Plastics (Laboratory Simulation)",
        "category": "Plastic Material Types",
        "definition": (
            "Plastics subjected to controlled laboratory weathering treatments to simulate environmental aging. "
            "Common weathering approaches: photooxidation via UV irradiation in the presence of oxygen (photo-oxidative weathering) "
            "and biofouling via microbial colonization. These processes alter surface chemistry (increased carbonyl and hydroxyl groups), "
            "crystallinity, and particle fragmentation propensity. "
            "No standardized weathering protocols currently exist (e.g., no consensus on UV dose, duration, temperature, "
            "or oxygen levels for photooxidative weathering)."
        ),
        "decision_tree_relevance": (
            "Navigate: Toxicology → Reference / Test Particles. "
            "Weathered particles are more environmentally relevant than pristine materials but are difficult to "
            "reproduce between laboratories without standardized protocols — a major research gap."
        ),
    },

    # ── Reference & Calibration Materials ───────────────────────────────────
    {
        "term": "Material Standards",
        "category": "Reference & Calibration Materials",
        "definition": (
            "Plastic materials used for validation purposes in optical, spectroscopic, and thermoanalytical "
            "methods during MP analysis. Material standards confirm that the analytical system is performing "
            "as expected and that the correct spectral or thermal signatures are being detected. "
            "Distinct from certified reference materials in that they may not carry full metrological traceability."
        ),
        "decision_tree_relevance": (
            "Navigate: Reference Materials / Positive Controls branch for guidance on appropriate standards for each method."
        ),
    },
    {
        "term": "Reference Standards",
        "category": "Reference & Calibration Materials",
        "definition": (
            "Plastic materials of scientific-grade quality that have been validated for polymer type. "
            "Available in various physical forms: powder, filament, sheet, pellets/nurdles (most common). "
            "Used to build spectral libraries, validate extraction recoveries (spike experiments), "
            "and calibrate instrument response. "
            "Distinguished from certified reference materials (CRMs) by the absence of full metrological traceability."
        ),
        "decision_tree_relevance": (
            "Widely used as spike materials for extraction recovery experiments. "
            "Navigate: Reference Materials / Positive Controls. "
            "Polymer type, size distribution, and morphology of reference standards should match expected environmental particles."
        ),
    },
    {
        "term": "Calibration Standards",
        "category": "Reference & Calibration Materials",
        "definition": (
            "Materials measured in precise masses (for thermoanalytical methods such as Py-GC/MS) or "
            "known particle quantities (for spectroscopic/counting methods) to establish instrument response curves. "
            "May be prepared in-house by the analyst (aliquoting reference standards) "
            "or purchased from a limited number of commercial vendors. "
            "Essential for quantitative analysis and inter-run comparability."
        ),
        "decision_tree_relevance": (
            "Required for quantitative Py-GC/MS and TED-GC/MS analysis. "
            "Also used in µFTIR and µRaman for size and spectral calibration. "
            "Navigate: Reference Materials / Positive Controls."
        ),
    },
    {
        "term": "Internal Standards",
        "category": "Reference & Calibration Materials",
        "definition": (
            "Materials added in known amounts to all samples and calibration standards before analysis "
            "to normalize for instrument detection variation across multiple analytical runs. "
            "Particularly important for mass-quantification methods (Py-GC/MS, TED-GC/MS). "
            "Ideal internal standards are unique — not found in the environment — "
            "and are commonly mass-labeled analogues (stable isotope-labeled, e.g., ¹³C or deuterium-labeled) "
            "of the target polymer pyrolyzates."
        ),
        "decision_tree_relevance": (
            "Best practice for Py-GC/MS and TED-GC/MS quantification. "
            "Without internal standards, inter-run variability can introduce significant quantification errors. "
            "Navigate: Analytical Identification → Py-GC-MS or TED-GC-MS."
        ),
    },
    {
        "term": "Certified Reference Material (CRM) / Standardized Reference Material",
        "category": "Reference & Calibration Materials",
        "definition": (
            "Metrologically characterized materials issued by a standards or metrology institute "
            "(e.g., JRC/IRMM, NIST, BAM) for method validation, quality control, and interlaboratory comparability. "
            "CRMs for MP-adjacent purposes exist (e.g., for nanoparticle bead sizing, phthalate concentrations in PVC), "
            "but very few environmental matrices containing known MP concentrations currently exist as true CRMs. "
            "The main available CRM for environmental MPs is EURM-060 (PET particles in water, European Commission JRC)."
        ),
        "decision_tree_relevance": (
            "CRITICAL GAP: Near-absence of CRMs is a major barrier to inter-laboratory comparability. "
            "Navigate: Reference Materials / Positive Controls for the most current CRM availability information."
        ),
    },

    # ── Analytical Method Classes ────────────────────────────────────────────
    {
        "term": "Vibrational Spectroscopy",
        "category": "Analytical Method",
        "definition": (
            "A class of analytical techniques that characterize molecular structures by measuring "
            "how chemical bonds absorb or scatter electromagnetic radiation. "
            "Particularly useful for polymer identification in MP analysis because each polymer type "
            "produces a characteristic spectral fingerprint. "
            "Often paired with microscopy ('micro-' or 'µ-' instruments) for particle-level analysis. "
            "Major types used in MP research: "
            "(1) ATR-FTIR — Attenuated Total Reflectance FTIR; contact technique for bulk/surface analysis; "
            "(2) µFTIR — mapping spectroscopy for particle-by-particle polymer ID; "
            "(3) µRaman — laser-excited inelastic scattering; finer spatial resolution (~1 µm); "
            "(4) LDIR — Laser Direct Infrared; automated high-throughput variant using a quantum cascade laser."
        ),
        "decision_tree_relevance": (
            "Vibrational spectroscopy methods are particle-counting approaches — they identify polymer type "
            "and measure particle size and morphology. "
            "Navigate: Analytical Identification → µFTIR/FPA-FTIR/LDIR or µRaman."
        ),
    },
    {
        "term": "ATR-FTIR (Attenuated Total Reflectance FTIR)",
        "category": "Analytical Method",
        "definition": (
            "A contact-based infrared technique in which the sample is pressed against an ATR crystal "
            "(commonly diamond or germanium). IR light undergoes total internal reflection within the crystal, "
            "creating an evanescent wave that penetrates ~0.5–2 µm into the sample surface. "
            "Used for bulk material identification (large particles, pellets, reference materials) "
            "and for confirming polymer identity of individual sorted particles. "
            "Not suitable for automated whole-filter mapping."
        ),
        "decision_tree_relevance": (
            "Used primarily for bulk polymer identification and reference material validation. "
            "For whole-filter automated analysis, µFTIR (mapping mode) or LDIR is preferred."
        ),
    },
    {
        "term": "Thermoanalytical Spectrometry (Py-GC/MS, TED-GC/MS, TD-GC/MS)",
        "category": "Analytical Method",
        "definition": (
            "A class of techniques combining thermal sample treatment with gas chromatography and mass spectrometry "
            "to analyze plastics and their additive constituents. Two temperature regimes: "
            "(1) Low-temperature thermal desorption (50–250 °C): volatilizes and extracts plasticizers, "
            "flame retardants, and other additives from melted particles without polymer destruction. "
            "(2) Pyrolysis (>450 °C): thermally decomposes polymer chains into characteristic volatile pyrolyzates "
            "used to fingerprint and quantify the parent polymer. "
            "Common instruments: TD-GC/MS (thermal desorption only), Py-GC/MS (pyrolysis only), "
            "TED-GC/MS (sequential thermal desorption then pyrolysis, enabling simultaneous polymer + additive analysis)."
        ),
        "decision_tree_relevance": (
            "Mass-based methods — provide polymer mass per sample (µg/g or µg/L), not particle count or size. "
            "Best for complex matrices (human tissue, blood, sediment) where particle isolation is impractical. "
            "Navigate: Analytical Identification → Py-GC-MS or TED-GC-MS."
        ),
    },
    {
        "term": "TD-GC/MS (Thermal Desorption Gas Chromatography–Mass Spectrometry)",
        "category": "Analytical Method",
        "definition": (
            "A thermoanalytical technique that heats a sample to relatively low temperatures (50–250 °C) "
            "to volatilize and desorb semi-volatile organic additives (plasticizers, flame retardants, stabilizers) "
            "without destroying the polymer backbone. The desorbed compounds are trapped and analyzed by GC/MS. "
            "Used as a standalone technique for additive profiling, or as the first stage of TED-GC/MS."
        ),
        "decision_tree_relevance": (
            "Useful for chemical additive characterization of plastic particles, "
            "complementing polymer identification by Py-GC/MS. "
            "Navigate: Analytical Identification → TED-GC-MS."
        ),
    },

    # ── QA/QC — Blanks ──────────────────────────────────────────────────────
    {
        "term": "Field Blanks",
        "category": "QA/QC",
        "definition": (
            "Blanks collected alongside environmental samples during field collection to quantify "
            "contamination introduced during the sampling process itself (not just the laboratory). "
            "Common approaches: exposing a volume of ultrapure or pre-filtered water in an open container "
            "during sampling; pouring water between containers; or leaving a collection disk (petri dish, filter) "
            "open to the ambient air adjacent to the sampling area, typically in a wetted condition. "
            "Field blank values are subtracted from sample results or used to assess contamination risk."
        ),
        "decision_tree_relevance": (
            "Required in all standardized monitoring protocols (SWRCB SOP, WHO 2019, GESAMP 2016). "
            "Navigate: Blanks & Contamination Control."
        ),
    },
    {
        "term": "Procedural Blanks (Laboratory Blanks)",
        "category": "QA/QC",
        "definition": (
            "Samples of a clean matrix (e.g., filtered or ultrapure water) processed through the complete "
            "laboratory preparation procedure alongside real samples. They quantify background MP contamination "
            "introduced during laboratory processing steps (digestion, density separation, filtration, handling). "
            "Identifying a truly MP-free 'clean matrix equivalent' for solid matrices (sand, sediment, soil) "
            "is challenging and remains an unsolved QA/QC problem in the field."
        ),
        "decision_tree_relevance": (
            "Procedural blanks are mandatory in Tier 1–2 methods and best practice for all studies. "
            "Results must be reported and used for blank subtraction. Navigate: Blanks & Contamination Control."
        ),
    },
    {
        "term": "Spike Recovery Sample",
        "category": "QA/QC",
        "definition": (
            "A clean matrix (procedural blank equivalent) to which a known number and/or mass of "
            "plastic particles of defined polymer types has been added before processing. "
            "Recovery is measured as the percentage of the original spike recovered after the full analytical workflow. "
            "In particle-counting methods, recovery can exceed 100% if fragmentation occurs during processing "
            "(one particle becomes multiple countable particles). "
            "No universally accepted recovery standard currently exists; reported acceptable ranges vary "
            "widely (50–150% has been cited in the literature)."
        ),
        "decision_tree_relevance": (
            "Required for extraction validation. Recovery must be reported with monitoring data. "
            "Navigate: Reference Materials / Positive Controls for spike material selection guidance."
        ),
    },
    {
        "term": "Air Handling / Laboratory Contamination Control",
        "category": "QA/QC",
        "definition": (
            "Practices to minimize airborne fiber contamination during sample processing and analysis. "
            "Includes: processing samples within a laminar flow hood or HEPA-filtered enclosure; "
            "covering samples with foil or glass lids between steps; "
            "using non-synthetic (cotton) lab coats — preferably a distinct color (e.g., blue dyed cotton) "
            "to facilitate visual identification of laboratory-derived contamination in analyzed samples; "
            "storing samples in glass containers rather than plastic."
        ),
        "decision_tree_relevance": (
            "Airborne fiber contamination is one of the largest sources of false-positive MPs in laboratory analysis. "
            "All Tier 1 and 2 protocols specify air handling requirements. Navigate: Blanks & Contamination Control."
        ),
    },
    {
        "term": "Size Limit of Detection (Upper and Lower)",
        "category": "QA/QC",
        "definition": (
            "The upper and lower size bounds of particles that can be detected by the analytical workflow. "
            "Upper size limit: the largest particle within study scope — set by collection device aperture "
            "(e.g., 5 mm for standard MP definition, or trawl mesh size). "
            "Lower size limit: determined by the processing step at which the greatest particle loss occurs. "
            "Example: samples collected with a 60 µm mesh manta trawl and filtered through a 10 µm filter — "
            "the effective lower size limit of detection is 60 µm (defined by the coarser collection step, not the finer filter). "
            "Both limits must be reported explicitly in all monitoring studies."
        ),
        "decision_tree_relevance": (
            "Critical for study comparability. Two studies with different size detection windows cannot be directly compared. "
            "Navigate: Definitions & Terminology for regulatory size definitions; "
            "Analytical Identification for instrument-specific detection limits."
        ),
    },
]

# Derive sorted category list for filter
ALL_CATEGORIES = sorted({entry["category"] for entry in GLOSSARY})


# ---------------------------------------------------------------------------
# Render function
# ---------------------------------------------------------------------------

def render_glossary_tab():
    """Render the searchable, filterable glossary tab."""
    st.markdown(
        "### Glossary of Key Terms\n"
        "Definitions for terminology used throughout the decision tree, "
        "organized by category. Use the filters below to find terms relevant to your study."
    )

    col_search, col_cat = st.columns([2, 1])

    with col_search:
        search_query = st.text_input(
            "Search terms or definitions",
            placeholder="e.g. density separation, in vitro, LLOD, SSD...",
            key="glossary_search",
        )

    with col_cat:
        selected_categories = st.multiselect(
            "Filter by category",
            options=ALL_CATEGORIES,
            default=[],
            key="glossary_category_filter",
        )

    # Apply filters
    entries = GLOSSARY
    if selected_categories:
        entries = [e for e in entries if e["category"] in selected_categories]

    if search_query.strip():
        query_lower = search_query.lower()
        entries = [
            e for e in entries
            if query_lower in e["term"].lower()
            or query_lower in e["definition"].lower()
            or query_lower in e["decision_tree_relevance"].lower()
            or query_lower in e["category"].lower()
        ]

    st.caption(f"{len(entries)} of {len(GLOSSARY)} terms shown")

    if not entries:
        st.info("No terms match the current filters. Try a broader search.")
        return

    # Display as styled cards grouped by category
    current_category = None
    for entry in entries:
        if entry["category"] != current_category:
            current_category = entry["category"]
            st.markdown(f"#### {current_category}")

        _render_glossary_card(entry)


def _render_glossary_card(entry: dict):
    """Render a single glossary entry as an expandable card."""
    with st.expander(f"**{entry['term']}**", expanded=False):
        st.markdown(f"**Definition:**  \n{entry['definition']}")
        st.markdown(
            f"**Decision Tree Relevance:**  \n"
            f"*{entry['decision_tree_relevance']}*"
        )
        st.caption(f"Category: {entry['category']}")
