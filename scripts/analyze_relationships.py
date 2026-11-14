#!/usr/bin/env python3
"""Validate and export *attributed relationship claims* without converting allegations to facts."""
import argparse,csv,json,re
from pathlib import Path

FIELDS=['claim_id','as_of_date','core_country','external_actor','other_actor','relationship_type','evidence_status','claim_attributed_to','source_url','response_or_denial','humanitarian_relevance','release_approved','synthetic_demo','notes']
CORE={'Ethiopia','Eritrea','Sudan','South Sudan','Somalia'}
TYPES={'diplomacy','mediation','humanitarian_support','economic_investment','security_cooperation','reported_military_support','alleged_armed_support','economic_pressure','other','unclear'}
EVIDENCE={'official_position','independently_documented','attributed_report','contested_allegation','unverified_allegation','unclear'}

def load(path):
    with path.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        missing=set(FIELDS)-set(reader.fieldnames or [])
        if missing:raise ValueError('Missing fields: '+', '.join(sorted(missing)))
        return list(reader)

def validate(rows):
    errors=[];ids=set()
    if not rows:return ['No relationship records provided.']
    flags={r.get('synthetic_demo','').lower() for r in rows}
    if flags not in ({'true'},{'false'}):errors.append('Mixed or missing synthetic_demo flags.')
    for i,r in enumerate(rows,2):
        id=r.get('claim_id','').strip()
        if not id or id in ids:errors.append(f'Row {i}: missing or duplicate claim_id')
        ids.add(id)
        if r.get('core_country','') not in CORE:errors.append(f'Row {i}: invalid core_country')
        if r.get('relationship_type','') not in TYPES:errors.append(f'Row {i}: invalid relationship_type')
        if r.get('evidence_status','') not in EVIDENCE:errors.append(f'Row {i}: invalid evidence_status')
        if r.get('release_approved','')!='yes':errors.append(f'Row {i}: release not approved')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',r.get('as_of_date','')):errors.append(f'Row {i}: invalid date')
        if not r.get('external_actor','').strip() or not r.get('other_actor','').strip():errors.append(f'Row {i}: actor missing')
        if r.get('relationship_type')=='alleged_armed_support' or r.get('evidence_status') in {'contested_allegation','unverified_allegation'}:
            if not r.get('claim_attributed_to','').strip():errors.append(f'Row {i}: attribution required for allegation')
        if flags=={'false'} and not r.get('source_url','').startswith('https://'):
            errors.append(f'Row {i}: empirical claim missing https source_url')
    return errors

def run(infile,outdir):
    rows=load(infile);e=validate(rows)
    if e:raise ValueError('Validation failed: \n'+'\n'.join(e))
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/'attributed_relationship_claims.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['core_country','external_actor','other_actor','described_relation','evidence_status','claim_attributed_to','source_url','response_or_denial','note'])
        for r in rows:
            w.writerow([r['core_country'],r['external_actor'],r['other_actor'],r['relationship_type'],r['evidence_status'],r['claim_attributed_to'],r['source_url'],r['response_or_denial'],'ATTRIBUTED CLAIM, NOT VERIFIED PROXY TIE'])
    status='SYNTHETIC DEMONSTRATION - NOT FINDINGS' if rows[0]['synthetic_demo']=='true' else 'EMPIRICAL - CHECK SOURCE AND RELEASE REVIEW'
    with (outdir/'relationship_summary.json').open('w',encoding='utf-8') as f:json.dump({'status':status,'relation_claim_records':len(rows),'warning':'Claim edges are not evidence of proven proxy control or causality.'},f,indent=2)
    print('Validated',len(rows),'attributed relationship claims:',status)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    try:run(a.input,a.output)
    except ValueError as exc:p.error(str(exc))
