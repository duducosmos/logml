#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Inference system from logml file.
By: E. S. Pereira
Version: 0.0.1
Date: 08/09/2017
"""

from gettext import gettext as _

from parser import Parser
from numpy import where, array, array_equal
from exceptions import InputArgsSizeError


class InferenceMachine:
    """
    Inference Machine for logml
    """

    def __init__(self, logml_file):
        self._parser = Parser(logml_file)
        self.facts = self._parser.get_array_facts()
        self.predicates = [list(i.keys())[0] for i in self._parser.predicates]

    def know_about(self):
        """
        Return the list of predicates.
        """
        know = [list(i.keys())[0] for i in self._parser.predicates]
        print(_("I know about: "))

        for pred in self._parser.predicates:
            value = list(pred.items())[0][1]
            mainword = value.split("#")[1].lower()
            print("pred: {0}; meta: {1}".format(
                list(pred.keys())[0], _(mainword)))
        return know

    def _get_facts(self, predicate, *args):

        args = args[0]

        argi = array(
            [argi for argi in args if argi in self._parser.constants])

        dinfact = self.facts[predicate].shape

        if len(dinfact) == 1:
            self.facts[predicate] = array([list(self.facts[predicate])])

        dinfact = self.facts[predicate].shape

        if len(args) != dinfact[1]:
            raise InputArgsSizeError(_("Input Args not correspondet to: ")
                                     + predicate)
        args = array(args)

        search = where((self.facts[predicate] == args).all(axis=1))
        search = self.facts[predicate][search]
        if search.size:
            return search

        else:

            if array_equal(argi, args):
                argsi = ",".join(list(argi))
                neg = _("not({0}({1}))".format(predicate, argsi))
                return False, neg
            else:
                if argi.size:
                    subset = []
                    for j in args:
                        if j in argi:
                            index = where(argi == j)[0][0]
                            seai = where(
                                self.facts[predicate][:, index] == j)[0]
                            if not subset:
                                subset = set(seai)
                            else:
                                subset = subset & set(seai)


                            if not list(seai):
                                argsi = ",".join(list(args))
                                neg = _("not({0}({1}))".format(
                                    predicate, argsi))
                                return False, neg
                        else:

                            index = where(args == j)[0][0]
                            seai = set(range(self.facts[predicate][:, index].size))

                            if not subset:
                                subset = set(seai)
                            else:
                                subset = subset & set(seai)

                    if not subset:
                        argsi = ",".join(list(args))
                        neg = _("not({0}({1}))".format(
                            predicate, argsi))
                        return False, neg

                    return self.facts[predicate][list(subset)]


    def question(self, predicate, *args):
        """
        Given a text make a query in logml file.
        """

        if predicate in self.facts:
            if args:
                facts = self._get_facts(predicate, args)
            else:
                facts = self.facts[predicate]

            return facts


if __name__ == "__main__":
    OBJ = InferenceMachine("./database/teste_extended.logml")
    print(OBJ.question("mulher", "marta"))
    print(OBJ.question("parente", "tony", "x"))
    print(OBJ.question("parente", "tony", "sara"))
    print(OBJ.question("quadrado", "3", "2", "x"))
    print(OBJ.question("quadrado", "2", "3", "25"))
    print(OBJ.question("quadrado", "3", "2", "25"))
