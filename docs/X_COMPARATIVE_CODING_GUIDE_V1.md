# X candidate comparative coding guide | v1.0
**Date:** 2026-11-12 | **Researcher:** Abel W. Sugebo | **Status:** the author reports manually checking all 49 unique original X posts (50 country-case entries). No separate second-researcher re-authentication or second-coder reliability review is documented. Frame and temporality coding remains provisional; engagement metrics are unverified.

## Purpose and permitted inference
The unit is one **country-case observation** of a candidate X post. The same status ID can appear as two case observations; it must be deduplicated in *unique post counts* but not automatically in country-case coding. The current sample is ten purposefully selected candidates per country. A post can refer to another country and still be included because of the original case-specific collection strategy. Do not infer platform-wide source diversity, volumes, sentiment, neglect, coordination, or reach from this convenience sample.

The background 24 official/news documents are a separate corpus with a different sampling design. Do not sum or aggregate them with the X sample.

## Operational code definitions

### Publisher class
- `government`: authorial account of a national state official, government body or minister; includes official allegations, not their downstream reporting.
- `multilateral`: UN institutional or AU account primarily acting in political/diplomatic, rights-mandate or peacekeeping capacity (UNMISS, UN Secretary-General Spokesperson, HRC and AU).
- `humanitarian`: an agency or leading official posting primarily in an aid, health, refugee, food-security, disaster or humanitarian operational capacity (WFP, OCHA, UNHCR, IFRC, UNICEF, WHO, MSF). This is a **role-based analytical classification**, not a statement that the institution is politically neutral.
- `news_media`: newsroom or journalistic outlet, including reports that *quote* SAF, RSF, government or humanitarian claims. A quoted actor does not become the publisher.
- `commentary_civil`: public analyst, conflict-monitor account, think tank, journalist using a personal account, or civil-society organization. Posts may still contain self-reported programme outputs.

### Primary frame (one provisional label)
- `security`: battle, armed-force capabilities, alleged military support, sovereignty threat or internal armed contest is primary.
- `humanitarian`: displacement, civilian protection, hunger, illness, humanitarian funding or response is primary.
- `climate`: drought, flooding, agriculture/climate exposure or climate finance is primary.
- `diplomacy`: ceasefire/mediation demands, bilateral talks, multilateral statements or conflict prevention through diplomacy is primary.
- `governance`: elections, political legitimacy, institutional appointment, government claims about assessment methodology or governance of public services is primary.
- `historical`: principal content is retrospective historical sovereignty or earlier civilian harm. Such an item is **not** a current incident.

Frames are about **what the selected post foregrounds**, not proof of its factual claims. Coders should read the actual post before promotion. The same record can include secondary themes that are not coded in this one-label matrix; a later multi-label pass should retain these separately.

### Humanitarian temporality
- `none`: no substantive humanitarian impact is discussed in the post, even if the linked report has such details.
- `current_reported`: present/past-period consequences are asserted or reported; may remain unverified.
- `current_estimate`: estimate for currently affected/in need, with assessment uncertainty; not census.
- `current_need`: situation, needs or service constraints described contemporaneously without audited incident-level evidence.
- `future_risk`: potential escalation or future civilian impacts, not observed casualties.
- `forecast`: explicit projection for a future reference period, including IPC phases or expected flooding.
- `planned_response`: announced allocation, target or planned assistance, not proof of delivery.
- `funding_requirement`: prospective agency resource requirement or shortfall, not an expense or disbursement.
- `preparedness_risk`: preventive health or climate service action addressing risk, not necessarily observed outbreak.
- `historical_only`: earlier-period civilian experiences are cited; not a 2026 incident.
Temporality codes deliberately represent different concepts. Do not sum them as one burden or treat a forecast as an observed toll.

### Cross-border and external actors
- `cross_border_provisional` means cross-border linkage is *described or alleged* in the selected record; it does not mean actual migration or military movement is independently confirmed.
- `attribution_caution` records the core boundary of evidentiary certainty.
- `reused_statistic_id` connects repeated numerical claims, while `shared_event_id` connects reports about a potential common incident. Neither proves news organizations relied on each other.
- `upstream_source_id` tracks a post's principal source document, institutional statement, or traceable source root. Repeating the same upstream means **not independent evidence**, not necessarily coordinated amplification.

### Verification
- `original_x_content_verified=no`: in this dataset, this means no separate second-researcher re-authentication of the complete live post is documented. It does **not** mean the author did not inspect the original post; the author reports manually checking all 49 unique statuses (50 country-case entries), as recorded in the attestation below.
- `engagement_metrics_verified=no`: engagement figures supplied during collection were not independently verified and are not suitable for reach comparisons.
- `upstream_review_status`: qualification concerning supporting documents, not a validation flag for the X post.
- `human_coder_reviewed=no`: no second coder independently reviewed the primary-frame and humanitarian-temporality assignments; those labels remain provisional. This is separate from the author's manual check of the original posts.
- `candidate_only=yes`: the posts were purposively selected and are not a representative platform sample. This label does not mean the author failed to inspect the posts.

## Key source-dependence tests

1. **Cross-country same post**: Ethiopia ETH2-010 and Eritrea ERI-009 use the same Addis Standard X status. Two case lenses, one original post.
2. **Same underlying report**: SSD-004 and SSD-010 both draw on the OCHA October 2026 snapshot. SOM-002 and SOM-009 draw on the September IPC projected food-security figures. SOM-005 and SOM-006 refer to one COP31 presidential appearance.
3. **Repeated number, distinct actions**: ETH2-005 estimated up to 50k Moyale arrivals; ETH2-006 repeats that estimated number while announcing a distinct CERF allocation.
4. **Same incident not necessarily same source**: ETH2-004 and ETH2-007 discuss a reported camp attack from Reuters and WHO-source chains, with differing uncorroborated details.
5. **Contested foreign backing**: SUD-008 and ERI-010 include claims involving foreign actors, but do not substantiate military sponsorship or a proxy relationship.

## Recommended manual adjudication

For each post, inspect original URL and attached context; store a timestamp and minimal audit log. Have a second coder independently assign primary frame and humanitarian temporality. Resolve disagreements by written rule: identify the *post's own leading claim*, avoid importing context from linked sources, and preserve original attribution/uncertainty. Keep evidence for the original claimed post, linked source, and coder judgment separate. Review all posts rated historical-only, reported/unverified military allegations, or involving a potentially sensitive civilian location before any public version.

## Citation and ethics
The exact review is a **private research working set**. Public dissemination should use minimal quoted excerpts, links to the original public post and primary source, aggregate frames only after human adjudication, and remove personal identifiers, active military positions, or potentially sensitive civilian site details. Keep exact source timestamp, collection limitations, language limitations and clear source provenance in the final methodology.

## Rebuild
```bash
python scripts/build_five_country_x_matrix.py
python -m unittest tests.test_five_country_x_matrix
```
The tests verify internal consistency, **not the truth of contested events or the authenticity of original X posts**.

## Researcher X-post verification attestation (November 12, 2026)

The researcher explicitly stated: **“I have checked each X posts. don't worry.”** This is an author attestation covering the **49 unique original X statuses** underlying 50 country-case entries. The exact per-post check steps were not itemized in the public record. The public validation summary records 49 author-attested manual post checks and 50 country-case entries. This attestation is distinct from (1) a separate second-researcher re-authentication of the original post and (2) independent second-coder review of the analytical labels; neither is documented. Engagement metrics remain unverified. The existence and manual inspection of a post do not establish the truth of its claims, disputed casualty figures, foreign military allegations, or the representativeness of the purposive sample. Re-checking every link is not a default next step.
