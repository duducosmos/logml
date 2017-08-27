#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Translate logml file to pl file.
By: E. S. Pereira
Version: 0.0.1
Date: 22/08/2017
"""


from parser import Parser
from numpy import array


class OnlyOneClausure(Exception):
    """
    Return Error when it is use more than one Clausure in comman  in class.
    """
    pass


class Compiler:
    """
    Translate the logml file to prolog program
    """

    def __init__(self, logml_file, pl_file):
        self._logml_file = logml_file
        self.pl_file = pl_file
        self._parser = Parser(self._logml_file)
        for predicate in self._parser.conditionals:
            self.validate_conditional(predicate)

        self.constants = None
        self.get_constants()
        self.facts = {}
        self.facts_matrix()

    def get_constants(self):
        """
        Return a list of constants defined in facts.
        """
        tmp = []
        for value in self._parser.facts.values():
            if isinstance(value, list):
                tmp.append(sum([pid["1"] for pid in value if "1" in pid], []))
            else:
                tmp.append(value["1"])

        self.constants = list(set(sum(tmp, [])))

    def _not_declared_predict(self, predicate):
        if predicate not in self._parser.facts:
            if predicate not in self._parser.conditionals:
                raise NameError("\"{}\" not declared".format(predicate))
        return False

    def _not_declared_var(self, predicate):
        """
        Search for vars in facts.
        """

    def validate_conditional(self, predicate):
        """
        Validate conditionals
        """

        facts = [pid for pid in
                 self._parser.conditionals[predicate]
                 if "1" not in pid][0]

        sub_fact = None

        for fact in facts:

            if "," in fact:
                if len(facts) > 1:
                    raise OnlyOneClausure(
                        "Only one Clausure with comma \"{}\"".format(fact))

                sub_fact = fact.split(",")

                for fact1 in sub_fact:
                    self._not_declared_predict(fact1)
            else:
                self._not_declared_predict(fact)

        return True


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
