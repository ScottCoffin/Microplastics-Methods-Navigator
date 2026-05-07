# Methods Navigator app

Install and run the Streamlit app from the project root:

```powershell
pip install -r methods_navigator/requirements.txt
streamlit run methods_navigator/app.py
```

## Crosswalk metadata fill

The metadata script fills `Particle Size Range`, `Key Metrics / Output`,
`Abstract`, `PDF Available in Zotero?`, and `Reviewed` in the `Crosswalk Table`
sheet. Zotero is read read-only. PDF files are converted to Markdown only when
Zotero lacks an `abstractNote`; rows without Zotero context can fall back to
the DOI/URL landing page listed in the workbook. PDF conversion is intentionally
limited to the first 5 pages and first 500 Markdown lines to control context
size and API costs.

Install optional metadata dependencies from `methods_navigator/`:

```powershell
python -m pip install -r metadata_requirements.txt
```

Common commands from `methods_navigator/`:

```powershell
# Dry-run one DOI
python fill_crosswalk_metadata.py --doi 10.1016/j.chemosphere.2022.134282

# Write one DOI to crosswalk.metadata_filled.xlsx
python fill_crosswalk_metadata.py --doi 10.1016/j.chemosphere.2022.134282 --write

# Process all rows into crosswalk.metadata_filled.xlsx
python fill_crosswalk_metadata.py --write

# Resume from crosswalk.metadata_filled.xlsx, batch size 3
python fill_crosswalk_metadata.py --resume --batch-size 3

# Resume at Excel row 42 and process the next 3 eligible rows
python fill_crosswalk_metadata.py --resume --start-row 42 --batch-size 3

# Keep processing batches of 3 until no more eligible rows remain in this run
python fill_crosswalk_metadata.py --resume --batch-size 3 --batch-loop

# Retry skipped/unreviewed rows after adding PDFs to Zotero
python fill_crosswalk_metadata.py --resume --batch-size 3 --batch-loop

# Disable DOI/URL landing-page scraping for an offline Zotero/PDF-only run
python fill_crosswalk_metadata.py --resume --batch-size 3 --skip-url-scrape

# Overwrite existing metadata fields when needed
python fill_crosswalk_metadata.py --resume --overwrite
```

`--resume` uses `crosswalk.metadata_filled.xlsx` when it exists, restricts
processing to rows where `Reviewed` is not `Yes`, and writes in place.
`--start-row` uses Excel row numbers and starts scanning from that row; explicit
`--row` selections take precedence. During a single `--batch-loop` run, rows
that fail or are skipped are not retried until the next command invocation. URL
scraping is a fallback only: Zotero
`abstractNote` is still used directly when present, and PDFs remain the next
source before DOI/URL landing pages.

The audit CSV at `metadata_cache/crosswalk_metadata_audit.csv` is append-only
across batches and runs. Delete that CSV before starting if you want a fresh
audit log for a new run.

Rows with an empty `Short Citation` are skipped before Zotero, URL, PDF, or LLM
work starts. If three rows in a row have empty `Short Citation` values, the
batch stops scanning.
