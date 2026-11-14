# Research protocol (draft v0.2)

## Research questions

1. How do selected humanitarian institutions, national governments, media organizations and prominent public actors describe overlapping emergencies in Ethiopia, Eritrea, Sudan, South Sudan and Somalia?
2. Within the defined monitoring sources, how does the balance of security, humanitarian, climate, economic and diplomatic frames vary by country and over time?
3. Which sources are original, and which refer to the same upstream report or statement?
4. How often do selected accounts link conflict, displacement, access restrictions and economic or climate shocks across borders?
5. How do coverage and claims involving Egypt, UAE, Türkiye, Saudi Arabia and evidence-led external actors relate to core-country humanitarian issues, and with what evidence status?
6. What do two carefully chosen OSINT case reconstructions add beyond media summaries?

## Scope and denominators

- **Core countries:** Ethiopia, **Eritrea**, Sudan, South Sudan and Somalia.
- **External-actor overlay:** Egypt, UAE, Türkiye, Saudi Arabia; Qatar, Russia, China and others added if primary-source relevance is shown. **These are not classified as proxies by default.** See `ACTOR_SCOPE.md`.
- **Window:** 2026-10-01 to 2026-11-11 inclusive. Preserve each source's own time zone and convert dates cautiously.
- **Units:** An individual article, public statement, official report, or public social post. An article and its syndications may be separate records but share an `underlying_source` ID.
- **Sampling:** Document queries, URLs, filters, language restrictions, and exact collection cutoff. Do not represent a convenience sample as the complete information ecosystem.
- **Targets:** First a reproducible source inventory; then approximately 35–55 human-coded items across five core cases and source categories for the Friday brief. Larger retrieval totals can be descriptive only, subject to source API/data access.

## Candidate source strata

1. UN and humanitarian agencies (WHO, UN OCHA, UNHCR, IOM, WFP, UNICEF)
2. Official government and regional statements (ministries, IGAD, AU)
3. International and African media (with transparent list and time window)
4. External actor official statements and independently reported relations, ONLY when they concern core humanitarian/conflict cases
5. Selected public social-media voices (prioritize verified institutional accounts and public figures; avoid exposing vulnerable individuals)
6. Conflict-context data (such as ACLED) and publicly verifiable geospatial sources

Log selection/exclusion reasons. Record language and translation method separately in the private working file. DO NOT pool counts from sources with radically different retrieval coverage without stratification.

## Core analysis

- Calculate **counts within monitored sample**, not universal media attention.
- Deduplicate by canonical source URL; flag syndicated copies separately. Keep original URL and retrieval date privately.
- Codes use one **primary theme** with secondary themes recorded in the notes or expanded codebook; two coders or a documented recheck is preferred for disputed cases.
- Map upstream source citations using `underlying_source`. This is a provenance network, not a coordinated-inauthentic-behavior allegation.
- Map external actor **mentions** separately from relationship **claims**. An actor mention is not evidence of influence. State/armed-party support claims require named attribution, evidence status, and available response or denial.
- Do not describe data as demonstrating a proxy network unless individual relationships are independently established; distinguish diplomacy, mediation and allegations.
- Show numerators, denominators, and missingness for every percentage.

## OSINT case study protocol

Avoid expanding to tactical military surveillance. Select cases for humanitarian relevance, access, displacement and public accountability, not for military operational utility.

1. Define the event, minimum necessary claims, and date window.
2. Recover original official and independent materials with publication dates and source provenance.
3. Build a chronology, distinguishing **event date** from **posting date**.
4. Where necessary, use imagery, archives, geolocation or satellite data to assess assertions, noting independent confirmation and uncertainty.
5. Consult available humanitarian-access and civilian-impact records; do not imply direct causality from simultaneous developments.
6. Perform redaction and sensitivity review before public release. Do not reveal precise current routes, shelters, vulnerable civilians' locations, or operational troop positions.

## Falsification / negative findings

The project must be able to conclude that no consistent cross-country framing pattern is visible, that a sampled story is typical of coverage, or that an alleged information flow cannot be traced. Unproven hypotheses are not transformed into findings.

## Disclosure thresholds

Keep item-level evidence private when exposing it could enable persecution, doxxing, re-identification, retaliation or military targeting. Share aggregate statistics and reproducible methods when raw rows cannot safely be released. Document missing data, social-platform access limits, translation uncertainty, and editorial decisions.
