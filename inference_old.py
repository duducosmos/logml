#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Inference system from logml file.
By: E. S. Pereira
Version: 0.0.1
Date: 01/09/2017
"""

import string

from exceptions import OnlyOneFactBySide
from parser import Parser, remover_acentos
from gettext import gettext as _

from numpy import where, array, array_equal


QUEST = ["quem"]

STOP_WORDS = ["e", "a", "um", "uma", "o", "de", "da", "do", "esta", "com", "sente"]


def _replace_answer(value, args):
    resp = " ".join(value.split("#")).lower().split(" ")
    for argi in args:
        resp[resp.index("*")] = argi
    resp = " ".join(resp)
    return resp


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

    def __search_facts(self, key, value, mainword, predicate):
        translator = str.maketrans('', '', string.punctuation)
        if key in self.facts:
            maink = " ".join(remover_acentos(value).split("#")).lower()
            mainks = [i for i in maink.split(" ")
                      if i != "" and i not in STOP_WORDS]
            sindix = [i for i, x in enumerate(mainks) if x == '*']
            pred = remover_acentos(predicate).translate(
                translator).lower().split(" ")
            pred = [i for i in pred if i not in STOP_WORDS]
            pred_mindex = pred.index(mainword)
            q_mindex = mainks.index(mainword)

            return q_mindex, sindix, pred_mindex, mainks, pred

    def __exact_match(self, key, value, mainword, predicate, deep):

        q_mindex, sindix, pred_mindex, mainks, pred = self.__search_facts(key,
                                                                          value,
                                                                          mainword,
                                                                          predicate)
        if pred_mindex == q_mindex:
            if len(mainks) == len(pred):
                args = array([pred[i] for i in sindix])
                search = where((self.facts[key] == args).all(axis=1))
                search = self.facts[key][search]
                if search.size:

                    return True, _replace_answer(value, args)
                else:

                    argi = array(
                        [argi for argi in args if argi in self._parser.constants])
                    if array_equal(argi, args):
                        argsi = ",".join(list(argi))
                        neg = _("not({0}({1}))".format(key, argsi))
                        return False, neg
                    else:
                        if argi.size:

                            

                            i = where(args == argi)[0][0]
                            if i == 0:
                                search = self.facts[key][where(
                                    self.facts[key][:, 0] == argi)]
                            else:
                                search = self.facts[key][where(
                                    self.facts[key][:, 1] == argi)]

                            aws = ""
                            for i in search:
                                aws += _replace_answer(value, i) + "\n"
                            return True, aws
                        else:
                            if deep:
                                print(predicate, args, argi)

            else:
                left_p = [i for i in pred[:pred_mindex] if i != key]
                right_p = [i for i in pred[pred_mindex:] if i != key]

                if len(left_p) > 1:
                    raise OnlyOneFactBySide(
                        "Wrong question formulation: {}".format(predicate))

                if len(right_p) > 1:
                    raise OnlyOneFactBySide(
                        "Wrong question formulation: {}".format(predicate))

                if right_p:
                    print(right_p)

                if left_p:
                    print(left_p)

        return False, ""

    def get_facts(self, predicate, *args):
        """
        Get facts
        """
        argi = array(
            [argi for argi in args if argi in self._parser.constants])

        args = array([i for i in args if i != ""])

        search = where((self.facts[predicate] == args).all(axis=1))
        search = self.facts[predicate][search]
        if search.size:
            return search

        else:

            if array_equal(argi, args):
                print(argi)
                argsi = ",".join(list(argi))
                neg = _("not({0}({1}))".format(predicate, argsi))
                return False, neg
            else:
                if argi.size:
                    i = where(args == argi)[0][0]
                    if i == 0:
                        search = self.facts[predicate][where(
                            self.facts[predicate][:, 0] == argi)]
                    else:
                        search = self.facts[predicate][where(
                            self.facts[predicate][:, 1] == argi)]

                    return search
                else:
                    #if deep:
                    print(predicate, args, argi)

    def question(self, predicate, *args, **kwargs):
        """
        Given a text make a query in logml file.
        """

        if "deep" in kwargs:
            deep = kwargs["deep"]
        else:
            deep = False



        if predicate in self.facts:

            print(self.get_facts(predicate, *args))
            #print("A lista de {}".format(predicate))
            #print(self.facts[predicate])

        if len(predicate.split(" ")) > 1:

            found = False
            for pred in self._parser.predicates:
                key, value = list(pred.items())[0]
                mainword = value.split("#")[1].lower()
                if mainword in predicate.lower():
                    found = True
                    break

            if found:
                rep, ans = self.__exact_match(key,
                                              value,
                                              mainword,
                                              predicate,
                                              deep)
                if rep is True:
                    print(ans)
                    return rep
                else:
                    print(ans)
                    return rep

            else:
                print("Não entendi sua pergunta")

        if not kwargs:
            pass


if __name__ == "__main__":
    OBJ = Inference("./database/teste_extended.logml")
    # OBJ.know_about()
    OBJ.question("mulher", "marta")
    OBJ.question("parente", "dino", "marta")
    '''
    OBJ.question("mulher")
    OBJ.question("Quem é mulher?")
    OBJ.question("Quem é parente?")
    OBJ.question("Maria é uma mulher?")
    OBJ.question("Marta é uma mulher?")
    OBJ.question("Maria é parente de gustavo?")
    OBJ.question("Dino é parente de Tony?")
    OBJ.question("Dino é parente de Abe?")
    OBJ.question("Dino é parente de quem?")
    OBJ.question("tony é parente de quem?")
    OBJ.question("Quem é parente de Abe?")
    '''
    #OBJ.question("Quem é parente de Quem?")

    #OBJ.question("Quem é mula?")

    #OBJ.question("Dino é parente de marta e clara?")
