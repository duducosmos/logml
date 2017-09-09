#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Inference Machine Test  from logml file.
By: E. S. Pereira
Version: 0.0.1
Date: 08/09/2017
"""

import unittest
from inferencemachine import InferenceMachine
from exceptions import InputArgsSizeError


class TestInferenceMachine(unittest.TestCase):
    """
    Inference Machine unit Test
    """

    def setUp(self):

        self.inference_machine = InferenceMachine("./database/teste_extended.logml")

    def test_know_about(self):
        """
        Test result when the input is only a predicate
        """
        result = self.inference_machine.know_about()
        expect = ['mortal', 'gripe', 'irmao', 'pai', 'mae', 'avo',
                  'bisavo', 'mulher', 'quadrado', 'homem', 'parente', 'febre',
                  'mal_estar', 'dor_de_garganta']
        self.assertEqual(result, expect)

    def test_question_fact_in_file(self):
        """
        Test result when the input is only a predicate.
        """
        result = self.inference_machine.question("mulher")
        self.assertEqual(result[1][0], "lisa")

    def test_question_fact_name(self):
        """
        Test result when the input is only a predicate.
        """
        result = self.inference_machine.question("mulher", "marta")
        self.assertEqual(result[1], "marta")

    def test_not_in_fact(self):
        """
        Test result when the input is only a predicate.
        """
        result = self.inference_machine.question("mulher", "martolo", precise=True)
        self.assertFalse(result[0])

    def test_question_fact_2d(self):
        """
        Test result when the input is only a predicate.
        """
        result = self.inference_machine.question("parente")

        self.assertTrue(list(result[0]) == ['dino', 'tony'])

    def test_question_fact_moreargs(self):
        """
        Test result when the input is only a predicate.
        """
        with self.assertRaises(InputArgsSizeError) as context:
            self.inference_machine.question("parente", "dino")
        self.assertTrue("Input Args not correspondet to: parente" in str(context.exception))

    def test_question_fact_n1_2d(self):
        """
        Test result when the input is only a predicate.
        """
        result = self.inference_machine.question("parente", "dino", "x")
        self.assertTrue(list(result[1][0]) == ['dino', 'tony'])

    def test_question_fact_vars_2d(self):
        """
        Test result when the input is only a predicate.
        """
        result = self.inference_machine.question("parente", "y", "x")
        self.assertTrue(list(result[1][0]) == ['dino', 'tony'])

    def test_question_fact_3d(self):
        """
        Test result when the input is only a predicate.
        """
        result = self.inference_machine.question("quadrado")
        self.assertTrue(list(result) == ['3', '2', '25'])

    def test_question_fact_args_3d(self):
        """
        Test result when the input is only a predicate.
        """
        result = self.inference_machine.question("quadrado", "2", "3", "x")
        self.assertTrue(result[0] is False)

    def test_question_fact_2d_extra(self):
        """
        Test result when the input is only a predicate.
        """
        result = self.inference_machine.question("parente", "tony", "x")
        result = list(result[1])
        self.assertTrue(len(result) == 2)

    def test_rule_level1(self):
        """
        Test result when the input predicate not in logml.
        """
        result = self.inference_machine.question("mortal")
        self.assertEqual(result[1][0], "socrates")



if __name__ == "__main__":
    unittest.main()