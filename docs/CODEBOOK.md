# Media-monitoring codebook v0.2

One record = one document/post. `records_template.csv` contains the full column set. For real analyses, collect records reproducibly and preserve collection timestamp/queries in private source logs.

| Field | Rule |
|---|---|
| `record_id` | Stable unique ID (not a user's handle). |
| `published_date` | YYYY-MM-DD of original item; do not substitute collection time. |
| `country` | `Ethiopia`, `Eritrea`, `Sudan`, `South Sudan`, `Somalia`, `Regional`, `Other`. Use main country of focus. |
| `source_type` | `media`, `government`, `humanitarian`, `social`, `other`. |
| `source_name` | Public institution/outlet, not vulnerable person ID. |
| `title` | Brief title or neutral description; do not redistribute copyrighted articles. |
| `url` | Original public record URL; blanks allowed only in synthetic examples. |
| `primary_theme` | `conflict`, `humanitarian`, `climate`, `economy`, `diplomacy`, `other`. Pick dominant frame with evidence. |
| `humanitarian_mentioned` | `yes`, `no`, `unclear`. `yes` if substantive reference to civilians, aid, displacement, health, food security or access; a passing generic mention should be coded carefully. |
| `cross_border` | `yes`, `no`, `unclear`. Explicitly references links between at least two countries. |
| `narrative_frame` | Short, descriptive coded phrase, not an accusation. e.g., `security-first`, `civilian-impact`, `resource-gap`, `climate-shock`, `mixed`, `unclear`. |
| `underlying_source` | Canonical public upstream report/statement identifier, when observed; blank when unknown. |
| `actor_mentions` | Semicolon-separated publicly identifiable entities mentioned; do not include private individual handles. |
| `external_actor_mentions` | Semicolon-separated controlled country tags: `Egypt`, `UAE`, `Türkiye`, `Saudi Arabia`, and contextual states when documented. A mere mention is not proof of action. |
| `external_involvement_type` | `none`, `diplomacy`, `mediation`, `humanitarian_support`, `economic_investment`, `security_cooperation`, `reported_military_support`, `alleged_armed_support`, `economic_pressure`, `other`, `unclear`. One dominant *described* involvement, not a factual finding. |
| `claim_evidence_status` | `official_position`, `independently_documented`, `attributed_report`, `contested_allegation`, `unverified_allegation`, `unclear`, `not_applicable`. |
| `claim_attributed_to` | Named speaker/outlet behind an external support allegation; required for `alleged_armed_support` and any `*_allegation` evidence status. |
| `release_approved` | `yes` or `no`. Must be `yes` for rows exported into public analysis. |
| `synthetic_demo` | `true` for invented test examples; `false` for genuine source records. Never mix them. |
| `coder_notes` | Short evidence-based rationale, redacted for public release. |

**Coding decisions:** Use `unclear` when evidence is insufficient; do not infer intent, coordination, algorithmic amplification, or actual audience reach. Maintain a separate private adjudication log for disagreement. The network edges indicate observed `underlying_source` reuse only.

**Relation-level evidence:** `data/relationship_claims_template.csv` logs who allegedly did what, to whom, and on what basis. Use it for relationship analysis; do not infer external backing merely from the `external_actor_mentions` field. For conflicting claims, preserve both perspectives as separately attributed entries.
