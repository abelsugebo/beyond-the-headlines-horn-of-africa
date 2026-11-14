"""Reproduce retrieval diagnostics without modifying baseline or original exports.
Run from repository root: python scripts/diagnose_mediacloud_v2.py
"""
import csv, gzip, hashlib, io, json, random
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'data/mediacloud/diagnostic_v2_2026-11-12'
BASE=ROOT/'data/mediacloud/2026-11-12'
DOMAINS=['regional-site-A','regional-site-B','regional-site-C']
def raw(p):
 b=p.read_bytes()
 return gzip.decompress(b) if p.suffix=='.gz' else b
def rows(p): return list(csv.DictReader(io.StringIO(raw(p).decode('utf-8-sig'))))
def save(name,obj): (RUN/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
manifest=json.loads((RUN/'download_manifest.json').read_text())
for m in manifest:
 b=raw(RUN/m['file'])
 assert len(b)==m['original_bytes'] and hashlib.sha256(b).hexdigest()==m['original_sha256'],m['label']
files={m['label']:RUN/m['file'] for m in manifest}
base={c:rows(BASE/'audit'/f'{c}_country_urls.csv.gz') for c in ['ethiopia','eritrea','sudan','somalia']}
shared=set.intersection(*[{r['id'] for r in rr} for rr in base.values()])
records={r['id']:r for r in base['ethiopia']}
suspect={i for i in shared if records[i]['media_name'] in DOMAINS}
assert len(shared)==1883 and len(suspect)==1867
expected=[str(date(2026,10,1)+timedelta(days=i)) for i in range(42)]
baseline_timeline=rows(BASE/'originals/ethiopia_country.csv')
denom={r['date']:int(r['total_count']) for r in baseline_timeline}
result={'collection_id':34412234,'language_filter':None,'start':'2026-10-01','end':'2026-11-11','days':42,'baseline_shared_ids':len(shared),'baseline_shared_suspicious_ids':len(suspect),'denominator_sum':sum(denom.values()),'queries':{}}
data={}
for key in ['negative_control','ethiopia_single','eritrea_single','ethiopia_title','eritrea_title']:
 timeline=rows(files[key+'_attention']); rr=rows(files[key+'_urls']);data[key]=rr
 assert [r['date'] for r in timeline]==expected
 assert {r['date']:int(r['total_count']) for r in timeline}==denom
 ids={r['id'] for r in rr};assert len(ids)==len(rr)
 daily=Counter(r['publish_date'] for r in rr); assert set(daily)<=set(expected)
 for r in timeline:
  n=int(r['count']);d=int(r['total_count']);assert n==daily[r['date']] and 0<=n<=d
  assert abs(float(r['ratio'])-n/d)<1e-12
 counts=Counter(r['media_name'] for r in rr)
 result['queries'][key]={'matches':len(rr),'suspicious_domain_counts':{d:counts[d] for d in DOMAINS},'shared_1883_retained':len(ids&shared),'suspicious_1867_retained':len(ids&suspect),'suspicious_ids_outside_baseline_block':len({r['id'] for r in rr if r['media_name'] in DOMAINS}-suspect)}
 if key.endswith('single'):save(key+'_first20_export_order.json',rr[:20])
assert raw(files['negative_control_urls'])==b''
for c in ['ethiopia','eritrea']:
 assert {r['id'] for r in data[c+'_title']} <= {r['id'] for r in data[c+'_single']}
 assert {r['id'] for r in data[c+'_single'] if r['media_name'] in DOMAINS}==suspect
result['single_term_id_intersection']=len({r['id'] for r in data['ethiopia_single']} & {r['id'] for r in data['eritrea_single']})
result['first20_shared_ids']=len({r['id'] for r in data['ethiopia_single'][:20]} & {r['id'] for r in data['eritrea_single'][:20]})
result['first20_domain_counts']={c:dict(Counter(r['media_name'] for r in data[c+'_single'][:20])) for c in ['ethiopia','eritrea']}
sample=[]
for domain in DOMAINS:
 pool=sorted([records[i] for i in suspect if records[i]['media_name']==domain],key=lambda r:r['id'])
 sample.extend(random.Random(20261112).sample(pool,2))
assert sample==json.loads((RUN/'evidence/stratified_sample.json').read_text())
save('other_16_shared_records.json',[records[i] for i in sorted(shared-suspect)])
save('diagnostic_results.json',result)
print(json.dumps(result,indent=2))
