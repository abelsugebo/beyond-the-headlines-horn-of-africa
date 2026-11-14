# Media Cloud retrieval diagnostic, version 2

Research date: November 12, 2026 (America/New_York). Exports retrieved November 13, 2026, 02:07–02:13 UTC. Public context: [Media Cloud diagnostic history and release decisions](MEDIACLOUD_DIAGNOSTIC_HISTORY.md) and [baseline comparative findings](MEDIACLOUD_COMPARATIVE_FINDINGS_2026-11-12.md), baseline commit `a78c38a091f11bd1ef3c8095b60095912cb0766b`.

## Conclusion and decision

The anomaly persists without Boolean OR expressions. Both literal country searches retrieve all 1,883 previously shared story IDs, including the identical 1,867-ID block from regional-site-A, regional-site-B, and regional-site-C. The impossible-term control returns zero. Documented title-only searches return no records from those three domains.

These observations disfavor an unconditional fallback that ignores every query, and show that OR expansion is not necessary for the anomaly. They do not establish the root cause. Shared extracted text or page boilerplate is a plausible explanation, but remains unverified. Selective indexing, field mapping, query execution, or retrieval problems remain possible. An unrelated-looking headline is not sufficient evidence that the indexed document lacks a country mention.

**No sources are excluded, no baseline datasets are changed, and no revised attention figures are published.** Numbers below are diagnostic query counts, not replacement estimates of substantive country coverage. Keyword matches do not demonstrate humanitarian neglect.

## Fixed settings and execution

All five searches used United States - National, collection **34412234**, the inclusive publication-date window **October 1 through November 11, 2026**, and **no language filter**. No individual source was added or removed. The negative control ran first, followed by `Ethiopia`, `Eritrea`, and two supplementary title diagnostics. The title field follows the [official query guide](https://www.mediacloud.org/documentation/query-guide). The [search guide](https://www.mediacloud.org/documentation/search-tool-guide) describes the interface and downloads.

The saved URL, timestamp, byte length, and SHA-256 of each export are in [download_manifest.json](../data/mediacloud/diagnostic_v2_2026-11-12/download_manifest.json). URL metadata exports are losslessly gzip-compressed; decompression restores the exact downloaded bytes. The zero-result URL export is preserved as its original **zero-byte file**, without an invented header. Attention CSVs are unchanged downloads. UI snapshots and a negative-control screenshot are in the evidence directory.

The interface displayed “Invalid Date” headings, while its selected-date controls, URL parameters, and all 42 exported date rows agreed on the requested window. Query labels and result URLs were checked before accepting each download. These records establish the settings used; they do not independently certify the provider's indexing completeness or date semantics beyond the exported labels.

## Exact results

| Query, executed in this order | Matching IDs / URL rows | regional-site-A | regional-site-B | regional-site-C | Original 1,883 IDs retained |
|---|---:|---:|---:|---:|---:|
| `qzvtrnplm2026` | 0 | 0 | 0 | 0 | 0 |
| `Ethiopia` | 2,258 | 792 | 660 | 415 | 1,883 |
| `Eritrea` | 2,012 | 792 | 660 | 415 | 1,883 |
| `article_title: Ethiopia` | 82 | 0 | 0 | 0 | 5 |
| `article_title: Eritrea` | 22 | 0 | 0 | 0 | 1 |

The negative control has **42 daily rows, every count and ratio equal to zero**, zero returned story IDs, and an empty URL export. Its UI displayed zero attention and no sample results. Daily denominators match the baseline and all other diagnostic searches, summing to **390,949 indexed collection records** over the window. This denominator is an index count, not an independent census of US news production.

For each literal country search, the three-domain ID set equals the baseline suspicious block exactly: no missing IDs and no additional IDs from those domains. The two literal-query ID sets intersect in **1,976** records, so the original four-country intersection of 1,883 is not the entire two-country overlap.

The first 20 rows in provider URL-export order share 18 IDs. Ethiopia's first 20 comprise 14 regional-site-A, four regional-site-C, and two usatoday.com rows; Eritrea's comprise 16 regional-site-A and four regional-site-C rows. These are preserved in the two `*_first20_export_order.json` files. They are **not** a random sample, relevance ranking, or the interface's displayed random sample. The domain census above uses all returned rows.

## Article-text review

A reproducible sample selects two IDs per suspicious domain from the original shared block: sort IDs within each domain, reset Python `random.Random(20261112)` for each stratum, then sample two. All six selections and their original metadata are preserved in `evidence/stratified_sample.json`. The first selected URL from each domain was opened through public web retrieval. Retrieval failed, and a subsequent domain/title search reported robots restrictions for all three domains. No workaround was attempted. The other three selected URLs were not individually opened after those domain-level restrictions were observed.

Consequently, all six sampled records remain **unknown** for body relevance, actual matched-term context, humanitarian/security relevance, and wire attribution. Titles suggest local crime, an obituary, restaurants, a local budget, high-school volleyball, and a football kickoff story. That is an anomaly signal, not a body-text finding. No record is coded “unrelated” merely because its text was inaccessible. Indexed full text and match offsets were not available in the exports or inspected search interface.

Two accessible comparison cases were purposively chosen from the other 16 shared IDs, rather than sampled to estimate precision:

| Case | Observed text and interpretation | Limit |
|---|---|---|
| [Guardian editorial](https://www.theguardian.com/commentisfree/2026/oct/08/the-guardian-view-on-ethiopias-return-to-conflict-civilian-catastrophe-and-a-spiralling-regional-polycrisis) | All four country names occur in the editorial's regional-conflict discussion. | Current page, not archived indexed text. |
| [TechRadar NFL viewing guide](https://www.techradar.com/how-to-watch/american-football/nfl-london-games-2026-free) | Ethiopia, Eritrea, Sudan, and Somalia occur in a long African broadcast-availability list within the article. These are incidental geographic mentions in sports-viewing information, not substantive humanitarian/security coverage. This is article content, not demonstrated navigation boilerplate. | Current headline differs from the export, indicating an updated page. The historical indexed version was not recovered. |

A third comparison URL at USNews was inaccessible and remains unclassified. See `evidence/manual_review.json` for record IDs, access outcomes, coding, and supporting URLs. No accessible comparison proves the cause of the three-domain block. Conversely, the comparison cases demonstrate why shared IDs cannot automatically be treated as erroneous matches: co-mentions can be substantive or incidental.

## What is established, and what is not

| Candidate explanation | Evidence from this run | Conclusion |
|---|---|---|
| Every query is ignored or returns a default fixed set | Nonce gives zero; literal searches differ; title searches differ | Not supported by these controls. A selective fault remains possible. |
| OR query structure alone causes the suspicious block | Both single-token queries retain the exact block | OR is not required for the observed behavior. |
| Countries are matched in article headlines on these domains | No suspicious-domain records in either title-only query | Not supported for the tested literal terms and field. |
| Countries occur in body text or extracted boilerplate | No suspicious-domain body or indexed text accessible | Unresolved; do not label boilerplate as confirmed. |
| Selective indexing/retrieval error | No matched offsets, extraction payloads, or backend diagnostics | Remains possible; cannot diagnose the internal mechanism. |
| Every shared story is a false positive | Accessible comparison cases have real textual country mentions | Blanket classification is unsupported. |

Title-only queries change the construct and reduce recall. Their counts are a diagnostic of field behavior, not corrected coverage figures. Even confirmation of boilerplate in some pages would require an explicit, consistently applied relevance rule and wider validation before removing entire sources.

## Validation and reproducibility

Run from repository root:

```sh
python scripts/diagnose_mediacloud_v2.py
```

The script verifies raw-export hashes and byte lengths, all 42 dates in order, daily denominator identity with the baseline, nonnegative counts bounded by denominators, ratios within 1e-12, unique story IDs, publication dates within the window, and exact reconciliation of each daily count to URL metadata. It checks the nonce's empty export, the baseline four-country intersection, exact suspicious-block retention, title-result ID subsets, and reproducible sample selection. Results are saved in [diagnostic_results.json](../data/mediacloud/diagnostic_v2_2026-11-12/diagnostic_results.json). All checks passed. Validation establishes internal consistency, not semantic relevance or correctness of the underlying index.

The baseline files remain at their original paths. This version adds a separate diagnostic directory, a separate script, and this report. Original dataset content is not overwritten, normalized, deduplicated, or source-filtered. `file_manifest.json` lists SHA-256 and byte lengths for the new evidence and analysis files; the download manifest additionally records hashes of decompressed original bytes.

## Remaining work and release threshold

The core nonce and single-term tests requested for this continuation are complete. The broader retrieval investigation remains open in substance; its public chronology and current release boundary are summarized in [Media Cloud diagnostic history](MEDIACLOUD_DIAGNOSTIC_HISTORY.md). Separate source-restricted reruns were not performed; this run instead provides complete per-domain ID slices of the unchanged collection, avoiding a change to the specified source universe. These slices are not represented as independent source-restricted query executions.

The critical unresolved requirement is access to the exact indexed extraction and matched-term context for suspicious IDs. A provider investigation could use the preserved IDs, query URLs, timestamps, nonce control, and title diagnostic to compare indexed payloads against publisher body text. No message to Media Cloud was sent. If such text becomes available, code direct, secondary, incidental, and unrelated country relevance separately from body/quotation/boilerplate location and humanitarian/security relevance. Obtain researcher adjudication and assess disagreement before estimating precision or revising counts.

The six restricted-domain samples and two purposive accessible comparisons cannot support a population precision estimate. Historical pages may have changed, syndication duplicates editorial material across IDs, and title-only tests cannot establish body extraction quality. Do not infer neglect, framing, or editorial intent from these keyword counts. Keep substantive attention claims on hold until relevance and retrieval uncertainties are resolved.
