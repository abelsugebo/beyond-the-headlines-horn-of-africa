#!/usr/bin/env python3
"""Sample-bounded media monitoring analysis. Never mix demo and empirical data."""
import argparse, csv, json, re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

FIELDS = ['record_id','published_date','country','source_type','source_name','title','url','primary_theme',
          'humanitarian_mentioned','cross_border','narrative_frame','underlying_source',
          'release_approved','synthetic_demo','coder_notes','actor_mentions','external_actor_mentions','external_involvement_type','claim_evidence_status','claim_attributed_to']
VALID_FLAGS = {'yes','no','unclear'}
VALID_THEMES = {'conflict','humanitarian','climate','economy','diplomacy','other'}
VALID_TYPES = {'media','government','humanitarian','social','other'}
VALID_COUNTRIES = {'Ethiopia','Eritrea','Sudan','South Sudan','Somalia','Regional','Other'}
VALID_INVOLVEMENT = {'none','diplomacy','mediation','humanitarian_support','economic_investment','security_cooperation','reported_military_support','alleged_armed_support','economic_pressure','other','unclear'}
VALID_EVIDENCE = {'official_position','independently_documented','attributed_report','contested_allegation','unverified_allegation','unclear','not_applicable'}

def canonical_url(url):
    """Strip tracking params while retaining meaningful paths/queries."""
    url = (url or '').strip()
    if not url:return ''
    parsed = urlsplit(url)
    query = [(k,v) for k,v in parse_qsl(parsed.query,keep_blank_values=True)
             if not (k.lower().startswith('utm_') or k.lower() in {'fbclid','gclid'})]
    path=parsed.path.rstrip('/') or '/'
    return urlunsplit((parsed.scheme.lower(),parsed.netloc.lower(),path,urlencode(query),''))

def validate(rows):
    errors=[]; IDs=set()
    if not rows:return ['No records were provided.']
    modes={r.get('synthetic_demo','').lower() for r in rows}
    if modes != {'true'} and modes != {'false'}:
        errors.append('Do not mix real and synthetic data or use missing synthetic_demo flags.')
    for n,r in enumerate(rows,2):
        rid=r.get('record_id','').strip()
        if not rid:errors.append(f'Row {n}: missing record_id.')
        elif rid in IDs:errors.append(f'Row {n}: duplicate record_id {rid}.')
        IDs.add(rid)
        if r.get('release_approved','').lower()!='yes':errors.append(f'Row {n}: release not approved.')
        if r.get('source_type','') not in VALID_TYPES:errors.append(f'Row {n}: invalid source_type.')
        if r.get('country','') not in VALID_COUNTRIES:errors.append(f'Row {n}: invalid country.')
        if r.get('external_involvement_type','') not in VALID_INVOLVEMENT:errors.append(f'Row {n}: invalid external_involvement_type.')
        if r.get('claim_evidence_status','') not in VALID_EVIDENCE:errors.append(f'Row {n}: invalid claim_evidence_status.')
        if (r.get('external_involvement_type') == 'alleged_armed_support' or r.get('claim_evidence_status') in {'contested_allegation','unverified_allegation'}) and not r.get('claim_attributed_to','').strip():
            errors.append(f'Row {n}: an allegation must name who made it.')
        if r.get('external_involvement_type') not in {'none','unclear'} and not r.get('external_actor_mentions','').strip():
            errors.append(f'Row {n}: external involvement requires an external actor mention.')
        if r.get('primary_theme','') not in VALID_THEMES:errors.append(f'Row {n}: invalid primary_theme.')
        for field in ('humanitarian_mentioned','cross_border'):
            if r.get(field,'') not in VALID_FLAGS:errors.append(f'Row {n}: invalid {field}.')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',r.get('published_date','')):errors.append(f'Row {n}: invalid date format.')
        if modes=={'false'} and not r.get('url','').startswith('https://'):
            errors.append(f'Row {n}: empirical record must have a public https URL.')
    return errors

def summarize(rows):
    mode='SYNTHETIC DEMONSTRATION, NOT EMPIRICAL RESEARCH' if rows[0]['synthetic_demo'].lower()=='true' else 'EMPIRICAL SAMPLE, CHECK METHODS BEFORE CITING'
    canonical=Counter(canonical_url(r['url']) for r in rows if r['url'].strip())
    by_country=Counter(r['country'] for r in rows)
    by_type=Counter(r['source_type'] for r in rows)
    by_theme=Counter(r['primary_theme'] for r in rows)
    human=Counter(r['humanitarian_mentioned'] for r in rows)
    cross=Counter(r['cross_border'] for r in rows)
    source_links=Counter((r['underlying_source'],r['source_name']) for r in rows if r['underlying_source'].strip())
    external_mentions=Counter(a.strip() for r in rows for a in r['external_actor_mentions'].split(';') if a.strip())
    involvement=Counter(r['external_involvement_type'] for r in rows)
    evidence=Counter(r['claim_evidence_status'] for r in rows)
    return {
        'status':mode, 'total_coded_records':len(rows), 'note':'Counts are sample-specific, not all media attention or causal influence.',
        'by_country':dict(sorted(by_country.items())), 'by_source_type':dict(sorted(by_type.items())),
        'by_primary_theme':dict(sorted(by_theme.items())), 'humanitarian_mentioned':dict(sorted(human.items())),
        'cross_border':dict(sorted(cross.items())),
        'by_external_actor_mention':dict(sorted(external_mentions.items())),
        'by_described_external_involvement':dict(sorted(involvement.items())),
        'by_claim_evidence_status':dict(sorted(evidence.items())),
        'distinct_nonblank_public_urls':len(canonical), 'same_url_groups_more_than_one_record':sum(v>1 for v in canonical.values()),
        'unique_upstream_to_publisher_links':len(source_links),
        'external_actor_caveat':'Mentions and attributed descriptions do NOT prove control, sponsorship, actual reach or causation.'
    },source_links

def load(path):
    with open(path,newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        missing=set(FIELDS)-set(reader.fieldnames or [])
        if missing:raise ValueError('Missing columns: '+', '.join(sorted(missing)))
        return list(reader)

def run(infile,outdir):
    rows=load(infile)
    errors=validate(rows)
    if errors:raise ValueError('Validation failed:\n'+'\n'.join(errors))
    stats,edges=summarize(rows)
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/'summary.json').write_text(json.dumps(stats,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    with (outdir/'source_relationship_edges.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['underlying_source','publisher_or_source','records_in_sample','interpretation'])
        for (upstream,publisher),count in sorted(edges.items()):
            w.writerow([upstream,publisher,count,'citation/reuse link; NOT evidence of coordination'])
    with (outdir/'theme_counts.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['primary_theme','records_in_sample','sample_size','status'])
        for theme,count in stats['by_primary_theme'].items():w.writerow([theme,count,len(rows),stats['status']])
    print('Created analysis for',len(rows),'records. Status:',stats['status'])
    return stats

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    try:run(a.input,a.output)
    except ValueError as exc:p.error(str(exc))
