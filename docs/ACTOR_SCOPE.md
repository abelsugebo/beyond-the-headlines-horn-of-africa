# Actor scope and interpretation safeguards | v0.2

## The unit of analysis
The **core study is the humanitarian information environment**, not a military intelligence tracking project. The core cases are **Ethiopia, Eritrea, Sudan, South Sudan, and Somalia**. Each article, official report, statement or public post has one primary `country` of subject matter; a record can mention many actors and multiple core countries.

## Core case: Eritrea
Code Eritrea as a full main-country subject, including government communications, relations with Ethiopia, refugees and displacement, Red Sea access, regional diplomacy, and humanitarian consequences. Do **not** code Eritrea automatically as a proxy actor. The existence of Ethiopia-Eritrea allegations is not proof of specific incursions or rebel sponsorship.

## External actor inclusion rule
Track **Egypt, UAE, Türkiye and Saudi Arabia** as named priority external actors if and only if a record concerns one or more of the five core country cases. Other countries (e.g., Qatar, Russia, China, United States) are added by a logged relevance decision. Neighboring **Djibouti, Kenya, Chad, Uganda, Libya** are contextual geographies when documented movement, aid, trade, diplomatic ties or displacement crosses borders. Their mentions must not inflate the count of core-country crisis records.

### Distinct categories of external involvement
- `diplomacy`: state visits, public declarations, formal alignment, multilateral forums.
- `mediation`: documented attempts to facilitate dialogue or agreements.
- `humanitarian_support`: humanitarian financing, relief operations, refugee hosting.
- `economic_investment`: infrastructure, trade, ports, finance, energy ties.
- `security_cooperation`: documented security cooperation or training, without implying combat support.
- `reported_military_support`: source-documented assistance, with precisely identified recipient and evidentiary status.
- `alleged_armed_support`: accusation of backing an armed party, **never recorded as established by default**.
- `economic_pressure`: demonstrated or specifically attributed embargo, disruption, sanctions or financing pressure.
- `other`, `none`, `unclear`.

### Evidence status (do not collapse)
- `official_position`: directly documented public statement or treaty, not independent validation of disputed factual claims in that statement.
- `independently_documented`: supported by verifiable independent investigation, limited to what that investigation actually established.
- `attributed_report`: reported by named organization or outlet, still subject to limitations.
- `contested_allegation`: specific party accuses another; includes opposing account/denial when available.
- `unverified_allegation`: claim is traceable but independent support is not established.
- `unclear`, `not_applicable`.

**Critical:** `contested_allegation` is a status of a *claim*, not a rank of certainty. A primary government's assertion is never automatically promoted to `independently_documented`. Record *who said what* and the source URL. Use separate rows for claim and denial where each has its own record.

## Evidence-first relationship records
Use `data/relationship_claims_template.csv` only for described relations among governments, coalitions and institutions. Fields include source attribution, evidence status, response/denial, and link to the humanitarian consequences. Public `scripts/analyze_relationships.py` exports **claim-bearing edges**, not a purported actual network of covert links. Do not calculate or publish a definitive proxy-war network from allegations.

## Examples illustrating editorial handling (not monitoring findings)
1. Egypt–Eritrea diplomatic meeting: `diplomacy`, `official_position`; public meeting documented, **does not prove** covert support for a specific Ethiopian armed group.
2. Türkiye mediation between Ethiopia and Somalia: `mediation`, `official_position`; a mediation role is not equivalent to a belligerent proxy relationship.
3. Sudan RSF/UAE involvement: Human Rights Watch documents evidence of contractors and UAE-linked assistance, while noting UAE denials and limits to establishing state command/control. Reflect both the documented investigation and the contested state-responsibility question without exaggeration.
4. Ethiopia–Eritrea troop-crossing allegation: attribute to Ethiopian government; include Eritrea's denial and distinguish alleged occurrence from the fact of diplomatic rupture.

## Publication guardrails
Avoid active tactical routes, exact civilian/aid-worker locations, vulnerable individuals, operational time-critical sites and raw platform handles when such details could put people at risk. Record sources and methods in private, release only safe metadata and aggregate analysis. Source-reuse edges are not covert coordination findings. No blanket claim that 'Egypt/UAE/Türkiye are proxies'.

## Research background readings (secondary sources, not coded corpus)
- Congressional Research Service (2026-11-06), *The Unfolding Conflict in Ethiopia*: https://www.everycrsreport.com/reports/IF13344.html
- UN Secretary-General statement (2026-10-10): https://ethiopia.un.org/en/324191-un-secretary-generals-statement-ethiopia
- Human Rights Watch (2026-05-25), *From Bogotá to El Fasher*: https://www.hrw.org/report/2026/05/25/from-bogota-to-el-fasher/the-uaes-role-in-the-deployment-of-colombian-fighters
- European Council on Foreign Relations (2026), *Shoring up the Red Sea*: https://ecfr.eu/article/shoring-up-the-red-sea-why-the-next-crisis-may-begin-in-the-horn-of-africa
- Security Council Report, Oct 2026 closed consultations: https://www.securitycouncilreport.org/whatsinblue/2026/10/horn-of-africa-closed-consultations.php

These readings establish relevance and prompts for further verification; they do not automatically establish the specific claims in newly collected records.
