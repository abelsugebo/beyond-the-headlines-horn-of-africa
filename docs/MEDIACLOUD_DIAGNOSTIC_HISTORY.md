# Media Cloud retrieval diagnostic: public history and decisions

**Project:** Beyond the Headlines: How Competing Narratives Obscure Humanitarian Crises in the Horn of Africa  
**Research window:** October 1-November 11, 2026  
**Collection:** United States - National, Media Cloud collection 34412234

This note gives the public, reproducible account of the retrieval-quality investigation. It summarizes evidence and decisions needed to understand the public reports; it does not reproduce private working discussions or internal coordination notes.

## 1. Initial comparative audit

The initial comparative audit found **1,883 exact story IDs shared** across the Ethiopia, Eritrea, Sudan and Somalia country exports. Of those, **1,867 IDs** came from three U.S. regional-news domains, anonymized in the public release as regional-site-A, regional-site-B and regional-site-C.

The shared block raised a retrieval-precision question. Headline metadata alone could not establish whether the country terms appeared in article bodies, incidental references, page boilerplate or extracted text. The original exports and baseline counts were preserved; no source was removed and no corrected attention ranking was produced.

See [Media Cloud comparative findings](MEDIACLOUD_COMPARATIVE_FINDINGS_2026-11-12.md).

## 2. Follow-up diagnostic controls

The follow-up diagnostic used the same collection, date window and no-language-filter setting. It ran an impossible-term negative control first, then literal single-term searches and title-only diagnostics.

| Query | Matching records | Shared 1,883 IDs retained | Records from the three anonymized domains |
|---|---:|---:|---:|
| qzvtrnplm2026 | 0 | 0 | 0 |
| Ethiopia | 2,258 | 1,883 | 1,867 |
| Eritrea | 2,012 | 1,883 | 1,867 |
| article_title: Ethiopia | 82 | 5 | 0 |
| article_title: Eritrea | 22 | 1 | 0 |

The negative control returning zero argues against a simple explanation in which every query is ignored and returns a fixed default set. The identical block in the two single-term searches shows that Boolean OR expansion is not required for the anomaly. The title-only results show different field behavior, but they do not establish what was present in the indexed article bodies.

## 3. What remains unresolved

The exact indexed full text, extracted payloads and matched-term offsets for the three domains were not available for inspection. Public retrieval attempts were blocked by publisher access restrictions. As a result:

- the root cause of the shared block is **not established**;
- the sampled records whose bodies could not be accessed remain **unknown**, not confirmed false positives;
- incidental mentions, page boilerplate, extraction artifacts, selective indexing and retrieval problems remain possible explanations;
- the diagnostic does not provide a defensible estimate of substantive media-attention coverage.

See [Media Cloud retrieval diagnostic v2](MEDIACLOUD_RETRIEVAL_DIAGNOSTIC_V2_2026-11-12.md) for exact methods, checks, evidence and limitations.

## 4. Decisions and release boundary

The project has **not** excluded sources, altered original baseline datasets, or published revised attention figures on the basis of this anomaly. Keyword-match counts are not treated as validated measures of humanitarian coverage, editorial intent, audience exposure or humanitarian need. No country ranking or claim of media neglect should be inferred from them.

Any future correction requires access to the indexed text or equivalent provider evidence, a documented relevance rule, a sufficiently broad human review, and a reproducible audit. Until then, preserve the original exports and keep substantive attention comparisons on hold.

## 5. Reproducibility

- [Baseline comparative findings](MEDIACLOUD_COMPARATIVE_FINDINGS_2026-11-12.md)
- [Follow-up diagnostic report](MEDIACLOUD_RETRIEVAL_DIAGNOSTIC_V2_2026-11-12.md)
- [Diagnostic results JSON](../data/mediacloud/diagnostic_v2/diagnostic_results.json)
- [Diagnostic script](../scripts/diagnose_mediacloud_v2.py)
