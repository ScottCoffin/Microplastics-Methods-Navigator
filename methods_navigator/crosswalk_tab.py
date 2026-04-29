"""Interactive crosswalk table tab for the MP Methods Navigator."""

from __future__ import annotations

import re
from urllib.parse import urlparse

import pandas as pd
import streamlit as st


DEFAULT_COLUMNS = [
    "#",
    "Short Citation",
    "Year",
    "Primary Domain",
    "Document Type",
    "Priority Tier",
    "Instrumentation Tags",
    "Matrix Tags",
    "Key Notes",
    "Open Link",
]

NON_TOPIC_COLUMNS = {
    "#",
    "Short Citation",
    "Year",
    "Full Title",
    "DOI/URL",
    "Open Link",
    "Primary Domain",
    "Primary Focus",
    "Document Type",
    "Priority Tier",
    "Instrumentation Tags",
    "Matrix Tags",
    "Key Notes",
    "Scope",
    "Status",
    "Particle Size Range",
    "Key Metrics / Output",
    "tier_num",
}

TIER_STYLES = {
    1: "background-color: #dff3e4; color: #134e22; font-weight: 600;",
    2: "background-color: #dcecf4; color: #164760; font-weight: 600;",
    3: "background-color: #f5edcf; color: #594814; font-weight: 600;",
    4: "background-color: #eeeeee; color: #4f4f4f;",
}

DOMAIN_STYLES = {
    "monitoring": "background-color: #e3f2fd; color: #174a69;",
    "toxicology": "background-color: #f4e4f7; color: #5a2d65;",
    "both": "background-color: #e9f5df; color: #31551d;",
    "cross-cutting": "background-color: #f3eee3; color: #5b4a25;",
}

STATUS_STYLES = {
    "final": "background-color: #e7f4e4; color: #24501c;",
    "published": "background-color: #e7f4e4; color: #24501c;",
    "draft": "background-color: #fff3cd; color: #5c4700;",
    "in development": "background-color: #fff3cd; color: #5c4700;",
}

NORMATIVE_DOC_TYPES = {
    "Consensus Standard",
    "Government SOP",
    "Legislation",
    "Regulation / Regulatory Decision",
    "Regulatory Definition",
    "Regulatory-Adopted Method",
}
INSTITUTIONAL_DOC_TYPES = {
    "Agency Technical Report",
    "International Guidance",
    "Scientific Advisory Report",
}
METHOD_DOC_TYPES = {
    "Certified Reference Material",
    "Interlaboratory Study",
    "Method / Protocol",
}


def render_crosswalk_tab(df):
    """Render an interactive, filterable table for the crosswalk workbook."""
    table_df = prepare_table(df)
    filtered_df = render_filters(table_df)

    left, right = st.columns([2, 1])
    with left:
        st.markdown("### Crosswalk")
        st.caption(f"{len(filtered_df)} of {len(table_df)} references")
    with right:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "Export filtered CSV",
            csv,
            file_name="crosswalk_filtered.csv",
            mime="text/csv",
            key="crosswalk_export",
            width="stretch",
        )

    selected_columns = render_column_picker(filtered_df)
    display_df = filtered_df[selected_columns].copy()

    column_config = {}
    if "Open Link" in display_df.columns:
        column_config["Open Link"] = st.column_config.LinkColumn(
            "Open Link",
            display_text="Open",
            width="small",
        )

    if "Key Notes" in display_df.columns:
        column_config["Key Notes"] = st.column_config.TextColumn(
            "Key Notes",
            width="large",
        )

    if "Full Title" in display_df.columns:
        column_config["Full Title"] = st.column_config.TextColumn(
            "Full Title",
            width="large",
        )

    st.dataframe(
        style_crosswalk(display_df),
        column_config=column_config,
        hide_index=True,
        width="stretch",
        height=650,
    )


def prepare_table(df):
    table_df = df.copy()
    table_df["Open Link"] = table_df["DOI/URL"].apply(normalize_link)
    if "Year" in table_df.columns:
        table_df["Year"] = pd.to_numeric(table_df["Year"], errors="coerce").astype("Int64")
    return table_df


def render_filters(df):
    filtered = df.copy()

    filter_left, filter_mid, filter_right = st.columns([1.2, 1, 1])

    with filter_left:
        search = st.text_input("Search", key="crosswalk_search")
        selected_tiers = st.multiselect(
            "Authority Tier",
            options=[1, 2, 3, 4],
            default=[1, 2, 3, 4],
            format_func=lambda value: f"Tier {value}",
            key="crosswalk_tier",
        )
        selected_topics = st.multiselect(
            "Topic Coverage",
            options=topic_columns(df),
            key="crosswalk_topics",
        )

    with filter_mid:
        selected_domains = st.multiselect(
            "Primary Domain",
            options=sorted(non_empty_values(df, "Primary Domain")),
            key="crosswalk_domain",
        )
        selected_doc_types = st.multiselect(
            "Document Type",
            options=sorted(non_empty_values(df, "Document Type")),
            key="crosswalk_doc_type",
        )
        linked_only = st.checkbox(
            "Has web link",
            value=False,
            key="crosswalk_linked_only",
        )

    with filter_right:
        selected_matrices = st.multiselect(
            "Matrix Tags",
            options=split_tag_options(df, "Matrix Tags"),
            key="crosswalk_matrix_tags",
        )
        selected_instruments = st.multiselect(
            "Instrumentation Tags",
            options=split_tag_options(df, "Instrumentation Tags"),
            key="crosswalk_instrument_tags",
        )
        year_range = year_filter(df)

    if search:
        haystack = filtered.fillna("").astype(str).agg(" ".join, axis=1)
        filtered = filtered[haystack.str.contains(search, case=False, regex=False)]

    if selected_tiers:
        filtered = filtered[filtered["tier_num"].isin(selected_tiers)]

    if selected_domains:
        filtered = filtered[filtered["Primary Domain"].isin(selected_domains)]

    if selected_doc_types:
        filtered = filtered[filtered["Document Type"].isin(selected_doc_types)]

    if selected_matrices:
        filtered = filter_tag_column(filtered, "Matrix Tags", selected_matrices)

    if selected_instruments:
        filtered = filter_tag_column(
            filtered, "Instrumentation Tags", selected_instruments
        )

    if selected_topics:
        topic_mask = pd.Series(False, index=filtered.index)
        for column in selected_topics:
            topic_mask = topic_mask | has_topic_value(filtered[column])
        filtered = filtered[topic_mask]

    if year_range and "Year" in filtered.columns:
        start, end = year_range
        filtered = filtered[
            filtered["Year"].isna()
            | filtered["Year"].between(start, end, inclusive="both")
        ]

    if linked_only:
        filtered = filtered[filtered["Open Link"].notna()]

    return filtered.sort_values(
        by=["tier_num", "Year", "Short Citation"],
        ascending=[True, False, True],
        na_position="last",
    )


def render_column_picker(df):
    selectable_columns = [
        col for col in df.columns if col != "tier_num"
    ]
    default_columns = [
        col for col in DEFAULT_COLUMNS if col in selectable_columns
    ]
    selected = st.multiselect(
        "Columns",
        options=selectable_columns,
        default=default_columns,
        key="crosswalk_columns",
    )
    if selected:
        return selected
    return default_columns or selectable_columns


def normalize_link(value):
    if pd.isna(value):
        return None

    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return None

    match = re.search(r"https?://[^\s,;]+", text)
    if match:
        return match.group(0)

    if text.lower().startswith("www."):
        return f"https://{text}"

    if text.lower().startswith("doi:"):
        return f"https://doi.org/{text[4:].strip()}"

    if re.match(r"^10\.\S+/\S+$", text):
        return f"https://doi.org/{text}"

    parsed = urlparse(text)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return text

    return None


def non_empty_values(df, column):
    if column not in df.columns:
        return []
    return [
        value
        for value in df[column].dropna().astype(str).unique().tolist()
        if value.strip()
    ]


def split_tag_options(df, column):
    values = set()
    if column not in df.columns:
        return []
    for cell in df[column].dropna().astype(str):
        for part in cell.split(";"):
            tag = part.strip()
            if tag and tag.lower() not in {"nan", "none"}:
                values.add(tag)
    return sorted(values)


def filter_tag_column(df, column, selected_tags):
    if column not in df.columns:
        return df
    pattern = "|".join(re.escape(tag) for tag in selected_tags)
    return df[df[column].astype(str).str.contains(pattern, case=False, na=False)]


def topic_columns(df):
    columns = []
    for column in df.columns:
        if column in NON_TOPIC_COLUMNS:
            continue
        if has_topic_value(df[column]).any():
            columns.append(column)
    return columns


def has_topic_value(series):
    return series.notna() & ~series.astype(str).str.strip().isin(["", "0", "nan", "None"])


def year_filter(df):
    if "Year" not in df.columns:
        return None

    years = pd.to_numeric(df["Year"], errors="coerce").dropna()
    if years.empty:
        return None

    min_year = int(years.min())
    max_year = int(years.max())
    if min_year == max_year:
        st.caption(f"Year: {min_year}")
        return (min_year, max_year)

    return st.slider(
        "Year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        key="crosswalk_year",
    )


def style_crosswalk(display_df):
    return display_df.style.apply(style_row, axis=1)


def style_row(row):
    styles = [""] * len(row)
    for idx, column in enumerate(row.index):
        value = row[column]
        if column == "Priority Tier":
            styles[idx] = TIER_STYLES.get(extract_tier(value), "")
        elif column == "Primary Domain":
            styles[idx] = DOMAIN_STYLES.get(str(value).strip().lower(), "")
        elif column == "Document Type":
            styles[idx] = doc_type_style(value)
        elif column == "Status":
            styles[idx] = status_style(value)
    return styles


def extract_tier(value):
    if pd.isna(value):
        return None
    match = re.search(r"Tier\s*(\d)", str(value))
    if not match:
        return None
    return int(match.group(1))


def doc_type_style(value):
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if text in NORMATIVE_DOC_TYPES:
        return "background-color: #dff3e4; color: #134e22;"
    if text in INSTITUTIONAL_DOC_TYPES:
        return "background-color: #dcecf4; color: #164760;"
    if text in METHOD_DOC_TYPES:
        return "background-color: #f5edcf; color: #594814;"
    if text in {"Framework", "Review", "Database / Tool", "Support Tool"}:
        return "background-color: #eeeeee; color: #4f4f4f;"
    return ""


def status_style(value):
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    return STATUS_STYLES.get(text, "")
