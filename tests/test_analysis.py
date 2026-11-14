import csv,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from analyze import load,validate,summarize,canonical_url
from analyze_relationships import load as load_rel,validate as validate_rel

class AnalysisTests(unittest.TestCase):
    def setUp(self):self.rows=load(ROOT/'examples/demo_synthetic.csv')
    def test_sample_is_explicitly_synthetic(self):
        self.assertEqual({r['synthetic_demo'] for r in self.rows},{'true'})
        self.assertEqual(validate(self.rows),[])
    def test_summary_is_bounded(self):
        stats,edges=summarize(self.rows)
        self.assertEqual(stats['total_coded_records'],16)
        self.assertIn('SYNTHETIC',stats['status'])
        self.assertTrue(all('DEMO-' in a for a,b in edges.keys()))
    def test_mixed_real_demo_is_rejected(self):
        r=[x.copy() for x in self.rows]
        r[-1]['synthetic_demo']='false'
        self.assertTrue(any('mix real and synthetic' in e for e in validate(r)))
    def test_unapproved_release_rejected(self):
        r=[x.copy() for x in self.rows]
        r[0]['release_approved']='no'
        self.assertTrue(any('release not approved' in e for e in validate(r)))
    def test_eritrea_is_core_country(self):
        self.assertIn('Eritrea',{r['country'] for r in self.rows})
        self.assertEqual(validate(self.rows),[])
    def test_unattributed_proxy_allegation_rejected(self):
        r=[x.copy() for x in self.rows]
        n=next(x for x in r if x['external_involvement_type']=='alleged_armed_support')
        n['claim_attributed_to']=''
        self.assertTrue(any('allegation must name' in err for err in validate(r)))
    def test_external_country_counts_are_mentions_only(self):
        stats,_=summarize(self.rows)
        self.assertIn('Egypt',stats['by_external_actor_mention'])
        self.assertIn('UAE',stats['by_external_actor_mention'])
        self.assertIn('do NOT prove',stats['external_actor_caveat'])
    def test_relationships_must_have_attribution(self):
        rs=load_rel(ROOT/'examples/demo_relationships_synthetic.csv')
        self.assertEqual(validate_rel(rs),[])
        rs[1]['claim_attributed_to']=''
        self.assertTrue(any('attribution required' in err for err in validate_rel(rs)))
    def test_tracking_params(self):
        self.assertEqual(canonical_url('https://example.org/a?utm_source=linkedin'), 'https://example.org/a')

if __name__=='__main__':unittest.main()
