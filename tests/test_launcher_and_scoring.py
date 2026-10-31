import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('strict_scoring',ROOT/'scripts/strict_verifier_results.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class LauncherAndScorerTests(unittest.TestCase):
    def test_raw_task_specs_are_refused_before_modal_import(self):
        r=subprocess.run([sys.executable,str(ROOT/'scripts/launch.py'),'--train',
                          '--prepared-dir',str(ROOT/'data/task_inputs')],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)
        self.assertIn('Task specifications are not training answers',r.stderr)
        self.assertNotIn('No module named',r.stderr)
    def test_missing_duplicate_and_held_checks_never_pass(self):
        task={'task_id':'t','verifiers':[{'name':'same'},{'name':'same'}]}
        with self.assertRaises(module.VerifierResultError): module.strict_task_success(task,[])
        with self.assertRaises(module.VerifierResultError): module.strict_task_success(task,[{'verifier_index':0,'passed':True}])
        with self.assertRaises(module.VerifierResultError): module.strict_task_success(task,[{'verifier_index':0,'passed':True}]*2)
        good=[{'verifier_index':0,'passed':True},{'verifier_index':1,'passed':True}]
        with self.assertRaises(module.VerifierResultError): module.strict_task_success(task,good,quality_holds=['t'])
        self.assertTrue(module.strict_task_success(task,good))
        good[1]['passed']=False
        self.assertFalse(module.strict_task_success(task,good))

if __name__=='__main__': unittest.main()
