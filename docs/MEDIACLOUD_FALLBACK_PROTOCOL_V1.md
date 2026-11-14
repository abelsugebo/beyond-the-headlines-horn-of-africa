# Media Cloud Search pilot | Alternative news-attention baseline v1

**Researcher:** Abel W. Sugebo | **Status:** Prepared, **no Media Cloud data collected**  
**Period:** 2026-10-01 through 2026-11-11 inclusive, UTC.

## Why the GDELT DOC baseline is paused

The GDELT pilot runs [#1](https://github.com/abelsugebo/horn-africa-humanitarian-media-intelligence-2026/actions/runs/43328735373), [#2](https://github.com/abelsugebo/horn-africa-humanitarian-media-intelligence-2026/actions/runs/43330010030), and [#3](https://github.com/abelsugebo/horn-africa-humanitarian-media-intelligence-2026/actions/runs/43330460623) failed. All 33 offline tests passed in the later runs. Run #1 rejected an extra Nov12 bucket; run #2's raw artifact reveals mixed temporal resolution and incomplete returned coverage (e.g. 24 hourly intervals Oct1 and 11 hourly intervals Oct2) and the parser correctly rejected repeated date keys. Run #3 returned **HTTP 429 Too Many Requests**. Neither failure establishes that real news coverage was absent. Do not keep resubmitting API requests or fill absent data with zero.

## Alternative: Media Cloud Search

Media Cloud Search: https://search.mediacloud.org/ and its [official search guide](https://www.mediacloud.org/documentation/search-tool-guide) explain how to choose a fixed media collection, date range, and compare attention over time and total attention; CSV exports are available. Its media universe is defined by the sources and time spans indexed in Media Cloud, not all publications worldwide.

**First pilot:** choose one **explicitly named and recorded media collection** suitable for global or international news, and use it unchanged for all three Ethiopia queries. Record the collection name, ID if visible, source count if given, language, Media Cloud provider, retrieval date and exact three search strings. If no suitable collection is verified, do not invent one.

### Exact query families for Ethiopia

All country-mention articles:
```
(Ethiopia OR Ethiopian OR Tigray OR Amhara)
```

Humanitarian-term subset:
```
(Ethiopia OR Ethiopian OR Tigray OR Amhara) AND (humanitarian OR refugees OR refugee OR displacement OR displaced OR hunger OR famine OR malnutrition OR drought OR flooding OR cholera)
```

Security-term subset:
```
(Ethiopia OR Ethiopian OR Tigray OR Amhara) AND (military OR armed OR fighting OR clashes OR troops OR insurgency OR war OR attacks)
```

Official Media Cloud [Query Guide](https://www.mediacloud.org/documentation/query-guide) says boolean operators must be uppercase, phrases quoted, and language-specific filters such as `language:en` are available. If choosing English, append `AND language:en` to **all three** queries and record it. Do not combine results from different collections or language filters.

Use October 1 through November 11, 2026 **for all three**. Download the **Attention over time** CSV (not only the matching URL sample) for each query. Rename exported CSVs:
- `ethiopia_country.csv`
- `ethiopia_humanitarian.csv`
- `ethiopia_security.csv`

Keep these original exports privately, untouched. The offline validator handles columns `date,count` or `date,count,total_count,ratio`. Do not construct dummy data or adjust counts by hand. CSV field names may vary by Media Cloud interface version: examine the actual exports, and map their schema transparently if necessary.

### Analysis only after validation

Run:
```
python scripts/validate_mediacloud_exports.py \
  --input-dir path/to/private/mediacloud_exports \
  --country Ethiopia \
  --media-collection 'exact collection name or ID' \
  --output-dir path/to/private/validated_outputs
```

Output: 42 daily rows plus bounded ratios for humanitarian-term / all country matching and security-term / all country matching. If the Media Cloud CSV supplies monitored totals, produce the country/global-style proportion only if the denominator is consistent across three queries. A within-country ratio **does not require** a global denominator. Do not treat match percentages as evidence of deliberate neglect or subjective media value.

The validator **refuses** missing, duplicate, extra, non-integer or negative dates/counts, topic match count exceeding country count, and inconsistent daily total-count denominators. No zero imputation. The source collection metadata stays attached to each output row.

### Follow-up design

1. Inspect a small sample of matching URLs for relevance and repeated syndicated headlines. The country term alone may be incidental; humanitarian keywords may be mentioned only once.
2. Once Ethiopia succeeds, run the same three query families for the other four countries with identical media collection, language, time range, retrieval and article-precision audit.
3. Only then consider a crisis-severity matched comparator group. **Attention per source-universe share** is not burden-adjusted humanitarian neglect.
4. When building a manuscript, report separate results for the 49 original researcher-checked X posts and the Media Cloud article-volume universe. They are different selection frames.

Official documentation: https://www.mediacloud.org/documentation/search-tool-guide, https://www.mediacloud.org/documentation/query-guide, https://www.mediacloud.org/documentation/faqs .

**No Media Cloud numerical findings have been obtained yet.**
