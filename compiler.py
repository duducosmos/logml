#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Translate logml file to database.
By: E. S. Pereira
Version: 0.0.1
Date: 22/08/2017
"""

from exceptions import OnlyOneClausure

from parser import Parser
from numpy import array


class Compiler:
    """
    Translate the logml file to prolog program
    """

    def __init__(self, logml_file, pl_file):
        self._logml_file = logml_file
        self.pl_file = pl_file
        self._parser = Parser(self._logml_file)
        self.facts = {}
        self.facts_matrix()


    def _generate_rules(self, rule):
        #args = self._parser.conditionals[rule][0]["1"]
        facts = self._parser.conditionals[rule][1]
        matrix = []
        i = 0

        all_in_facts = True

        for fact in facts:
            if isinstance(facts[fact], list):
                for _ in facts[fact]:

                    if fact in self.facts:
                        matrix.append(fact)
                    else:
                        matrix.append(i)
                        all_in_facts = False
                    i += 1
            else:
                if ',' in fact:
                    for sub_fact in fact.split(","):
                        if sub_fact in self.facts:
                            matrix.append(sub_fact)
                        else:
                            matrix.append(i)
                            all_in_facts = False
                        i += 1
                else:
                    if fact in self.facts:
                        matrix.append(fact)
                    else:
                        matrix.append(i)
                        all_in_facts = False
                    i += 1

        return all_in_facts, matrix

    def new_fact_from_facts(self, rule):
        args = self._parser.conditionals[rule][0]["1"]
        body = self._parser.conditionals[rule][1]
        print(rule, args, body)

    def generate_rules(self):
        """
        Validate de args of rules .
        """
        for rule in self._parser.conditionals:

            all_in_facts, matrix = self._generate_rules(rule)
            if all_in_facts is True:
                self.new_fact_from_facts(rule)
            else:
                facts = self._parser.conditionals[rule][1]
                #print(rule, facts, matrix)

    def facts_matrix(self):
        "Returna a list of  facts "

        for fact in self._parser.facts:
            tmp = self._parser.facts[fact]
            mfacts = []

            if isinstance(tmp, list):
                for tmpi in tmp:
                    mfacts.append(tmpi["1"])
                self.facts[fact] = array(mfacts)

            else:
                mfacts.append(tmp["1"])
                self.facts[fact] = array(mfacts)


if __name__ == "__main__":

    import sys
    if len(sys.argv) > 2:
        INPUT_F = sys.argv[1]
        OUTPUT_F = sys.argv[2]
        CMP = Compiler(INPUT_F, OUTPUT_F)
        CMP.generate_rules()
