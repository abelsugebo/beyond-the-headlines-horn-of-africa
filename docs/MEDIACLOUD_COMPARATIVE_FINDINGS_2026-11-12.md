# Media Cloud attention export and comparative quality audit

**Decision: all 15 timelines pass structural validation, but substantive media-attention comparisons are on hold because relevance is not validated.** These are provider keyword-match counts, not verified counts of humanitarian or security reporting. Nothing here establishes humanitarian neglect, editorial intent, audience exposure, or crisis severity.

## Fixed acquisition scope

- Publication dates: **October 1 through November 11, 2026, inclusive**, 42 calendar dates. Export date labels are retained unchanged. The project uses UTC date labels; the interface did not independently specify its publication-date timezone, so timezone equivalence is not established.
- Provider: Media Cloud Search, `onlinenews-mediacloud`, interface v3.2.3.
- Collection: **United States - National**, ID **34412234**, 246 listed sources at retrieval. Membership CSV is archived. This is a named collection, not a census of US national journalism. It includes regional newspapers, sports sources and the UK Guardian. The collection notes say Guardian UK replaced Guardian US in September 2024.
- Language: **no explicit language filter**, unchanged for every query. English query terms do not make the corpus English-only. Exported provider language labels include non-English records; these are automated labels, not independently verified language coding.
- Retrieval session: November 12, 2026 (ET). Original browser download identities and accepted search URLs are retained in the acquisition records. Files contain no credentials.
- Exact queries: frozen `config/mediacloud_attention_queries_v1.json`; the user-specified Ethiopia strings were used verbatim. No source exclusions or additional language restrictions were introduced.

The Ethiopia pilot's three exports passed the existing validator before the four-country extension began. Scaling tested reproducibility and comparative data quality; it did not certify semantic precision. All primary searches retained the same collection and date settings.

## Retrieved keyword matches

The percentages below use **the sum of topic matches divided by the sum of country matches**, not the mean of daily percentages. Humanitarian and security sets overlap and must not be added. Countries overlap too.

| Query family | All matches | Humanitarian matches | Humanitarian / all | Security matches | Security / all |
|---|---:|---:|---:|---:|---:|
| Ethiopia | 2,398 | 168 | 7.01% | 2,231 | 93.04% |
| Eritrea | 2,021 | 75 | 3.71% | 1,990 | 98.47% |
| Sudan | 2,508 | 309 | 12.32% | 2,395 | 95.49% |
| South Sudan | 133 | 43 | 32.33% | 99 | 74.44% |
| Somalia | 3,276 | 367 | 11.20% | 2,644 | 80.71% |

The common exported collection denominator sums to **390,949 indexed stories** across the window. Daily denominators match across all 15 exports. That denominator is the provider's indexed collection universe, not all US news production, readership, or a humanitarian-need baseline. Numerical differences in this table are not a defensible ranking of crisis attention while the relevance problem below remains unresolved.

## What the quality audit found

**A large shared source block dominates four country searches.** The Ethiopia, Eritrea, Sudan and Somalia country exports share 1,883 exact provider story IDs. Of these, **1,867** are from three domains: `regional-site-A` (792), `regional-site-B` (660), and `regional-site-C` (415). These same 1,867 records account for 77.86% of Ethiopia's all-query matches and 92.38% of Eritrea's. They also account for 83.68% of the Ethiopia security subset (1,867 / 2,231).

The metadata includes US football, volleyball, baseball and local-news titles, such as “Two Blackshirts ruled out of Nebraska's game at Rutgers.” A deterministic audit sample selects the first ten lexicographically sorted provider IDs per country and preserves title, date, domain and URL for inspection. The Ethiopia sample includes local playground spending, vitamin C advice, volleyball and baseball headlines. This is strong evidence of a retrieval-precision concern, but a headline alone cannot establish absence of a country term in the body.

Possible causes include incidental mentions, page boilerplate, extraction artifacts, or query/index behavior. **The cause is not confirmed.** One attempted direct publisher retrieval was inaccessible; no full-text precision estimate is claimed. The provider's displayed random sample of ten stories included relevant-looking crisis headlines, but did not reveal how much of the complete export consisted of these unrelated-looking records. The complete URL exports therefore provide an essential diagnostic beyond the on-screen sample.

**Sudan and South Sudan are not independent cases under these searches.** All **133** South Sudan country-export IDs also appear in the Sudan country export. This follows the broad Sudan term's potential to match South Sudan; results must not be summed or treated as mutually exclusive country coverage. No unapproved exclusion of South Sudan was added.

**Syndication and repeat titles matter.** Exact case-insensitive title repetition produces excess rows of 161 (Ethiopia), 77 (Eritrea), 251 (Sudan), 66 (South Sudan), and 294 (Somalia). These are diagnostic title repetitions, not proven duplicate reporting or coordination. Multiple domains carry the same Ethiopia health-system headline in the visible sample. Primary counts remain provider story counts, without deduplication by title, wire origin, or editorial event.

**Language and collection coverage are bounded.** The five country exports contain provider language labels beyond English, including Spanish. The archived collection's New York Times note explicitly cautions that paywall-limited ingestion is not representative of that outlet's full coverage. A collection membership snapshot does not prove continuous or complete ingestion from every source throughout all 42 days.

## Validation and preservation

- Fifteen original Attention Over Time CSVs are byte-preserved under `data/mediacloud/2026-11-12/originals/`; the provider schema is `date,count,total_count,ratio`, so no column mapping was needed.
- All 630 input daily records pass expected-date, uniqueness, nonnegative integer, nonzero denominator and ratio checks. No missing-day zero filling, trimming, count editing, source removal or deduplication occurred.
- Topic counts never exceed the corresponding country count. All daily collection denominators agree across all countries and topics.
- Five complete country URL exports reconcile with their attention timelines **on every publication date**, with unique provider IDs. An additional Ethiopia security URL export is archived for diagnosis.
- URL CSVs are losslessly gzip-compressed; decompressed bytes match the downloaded originals. Hashes and byte lengths provide provenance. These are article metadata, not archived full article bodies.
- One attempted Somalia baseline download still referred to the prior South Sudan security query. It was quarantined as `excluded/stale_south_sudan_security.csv`; the corrected Somalia baseline was downloaded only after its submitted URL and dialog matched Somalia. The stale file is excluded from every metric.
- The interface showed cosmetic “Invalid Date” headings while its date-picker buttons, submitted URL and all CSV rows confirmed the requested dates. This anomaly is recorded rather than silently ignored.
- Existing eight Media Cloud validator tests pass. The new run script checks all real exports, validates ratios, checks cross-country denominators, reconciles URL exports by date, and reproduces the diagnostic tables.

Reproduce from the repository root:

```bash
python -m unittest discover -s tests -p 'test_mediacloud_exports.py' -v
python scripts/analyze_mediacloud_run.py
```

## Interpretation and next research decision

These data support an auditable statement about what the specified queries retrieved. They do **not** yet support claims that security reporting displaced humanitarian reporting, that Eritrea received less meaningful attention, or that any country was neglected. Broad terms can match diaspora, migration, sport, politics, historical references, or incidental text. Humanitarian and security keywords do not identify dominant frames, article prominence, sentiment, actual civilian outcomes or audience attention.

Before manuscript-level comparison, inspect indexed text for a stratified sample from the three anomalous domains, plus other sources, and identify why records match. Then explicitly approve a revised design if warranted: a consistently applied source exclusion, a verified headline/body restriction, or a coded relevant-article sample. Any revised analysis must be separately versioned and retain this unchanged baseline. Removing those domains now would be a substantive source-universe change and is **not** done here.

The 49 researcher-checked X posts remain a separate purposive dataset; they are not pooled with Media Cloud. Any later neglect hypothesis also needs a defensible comparison or severity baseline and independent content coding.

## Release scope

