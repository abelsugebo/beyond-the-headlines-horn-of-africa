# GDELT attention baseline v1 | Preregistered pilot protocol

**Researcher:** Abel W. Sugebo | **Specified November 12, 2026**  
**Monitoring:** October 1 00:00 UTC through November 11 23:59 UTC, 42 days.  
**Status:** Research design and automated retrieval prepared; **no measured GDELT baseline figures have yet been obtained or validated in this repository**.

## Main research question

Within GDELT's documented monitored-online-news coverage and exactly stated queries, what share of global articles mentions each of the five country cases, and what fraction of those country-matching articles also includes humanitarian-risk or security terms?

This is an **operationalized proxy for textual coverage visibility**, not a definitive measure of actual editorial attention, audience reach, burden-adjusted attention, or deliberate neglect. GDELT monitors an uneven multilingual web-news universe.

## Five main country query families (fixed before seeing results)

- Ethiopia: `(Ethiopia OR Ethiopian OR Tigray OR Amhara)`
- Eritrea: `(Eritrea OR Eritrean OR Asmara)`
- Sudan: `(Sudan OR Sudanese OR Darfur OR Kordofan)`
- South Sudan: `("South Sudan" OR "South Sudanese" OR UNMISS)`
- Somalia: `(Somalia OR Somali OR Mogadishu OR Puntland)`

These country name aliases may capture unrelated stories, miss other local terms, and overlap country cases, especially *Sudan vs South Sudan*. A post discussing cross-border flows may legitimately match two cases. Country totals must **not** be added to obtain a region-wide unique article count.

For each country, query exactly three nested topic families:
1. `country_mentions`: the country query alone.
2. `humanitarian_terms`: country query plus `(humanitarian OR refugee OR refugees OR displaced OR displacement OR hunger OR famine OR malnutrition OR drought OR flooding OR cholera)`.
3. `security_terms`: country query plus `(military OR armed OR fighting OR clashes OR troops OR insurgency OR war OR attacks)`.

These are **keywords**, not a validated machine classifier. An article can match both topic categories; shares must not sum to 100%. A sensitivity run appends `sourcelang:english` to all three queries. We must inspect multilingual coverage bias and query recall/precision.

## GDELT 2.0 measurement

Use GDELT DOC `mode=timelinevolraw`, `format=json`, `startdatetime=20261001000000`, `enddatetime=20261112000000`, `timelinesmooth=0`. Request 42 exact daily buckets. For each day return:
- `value`: reported distinct matching articles (integer)
- `norm`: total GDELT-monitored articles over the corresponding interval

Compute daily:
- `country_share_of_global_percent = 100 * country_mentions / norm`
- `humanitarian_share_of_country_percent = 100 * humanitarian_term_matches / country_mentions`
- `security_share_of_country_percent = 100 * security_term_matches / country_mentions`

For period totals use the **ratio of summed counts** across all 42 dates, not mean daily rates. These are different denominators. The `norm` in raw mode must not be used as a humanitarian burden estimate. Keep the query URLs, raw response, retrieval timestamps, exact country/time scope and checksum-worthy JSON.

GDELT's official documentation identifies `TimelineVolRaw` and the monitored `norm` field. See https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ and https://blog.gdeltproject.org/gdelt-2-0-api-now-supports-raw-result-counts/ .

## Quality gates

- Refuse an empty JSON result, non-JSON API message, invalid raw counts, repeated dates, dates outside the requested window or missing daily buckets. A missing bucket is **not evidence of zero articles**.
- Refuse mismatched monitored denominators across topic queries for the same day, or a subtopic result larger than the all-country query. This prevents silent invalid ratios.
- Persist partial raw payloads for troubleshooting, but **do not write numerical summary as a valid result** if any required query fails.
- Apply at least 3 seconds between requests and retry temporary 429/503 errors.
- Pilot Ethiopia (3 requests) first; then all five (15 requests), then English-only sensitivity. Manually review sample article matches to estimate false positives and false negatives before interpretation.
- Preserve a separate count of metadata/search candidates, **not** GDELT time-series volume, in the older `collect_gdelt_doc.py` tool. Its `artlist` endpoint is capped and cannot estimate total attention.

## Baseline interpretation

A larger GDELT country count may reflect naming, language mix, source duplication, different country sizes, type of news, geography or data-collection biases. Higher topic shares do not mean more aid or less neglect. No humanitarian-severity-normalized denominator is collected here. Claims such as 'the Horn receives less attention than crisis X relative to humanitarian need' require:

1. A separate contemporaneous comparator group selected and declared **before viewing** GDELT results, preferably similar risk and conflict levels.
2. Independent, reference-dated OCHA/IPC/UNHCR burden indicators that do not double-count displacement and food-insecurity categories.
3. Article-level manual precision checks by country and language, common query sensitivity tests, and confidence around coverage missingness.
4. A separate treatment of local vs international publication, including possible English-source bias.
5. An explicit distinction between absence of coverage and low representation in *this provider's monitored source universe*.

A defensible immediate output is 'within-GDELT relative volume and relative humanitarian-term visibility', **not** 'international media deliberately ignored these crises'.

## Execution

GitHub Actions: [GDELT attention baseline pilot](../.github/workflows/gdelt_attention_baseline.yml), choose scope Ethiopia and language all, dry_run false. Download the run artifact and examine both `validated_summary.json` and `daily_attention.csv` alongside raw responses. On query failures, the artifact has `ERROR_NOT_PUBLISHABLE.txt`, and no valid result is claimed.

Reproduce locally:

```bash
python -m unittest discover -s tests -v
python scripts/measure_gdelt_attention.py --country Ethiopia --language all --output-dir output/gdelt_ethiopia
python scripts/measure_gdelt_attention.py --country all --language all --output-dir output/gdelt_all
python scripts/measure_gdelt_attention.py --country all --language english --output-dir output/gdelt_all_english
```

The repository remains private. Live numeric GDELT outputs should be evaluated before adding them to the reviewed evidence matrix.

## Initial live pilot failure and stricter retry protocol (November 12, 2026)

GitHub Actions [run #1](https://github.com/abelsugebo/horn-africa-humanitarian-media-intelligence-2026/actions/runs/43328735373) successfully ran **30 offline tests** and then stopped on the first GDELT country volume response. The stored raw JSON returned **28 daily buckets**: **27 within the 42-day requested window, 15 absent days, and an extra bucket for November 12**, which was outside the cutoff. This is not a valid 42-day baseline. The Node.js deprecation warning was unrelated to the exit code.

The updated collector now excludes **only an observed exact-midnight boundary date equal to the exclusive end** and writes `gap_diagnostics_*.json`. When the full interval is incomplete, it retries the *same query* in 7-day bounded windows and requires every requested day, no conflicting daily count/norm on overlapping dates, and consistent topic denominators. Absent dates remain **unknown, not zero**. If the provider still has missing or contradictory coverage, the run intentionally fails with `ERROR_NOT_PUBLISHABLE.txt` and leaves raw JSON for audit. Do not publish a country percentage from an incomplete result.

This is a provider-data completeness issue, not evidence that Ethiopian or Horn crises received zero coverage on any of the missing dates. If weekly recovery remains incomplete, suspend numerical attention analysis using the DOC endpoint and design a different denominator/data source rather than weakening validation.
