#!/usr/bin/env python3
"""Reproduce structural checks and metadata diagnostics; never clean or impute counts."""
import csv, gzip, hashlib, itertools, json, math
from collections import Counter
from pathlib import Path
from validate_mediacloud_exports import validate_three

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/mediacloud/2026-11-12'
CFG = json.loads((ROOT/'config/mediacloud_attention_queries_v1.json').read_text())
COLLECTION = 'United States - National (34412234)'
LANGUAGE = 'No explicit language filter; all indexed languages in collection'

def write_csv(path, rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    out=BASE/'validated';out.mkdir(exist_ok=True)
    summaries=[]; daily=[]; audit={}; sources=[]; samples=[]; denom=None
    for country in CFG['country_queries']:
        stem=country.lower().replace(' ','_')
        rows=validate_three(BASE/'originals',country,COLLECTION,LANGUAGE,CFG)
        for kind in ('country','humanitarian','security'):
            raw=list(csv.DictReader((BASE/'originals'/f'{stem}_{kind}.csv').open()))
            for r in raw:
                assert len(r['date'])==10
                assert math.isclose(float(r['ratio']),int(r['count'])/int(r['total_count']),rel_tol=1e-9,abs_tol=1e-12)
            current=[(r['date'],r['total_count']) for r in raw]
            if denom is None:denom=current
            assert current==denom, 'Denominator drift across countries or queries'
        daily.extend(rows)
        c,h,s=[sum(r[k] for r in rows) for k in ('country_matching_articles','humanitarian_matching_articles','security_matching_articles')]
        total=sum(r['indexed_source_total_if_available'] for r in rows)
        summaries.append(dict(country=country,days=len(rows),country_matches=c,humanitarian_matches=h,security_matches=s,humanitarian_percent=round(100*h/c,5),security_percent=round(100*s/c,5),collection_matches=total,country_percent_of_collection=round(100*c/total,5),validation='STRUCTURAL_PASS; RELEVANCE_NOT_VALIDATED'))
        path=BASE/'audit'/f'{stem}_country_urls.csv.gz'
        with gzip.open(path,'rt',encoding='utf-8-sig',newline='') as f:articles=list(csv.DictReader(f))
        assert len(articles)==c
        assert len({a['id'] for a in articles})==len(articles)
        per_day=Counter(a['publish_date'] for a in articles)
        assert all(per_day[r['day_utc']]==r['country_matching_articles'] for r in rows)
        counts=Counter(a['media_name'] for a in articles)
        for source,count in counts.most_common():sources.append(dict(country=country,source=source,matches=count,percent=round(100*count/c,5)))
        audit[country]={'rows':len(articles),'languages':dict(Counter(a['language'] for a in articles)),'duplicate_title_excess':len(articles)-len({a['title'].casefold() for a in articles}),'ids':{a['id'] for a in articles},'articles':articles}
        ordered=sorted(articles,key=lambda a:a['id'])
        for a in ordered[:10]:samples.append(dict(country=country,selection='first_10_lexicographically_sorted_provider_ids',**a,review_scope='METADATA_ONLY; NOT FULL-TEXT RELEVANCE VALIDATION'))
    overlap=[]
    for a,b in itertools.combinations(audit,2):overlap.append(dict(country_a=a,country_b=b,shared_provider_ids=len(audit[a]['ids']&audit[b]['ids'])))
    common=set.intersection(*(audit[c]['ids'] for c in ['Ethiopia','Eritrea','Sudan','Somalia']))
    common_sources=Counter(a['media_name'] for a in audit['Ethiopia']['articles'] if a['id'] in common)
    diagnostic={'four_country_shared_ids':len(common),'four_country_shared_sources':dict(common_sources),'country_audits':{k:{a:b for a,b in v.items() if a not in ('ids','articles')} for k,v in audit.items()},'full_text_precision':'NOT VALIDATED','source_exclusions':'NONE','zero_imputation':False,'counts_modified':False,'all_15_daily_denominators_identical':True,'ratio_checks_pass':True,'all_five_country_metadata_exports_reconcile_by_day':True}
    write_csv(out/'daily_counts.csv',daily);write_csv(out/'comparative_keyword_matches.csv',summaries)
    write_csv(out/'source_concentration.csv',sources);write_csv(out/'country_overlap.csv',overlap);write_csv(out/'metadata_review_sample.csv',samples)
    (out/'validation_and_audit.json').write_text(json.dumps(diagnostic,indent=2)+'\n')
    manifests=[]
    for p in sorted(BASE.rglob('*')):
        if p.is_file() and p.name!='checksums.json':manifests.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (BASE/'checksums.json').write_text(json.dumps(manifests,indent=2)+'\n')
    print(json.dumps(summaries,indent=2))

if __name__=='__main__':main()
