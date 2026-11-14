#!/usr/bin/env python3
"""Download GDELT DOC 2.0 article METADATA for one country and one UTC day."""
import argparse, csv, json, re, sys
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

QUERIES = {
    "Ethiopia": '(Ethiopia OR Tigray) (humanitarian OR conflict OR displacement)',
    "Eritrea": '(Eritrea OR Asmara) (Ethiopia OR refugees OR conflict OR border)',
    "Sudan": '(Sudan OR Darfur OR Kordofan) (humanitarian OR displacement OR conflict)',
    "South Sudan": '"South Sudan" (elections OR displacement OR humanitarian OR conflict)',
    "Somalia": '(Somalia OR Mogadishu) (drought OR flood OR humanitarian OR conflict)',
}
FIELDS = ["query_country","day_utc","query","retrieval_utc","title","url",
          "domain","language","sourcecountry","gdelt_seen_utc","review_status","request_url"]

def make_url(country, day, maxrecords=100):
    if country not in QUERIES: raise ValueError("Unknown country")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}",day): raise ValueError("Use YYYY-MM-DD")
    d = date.fromisoformat(day)
    if d > datetime.now(timezone.utc).date(): raise ValueError("Future day")
    if not 1 <= maxrecords <= 250: raise ValueError("maxrecords must be 1..250")
    q = {"query":QUERIES[country],"mode":"artlist","format":"json","sort":"datedesc",
         "maxrecords":maxrecords,"startdatetime":d.strftime("%Y%m%d")+"000000",
         "enddatetime":(d+timedelta(days=1)).strftime("%Y%m%d")+"000000"}
    return "https://api.gdeltproject.org/api/v2/doc/doc?"+urlencode(q)

def convert(payload, country, day, url):
    articles=payload.get("articles") or []
    if not isinstance(articles,list): raise ValueError("Unexpected articles format")
    timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows=[]; seen=set()
    for article in articles:
        link=article.get("url","")
        if not link.startswith(("https://","http://")) or link in seen: continue
        seen.add(link)
        rows.append({"query_country":country,"day_utc":day,"query":QUERIES[country],
          "retrieval_utc":timestamp,"title":article.get("title",""),"url":link,
          "domain":article.get("domain",""),"language":article.get("language",""),
          "sourcecountry":article.get("sourcecountry",""),
          "gdelt_seen_utc":article.get("seendate",""),
          "review_status":"discovery_candidate_not_verified","request_url":url})
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--country",required=True,choices=sorted(QUERIES))
    p.add_argument("--day",required=True)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--maxrecords",type=int,default=100)
    p.add_argument("--dry-run",action="store_true")
    a=p.parse_args()
    try:
        url=make_url(a.country,a.day,a.maxrecords)
        if a.dry_run:
            print(url);return 0
        req=Request(url,headers={"User-Agent":"HornHumanitarianMediaResearch/0.1"})
        with urlopen(req,timeout=35) as response:
            if "json" not in response.headers.get("Content-Type","").lower():
                raise ValueError("Non-JSON response; inspect service and query")
            payload=json.loads(response.read().decode("utf-8"))
        rows=convert(payload,a.country,a.day,url)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
        print(json.dumps({"count":len(rows),"file":str(a.output),
          "capped_possible":len(rows)>=a.maxrecords,
          "status":"DISCOVERY CANDIDATES ONLY, NOT CODED FINDINGS"}))
        return 0
    except (ValueError,HTTPError,URLError,TimeoutError) as exc:
        print("No findings created: "+str(exc),file=sys.stderr);return 2

if __name__=="__main__": raise SystemExit(main())
