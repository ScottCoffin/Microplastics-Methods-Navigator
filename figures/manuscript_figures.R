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

CROSSWALK_FILE <- "methods_navigator/crosswalk.xlsx"
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
  "1" = "Tier 1: Normative",
  "2" = "Tier 2: Authoritative",
  "3" = "Tier 3: Peer-Reviewed",
  "4" = "Tier 4: Supporting"
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


# ── FIGURE 2: Coverage Heatmap (Matrix × Workflow Step) ─────────────────────

fig2_coverage_heatmap <- function(df) {
  # Define the matrix columns and workflow step columns to cross
  matrix_defs <- tribble(
    ~matrix_label          , ~col_candidates                                      ,
    "Drinking Water"       , c("matrix: drinking water", "drinking water")        ,
    "Surface Water"        , c("matrix: surface water", "surface water")          ,
    "Wastewater"           , c("matrix: wastewater", "wastewater")                ,
    "Biosolids"            , c("matrix: biosolids", "biosolids", "sludge")        ,
    "Sediment"             , c("matrix: sediment")                                ,
    "Biota / Tissue"       , c("matrix: biota/tissue", "biota")                   ,
    "Air / Atmospheric"    , c("matrix: air/atmos", "air")                        ,
    "Food / Dietary"       , c("matrix: food/dietary", "food")                    ,
    "Human Tissue"         , c("matrix: human tissue", "human tissue/biomonitor") ,
    "Soil / Terrestrial"   , c("matrix: soil", "soil")
  )

  step_defs <- tribble(
    ~step_label       , ~col_candidates                                             ,
    "Sampling"        , c("sampling (field methods)", "sampling")                   ,
    "Extraction"      , c("sample processing / extraction", "sample processing")    ,
    "Analysis"        , c("analytical methods (general)", "analytical methods")     ,
    "Ref. Materials"  , c("reference materials / +controls", "reference materials") ,
    "Blanks / QC"     , c("blanks & contamination control", "blanks")               ,
    "Reporting"       , c("reporting & harmonization", "reporting")                 ,
    "Interlaboratory" , c("interlaboratory/validation", "interlaboratory")
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
    stp_col <- find_col(df, stp$col_candidates[[1]])

    if (is.na(mat_col) || is.na(stp_col)) {
      best_tiers[i] <- NA_real_
      next
    }

    # Entries that score in BOTH the matrix column and the step column
    subset <- df %>%
      filter(
        !is.na(.data[[mat_col]]) &
          .data[[mat_col]] != "" &
          .data[[mat_col]] != 0,
        !is.na(.data[[stp_col]]) &
          .data[[stp_col]] != "" &
          .data[[stp_col]] != 0
      )

    if (nrow(subset) == 0) {
      best_tiers[i] <- NA_real_
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
        "Tier 1" = "#1a7a2e",
        "Tier 2" = "#2e6b8a",
        "Tier 3" = "#b8860b",
        "Tier 4" = "#cccccc",
        "No coverage" = "#f5f0f0"
      ),
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
      panel.grid = element_blank(),
      plot.title = element_text(face = "bold", size = 14),
      plot.subtitle = element_text(size = 10, color = "gray40")
    )

  ggsave(
    file.path(OUT_DIR, "fig2_coverage_heatmap.pdf"),
    p,
    width = 10,
    height = 6
  )
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

  ggsave(file.path(OUT_DIR, "fig4_temporal.pdf"), p, width = 12, height = 5)
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


# ── FIGURE 5: Instrumentation × Matrix Bubble Chart ────────────────────────

fig5_instrument_matrix <- function(df) {
  inst_col <- find_col(df, c("instrumentation tags"))

  if (is.na(inst_col)) {
    message("⚠️ Instrumentation Tags column not found. Skipping Figure 5.")
    return(NULL)
  }

  # Target instruments and matrices
  instruments <- c(
    "µFTIR",
    "µRaman",
    "Py-GC-MS",
    "TED-GC-MS",
    "LDIR",
    "Nile Red"
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

  # Build long-form data: for each instrument × matrix, count refs and find best tier
  results <- list()

  for (inst in instruments) {
    inst_rows <- df %>%
      filter(str_detect(.data[[inst_col]], fixed(inst, ignore_case = TRUE)))

    for (j in seq_len(nrow(matrix_defs))) {
      mat_label <- matrix_defs$matrix_label[j]
      mat_col <- find_col(df, matrix_defs$col_candidates[[j]])

      if (is.na(mat_col)) {
        n <- 0
        best <- NA_real_
      } else {
        matched <- inst_rows %>%
          filter(
            !is.na(.data[[mat_col]]) &
              .data[[mat_col]] != "" &
              .data[[mat_col]] != 0
          )
        n <- nrow(matched)
        best <- if (n > 0) min(matched$tier_num, na.rm = TRUE) else NA_real_
      }

      results <- c(
        results,
        list(tibble(
          instrument = inst,
          matrix = mat_label,
          n_refs = n,
          best_tier = best
        ))
      )
    }
  }

  plot_df <- bind_rows(results) %>%
    filter(n_refs > 0) %>%
    mutate(
      instrument = factor(instrument, levels = instruments),
      matrix = factor(matrix, levels = rev(matrix_defs$matrix_label)),
      tier_label = paste0("Tier ", best_tier)
    )

  if (nrow(plot_df) == 0) {
    message(
      "⚠️ No instrument × matrix combinations found. Check Instrumentation Tags column."
    )
    return(NULL)
  }

  p <- ggplot(plot_df, aes(x = instrument, y = matrix)) +
    geom_point(aes(size = n_refs, color = factor(best_tier)), alpha = 0.8) +
    geom_text(
      aes(label = n_refs),
      size = 2.5,
      color = "white",
      fontface = "bold"
    ) +
    scale_color_manual(
      values = TIER_PALETTE,
      labels = TIER_LABELS,
      name = "Best Available Tier"
    ) +
    scale_size_continuous(
      range = c(4, 16),
      name = "Number of\nReferences",
      breaks = c(1, 3, 5, 10)
    ) +
    labs(
      title = "Instrumentation Coverage Across Matrices",
      subtitle = "Bubble size = number of references; color = highest authority tier",
      x = NULL,
      y = NULL
    ) +
    theme_minimal(base_size = 12) +
    theme(
      axis.text.x = element_text(angle = 25, hjust = 1, size = 10),
      axis.text.y = element_text(size = 10),
      legend.position = "right",
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      plot.title = element_text(face = "bold", size = 14),
      plot.subtitle = element_text(size = 10, color = "gray40")
    )

  ggsave(
    file.path(OUT_DIR, "fig5_instrument_matrix.pdf"),
    p,
    width = 10,
    height = 6
  )
  ggsave(
    file.path(OUT_DIR, "fig5_instrument_matrix.png"),
    p,
    width = 10,
    height = 6,
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
      values = c(
        "1" = "#1a7a2e",
        "2" = "#2e6b8a",
        "3" = "#b8860b",
        "4" = "#cccccc"
      ),
      labels = c(
        "1" = "Tier 1",
        "2" = "Tier 2",
        "3" = "Tier 3",
        "4" = "Tier 4"
      ),
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

  ggsave(file.path(OUT_DIR, "fig6_tox_workflow.pdf"), p, width = 9, height = 5)
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

  message("── Generating Figure 5: Instrumentation × Matrix ──")
  p5 <- fig5_instrument_matrix(df)

  message("── Generating Figure 6: Toxicology Workflow ──")
  p6 <- fig6_tox_workflow(df)

  message("")
  message("All figures saved to: ", OUT_DIR, "/")

  # Return all plots invisibly
  invisible(list(fig2 = p2, fig4 = p4, fig5 = p5, fig6 = p6))
}

# Run
main()
