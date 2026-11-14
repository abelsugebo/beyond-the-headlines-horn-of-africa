#!/usr/bin/env python3
"""Validate Media Cloud attention-over-time CSV exports; no network access.

Original exports should be preserved privately. This helper never imputes zeros.
"""
import argparse
import csv
import json
import re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "mediacloud_attention_queries_v1.json"
TYPES = ("country", "humanitarian", "security")
OUTPUT_COLUMNS = ["day_utc", "country", "media_collection", "language_scope",
                  "country_matching_articles", "humanitarian_matching_articles",
                  "security_matching_articles", "indexed_source_total_if_available",
                  "humanitarian_percent_of_country_articles",
                  "security_percent_of_country_articles",
                  "country_percent_of_source_collection_if_available"]

class ExportValidationError(ValueError):
    pass

def exact_integer(v, field):
    s = str(v).strip()
    if not re.fullmatch(r"\d+", s):
        raise ExportValidationError(f"{field}: expected nonnegative integer, got {v!r}")
    return int(s)

def parse_day(v):
    try:
        return date.fromisoformat(str(v).strip()[:10])
    except (ValueError, TypeError):
        raise ExportValidationError("Invalid ISO date: " + str(v))

def read_export(path, start, end):
    with Path(path).open(encoding="utf-8-sig", newline="") as h:
        reader = csv.DictReader(h)
        fields = reader.fieldnames or []
        if "date" not in fields or "count" not in fields:
            raise ExportValidationError(f"{path}: expected date,count columns. Got {fields}")
        has_total = "total_count" in fields
        rows = {}
        for item in reader:
            d = parse_day(item["date"])
            if not start <= d < end:
                raise ExportValidationError(f"{path}: out-of-window date {d}")
            if d in rows:
                raise ExportValidationError(f"{path}: repeated daily date {d}")
            n = exact_integer(item["count"], "count")
            tot = exact_integer(item["total_count"], "total_count") if has_total and item["total_count"] not in (None, "") else None
            if tot == 0:
                raise ExportValidationError("Global monitored denominator cannot be zero")
            if tot is not None and n > tot:
                raise ExportValidationError("Match exceeds monitored total")
            rows[d] = (n, tot)
    expected = {start + timedelta(days=i) for i in range((end-start).days)}
    missing = sorted(expected - set(rows))
    if missing:
        raise ExportValidationError(
            f"{path}: {len(missing)} missing dates: {[str(x) for x in missing]}. "
            "Missing is not zero. Inspect the provider export."
        )
    return rows

def validate_three(directory, country, collection, language, cfg):
    if country not in cfg["country_queries"]:
        raise ExportValidationError("Unknown country")
    if not collection.strip():
        raise ExportValidationError("A documented Media Cloud collection name or ID is required")
    start = date.fromisoformat(cfg["monitoring_start_utc"])
    end = date.fromisoformat(cfg["monitoring_end_exclusive_utc"])
    stem = country.lower().replace(" ", "_")
    data = {kind: read_export(Path(directory) / f"{stem}_{kind}.csv", start, end)
            for kind in TYPES}
    out = []
    for d in sorted(data["country"]):
        c, c_tot = data["country"][d]
        h, h_tot = data["humanitarian"][d]
        s, s_tot = data["security"][d]
        totals = [x for x in (c_tot, h_tot, s_tot) if x is not None]
        if len(set(totals)) > 1:
            raise ExportValidationError(f"{d}: inconsistent monitored totals across query exports")
        if h > c or s > c:
            raise ExportValidationError(f"{d}: topic subset exceeds country universe")
        total = totals[0] if len(totals) == 3 else None
        out.append(dict(zip(OUTPUT_COLUMNS, [
            d.isoformat(), country, collection, language, c, h, s,
            total if total is not None else "",
            round(100*h/c, 5) if c else "",
            round(100*s/c, 5) if c else "",
            round(100*c/total, 5) if total is not None else ""
        ])))
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", type=Path, required=True)
    p.add_argument("--country", required=True)
    p.add_argument("--media-collection", required=True)
    p.add_argument("--language", default="recorded_by_researcher")
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    try:
        result = validate_three(args.input_dir, args.country, args.media_collection, args.language, cfg)
    except (ExportValidationError, OSError, KeyError) as err:
        p.exit(2, f"INVALID OR INCOMPLETE MEDIA CLOUD EXPORT: {err}\n")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir/"daily_counts.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(result)
    c = sum(r["country_matching_articles"] for r in result)
    h = sum(r["humanitarian_matching_articles"] for r in result)
    s = sum(r["security_matching_articles"] for r in result)
    valid_global = all(r["indexed_source_total_if_available"] != "" for r in result)
    total = sum(r["indexed_source_total_if_available"] for r in result) if valid_global else None
    summary = {
        "country": args.country, "media_collection": args.media_collection,
        "language_scope": args.language, "window": [cfg["monitoring_start_utc"], cfg["monitoring_end_exclusive_utc"]],
        "complete_days": len(result), "country_matching_articles": c,
        "humanitarian_matching_articles": h, "security_matching_articles": s,
        "humanitarian_percent_of_country_articles": round(100*h/c, 5) if c else None,
        "security_percent_of_country_articles": round(100*s/c, 5) if c else None,
        "country_percent_of_collection": round(100*c/total, 5) if total else None,
        "provider": "Media Cloud Search CSV exports; source collection and query audits required",
        "source_precision_review": "NOT YET DONE",
        "status": "INTERNALLY VALIDATED EXPORT, NOT A FINDING OF NEGLECT",
        "warning": "Overlapping topic searches; no combined shares or population inference."
    }
    (args.output_dir/"validated_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
