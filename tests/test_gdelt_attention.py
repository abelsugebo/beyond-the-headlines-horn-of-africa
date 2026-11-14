"""Offline test fixtures for GDELT raw timeline attention measurement."""
import unittest
from datetime import date
from scripts.measure_gdelt_attention import (
    DataValidationError, parse_payload, build_query, make_url, ratios, to_row
)

CFG = {
    "version": "test",
    "monitoring_start_utc": "2026-10-01",
    "monitoring_end_exclusive_utc": "2026-10-03",
    "countries": {"Ethiopia": "(Ethiopia OR Tigray)"},
    "topic_queries": {
        "country_mentions": None,
        "humanitarian_terms": "(hunger OR refugees)",
        "security_terms": "(war OR troops)"
    }
}

def payload(a, b, norm=1000):
    return {"timeline": [{"series": "Volume", "data": [
        {"date": "20261001T000000Z", "value": a, "norm": norm},
        {"date": "20261002T000000Z", "value": b, "norm": norm}
    ]}]}

class GdeltBaselineTests(unittest.TestCase):
    def setUp(self):
        self.start, self.end = date(2026, 10, 1), date(2026, 10, 3)

    def test_build_query_has_country_and_topic(self):
        self.assertEqual(build_query(CFG, "Ethiopia", "country_mentions", "all"),
                         "(Ethiopia OR Tigray)")
        self.assertIn("(hunger OR refugees)", build_query(CFG, "Ethiopia", "humanitarian_terms", "all"))
        self.assertTrue(build_query(CFG, "Ethiopia", "security_terms", "english").endswith("sourcelang:english"))

    def test_request_uses_raw_counts_and_exclusive_end(self):
        url = make_url(CFG, "Ethiopia", "humanitarian_terms", "all")
        self.assertIn("timelinevolraw", url)
        self.assertIn("startdatetime=20261001000000", url)
        self.assertIn("enddatetime=20261003000000", url)
        self.assertIn("timelinesmooth=0", url)

    def test_success_parse_and_rate_calculation(self):
        base = parse_payload(payload(100, 200), self.start, self.end)
        hum = parse_payload(payload(20, 40), self.start, self.end)
        sec = parse_payload(payload(55, 77), self.start, self.end)
        result = ratios({"country_mentions": base, "humanitarian_terms": hum, "security_terms": sec}, "Ethiopia")
        self.assertEqual(len(result), 2)
        day,count,h,s,norm = result[0]
        rate = to_row("Ethiopia", "all", "2026-11-12T12:00:00Z", "test", day, count, h, s, norm)
        self.assertEqual(rate["humanitarian_share_of_country_percent"], 20.0)
        self.assertEqual(rate["country_share_of_global_percent"], 10.0)
        self.assertEqual(rate["security_share_of_country_percent"], 55.0)

    def test_missing_day_is_not_zero(self):
        data = payload(5, 0)
        data["timeline"][0]["data"].pop()
        with self.assertRaises(DataValidationError):
            parse_payload(data, self.start, self.end)

    def test_zero_is_supported_when_day_exists(self):
        d = parse_payload(payload(5, 0), self.start, self.end)
        self.assertEqual(d[date(2026,10,2)][0], 0)

    def test_denominator_disagreement_rejected(self):
        base = parse_payload(payload(100, 200), self.start, self.end)
        hum = parse_payload(payload(20, 40, norm=900), self.start, self.end)
        sec = parse_payload(payload(30, 50), self.start, self.end)
        with self.assertRaises(DataValidationError):
            ratios({"country_mentions": base, "humanitarian_terms": hum, "security_terms": sec}, "Ethiopia")

    def test_subset_violation_rejected(self):
        base = parse_payload(payload(10, 20), self.start, self.end)
        hum = parse_payload(payload(11, 40), self.start, self.end)
        sec = parse_payload(payload(1, 2), self.start, self.end)
        with self.assertRaises(DataValidationError):
            ratios({"country_mentions": base, "humanitarian_terms": hum, "security_terms": sec}, "Ethiopia")

    def test_non_integer_raw_count_rejected(self):
        with self.assertRaises(DataValidationError):
            parse_payload(payload(5.3, 8), self.start, self.end)

    def test_out_of_range_dates_rejected(self):
        d = payload(5, 8)
        d["timeline"][0]["data"][1]["date"] = "20261003T000000Z"
        with self.assertRaises(DataValidationError):
            parse_payload(d, self.start, self.end)

    def test_inclusive_end_boundary_is_not_counted(self):
        data = payload(5, 8)
        data["timeline"][0]["data"].append(
            {"date": "20261003T000000Z", "value": 999, "norm": 1000}
        )
        got = parse_payload(data, self.start, self.end)
        self.assertEqual(len(got), 2)
        self.assertEqual(got[date(2026,10,2)][0], 8)

    def test_partial_timeline_is_diagnostic_only(self):
        data = payload(5, 8)
        data["timeline"][0]["data"].pop()
        got = parse_payload(data, self.start, self.end, require_complete=False)
        self.assertEqual(len(got), 1)
        with self.assertRaises(DataValidationError):
            parse_payload(data, self.start, self.end)

    def test_weekly_window_url_overrides_range(self):
        url = make_url(CFG, "Ethiopia", "country_mentions", "all",
                       date(2026, 10, 2), date(2026, 10, 3))
        self.assertIn("startdatetime=20261002000000", url)
        self.assertIn("enddatetime=20261003000000", url)

    def test_unknown_country_rejected(self):
        with self.assertRaises(ValueError):
            build_query(CFG, "Utopia", "country_mentions", "all")

if __name__ == "__main__":
    unittest.main()
