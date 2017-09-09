#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Translate logml file to pl file.
By: E. S. Pereira
Version: 0.0.1
Date: 22/08/2017
"""


from parser import Parser


class OnlyOneClausure(Exception):
    """
    Return Error when it is use more than one Clausure in comman  in class.
    """
    pass


class Translater(object):
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
        self.lambda_func = []
        self.generate_facts()
        self.generate_rules()
        print(self.constants)

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

    def generate_rules(self):
        """
        Validate de args of rules .
        """
        for rule in self._parser.conditionals:
            args = self._parser.conditionals[rule][0]["1"]
            facts = self._parser.conditionals[rule][1]

            pl_rule = u"{0}({1}):- ".format(rule, ",".join(args).upper())

            for fact in facts:

                if isinstance(facts[fact], list):
                    for sub_fact in facts[fact]:
                        pl_rule += u"{0}({1}),".format(
                            fact, ",".join(sub_fact["1"]).upper())

                else:
                    if ',' in fact:
                        pl_rule += u"{0}({1}),".format(
                            fact.split(",")[0], ",".join(facts[fact]["1"]).upper())
                    else:
                        pl_rule += u"{0}({1}),".format(
                            fact, ",".join(facts[fact]["1"]).upper())
            pl_rule = pl_rule[:-1] + "."
            self.lambda_func.append(pl_rule)

    def generate_facts(self):
        "Returna a list of  facts "
        new_fact = ""
        for fact in self._parser.facts:
            tmp = self._parser.facts[fact]

            if isinstance(tmp, list):
                for tmpi in tmp:
                    new_fact += u"{0}({1}).\n".format(
                        fact, u",".join(tmpi["1"]).lower())

            else:
                new_fact += u"{0}({1}).\n".format(fact,
                                                  u",".join(tmp["1"]).lower())

        self.lambda_func.append(new_fact)

    def generate_program(self):
        """
        Save the generated prolog program.
        """
        prog = ""

        for predicate in self.lambda_func:
            prog += predicate + "\n"

        with open(self.pl_file, "w") as myfile:
            myfile.write(prog)


if __name__ == "__main__":

    import sys
    if len(sys.argv) > 2:
        INPUT_F = sys.argv[1]
        OUTPUT_F = sys.argv[2]
        CMP = Translater(INPUT_F, OUTPUT_F)
        CMP.generate_program()
