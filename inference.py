#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Inference system from logml file.
By: E. S. Pereira
Version: 0.0.1
Date: 01/09/2017
"""

import string

from parser import Parser, remover_acentos
from gettext import gettext as _

from numpy import where, array


QUEST = ["quem"]

STOP_WORDS = ["e", "a", "um", "uma", "o", "de", "da", "do"]


class Inference:
    """
    Inference system
    """

    def __init__(self, logml_file):
        self._parser = Parser(logml_file)
        self.facts = self._parser.get_array_facts()
        self.predicates = [list(i.keys())[0] for i in self._parser.predicates]

    def know_about(self):
        """
        Return the list of predicates.
        """
        print(_("I know about: "))
        print([list(i.keys())[0] for i in self._parser.predicates])

    def __replace_star(self, key, value, mainword, predicate):
        translator = str.maketrans('', '', string.punctuation)
        if key in self.facts:
            maink = " ".join(remover_acentos(value).split("#")).lower()
            mainks = [i for i in maink.split(" ")
                      if i != "" and i not in STOP_WORDS
                     ]
            sindix = [i for i, x in enumerate(mainks) if x == '*']
            pred = remover_acentos(predicate).translate(translator).lower().split(" ")
            pred = [i for i in pred if i not in STOP_WORDS]
            pred_mindex = pred.index(mainword)
            q_mindex = mainks.index(mainword)

            args = []

            if pred_mindex == q_mindex:
                if len(mainks) == len(pred):
                    args = array([pred[i] for i in sindix])
                    search = where((self.facts[key] == args).all(axis=1))
                    search = self.facts[key][search]
                    if search.size:
                        resply = " ".join(value.split("#")).lower().split(" ")
                        for argi in args:
                            resply[resply.index("*")] = argi
                        resply = " ".join(resply)

                        return True, resply
            return False, ""


    def question(self, predicate, **kwargs):
        """
        Given a text make a query in logml file.
        """

        if predicate in self.facts:
            print("A lista de {}".format(predicate))
            print(self.facts[predicate])

        if len(predicate.split(" ")) > 1:

            found = False
            for pred in self._parser.predicates:
                key, value = list(pred.items())[0]
                mainword = value.split("#")[1].lower()
                if mainword in predicate.lower():
                    found = True
                    break

            if found:
                rep, ans = self.__replace_star(key, value, mainword, predicate)
                print(ans)
                return rep

            else:
                print("Não entendi sua pergunta")


        if not kwargs:
            pass



if __name__ == "__main__":
    OBJ = Inference("./database/teste_extended.logml")
    #OBJ.know_about()
    #OBJ.question("mulher")
    OBJ.question("Quem é mulher?")
    OBJ.question("Quem é parente?")
    OBJ.question("Maria é uma mulher?")
    OBJ.question("Marta é uma mulher?")
    OBJ.question("Maria é parente de gustavo?")
    OBJ.question("Dino é parente de Tony?")
    OBJ.question("Dino é parente de quem?")
    OBJ.question("Quem é mula?")
