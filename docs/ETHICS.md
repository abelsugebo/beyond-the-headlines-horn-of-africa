# Publication, safety and privacy review

## Before collecting

- Work within platform terms, access controls, applicable law, and editorial standards; no unauthorized scraping or circumvention of technical controls.
- Make a source list and a retention schedule. Gather only records needed to answer the research question.
- Treat public social-media information as potentially sensitive when combined into datasets.

## Before making data public

- Remove identifiers for private citizens, witnesses, displaced persons, minors and vulnerable community members.
- Exclude direct links to live sensitive civilian movements, shelters, aid operations, safe routes or other precise locations that could facilitate harm.
- Do not publish precise real-time force positions or tactical operational details.
- Avoid sharing unreleased interviews, private correspondences, unpublished reporter notes or non-public platform escalation materials.
- Check copyright and licensing before redistributing article text, screenshots or proprietary databases. Prefer citations and metadata over copies of media.
- Keep a documented release checklist, including who approved the release and why each included field is necessary.
- Review all output CSVs, images, HTML, Git history and commit diffs. Deleting a file later does not reliably remove it from Git history.

## External relationship safeguards

- A diplomatic meeting does not demonstrate operational or clandestine proxy control.
- A government accusation of external support must identify the accuser, the accused, the date, the claim, and any on-record denial or alternative account.
- Classify independent investigative evidence within the documented scope of the source; never overstate chain of command or state responsibility.
- Avoid publishing sensitive operational geography, alleged transit routes in current use or identifiers of non-public individuals.
- Publishing a network of allegation edges can visually imply proven culpability. Always display evidence status prominently.

## Claims discipline

- A reused article or repeated quote does **not** establish coordination.
- A high volume of posts does **not** establish broad reach without platform impression data.
- A conflict event database is an independent contextual source, not automatically ground truth.
- AI-generated analysis must undergo independent source review.

## Working file policy

`data/raw/`, `data/private/`, `.env`, and local working notes are ignored in `.gitignore`. This is not sufficient as a security control: manually review staged files before upload. **No consent, participant, or active-case raw material is included in this starter.**
