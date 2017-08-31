#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
The logml parser.
Given a logml file, return the sintatic structure.
By: E. S. Pereira
Version: 0.0.1
Date: 22/08/2017
"""

import sys
from unicodedata import normalize
from validators import validate_meta, validate_meta_star


import xmltodict


IS_PYTHON3 = sys.version_info.major == 3
if IS_PYTHON3:
    unicode = str

    def remover_acentos(txt):
        """
        Remove acentuacao.
        """
        return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
else:
    def remover_acentos(txt, codif='utf-8'):
        """
        Remove acentuacao.
        """
        return normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore')




def _parse_li(arg):
    """
    Parse li an its type
    """
    if isinstance(arg, unicode):
        return {"1": arg.split(",")}

    elif isinstance(arg, dict):
        return [{arg["@type"]: arg["#text"].split(",")}]

    out = []
    for i in arg:
        if isinstance(i, dict):
            tmp = {i["@type"]: i["#text"].split(",")}
        else:
            tmp = {"1": i.split(",")}
        out.append(tmp)
    return out

def get_axioms(logml_file):
    """
    Return all Axioms from a File
    """
    axioms = None
    with open(logml_file, 'r') as logml:
        text = logml.read()
        result = xmltodict.parse(text)

        if "axiom" in result["logml"]:
            axioms = result["logml"]["axiom"]
    return axioms


class Parser:
    """
    The logml parser.
    """

    def __init__(self, logml_file):
        self.axioms = get_axioms(logml_file)
        self.clausures = self.get_clausures()
        self.facts = self.get_facts()
        self.gols = self.get_gols()
        self.conditionals = self.get_condictionals()

        for predicate in self.conditionals:
            self.validate_conditional(predicate)

        self.predicates = self.get_predicates()
        self.constants = self.get_constants()


    def _not_declared_predict(self, predicate):
        if predicate not in self.facts:
            if predicate not in self.conditionals:
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
                 self.conditionals[predicate]
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

    def get_constants(self):
        """
        Return a list of constants defined in facts.
        """
        tmp = []
        for value in self.facts.values():
            if isinstance(value, list):
                tmp.append(sum([pid["1"] for pid in value if "1" in pid], []))
            else:
                tmp.append(value["1"])

        return list(set(sum(tmp, [])))

    def _get_pred_fact(self):
        predicates = []
        for fact in self.clausures["fact"]:
            if isinstance(fact["head"]["pred"], list):
                for sub_fact in fact["head"]["pred"]:
                    if "meta" in sub_fact:
                        validate_meta(sub_fact["meta"], sub_fact["@class"])
                        predicates.append({remover_acentos(sub_fact["@class"]):
                                           sub_fact["meta"]})
                        head_li = _parse_li(sub_fact["li"])

                        validate_meta_star(sub_fact["meta"],
                                            sub_fact["@class"],
                                            head_li)

                    else:
                        predicates.append({remover_acentos(
                            sub_fact["@class"]): None})

            else:
                print(fact["head"]["pred"])
        return predicates

    def get_predicates(self):
        """
        Return a list of predicates in the logml file.
        Represent the questions that the sistem can responds.
        """
        predicates = []
        if self.conditionals is not None:

            for conditional in self.clausures["conditional"]:
                if "meta" in conditional["head"]["pred"]:
                    frase = conditional["head"]["pred"]["meta"]
                    validate_meta(frase, conditional)

                    predicates.append({remover_acentos(conditional["head"]["pred"]["@class"]):
                                       frase})
                else:
                    predicates.append({remover_acentos(
                        conditional["head"]["pred"]["@class"]): None})

        if self.gols is not None:
            for gol in self.gols:
                predicates.append(gol)

        if self.facts is not None:
            predicates += self._get_pred_fact()

        return predicates

    def get_gols(self):
        """Get All gols in the logml file"""
        if 'gol' in self.clausures:
            gols = {}
            for gol in self.clausures["gol"]:
                gols[remover_acentos(gol['body']["pred"]["@class"])] = \
                    _parse_li(gol['body']["pred"]["li"])
            return gols

    def get_condictionals(self):
        """Get All conditional"""

        if "conditional" in self.clausures:
            conditionals = {}

            for conditional in self.clausures["conditional"]:
                body = conditional['body']["pred"]

                if isinstance(body, list):
                    body = {bi["@class"]: _parse_li(bi["li"]) for bi in body}
                else:
                    body = {body["@class"]: _parse_li(body["li"])}

                head_li = _parse_li(conditional['head']["pred"]["li"])
                if isinstance(head_li, list):
                    if len(head_li) > 1:
                        raise NameError(
                            "Conditional with two predicates in head")

                conditionals[remover_acentos(conditional['head']["pred"]["@class"])] = [
                    head_li,
                    body
                ]

            return conditionals

    def get_facts(self):
        """
        Get All fact From logml file
        """

        if "fact" in self.clausures:
            unconditionals = {}
            for unconditional in self.clausures['fact']:
                facts = unconditional['head']["pred"]

                if isinstance(facts, list):
                    for fts in facts:
                        fts_li = _parse_li(fts["li"])
                        unconditionals[remover_acentos(fts["@class"])] = fts_li
                else:
                    unconditionals[remover_acentos(unconditional['head']["pred"]["@class"])] = \
                        _parse_li(facts["li"])
            return unconditionals


    def get_clausures(self):
        """
        Separete clausures tipe from axioms.
        """
        clausures = {}
        for axiom in self.axioms:
            if "head" in axiom and "body" not in axiom:
                if "fact" not in clausures:
                    clausures["fact"] = []
                clausures["fact"].append(axiom)

            elif "body" in axiom and "head" not in axiom:
                if "gol" not in clausures:
                    clausures["gol"] = []
                clausures["gol"].append(axiom)

            else:
                if "conditional" not in clausures:
                    clausures["conditional"] = []
                clausures["conditional"].append(axiom)
        return clausures


if __name__ == "__main__":
    OBJ = Parser("./database/teste_extended.logml")
    print("Predicados : {}".format(OBJ.get_predicates()))
    print("Constants : {}".format(OBJ.constants))
    print("Facts : {}".format(OBJ.facts))
    print("Rules : {}".format(OBJ.conditionals))
