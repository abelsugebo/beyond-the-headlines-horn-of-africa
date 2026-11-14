#!/usr/bin/env python3
"""Reproducible, conservative GDELT DOC timeline volume baseline.

GDELT query volumes are article-term matches, NOT the world's entire media.
Run manual pilot:
  python scripts/measure_gdelt_attention.py --country Ethiopia --language all --output-dir output/gdelt_ethiopia
Run all five only after validating pilot:
  python scripts/measure_gdelt_attention.py --country all --language all --output-dir output/gdelt_all
No numerical output is published unless the full specified query set succeeds.
"""
import argparse
import csv
import json
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "gdelt_attention_queries_v1.json"
API = "https://api.gdeltproject.org/api/v2/doc/doc"
MODES = ("country_mentions", "humanitarian_terms", "security_terms")
CSV_FIELDS = ("country", "day_utc", "language_scope", "country_article_count",
              "humanitarian_term_article_count", "security_term_article_count",
              "global_monitored_articles", "country_share_of_global_percent",
              "humanitarian_share_of_country_percent", "security_share_of_country_percent",
              "retrieved_utc", "query_version")

class DataValidationError(ValueError):
    pass

def iso_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def utc_date(value):
    """GDELT timeline labels may be YYYYMMDD[T]hhmmssZ or ISO-8601."""
    s = str(value).strip()
    if re.match(r"^\d{8}", s):
        return date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    if re.match(r"^\d{4}-\d\d-\d\d", s):
        return date.fromisoformat(s[:10])
    raise DataValidationError("Invalid GDELT date: " + s)

def build_query(cfg, country, mode, language):
    if country not in cfg["countries"] or mode not in MODES:
        raise ValueError("Invalid country or topic mode")
    base = cfg["countries"][country]
    sub = cfg["topic_queries"].get(mode)
    query = base + (" " + sub if sub else "")
    if language == "english":
        query += " sourcelang:english"
    elif language != "all":
        raise ValueError("Language must be all or english")
    return query

def make_url(cfg, country, mode, language, start_override=None, end_override=None):
    start = start_override or date.fromisoformat(cfg["monitoring_start_utc"])
    end = end_override or date.fromisoformat(cfg["monitoring_end_exclusive_utc"])
    if end <= start or end > datetime.now(timezone.utc).date() + timedelta(days=1):
        raise DataValidationError("Invalid or future window")
    query = build_query(cfg, country, mode, language)
    return API + "?" + urlencode({
        "query": query, "mode": "timelinevolraw", "format": "json",
        "startdatetime": start.strftime("%Y%m%d") + "000000",
        "enddatetime": end.strftime("%Y%m%d") + "000000",
        "timelinesmooth": "0",
    })

def parse_payload(payload, start, end, require_complete=True):
    """Parse unsmoothed GDELT daily raw volumes without imputing any absent dates.

    GDELT may emit an inclusive end-date bucket even when ENDDATETIME is
    midnight exclusive. Exclude that entire extra day, but record/report its
    existence in the collection log. Missing dates are never treated as zero.
    """
    series = payload.get("timeline")
    if not isinstance(series, list) or len(series) != 1:
        raise DataValidationError("Expected exactly one timeline series")
    points = series[0].get("data")
    if not isinstance(points, list) or not points:
        raise DataValidationError("Empty/malformed timeline. Zero cannot be inferred.")
    days = {}
    for p in points:
        d = utc_date(p.get("date"))
        # GDELT has been observed to emit a complete date bucket at midnight
        # on the requested exclusive end date. Never count that extra day.
        if d == end and str(p.get("date", "")).endswith("T000000Z"):
            continue
        if not (start <= d < end):
            raise DataValidationError("Out-of-window GDELT interval: " + str(d))
        if d in days:
            raise DataValidationError("Non-daily or repeated timeline interval: " + str(d))
        count, norm = p.get("value"), p.get("norm")
        if isinstance(count, bool) or not isinstance(count, (int, float)) or count < 0 or int(count) != count:
            raise DataValidationError("Raw matching count must be a nonnegative integer")
        if isinstance(norm, bool) or not isinstance(norm, (int, float)) or norm <= 0 or int(norm) != norm:
            raise DataValidationError("Global monitored denominator must be a positive integer")
        days[d] = (int(count), int(norm))
    expected = {start + timedelta(days=i) for i in range((end-start).days)}
    if require_complete and set(days) != expected:
        missing = sorted(expected - set(days))
        raise DataValidationError(
            f"Incomplete daily timeline: {len(days)}/{len(expected)} days; "
            f"missing {len(missing)}: {[str(d) for d in missing]}. "
            "Missing GDELT buckets cannot be assumed to mean zero news."
        )
    return days

def build_gap_report(initial, start, end):
    """Inspectable coverage diagnostics, including extra exclusive boundary bucket."""
    points = (initial.get("timeline") or [{}])[0].get("data") or []
    dates = [utc_date(p.get("date")) for p in points]
    expected = {start + timedelta(days=i) for i in range((end-start).days)}
    observed = set(d for d in dates if start <= d < end)
    return {
        "requested_days": len(expected),
        "observed_in_window_days": len(observed),
        "missing_dates": [d.isoformat() for d in sorted(expected - observed)],
        "out_of_window_dates": [d.isoformat() for d in sorted(set(dates)-expected)],
        "note": "Missing days are NOT zero-coverage days. Endpoint may return the exclusive end date."
    }

def recover_by_week(cfg, country, mode, language, start, end, initial, raw_dir, gap_seconds):
    """Retry incomplete long-range response in fixed seven-day windows.

    When a date appears in both responses, values *and* denominators must
    agree. If any date is absent or inconsistent after retry, fail closed.
    """
    initial_days = parse_payload(initial, start, end, require_complete=False)
    reconstructed = {}
    segment_start = start
    while segment_start < end:
        segment_end = min(segment_start + timedelta(days=7), end)
        time.sleep(gap_seconds)
        url = make_url(cfg, country, mode, language, segment_start, segment_end)
        segment = fetch_json(url)
        slug = country.lower().replace(" ", "_")
        out = raw_dir / f"{slug}_{mode}_{language}_{segment_start}_{segment_end}.json"
        out.write_text(json.dumps({
            "retrieved_utc": iso_now(), "request_url": url, "payload": segment
        }, indent=2) + "\n", encoding="utf-8")
        pieces = parse_payload(segment, segment_start, segment_end, require_complete=False)
        for day, result in pieces.items():
            if day in reconstructed and reconstructed[day] != result:
                raise DataValidationError("Weekly intervals disagree on date " + str(day))
            reconstructed[day] = result
        segment_start = segment_end
    expected = {start + timedelta(days=i) for i in range((end-start).days)}
    if set(reconstructed) != expected:
        missing = sorted(expected - set(reconstructed))
        raise DataValidationError(
            f"Weekly backfill incomplete for {country}/{mode}: "
            f"{len(reconstructed)}/{len(expected)} days; "
            f"missing: {[str(d) for d in missing]}; no zeros imputed."
        )
    disagreements = sorted(d for d in initial_days
                           if d in reconstructed and initial_days[d] != reconstructed[d])
    if disagreements:
        raise DataValidationError(
            "GDELT full-window and weekly-window counts or denominators disagree on "
            + str([str(d) for d in disagreements])
            + "; no headline metrics can be generated."
        )
    return reconstructed

# GDELT asks clients to send at most one request every 5 seconds per IP.
# GitHub-hosted runners share IPs, so pace conservatively and back off hard.
MIN_REQUEST_INTERVAL = 6.0
THROTTLE_CODES = (429, 503)
_last_request_at = [0.0]

class ThrottledError(RuntimeError):
    pass

def _pace():
    wait = MIN_REQUEST_INTERVAL - (time.monotonic() - _last_request_at[0])
    if wait > 0:
        time.sleep(wait)
    _last_request_at[0] = time.monotonic()

def _retry_after(error):
    headers = getattr(error, "headers", None)
    value = headers.get("Retry-After") if headers else None
    try:
        return max(0.0, float(value)) if value is not None else None
    except ValueError:
        return None

def fetch_json(url, attempts=6):
    for i in range(attempts):
        _pace()
        try:
            req = Request(url, headers={"User-Agent": "InformAfricaResearch-GDELTPilot/1.0 (research; no scraping)"})
            with urlopen(req, timeout=60) as response:
                content_type = response.headers.get("Content-Type", "").lower()
                body = response.read(5_000_000)
            if "json" not in content_type:
                text = body[:500].decode("utf-8", "replace").lower()
                if "limit requests" in text or "too many" in text:
                    raise ThrottledError("GDELT plain-text throttle response")
                raise DataValidationError("Unexpected response type (query rejection): " + text[:200])
            return json.loads(body.decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, ThrottledError) as e:
            code = getattr(e, "code", None)
            if code in (400, 401, 403, 404, 422):
                raise
            if i == attempts - 1:
                raise
            throttled = code in THROTTLE_CODES or isinstance(e, ThrottledError)
            delay = _retry_after(e) if code in THROTTLE_CODES else None
            if delay is None:
                delay = min(180, 15 * (2 ** i)) if throttled else min(30, 3 * (2 ** i))
            print(f"Retry {i + 1}/{attempts - 1} in {delay:.0f}s after: {e}", file=sys.stderr)
            time.sleep(delay)
    raise RuntimeError("Unreachable retry loop")

def ratios(counts, country):
    dates = set(counts["country_mentions"])
    records = []
    for day in sorted(dates):
        allcount, norm = counts["country_mentions"][day]
        hum, hnorm = counts["humanitarian_terms"][day]
        sec, snorm = counts["security_terms"][day]
        if (norm, norm) != (hnorm, snorm):
            raise DataValidationError("Global GDELT daily norm differs by query: " + str(day))
        if hum > allcount or sec > allcount:
            raise DataValidationError("Subtopic count exceeds all-country count: " + str(day))
        records.append((day, allcount, hum, sec, norm))
    return records

def to_row(country, language, stamp, version, day, count, hum, sec, norm):
    return dict(zip(CSV_FIELDS, [
        country, day.isoformat(), language, count, hum, sec, norm,
        round(100 * count / norm, 8),
        round(100 * hum / count, 5) if count else "",
        round(100 * sec / count, 5) if count else "",
        stamp, version,
    ]))

def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as output:
        w = csv.DictWriter(output, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)

def main(argv=None):
    global MIN_REQUEST_INTERVAL
    p = argparse.ArgumentParser()
    p.add_argument("--country", default="Ethiopia")
    p.add_argument("--language", default="all", choices=("all", "english"))
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--min-request-gap", type=float, default=MIN_REQUEST_INTERVAL)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args(argv)
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    countries = list(cfg["countries"]) if a.country == "all" else [a.country]
    if any(country not in cfg["countries"] for country in countries) or a.min_request_gap < 0:
        p.error("Invalid country or negative request gap")
    MIN_REQUEST_INTERVAL = max(a.min_request_gap, 5.0)  # never below GDELT's stated limit
    start = date.fromisoformat(cfg["monitoring_start_utc"])
    end = date.fromisoformat(cfg["monitoring_end_exclusive_utc"])
    a.output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = a.output_dir / "raw"
    plans = [{ "country": country, "mode": mode,
               "url": make_url(cfg, country, mode, a.language)}
             for country in countries for mode in MODES]
    (a.output_dir / "request_plan.json").write_text(
        json.dumps({"queries": plans, "dry_run": a.dry_run,
                    "measurement_state": "NOT MEASURED" if a.dry_run else "PLANNED"}, indent=2) + "\n",
        encoding="utf-8")
    if a.dry_run:
        print(json.dumps({"status": "REQUEST PLAN ONLY; NO COUNTS MEASURED", "requests": len(plans)}))
        return 0
    raw_dir.mkdir(exist_ok=True)
    stamp = iso_now()
    all_rows = []
    summaries = []
    try:
        for ci, country in enumerate(countries):
            data = {}
            for mode in MODES:
                plan = next(x for x in plans if x["country"] == country and x["mode"] == mode)
                if data or ci:
                    time.sleep(a.min_request_gap)
                payload = fetch_json(plan["url"])
                (raw_dir / f"{country.lower().replace(' ', '_')}_{mode}_{a.language}.json").write_text(
                    json.dumps({"retrieved_utc": iso_now(), "request_url": plan["url"], "payload": payload}, indent=2) + "\n",
                    encoding="utf-8")
                diag = build_gap_report(payload, start, end)
                slug = country.lower().replace(" ", "_")
                (a.output_dir / f"gap_diagnostics_{slug}_{mode}_{a.language}.json").write_text(
                    json.dumps(diag, indent=2) + "\n", encoding="utf-8")
                try:
                    data[mode] = parse_payload(payload, start, end)
                except DataValidationError as error:
                    if "Incomplete daily timeline" not in str(error):
                        raise
                    data[mode] = recover_by_week(
                        cfg, country, mode, a.language, start, end, payload,
                        raw_dir, a.min_request_gap)

            values = ratios(data, country)
            rows = [to_row(country, a.language, stamp, cfg["version"], *values[i])
                    for i in range(len(values))]
            all_rows.extend(rows)
            tot_country = sum(r[1] for r in values)
            tot_hum = sum(r[2] for r in values)
            tot_sec = sum(r[3] for r in values)
            tot_norm = sum(r[4] for r in values)
            summaries.append({
                "country": country, "days": len(values),
                "country_mentions": tot_country, "humanitarian_term_matches": tot_hum,
                "security_term_matches": tot_sec, "global_monitored_articles": tot_norm,
                "country_share_of_global_percent": round(100*tot_country/tot_norm, 8),
                "humanitarian_share_of_country_percent": round(100*tot_hum/tot_country, 5) if tot_country else None,
                "security_share_of_country_percent": round(100*tot_sec/tot_country, 5) if tot_country else None,
            })
        if not all_rows:
            raise DataValidationError("No valid output rows")
        write_csv(a.output_dir / "daily_attention.csv", all_rows)
        final = {"status": "SUCCESS: GDELT TERM-MATCH MEASUREMENT; NOT A NEGLECT FINDING",
                 "retrieval_utc": stamp, "monitoring_start_utc": str(start),
                 "monitoring_end_exclusive_utc": str(end),
                 "language": a.language, "version": cfg["version"], "query_count": len(plans),
                 "summary": summaries,
                 "interpretation_limits": cfg["notes"]}
        (a.output_dir / "validated_summary.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "VALIDATED TERM MATCH SERIES", "countries": len(countries),
                          "days_per_country": (end-start).days, "summary": summaries}, indent=2))
        return 0
    except (DataValidationError, ThrottledError, HTTPError, URLError, TimeoutError, json.JSONDecodeError) as e:
        (a.output_dir / "ERROR_NOT_PUBLISHABLE.txt").write_text(
            f"RETRIEVAL OR DATA VALIDATION FAILED; NOT A ZERO OR A NEGLECT FINDING\n{type(e).__name__}: {e}\n",
            encoding="utf-8")
        print("DATA NOT VALIDATED: " + str(e), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
