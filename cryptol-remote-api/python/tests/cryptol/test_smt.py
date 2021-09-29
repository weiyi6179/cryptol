import unittest
from pathlib import Path
import unittest
import cryptol
from cryptol.single_connection import *
from cryptol.bitvector import BV


class TestSMT(unittest.TestCase):
    def test_SMT(self):
        connect(verify=False)
        load_module('Cryptol')

        ex_true  = '\(x : [8]) -> x+x == x+x'
        ex_true_safe = safe(ex_true)
        self.assertTrue(ex_true_safe)
        self.assertIsInstance(ex_true_safe, cryptol.Safe)
        ex_true_prove = prove(ex_true)
        self.assertTrue(ex_true_prove)
        self.assertIsInstance(ex_true_prove, cryptol.Qed)
        ex_true_sat = sat(ex_true)
        self.assertTrue(ex_true_sat)
        self.assertIsInstance(ex_true_sat, cryptol.Satisfiable)

        ex_false = '\(x : [8]) -> x+2*x+1 == x'        
        ex_false_safe = safe(ex_false)
        self.assertTrue(ex_false_safe)
        self.assertIsInstance(ex_false_safe, cryptol.Safe)
        ex_false_prove = prove(ex_false)
        self.assertFalse(ex_false_prove)
        self.assertIsInstance(ex_false_prove, cryptol.Counterexample)
        self.assertEqual(ex_false_prove.type, "predicate falsified")
        ex_false_sat = sat(ex_false)
        self.assertFalse(ex_false_sat)
        self.assertIsInstance(ex_false_sat, cryptol.Unsatisfiable)

        ex_partial = '\(x : [8]) -> if x < 0x0f then x == x else error "!"'
        ex_partial_safe = safe(ex_partial)
        self.assertFalse(ex_partial_safe)
        self.assertIsInstance(ex_partial_safe, cryptol.Counterexample)
        self.assertEqual(ex_partial_safe.type, "safety violation")
        ex_partial_prove = prove(ex_partial)
        self.assertFalse(ex_partial_prove)
        self.assertIsInstance(ex_partial_prove, cryptol.Counterexample)
        self.assertEqual(ex_partial_prove.type, "safety violation")
        ex_partial_sat = sat(ex_partial)
        self.assertTrue(ex_partial_sat)
        self.assertIsInstance(ex_partial_sat, cryptol.Satisfiable)


if __name__ == "__main__":
    unittest.main()