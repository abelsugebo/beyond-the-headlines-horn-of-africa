#!/usr/bin/env python3
"""Build an explicitly candidate-only, purposive five-country X monitoring matrix.

No inference about X population-level distribution. Researcher checked each post;
claims and engagement are not independently corroborated.
Run from repository root: python scripts/build_five_country_x_matrix.py
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "analysis"
CONFIG = TARGET / "x_frame_annotations_v1.json"
EPOCH_MS = 1288834974657

def read_rows(path):
    with (ROOT / path).open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))

def x_id(url):
    path = urlparse(url).path
    parts = path.split("/status/")
    if len(parts) != 2 or not parts[-1].split("/")[0].isdigit():
        raise ValueError(f"Not a direct X status URL: {url}")
    return parts[-1].split("/")[0]

def snowflake_iso(post_id):
    from datetime import datetime, timezone
    millis = (int(post_id) >> 22) + EPOCH_MS
    return datetime.fromtimestamp(millis / 1000, timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

FIELDS = [
    "case_record_id", "case_country", "post_id", "post_url", "post_timestamp_utc",
    "account_claimed", "topic_provisional", "publisher_class",
    "primary_frame_provisional", "humanitarian_temporality",
    "cross_border_provisional", "underlying_claim_status", "attribution_caution",
    "reused_statistic_id", "shared_event_id", "upstream_source_id",
    "upstream_support_url", "upstream_review_status", "original_x_content_verified",
    "engagement_metrics_verified", "candidate_only", "human_coder_reviewed", "source_review_file",
    "researcher_attested_x_post_checked", "researcher_attestation_date", "researcher_attestation_scope",
]

def write_rows(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def build(config):
    cases = []
    for spec in config["sources"]:
        original = read_rows(spec["path"])
        assert len(original) == 10, (spec["country"], len(original))
        topic_lookup = (
            {r["Record ID"]: r["Primary topic"] for r in read_rows(spec["topic_fallback_file"])}
            if spec.get("topic_fallback_file") else {}
        )
        for r in original:
            rid = r[spec["id"]]
            ann = config["annotations"][rid]
            post = x_id(r[spec["post"]])
            iso = snowflake_iso(post)
            assert iso[:10] == r[spec["date"]][:10], rid
            underlying = (
                config["g7_shared_id"]
                if rid in {"ETH2-010", "ERI-009"}
                else r[spec["upstream"]] if spec["upstream"]
                else config["eritrean_upstream_overrides"][rid]
            )
            cases.append(dict(zip(FIELDS, [
                rid, spec["country"], post, r[spec["post"]], iso,
                r[spec["account"]],
                r[spec["topic"]] if spec["topic"] else topic_lookup.get(rid, "Source topic in original Grok record"),
                *ann[:6], ann[6] or "", ann[7] or "", underlying,
                r[spec["url"]] or "", r[spec["evidence"]] or "",
                "no", "no", "yes", "no", spec["path"],
                config["researcher_attestation"]["post_check_status"],
                config["researcher_attestation"]["date"],
                "Researcher states each X post was checked; specific verification fields not enumerated",
            ])))
    assert len(cases) == 50
    assert {r["case_record_id"] for r in cases} == set(config["annotations"])
    posts = defaultdict(list)
    upstreams = defaultdict(list)
    for r in cases:
        posts[r["post_id"]].append(r)
        upstreams[r["upstream_source_id"]].append(r)
    assert len(posts) == 49
    dup = [
        {"post_id": post, "case_record_ids": ";".join(x["case_record_id"] for x in rows),
         "distinct_countries": len(set(x["case_country"] for x in rows)),
         "note": "Exact same X post assigned to two country case lenses; count once in distinct post totals."}
        for post, rows in posts.items() if len(rows) > 1
    ]
    assert len(dup) == 1 and {x["case_record_id"] for x in posts[dup[0]["post_id"]]} == {"ETH2-010", "ERI-009"}
    composition = []
    for spec in config["sources"]:
        country = spec["country"]
        selected = [r for r in cases if r["case_country"] == country]
        for field, name in [
            ("primary_frame_provisional", "primary_frame"),
            ("publisher_class", "publisher_class"),
            ("humanitarian_temporality", "humanitarian_temporality"),
        ]:
            for category, count in sorted(Counter(r[field] for r in selected).items()):
                composition.append({
                    "country": country, "dimension": name, "category": category,
                    "candidate_case_count": count, "denominator_case_count": len(selected),
                    "caveat": "PURPOSIVE SAMPLE; NOT X PREVALENCE; RESEARCHER CHECKED POSTS, NOT INDEPENDENTLY RE-AUTHENTICATED",
                })
    repeat = []
    for key, rows in sorted(upstreams.items()):
        if len(rows) > 1:
            repeat.append({
                "upstream_source_id": key, "case_entries": len(rows),
                "distinct_post_ids": len({r["post_id"] for r in rows}),
                "case_record_ids": ";".join(r["case_record_id"] for r in rows),
                "note": "Post origin/shared document only. Does not establish coordinated behavior or independent corroboration.",
            })
    return cases, composition, repeat, dup

def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    cases, composition, repeat, duplicate = build(config)
    write_rows(TARGET / "five_country_case_matrix_v1.csv", cases, FIELDS)
    write_rows(TARGET / "five_country_composition_v1.csv", composition,
               ["country", "dimension", "category", "candidate_case_count", "denominator_case_count", "caveat"])
    write_rows(TARGET / "shared_upstream_groups_v1.csv", repeat,
               ["upstream_source_id", "case_entries", "distinct_post_ids", "case_record_ids", "note"])
    write_rows(TARGET / "duplicate_cross_country_posts_v1.csv", duplicate,
               ["post_id", "case_record_ids", "distinct_countries", "note"])
    report = {
        "case_entries": len(cases),
        "distinct_x_post_ids": len({r["post_id"] for r in cases}),
        "country_counts": dict(Counter(r["case_country"] for r in cases)),
        "original_X_posts_independently_authenticated": 0,
        "researcher_attested_x_posts_checked": len({r["post_id"] for r in cases}),
        "researcher_attested_country_case_entries": sum(r["researcher_attested_x_post_checked"] == "yes" for r in cases),
        "researcher_attestation_date": config["researcher_attestation"]["date"],
        "researcher_attestation_scope": "Researcher states every X post checked; post-level detail of check not specified",
        "engagement_metrics_independently_verified": 0,
        "eligible_for_population_inference": False,
        "shared_upstream_groups": len(repeat),
        "exact_duplicate_post_groups": len(duplicate),
        "separate_news_official_discovery_records_not_included": 24,
    }
    (TARGET / "validation_summary_v1.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
