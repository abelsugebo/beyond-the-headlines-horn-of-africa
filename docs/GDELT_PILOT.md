# GDELT DOC 2.0 | Manual discovery pilot

This pipeline creates **source-discovery metadata**, not verified media intelligence findings. It has not yet been run against the live API from this environment.

## Local use

    python scripts/collect_gdelt_doc.py --country "Somalia" --day 2026-11-10 --output gdelt_candidates.csv --dry-run
    python scripts/collect_gdelt_doc.py --country "Somalia" --day 2026-11-10 --output gdelt_candidates.csv

## GitHub Actions

From the repository, open **Actions**, select **Manual GDELT metadata retrieval**, click **Run workflow**, choose a country and day, then download the **gdelt-discovery-candidates** artifact. The action never commits outputs or automatically publishes anything. It requests metadata for exactly one UTC day, using one predeclared query and a 100-article result cap. If the cap is reached, subdivide query terms or time windows.

GDELT's \`seendate\` is an index timestamp, not necessarily the publication date printed on the source page. Review source titles, URLs and dates before converting candidates into coded records. GDELT coverage and language mix vary, and results cannot be compared to official statements or social-media records as if they represented the same sampling frame.

Official documentation: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/

**Status:** Code provided and offline fixture tests included. Live API call and GitHub Action execution remain unverified. Request failures should not create false research results.
