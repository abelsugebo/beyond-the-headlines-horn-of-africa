# Beyond the Headlines: methodology and resources

Methodology, code and aggregate data behind the Inform Africa investigation
[Beyond the Headlines: How Competing Narratives Obscure Humanitarian Crises in the Horn of Africa](https://informafrica.net/2026/11/14/beyond-the-headlines-how-competing-narratives-obscure-humanitarian-crises-in-the-horn-of-africa/)
by Abel W. Sugebo, published November 14, 2026.

Research period: October 1 to November 11, 2026. Cases: Ethiopia, Eritrea, Sudan, South Sudan and Somalia.

## What is here

| Path | Contents |
|---|---|
| `docs/PROTOCOL.md`, `docs/CODEBOOK.md`, `docs/ACTOR_SCOPE.md` | Research protocol, coding scheme and rules for recording external actors |
| `docs/X_COMPARATIVE_CODING_GUIDE_V1.md` | How the 49 unique X posts (50 country-case entries) were manually checked by the author, coded, and bounded; no second-researcher re-authentication or second-coder review is documented |
| `docs/MEDIACLOUD_COMPARATIVE_FINDINGS_2026-11-12.md` | The Media Cloud retrieval analysis and quality audit |
| `docs/MEDIACLOUD_RETRIEVAL_DIAGNOSTIC_V2_2026-11-12.md` | Follow-up diagnostic: control term, single-word and title-only searches |
| `docs/MEDIACLOUD_DIAGNOSTIC_HISTORY.md` | Public chronology, interpretation and release decisions for the Media Cloud retrieval investigation |
| `docs/ATTENTION_BASELINE_PROTOCOL_V1.md`, `docs/MEDIACLOUD_FALLBACK_PROTOCOL_V1.md`, `docs/GDELT_PILOT.md`, `docs/COLLECTION_QUERIES.md` | Attention-measurement protocols and the queries used |
| `docs/ETHICS.md` | Safety, privacy and publication rules |
| `docs/LICENSING.md` | Exact scope of the repository's mixed code, documentation and data licences |
| `config/` | Exact query definitions |
| `scripts/`, `tests/` | Analysis and validation code, with unit tests |
| `data/mediacloud/timelines/` | The 15 daily attention-over-time exports (42 days each; counts only) |
| `data/mediacloud/validated/`, `data/mediacloud/diagnostic_v2/` | Aggregate validation outputs and diagnostic results |
| `data/analysis/` | Aggregate composition of the X sample and shared-source groups |
| `data/*_template.csv`, `examples/` | Blank data schemas and a synthetic demo |

## What is not here, and why

This repository follows the project's own ethics rules, so it leaves out:

- the text, links and account handles of the individual X posts reviewed;
- story-level Media Cloud exports (headlines and URLs of third-party articles);
- working notes and the source-discovery records, which carry provisional codes.

The three U.S. regional news domains in the shared block are labelled
`regional-site-A`, `regional-site-B` and `regional-site-C`. Some documents refer
to files that are held privately for these reasons. Researchers who need them
for verification can contact Inform Africa through https://informafrica.net.

Scripts that read the withheld files (for example `build_five_country_x_matrix.py`)
are included for transparency but will not run without them.

## Key limits

- The author reports manually checking all 49 unique X posts (50 country-case entries). No separate second-researcher re-authentication or second-coder reliability review is documented; frame labels remain provisional. The posts were selected purposively, are not representative, and support no claims about platform-wide prevalence or reach. Engagement metrics were not independently verified.
- Media Cloud keyword counts are not validated measures of substantive coverage. No country ranking should be derived from the files here.
- Collection used Media Cloud's United States - National collection (ID 34412234).

## Run the tests

```
pip install -r requirements.txt
python -m unittest discover -s tests
```

## Licence and citation

Source code in `scripts/` and `tests/` is released under the MIT License (see `LICENSE`). Project-authored documentation, query configurations, templates, synthetic examples and curated aggregate outputs are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The licences do not relicense third-party source material. See `docs/LICENSING.md` for exact scope.

Please cite the article and this repository together; see `CITATION.cff`. The citation metadata omits a single repository-wide licence because the release uses mixed licensing.

AI-assisted tools supported code preparation, data processing and drafting.
The author is responsible for source selection, verification and conclusions.
