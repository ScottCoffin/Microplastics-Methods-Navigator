# ============================================================================
# manuscript_figures.R
# Generates Figures 2, 4, 5, and 6 for the microplastics crosswalk manuscript
#
# Usage:
#   1. Set CROSSWALK_FILE path below
#   2. Run entire script, or source individual figure functions
#   3. Figures saved as PDF + PNG to ./figures/
#
# Dependencies:
#   install.packages(c("readxl", "dplyr", "tidyr", "ggplot2", "stringr",
#                      "forcats", "patchwork", "viridis", "scales"))
# ============================================================================

library(readxl)
library(dplyr)
library(tidyr)
library(ggplot2)
library(stringr)
library(forcats)
library(patchwork)
library(viridis)
library(scales)

# ── CONFIG ──────────────────────────────────────────────────────────────────

CROSSWALK_FILE <- "methods_navigator/data/crosswalk.xlsx"
SHEET_NAME <- "Crosswalk Table"
OUT_DIR <- "figures"

# Create output directory
dir.create(OUT_DIR, showWarnings = FALSE)

# Tier color palette (consistent across all figures)
TIER_PALETTE <- c(
  "1" = "#1a7a2e", # dark green
  "2" = "#2e6b8a", # steel blue
  "3" = "#b8860b", # dark goldenrod
  "4" = "#999999" # gray
)

TIER_LABELS <- c(
  "1" = "Tier 1: Normative/ \n Binding",
  "2" = "Tier 2: Authoritative/ \n Institutional",
  "3" = "Tier 3: Interlab Tested/ \n Critical Guidance",
  "4" = "Tier 4: Supporting/ \n Contextual"
)

# order matrices by increasing complexity (e.g., drinking water is a simpler matrix than wastewater, etc.)
Matrix_order <- c(
  "Air / Atmospheric",
  "Drinking Water",
  "Surface Water",
  "Sediment",
  "Soil / Terrestrial",
  "Wastewater",
  "Biosolids",
  "Food / Dietary",
  "Biota / Tissue",
  "Human Tissue"
)


# ── DATA LOADING ────────────────────────────────────────────────────────────

load_crosswalk <- function(file = CROSSWALK_FILE, sheet = SHEET_NAME) {
  expected_cols <- c(
    "Short Citation",
    "Priority Tier",
    "Primary Domain",
    "Document Type",
    "Matrix Tags"
  )

  normalize_cols <- function(x) {
    names(x) <- str_replace_all(names(x), "\\n", " ")
    names(x) <- str_replace_all(names(x), "\\s+", " ")
    names(x) <- str_trim(names(x))
    x
  }

  schema_score <- function(x) {
    cols <- str_to_lower(str_trim(names(x)))
    sum(str_to_lower(expected_cols) %in% cols)
  }

  # Row 1 in the workbook is a grouped section header; row 2 has the
  # filterable crosswalk field names. Score both layouts so the script keeps
  # working if a future workbook is saved without the grouped header row.
  candidates <- lapply(c(0, 1), function(skip_rows) {
    normalize_cols(read_excel(
      file,
      sheet = sheet,
      skip = skip_rows,
      .name_repair = "minimal"
    ))
  })

  scores <- vapply(candidates, schema_score, numeric(1))
  df <- candidates[[which.max(scores)]]

  if (max(scores) == 0) {
    stop(
      "Could not find the crosswalk header row. Expected columns include: ",
      paste(expected_cols, collapse = ", ")
    )
  }

  # Drop completely empty rows and formula/formatting tail rows without an ID
  # or citation. This keeps Excel table formatting from inflating the dataset.
  df <- df %>%
    filter(if_any(
      everything(),
      ~ !is.na(.x) & str_trim(as.character(.x)) != ""
    ))

  # Rename # column to entry_id
  if ("#" %in% names(df)) {
    df <- df %>% rename(entry_id = `#`)
  }

  keep_row <- rep(FALSE, nrow(df))
  if ("entry_id" %in% names(df)) {
    keep_row <- keep_row |
      (!is.na(df$entry_id) & str_trim(as.character(df$entry_id)) != "")
  }
  if ("Short Citation" %in% names(df)) {
    keep_row <- keep_row |
      (!is.na(df$`Short Citation`) &
        str_trim(as.character(df$`Short Citation`)) != "")
  }
  if ("entry_id" %in% names(df) || "Short Citation" %in% names(df)) {
    df <- df[keep_row, , drop = FALSE]
  }

  # Extract tier number from Priority Tier string
  if ("Priority Tier" %in% names(df)) {
    df <- df %>%
      mutate(
        tier_num = as.numeric(str_extract(
          `Priority Tier`,
          "Tier\\s*(\\d)",
          group = 1
        ))
      )
  } else {
    # Infer from the minimum non-NA score across topic columns
    df <- df %>% mutate(tier_num = 4)
  }

  # Parse Year as numeric
  if ("Year" %in% names(df)) {
    df <- df %>% mutate(Year = as.numeric(Year))
  }

  return(df)
}


# Helper: find a column by fuzzy matching
find_col <- function(df, candidates) {
  cols <- names(df)
  cols_lower <- tolower(cols)
  for (cand in candidates) {
    cand_lower <- tolower(str_trim(cand))
    # Exact match
    idx <- which(cols_lower == cand_lower)
    if (length(idx) > 0) {
      return(cols[idx[1]])
    }
    # Substring match
    idx <- which(str_detect(cols_lower, fixed(cand_lower)))
    if (length(idx) > 0) return(cols[idx[1]])
  }
  return(NA_character_)
}


normalize_instrument_tags <- function(tags) {
  tags <- str_squish(as.character(tags))
  tags[tags == "" | str_to_upper(tags) == "NA"] <- NA_character_
  tag_lower <- str_to_lower(tags)

  normalized <- case_when(
    is.na(tags) ~ NA_character_,
    str_detect(tag_lower, "ted-gc-ms") ~ "TED-GC-MS",
    str_detect(tag_lower, "py-gc|pyr-gc") ~ "Py-GC-MS",
    str_detect(tag_lower, "raman") ~ "µRaman",
    str_detect(tag_lower, "ftir") ~ "µFTIR",
    str_detect(tag_lower, "ldir") ~ "LDIR",
    str_detect(tag_lower, "nile red|fluorescence") ~ "Fluorescence / Nile Red",
    str_detect(tag_lower, "imagej|image analysis") ~ "Image Analysis",
    str_detect(
      tag_lower,
      "visual|stereomicroscopy"
    ) ~ "Visual / Stereomicroscopy",
    str_detect(tag_lower, "scanning electron microscopy|sem") ~ "SEM",
    str_detect(tag_lower, "nmr") ~ "NMR",
    str_detect(tag_lower, "antibody") ~ "Antibody-Based",
    str_detect(tag_lower, "density separation") ~ "Density Separation",
    str_detect(tag_lower, "h295r") ~ "H295R Assay",
    TRUE ~ tags
  )

  unique(na.omit(normalized))
}


# ── FIGURE 2: Coverage Heatmap (Matrix × Workflow Step) ─────────────────────

fig2_coverage_heatmap <- function(df) {
  # Define the matrix columns and workflow step columns to cross
  matrix_defs <- tribble(
    ~matrix_label        , ~col_candidates                                      ,
    "Drinking Water"     , c("matrix: drinking water", "drinking water")        ,
    "Surface Water"      , c("matrix: surface water", "surface water")          ,
    "Wastewater"         , c("matrix: wastewater", "wastewater")                ,
    "Biosolids"          , c("matrix: biosolids", "biosolids", "sludge")        ,
    "Sediment"           , c("matrix: sediment")                                ,
    "Biota / Tissue"     , c("matrix: biota/tissue", "biota")                   ,
    "Air / Atmospheric"  , c("matrix: air/atmos", "air")                        ,
    "Food / Dietary"     , c("matrix: food/dietary", "food")                    ,
    "Human Tissue"       , c("matrix: human tissue", "human tissue/biomonitor") ,
    "Soil / Terrestrial" , c("matrix: soil", "soil")
  )

  step_defs <- tribble(
    ~step_label          , ~col_candidates                                                      ,
    "Sampling"           , c("sampling (field methods)")                                        ,
    "Extraction"         , c("sample processing / extraction", "sample processing")             ,
    "Analysis"           , c("analytical methods (general)", "analytical methods")              ,
    "Material Standards" , c("Material Standards - materials", "Material Standards - protocol") ,
    "QA/QC"              , c("blanks & contamination control", "blanks")                        ,
    "Reporting"          , c("reporting & harmonization", "reporting")
  )

  # Build the matrix: for each (matrix, step), find the BEST (lowest) tier
  results <- expand_grid(
    matrix_label = matrix_defs$matrix_label,
    step_label = step_defs$step_label
  )

  best_tiers <- numeric(nrow(results))

  for (i in seq_len(nrow(results))) {
    mat <- matrix_defs %>% filter(matrix_label == results$matrix_label[i])
    stp <- step_defs %>% filter(step_label == results$step_label[i])

    mat_col <- find_col(df, mat$col_candidates[[1]])
    stp_cols <- unique(na.omit(vapply(
      stp$col_candidates[[1]],
      function(candidate) find_col(df, candidate),
      character(1)
    )))

    if (is.na(mat_col) || length(stp_cols) == 0) {
      best_tiers[i] <- NA_real_
      next
    }

    # Entries that score in the matrix column and any matching workflow column.
    subset <- df %>%
      filter(
        !is.na(.data[[mat_col]]) &
          .data[[mat_col]] != "" &
          .data[[mat_col]] != 0,
        if_any(
          all_of(stp_cols),
          ~ !is.na(.x) & .x != "" & .x != 0
        )
      )

    if (nrow(subset) == 0) {
      best_tiers[i] <- NA_real_
    } else if (
      stp$step_label %in% c("Sampling", "Material Standards", "Reporting")
    ) {
      matrix_tiers <- suppressWarnings(as.numeric(subset[[mat_col]]))
      best_tiers[i] <- if (all(is.na(matrix_tiers))) {
        NA_real_
      } else {
        min(matrix_tiers, na.rm = TRUE)
      }
    } else {
      best_tiers[i] <- min(subset$tier_num, na.rm = TRUE)
    }
  }

  results$best_tier <- best_tiers
  results$tier_label <- factor(
    ifelse(
      is.na(results$best_tier),
      "No coverage",
      paste0("Tier ", results$best_tier)
    ),
    levels = c("Tier 1", "Tier 2", "Tier 3", "Tier 4", "No coverage")
  )

  # Order axes
  results$matrix_label <- factor(
    results$matrix_label,
    levels = rev(matrix_defs$matrix_label)
  )
  results$step_label <- factor(
    results$step_label,
    levels = step_defs$step_label
  )

  # Plot
  p <- ggplot(
    results,
    aes(x = step_label, y = matrix_label, fill = tier_label)
  ) +
    geom_tile(color = "white", linewidth = 1.2) +
    geom_text(
      aes(label = ifelse(is.na(best_tier), "No", paste0("T", best_tier))),
      size = 3.5,
      fontface = "bold",
      color = ifelse(results$best_tier %in% c(1, 2), "white", "gray30")
    ) +
    scale_fill_manual(
      values = c(
        setNames(TIER_PALETTE, paste0("Tier ", names(TIER_PALETTE))),
        "No coverage" = "#f5f0f0"
      ),
      breaks = paste0("Tier ", names(TIER_LABELS)),
      labels = setNames(TIER_LABELS, paste0("Tier ", names(TIER_LABELS))),
      name = "Best Available\nAuthority Tier",
      drop = FALSE
    ) +
    labs(
      title = "Standardization Coverage: Matrix × Workflow Step",
      subtitle = "Highest authority tier available for each combination",
      x = NULL,
      y = NULL
    ) +
    theme_minimal(base_size = 12) +
    theme(
      axis.text.x = element_text(angle = 35, hjust = 1, size = 10),
      axis.text.y = element_text(size = 10),
      legend.position = "right",
      legend.key.height = unit(0.5, "in"),
      legend.spacing.y = unit(0.12, "in"),
      legend.text = element_text(
        lineheight = 0.95,
        margin = margin(b = 8)
      ),
      legend.title = element_text(margin = margin(b = 6)),
      panel.grid = element_blank(),
      plot.title = element_text(face = "bold", size = 14),
      plot.subtitle = element_text(size = 10, color = "gray40")
    ) +
    guides(
      fill = guide_legend(
        keyheight = unit(0.5, "in"),
        label.position = "right",
        label.hjust = 0
      )
    )

  # ggsave(
  #   file.path(OUT_DIR, "fig2_coverage_heatmap.pdf"),
  #   p,
  #   width = 10,
  #   height = 6
  # )
  ggsave(
    file.path(OUT_DIR, "fig2_coverage_heatmap.png"),
    p,
    width = 10,
    height = 6,
    dpi = 300
  )
  message("✅ Figure 2 saved")
  return(p)
}


# ── FIGURE 4: Temporal Coverage (Year × Domain) ────────────────────────────

fig4_temporal <- function(df) {
  # Need Year and Primary Domain
  year_col <- find_col(df, c("year"))
  domain_col <- find_col(df, c("primary domain"))

  if (is.na(year_col)) {
    stop("Year column not found")
  }

  plot_df <- df %>%
    filter(!is.na(.data[[year_col]]), .data[[year_col]] >= 2004) %>%
    mutate(
      year = as.numeric(.data[[year_col]]),
      tier = factor(tier_num, levels = 1:4),
      domain = if (!is.na(domain_col)) {
        str_trim(as.character(.data[[domain_col]]))
      } else {
        "Unknown"
      },
      domain_y = case_when(
        domain == "Monitoring" ~ 1,
        domain == "Toxicology" ~ 2,
        TRUE ~ NA_real_
      )
    ) %>%
    filter(!is.na(year), !is.na(domain_y))

  # Milestone annotations
  milestones <- tribble(
    ~year , ~label                              , ~y_nudge ,
     2004 , "Thompson\n'microplastics'\ncoined" , 0.5      ,
     2009 , "NOAA\n5 mm\ndefinition"            , 1.5      ,
     2018 , "CA SB 1422"                        , 0.5      ,
     2020 , "CA MP\ndefinition"                 , 1.5      ,
     2023 , "EU REACH\nrestriction"             , 0.5      ,
     2025 , "ISO 16094-2\npublished"            , 1.5
  )

  p <- ggplot(plot_df, aes(x = year, y = domain_y)) +
    # Jittered dots
    geom_jitter(
      aes(color = tier, shape = tier),
      width = 0.45,
      height = 0.25,
      size = 3.2,
      alpha = 0.75
    ) +
    # Milestone lines
    geom_vline(
      data = milestones,
      aes(xintercept = year),
      linetype = "dotted",
      color = "gray60",
      linewidth = 0.4
    ) +
    geom_label(
      data = milestones,
      aes(x = year, y = 2.45 + y_nudge * 0.22, label = label),
      size = 2.2,
      fill = "white",
      linewidth = 0.2,
      lineheight = 0.85,
      hjust = 0.5
    ) +
    # Scales
    scale_color_manual(
      values = TIER_PALETTE,
      labels = TIER_LABELS,
      name = "Authority Tier"
    ) +
    scale_shape_manual(
      values = c("1" = 16, "2" = 17, "3" = 15, "4" = 1),
      labels = TIER_LABELS,
      name = "Authority Tier"
    ) +
    scale_x_continuous(breaks = seq(2004, 2026, 2), limits = c(2002.5, 2028)) +
    scale_y_continuous(
      breaks = c(1, 2),
      labels = c("Monitoring", "Toxicology"),
      limits = c(0.55, 3.05),
      expand = expansion(mult = c(0.02, 0.03))
    ) +
    labs(
      title = "Temporal Distribution of Crosswalk References",
      subtitle = "Monitoring and toxicology references by authority tier, with regulatory milestones",
      x = "Publication Year",
      y = NULL
    ) +
    theme_minimal(base_size = 12) +
    theme(
      axis.text.y = element_text(size = 10),
      legend.position = "bottom",
      panel.grid.minor = element_blank(),
      panel.grid.major.y = element_line(color = "gray90"),
      plot.title = element_text(face = "bold", size = 14),
      plot.subtitle = element_text(size = 10, color = "gray40"),
      plot.margin = margin(t = 16, r = 18, b = 8, l = 8)
    ) +
    guides(
      color = guide_legend(nrow = 1, override.aes = list(size = 3.2)),
      shape = guide_legend(nrow = 1)
    ) +
    coord_cartesian(clip = "off")

  #ggsave(file.path(OUT_DIR, "fig4_temporal.pdf"), p, width = 12, height = 5)
  ggsave(
    file.path(OUT_DIR, "fig4_temporal.png"),
    p,
    width = 12,
    height = 5,
    dpi = 300
  )
  message("✅ Figure 4 saved")
  return(p)
}


# ── FIGURE 5: Instrumentation × Matrix Concentric-Donut Chart ──────────────
#
# Each cell shows three concentric circles painted back-to-front:
#   Outer  (Tier 3 color, largest)  = all Tier 1–3 refs combined
#   Middle (Tier 2 color)           = Tier 1 + Tier 2 refs
#   Inner  (Tier 1 color, smallest) = Tier 1 refs only
#
# The visible annular ring between consecutive layers encodes that tier's count.
# Total ref count is labeled in white in the center.

fig5_instrument_matrix <- function(df) {
  inst_col <- find_col(df, c("instrumentation tags"))

  if (is.na(inst_col)) {
    message("⚠️ Instrumentation Tags column not found. Skipping Figure 5.")
    return(NULL)
  }

  df_fig5 <- df %>%
    filter(!is.na(tier_num), tier_num < 4)

  df_fig5$.instrument_tags <- lapply(
    str_split(
      ifelse(is.na(df_fig5[[inst_col]]), "", as.character(df_fig5[[inst_col]])),
      fixed(";")
    ),
    normalize_instrument_tags
  )

  # Display canonical instrument/method groups after semicolon-delimited parsing.
  instrument_order <- c(
    "µFTIR",
    "µRaman",
    "Py-GC-MS",
    "TED-GC-MS",
    "LDIR",
    "Fluorescence / Nile Red",
    "Visual / Stereomicroscopy",
    "Image Analysis",
    "SEM",
    "NMR",
    "Antibody-Based",
    "Density Separation",
    "H295R Assay"
  )
  observed_instruments <- sort(unique(unlist(df_fig5$.instrument_tags)))
  instruments <- c(
    intersect(instrument_order, observed_instruments),
    setdiff(observed_instruments, instrument_order)
  )

  matrix_defs <- tribble(
    ~matrix_label    , ~col_candidates                                      ,
    "Drinking Water" , c("matrix: drinking water", "drinking water")        ,
    "Surface Water"  , c("matrix: surface water", "surface water")          ,
    "Wastewater"     , c("matrix: wastewater", "wastewater")                ,
    "Biosolids"      , c("matrix: biosolids", "biosolids", "sludge")        ,
    "Sediment"       , c("matrix: sediment")                                ,
    "Biota"          , c("matrix: biota/tissue", "biota")                   ,
    "Air"            , c("matrix: air/atmos", "air")                        ,
    "Food"           , c("matrix: food/dietary", "food")                    ,
    "Human Tissue"   , c("matrix: human tissue", "human tissue/biomonitor") ,
    "Soil"           , c("matrix: soil", "soil")
  )

  # Build per-cell data with per-tier counts and cumulative circle sizes
  results <- list()

  for (inst in instruments) {
    inst_rows <- df_fig5 %>%
      filter(vapply(
        .instrument_tags,
        function(tags) inst %in% tags,
        logical(1)
      ))

    for (j in seq_len(nrow(matrix_defs))) {
      mat_label <- matrix_defs$matrix_label[j]
      mat_col <- find_col(df, matrix_defs$col_candidates[[j]])

      if (is.na(mat_col)) {
        n <- 0L
        t1 <- 0L
        t2 <- 0L
        t3 <- 0L
      } else {
        matched <- inst_rows %>%
          filter(
            !is.na(.data[[mat_col]]) &
              .data[[mat_col]] != "" &
              .data[[mat_col]] != 0
          )
        n <- nrow(matched)
        t1 <- sum(matched$tier_num == 1, na.rm = TRUE)
        t2 <- sum(matched$tier_num == 2, na.rm = TRUE)
        t3 <- sum(matched$tier_num == 3, na.rm = TRUE)
      }

      results <- c(
        results,
        list(tibble(
          instrument = inst,
          matrix = mat_label,
          n_refs = n,
          t1 = t1,
          t2 = t2,
          t3 = t3,
          # Cumulative counts drive each circle's radius:
          #   outer = T1+T2+T3 (= n_refs), middle = T1+T2, inner = T1 only
          outer = n,
          middle = t1 + t2,
          inner = t1
        ))
      )
    }
  }

  plot_df <- bind_rows(results) %>%
    filter(n_refs > 0) %>%
    mutate(
      instrument = factor(instrument, levels = instruments),
      matrix = factor(matrix, levels = rev(matrix_defs$matrix_label))
    )

  if (nrow(plot_df) == 0) {
    message(
      "⚠️ No instrument × matrix combinations found. Check Instrumentation Tags column."
    )
    return(NULL)
  }

  # Stack three layers painted back-to-front (biggest = Tier 3 drawn first):
  #   tier_ring "3" → outer  circle, Tier 3 color
  #   tier_ring "2" → middle circle, Tier 2 color
  #   tier_ring "1" → inner  circle, Tier 1 color
  circle_df <- bind_rows(
    plot_df %>% mutate(circle_n = outer, tier_ring = "3"),
    plot_df %>%
      filter(middle > 0) %>%
      mutate(circle_n = middle, tier_ring = "2"),
    plot_df %>% filter(inner > 0) %>% mutate(circle_n = inner, tier_ring = "1")
  ) %>%
    mutate(tier_ring = factor(tier_ring, levels = c("3", "2", "1")))

  p <- ggplot(circle_df, aes(x = instrument, y = matrix)) +
    geom_point(aes(size = circle_n, color = tier_ring), alpha = 1.0) +
    geom_text(
      data = plot_df,
      aes(label = n_refs),
      size = 2.5,
      color = "white",
      fontface = "bold"
    ) +
    scale_color_manual(
      values = TIER_PALETTE,
      labels = c(
        "1" = "Tier 1: Normative/\nBinding (inner circle)",
        "2" = "Tier 2: Authoritative/\nInstitutional (middle ring)",
        "3" = "Tier 3: Peer-Reviewed/\nValidated (outer ring)"
      ),
      name = "Authority Tier\n(ring = cumulative count)"
    ) +
    scale_size_continuous(
      range = c(5, 20),
      name = "Number of\nReferences\n(outer circle)",
      breaks = c(1, 3, 5, 10)
    ) +
    labs(
      title = "Instrumentation and Method Coverage Across Matrices",
      subtitle = paste0(
        "Concentric rings: outer = all Tiers 1–3; middle = Tiers 1–2; ",
        "inner = Tier 1 only. Total refs labeled. Tier 4 excluded."
      ),
      x = NULL,
      y = NULL
    ) +
    theme_minimal(base_size = 12) +
    theme(
      axis.text.x = element_text(angle = 25, hjust = 1, size = 10),
      axis.text.y = element_text(size = 10),
      legend.position = "right",
      legend.box.spacing = unit(0.2, "in"),
      legend.key.height = unit(0.5, "in"),
      legend.key.width = unit(0.35, "in"),
      legend.spacing.y = unit(0.12, "in"),
      legend.text = element_text(
        size = 9.5,
        lineheight = 0.95,
        margin = margin(l = 8, b = 8)
      ),
      legend.title = element_text(size = 11, margin = margin(b = 6)),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      plot.title = element_text(face = "bold", size = 14),
      plot.subtitle = element_text(size = 10, color = "gray40"),
      plot.margin = margin(t = 10, r = 24, b = 10, l = 10)
    ) +
    guides(
      color = guide_legend(
        order = 1,
        override.aes = list(size = 6),
        label.position = "right",
        label.hjust = 0
      ),
      size = guide_legend(
        order = 2,
        override.aes = list(color = "gray50")
      )
    )

  ggsave(
    file.path(OUT_DIR, "fig5_instrument_matrix.pdf"),
    p,
    width = 11,
    height = 6.5
  )
  ggsave(
    file.path(OUT_DIR, "fig5_instrument_matrix.png"),
    p,
    width = 11,
    height = 6.5,
    dpi = 300
  )
  message("✅ Figure 5 saved")
  return(p)
}


# ── FIGURE 6: Toxicology Workflow Coverage ──────────────────────────────────

fig6_tox_workflow <- function(df) {
  # Define tox workflow steps and their column mappings
  tox_steps <- tribble(
    ~step_order , ~step_label                  , ~col_candidates                           , ~keywords                            ,
              1 , "Particle\nCharacterization" , c("toxicology: study design & dosimetry") , NA_character_                        ,
              2 , "Reference\nParticles"       , c("reference materials / +controls")      , NA_character_                        ,
              3 , "Dosimetry"                  , c("toxicology: study design & dosimetry") , "dosimetry;particokinetics;ISDD;PBK" ,
              4 , "Effects\nTesting"           , c("toxicology: effects testing methods")  , NA_character_                        ,
              5 , "Reporting\n(Tox)"           , c("reporting & harmonization")            , NA_character_                        ,
  )

  # Get domain column for filtering
  domain_col <- find_col(df, c("primary domain"))

  # Filter to tox-relevant entries
  if (!is.na(domain_col)) {
    df_tox <- df %>%
      filter(
        str_to_lower(.data[[domain_col]]) %in%
          c("toxicology", "both", "cross-cutting")
      )
  } else {
    df_tox <- df
  }

  step_results <- list()

  for (i in seq_len(nrow(tox_steps))) {
    s <- tox_steps[i, ]
    col <- find_col(df_tox, s$col_candidates[[1]])

    if (is.na(col)) {
      subset <- df_tox[0, ]
    } else {
      subset <- df_tox %>%
        filter(!is.na(.data[[col]]) & .data[[col]] != "" & .data[[col]] != 0)
    }

    # Additional keyword filtering
    if (!is.na(s$keywords)) {
      notes_col <- find_col(subset, c("key notes"))
      if (!is.na(notes_col)) {
        kws <- str_split(s$keywords, ";")[[1]]
        kw_mask <- Reduce(
          `|`,
          lapply(kws, function(kw) {
            str_detect(
              tolower(subset[[notes_col]]),
              fixed(tolower(str_trim(kw)))
            )
          })
        )
        kw_mask[is.na(kw_mask)] <- FALSE
        subset <- subset[kw_mask, ]
      }
    }

    n <- nrow(subset)
    best <- if (n > 0) min(subset$tier_num, na.rm = TRUE) else NA_real_

    # Tier breakdown
    tier_counts <- if (n > 0) {
      table(factor(subset$tier_num, levels = 1:4))
    } else {
      table(factor(integer(0), levels = 1:4))
    }

    step_results <- c(
      step_results,
      list(tibble(
        step_order = s$step_order,
        step_label = s$step_label,
        n_refs = n,
        best_tier = best,
        t1 = as.integer(tier_counts["1"]),
        t2 = as.integer(tier_counts["2"]),
        t3 = as.integer(tier_counts["3"]),
        t4 = as.integer(tier_counts["4"])
      ))
    )
  }

  plot_df <- bind_rows(step_results) %>%
    mutate(step_label = factor(step_label, levels = step_label)) %>%
    pivot_longer(
      cols = c(t1, t2, t3, t4),
      names_to = "tier",
      values_to = "count"
    ) %>%
    mutate(
      tier = factor(str_replace(tier, "t", ""), levels = c("4", "3", "2", "1"))
    )

  # Summary labels for each step
  summary_df <- bind_rows(step_results) %>%
    mutate(
      step_label = factor(step_label, levels = step_label),
      gap_label = case_when(
        is.na(best_tier) ~ "⚠ GAP",
        best_tier >= 3 ~ paste0("Best: Tier ", best_tier),
        TRUE ~ paste0("Best: Tier ", best_tier)
      )
    )

  p <- ggplot(plot_df, aes(x = step_label, y = count, fill = tier)) +
    geom_col(width = 0.7) +
    geom_text(
      data = summary_df,
      aes(x = step_label, y = n_refs + 0.5, label = gap_label, fill = NULL),
      size = 3,
      fontface = "italic",
      color = "gray30"
    ) +
    scale_fill_manual(
      values = TIER_PALETTE,
      labels = TIER_LABELS,
      name = "Authority Tier"
    ) +
    labs(
      title = "Toxicology Workflow: Reference Coverage by Step",
      subtitle = "Stacked by authority tier; annotations show best available tier or gap status",
      x = NULL,
      y = "Number of References"
    ) +
    theme_minimal(base_size = 12) +
    theme(
      axis.text.x = element_text(size = 10, lineheight = 0.9),
      legend.position = "bottom",
      panel.grid.major.x = element_blank(),
      plot.title = element_text(face = "bold", size = 14),
      plot.subtitle = element_text(size = 10, color = "gray40")
    ) +
    guides(fill = guide_legend(reverse = TRUE, nrow = 1))

  #ggsave(file.path(OUT_DIR, "fig6_tox_workflow.pdf"), p, width = 9, height = 5)
  ggsave(
    file.path(OUT_DIR, "fig6_tox_workflow.png"),
    p,
    width = 9,
    height = 5,
    dpi = 300
  )
  message("✅ Figure 6 saved")
  return(p)
}


# ── FIGURE 4b: Workflow Step Coverage (stacked bar by tier) ─────────────────

fig4_coverage <- function(df) {
  # Three-panel stacked bar chart mirroring fig4_coverage.py.
  # Tier attribution uses per-cell integer values from topic scoring columns,
  # consistent with fig2's matrix-column approach.
  # "Analytical Methods (General)" excluded to avoid double-counting with
  # FTIR / Raman / Py-GC-MS columns.

  steps_raw <- list(
    # Panel 1 — Framing & Sampling
    list(
      c("definitions & terminology"),
      "Definitions &\nTerminology",
      1L,
      "Framing"
    ),
    list(c("problem formulation"), "Problem\nFormulation", 1L, "Framing"),
    list(
      c("sampling (field methods)"),
      "Sampling\n(Field)",
      1L,
      "Sampling & Matrix"
    ),
    list(
      c("matrix: drinking water"),
      "Matrix:\nDrinking Water",
      1L,
      "Sampling & Matrix"
    ),
    list(
      c("matrix: surface"),
      "Matrix:\nSurface /\nWastewater",
      1L,
      "Sampling & Matrix"
    ),
    list(c("matrix: sediment"), "Matrix:\nSediment", 1L, "Sampling & Matrix"),
    list(
      c("matrix: biota"),
      "Matrix:\nBiota / Tissue",
      1L,
      "Sampling & Matrix"
    ),
    list(c("matrix: air"), "Matrix:\nAir / Atmos.", 1L, "Sampling & Matrix"),
    list(c("matrix: food"), "Matrix:\nFood / Diet", 1L, "Sampling & Matrix"),
    list(
      c("matrix: human tissue", "human tissue/biomonitor"),
      "Matrix:\nHuman Tissue /\nBiomonit.",
      1L,
      "Sampling & Matrix"
    ),
    # Panel 2 — Lab Processing & Analysis
    list(
      c("sample processing / extraction", "sample processing"),
      "Sample\nProcessing /\nExtraction",
      2L,
      "Lab Processing"
    ),
    list(
      c("sub-sampling", "subsampling"),
      "Sub-\nsampling",
      2L,
      "Lab Processing"
    ),
    list(
      c("reference materials"),
      "Reference\nMaterials /\nControls",
      2L,
      "Lab Processing"
    ),
    list(
      c("blanks & contamination", "blanks"),
      "Blanks &\nContam. Control",
      2L,
      "Lab Processing"
    ),
    list(
      c("ftir / ir spectroscopy", "ftir"),
      "FTIR / IR",
      2L,
      "Spectroscopic Analysis"
    ),
    list(
      c("raman spectroscopy", "raman"),
      "Raman /\nµRaman",
      2L,
      "Spectroscopic Analysis"
    ),
    list(c("py-gc-ms"), "Py-GC-MS", 2L, "Spectroscopic Analysis"),
    list(
      c("interlaboratory"),
      "Interlaboratory\nValidation",
      2L,
      "Spectroscopic Analysis"
    ),
    # Panel 3 — Data, Reporting & Toxicology
    list(
      c("data analysis & statistics"),
      "Data Analysis\n& Statistics",
      3L,
      "Data & Reporting"
    ),
    list(
      c("reporting & harmonization"),
      "Reporting &\nHarmonization",
      3L,
      "Data & Reporting"
    ),
    list(
      c("databases & data sharing", "databases"),
      "Data\nDeposition",
      3L,
      "Data & Reporting"
    ),
    list(
      c("toxicology: study design"),
      "Tox: Study\nDesign &\nDosimetry",
      3L,
      "Toxicology"
    ),
    list(
      c("toxicology: effects testing"),
      "Tox: Effects\nTesting",
      3L,
      "Toxicology"
    ),
    list(
      c("risk assessment"),
      "Risk\nAssessment /\nRisk Char.",
      3L,
      "Toxicology"
    )
  )

  step_labels_ordered <- vapply(steps_raw, `[[`, character(1), 2)

  # Count tier hits per step using per-cell integer values from topic columns
  results <- lapply(steps_raw, function(s) {
    col_name <- find_col(df, s[[1]])
    if (is.na(col_name)) {
      tier_counts <- integer(4)
    } else {
      vals <- suppressWarnings(as.numeric(df[[col_name]]))
      tier_counts <- vapply(
        1:4,
        function(t) sum(vals == t, na.rm = TRUE),
        integer(1)
      )
    }
    tibble(
      step_label = s[[2]],
      panel = s[[3]],
      subgroup = s[[4]],
      tier = factor(as.character(1:4), levels = c("4", "3", "2", "1")),
      count = tier_counts
    )
  })

  plot_df <- bind_rows(results) %>%
    mutate(step_label = factor(step_label, levels = step_labels_ordered))

  subgroup_colors <- c(
    "Framing" = "#E3F2FD",
    "Sampling & Matrix" = "#F3E5F5",
    "Lab Processing" = "#E8F5E9",
    "Spectroscopic Analysis" = "#FFF3E0",
    "Data & Reporting" = "#E0F7FA",
    "Toxicology" = "#FCE4EC"
  )

  panel_titles <- c(
    "1" = "Framing & Sampling",
    "2" = "Lab Processing & Analysis",
    "3" = "Data, Reporting & Toxicology"
  )

  make_panel <- function(pnl_num, show_legend = FALSE) {
    pd <- plot_df %>% filter(panel == pnl_num)

    # Sub-group bounding boxes for background shading (drawn before bars)
    sg_df <- pd %>%
      select(step_label, subgroup) %>%
      distinct() %>%
      mutate(xpos = as.integer(step_label)) %>%
      group_by(subgroup) %>%
      summarise(
        xmin = min(xpos) - 0.5,
        xmax = max(xpos) + 0.5,
        .groups = "drop"
      ) %>%
      mutate(bg = subgroup_colors[subgroup])

    tot_df <- pd %>%
      group_by(step_label) %>%
      summarise(total = sum(count), .groups = "drop") %>%
      filter(total > 0)

    p <- ggplot(pd, aes(x = step_label, y = count, fill = tier))

    for (i in seq_len(nrow(sg_df))) {
      p <- p +
        annotate(
          "rect",
          xmin = sg_df$xmin[i],
          xmax = sg_df$xmax[i],
          ymin = -Inf,
          ymax = Inf,
          fill = sg_df$bg[i],
          alpha = 0.30
        )
    }

    p <- p +
      geom_col(width = 0.7) +
      geom_text(
        aes(label = ifelse(count > 0, as.character(count), "")),
        position = position_stack(vjust = 0.5),
        size = 2.2,
        color = "white",
        fontface = "bold"
      ) +
      geom_text(
        data = tot_df,
        aes(x = step_label, y = total + 0.35, label = total, fill = NULL),
        size = 2.8,
        fontface = "bold",
        color = "gray30",
        inherit.aes = FALSE
      ) +
      scale_fill_manual(
        values = TIER_PALETTE,
        labels = TIER_LABELS,
        name = "Authority Tier",
        breaks = c("1", "2", "3", "4"),
        drop = FALSE
      ) +
      scale_y_continuous(expand = expansion(mult = c(0, 0.12))) +
      labs(
        title = panel_titles[as.character(pnl_num)],
        x = NULL,
        y = "Papers (n)"
      ) +
      coord_cartesian(clip = "off") +
      theme_minimal(base_size = 11) +
      theme(
        # Angled labels; generous bottom margin prevents bleeding into the
        # panel below when assembled by patchwork
        axis.text.x = element_text(
          angle = 40,
          hjust = 1,
          vjust = 1,
          size = 8.5,
          lineheight = 0.82
        ),
        axis.text.y = element_text(size = 9),
        axis.title.y = element_text(size = 9),
        plot.title = element_text(face = "bold", size = 10.5, color = "#333"),
        panel.grid.major.x = element_blank(),
        panel.grid.minor = element_blank(),
        panel.grid.major.y = element_line(color = "#EEEEEE"),
        plot.margin = margin(
          t = 4,
          r = 10,
          b = if (show_legend) 8 else 55,
          l = 10
        ),
        legend.position = if (show_legend) "bottom" else "none",
        legend.direction = "horizontal"
      )

    if (show_legend) {
      p <- p + guides(fill = guide_legend(reverse = TRUE, nrow = 2))
    }

    return(p)
  }

  p1 <- make_panel(1)
  p2 <- make_panel(2)
  p3 <- make_panel(3, show_legend = TRUE)

  combined <- (p1 / p2 / p3) +
    plot_layout(heights = c(10, 8, 6)) +
    plot_annotation(
      title = "Coverage of MNP Research Workflow Steps by Priority Tier",
      subtitle = paste0(
        'Papers per step · per-cell tier ratings · ',
        '"Analytical Methods (General)" excluded to avoid double-counting with FTIR / Raman / Py-GC-MS'
      ),
      theme = theme(
        plot.title = element_text(face = "bold", size = 13),
        plot.subtitle = element_text(size = 9, color = "gray40")
      )
    )

  ggsave(
    file.path(OUT_DIR, "fig4_coverage.png"),
    combined,
    width = 12,
    height = 14,
    dpi = 300
  )
  message("✅ Figure 4 (coverage) saved")
  return(combined)
}


# ── MAIN ────────────────────────────────────────────────────────────────────

main <- function() {
  message("Loading crosswalk from: ", CROSSWALK_FILE)
  df <- load_crosswalk()
  message("  Loaded ", nrow(df), " entries with ", ncol(df), " columns")
  message(
    "  Tier distribution: ",
    paste(
      names(table(df$tier_num)),
      table(df$tier_num),
      sep = "=",
      collapse = ", "
    )
  )
  message("")

  # Generate figures
  message("── Generating Figure 2: Coverage Heatmap ──")
  p2 <- fig2_coverage_heatmap(df)

  message("── Generating Figure 4: Temporal Coverage ──")
  p4 <- fig4_temporal(df)

  message("── Generating Figure 4 (coverage): Workflow Step Coverage ──")
  p4b <- fig4_coverage(df)

  message("── Generating Figure 5: Instrumentation × Matrix ──")
  p5 <- fig5_instrument_matrix(df)

  message("── Generating Figure 6: Toxicology Workflow ──")
  p6 <- fig6_tox_workflow(df)

  message("")
  message("All figures saved to: ", OUT_DIR, "/")

  # Return all plots invisibly
  invisible(list(fig2 = p2, fig4 = p4, fig4b = p4b, fig5 = p5, fig6 = p6))
}

# Run
main()
