# Layered media collection queries | v0.2

**Collection window:** October 1–November 11, 2026 inclusive for the main report, captured with the retrieval datetime, timezone, language, search parameters, platform and pagination. Historical sources outside the window are context references and must not be mixed into within-window coverage statistics.

**Primary denominator:** Items about a humanitarian or conflict development in **Ethiopia / Eritrea / Sudan / South Sudan / Somalia**. Secondary external-actor tags require a named relationship to one of those cases. Count results per stratum before combining; don't compare search-result volumes across languages, APIs or platforms as equal global coverage.

## Layer 1: Five core countries
Construct each daily monitored query using the subject plus humanitarian/conflict context; record the exact syntax accepted by the service.

| Main case | Core search concepts (adapt syntax to each API) |
|---|---|
| Ethiopia | Ethiopia OR Tigray OR Amhara OR Afar OR Oromia AND displacement OR humanitarian access OR conflict OR food security |
| Eritrea | Eritrea OR Asmara OR Assab AND Ethiopia OR Tigray OR refugees OR border OR Red Sea access |
| Sudan | Sudan OR Darfur OR El Fasher OR Kordofan AND displacement OR humanitarian aid OR food insecurity OR armed conflict |
| South Sudan | South Sudan OR Juba AND elections OR displacement OR refugee returns OR civil conflict OR humanitarian access |
| Somalia | Somalia OR Mogadishu AND drought OR flooding OR El Niño OR food insecurity OR conflict |

Parenthesize explicitly in actual queries to avoid unintended AND/OR behavior; the table records concepts, not copy-paste API syntax.

## Layer 2: External actor overlay (link required)
Query on one core case and one external actor simultaneously, then code relationship type and status from the actual source. Example **search concepts**, not proof of relations:

- `(Egypt OR Cairo) AND (Ethiopia OR Eritrea OR Sudan OR Somalia) AND (Nile OR GERD OR Red Sea OR security OR diplomacy OR humanitarian)`
- `(UAE OR "United Arab Emirates" OR Abu Dhabi) AND (Sudan OR Darfur OR Ethiopia OR Somalia) AND (RSF OR humanitarian OR finance OR logistics OR allegations)`
- `(Türkiye OR Turkey OR Ankara) AND (Ethiopia OR Somalia OR Sudan OR Eritrea) AND (mediation OR security OR aid OR port)`
- `("Saudi Arabia" OR Riyadh OR Jeddah) AND (Sudan OR Eritrea OR Somalia OR Ethiopia) AND (mediation OR Red Sea OR humanitarian)`
- Add Qatar, Russia, China or other states only following evidence-led inclusion and note the expanded denominator.

## Layer 3: Regional systems, not a generic war keyword list
- Humanitarian access and cross-border displacement
- Red Sea ports, corridors, import and transport costs
- Climate hazards (drought, forecasts for flood risk) and food systems
- Sudan's war and refugee arrivals into host countries
- Diplomacy, mediation and externally alleged support to armed parties

## Sampling and inclusion
1. Retrieve links and metadata from official sources, news databases or permitted public platforms. No circumvention or noncompliant scraping.
2. Deduplicate using canonical URL, then group syndication or attributed upstream reports separately.
3. Apply source-type and country strata. Preserve `language`, authoring organization and collection query in a private source log.
4. Human-code a manageable, predeclared item sample. Every external-support claim requires a traceable speaker and precise status in the actor-claims ledger.
5. Calculate within-stratum counts and confidence limitations. Compare humanitarian visibility and narrative framing without asserting causation from association.
6. Log searches yielding zero results; avoid selecting only controversial items for publication.

## Safety-first redaction
Release only metadata approved by an explicit case review. Do not publish raw vulnerable-person account IDs, sensitive civilian locations, ongoing aid logistics, or unverified claims as if true.
