import tempfile
import unittest
from pathlib import Path
from decimal import Decimal
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from budget_control import load_json, rate_per_second, reservation_cost, reserve_call, finish_call, summarize

class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.config=load_json(Path(__file__).resolve().parents[1]/'config/modal.json')
    def test_verified_modal_rate_and_reservation(self):
        self.assertEqual(rate_per_second(self.config)*3600,Decimal('2.814912'))
        self.assertEqual(reservation_cost(self.config),Decimal('3.34'))
    def test_failure_does_not_refund_or_reset_account_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'ledger.json'
            a=reserve_call(self.config,p,run_name='one',dataset_sha256='abc')
            with self.assertRaises(ValueError):
                reserve_call(self.config,p,run_name='two',dataset_sha256='abc')
            finish_call(p,a['run_id'],'interrupted_or_failed')
            self.assertEqual(load_json(p)['calls'][0]['reserved_usd'],'3.34')
            for i in range(7):
                a=reserve_call(self.config,p,run_name='resume',dataset_sha256='abc')
                finish_call(p,a['run_id'],'completed')
            with self.assertRaises(ValueError):
                reserve_call(self.config,p,run_name='over-budget',dataset_sha256='abc')
            self.assertEqual(summarize(self.config,load_json(p))['reserved_gpu_usd'],'26.72')
    def test_cannot_expand_total_above_user_cap(self):
        c=dict(self.config); c['campaign_caps_usd']=dict(c['campaign_caps_usd'],total='41')
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): reserve_call(c,Path(tmp)/'ledger.json',run_name='x',dataset_sha256='a')

if __name__=='__main__': unittest.main()
