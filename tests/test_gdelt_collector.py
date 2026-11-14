import importlib.util,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("gdelt",root/"scripts"/"collect_gdelt_doc.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class GDELTTests(unittest.TestCase):
    def test_url(self):
        url=m.make_url("Eritrea","2026-11-10",40)
        self.assertIn("startdatetime=20261110000000",url)
        self.assertIn("enddatetime=20261111000000",url)
        self.assertIn("maxrecords=40",url)
    def test_bad_parameters(self):
        for args in [("Other","2026-11-10",20),("Ethiopia","2026-13-40",20),("Somalia","2026-11-10",251)]:
            with self.assertRaises(ValueError):m.make_url(*args)
    def test_parse_and_dedup(self):
        p={"articles":[{"url":"https://test.example/article","title":"Example"},
                        {"url":"https://test.example/article","title":"Repeated"}]}
        r=m.convert(p,"Sudan","2026-11-10","https://api.gdeltproject.org")
        self.assertEqual(len(r),1)
        self.assertEqual(r[0]["review_status"],"discovery_candidate_not_verified")
