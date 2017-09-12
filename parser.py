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
from  collections import OrderedDict
import warnings
from unicodedata import normalize
from gettext import gettext as _

from exceptions import OnlyOneClausure, OnVarNeed, NoVarConstFound, NoRecursionPermited

from validators import validate_meta, validate_meta_star
from numpy import array

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


def get_clausures(axioms):
    """
    Separete clausures tipe from axioms.
    """
    clausures = OrderedDict()
    for axiom in axioms:
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


def _facts_array(constants):
    tmp = []

    if isinstance(constants, dict):
        return array(constants["1"])

    for const in constants:
        tmp.append(const["1"])
    return array(tmp)


class Parser(object):
    """
    The logml parser.
    """

    def __init__(self, logml_file):
        self.clausures = get_clausures(get_axioms(logml_file))
        self.facts = self.get_facts()
        self.constants = self.get_constants()
        self.gols = self.get_gols()
        self.conditionals = self.get_condictionals()
        for predicate in self.conditionals:
            self.validate_conditional(predicate)
            #self.expanding_rule(predicate)

        self.predicates = self.get_predicates()

    def get_array_facts(self):
        """
        Return a dict of facts and corresponding array of facts
        """
        facts = OrderedDict()
        for fact in self.facts:
            facts[fact] = _facts_array(self.facts[fact])
        return facts

    def _not_declared_predict(self, predicate):
        if predicate not in self.facts:
            if predicate not in self.conditionals:
                raise NameError(_("\"{}\" not declared".format(predicate)))
        return False

    def _get_body(self, comp, head_pred):
        body = []
        all_vars = []
        for key, value in comp.items():
            if key == head_pred:
                raise NoRecursionPermited(_("No recursion permited: ") + head_pred)

            if isinstance(value, list):

                for arg in value:
                    all_vars += arg["1"]
                    const_in_body = [
                        i for i in arg["1"] if i in self.constants]

                    if const_in_body:
                        body.append(
                            {key: arg["1"], "const": const_in_body})
                    else:
                        body.append({key: arg["1"]})

            else:
                const_in_body = [i for i in value["1"]
                                 if i in self.constants]
                all_vars += value["1"]

                if const_in_body:
                    body.append(
                        {key: value["1"], "const": const_in_body})
                else:
                    body.append({key: value["1"]})

        return body, all_vars


    def expanding_rule(self, predicate):
        """
        Separete head, body of a rule
        """

        head = OrderedDict()
        in_head = []
        all_vars = []

        for comp in self.conditionals[predicate]:
            if "1" in comp:
                in_head = comp["1"]
                all_vars += in_head

                head[predicate] = in_head
                const_in_head = [i for i in in_head if i in self.constants]
                if len(in_head) == len(const_in_head):
                    raise OnVarNeed(
                        _("No vars found in the head of: {}".format(predicate)))
                if not in_head:
                    NoVarConstFound(
                        _("No vars or constants found in {}".format(predicate)))
            else:
                body = self._get_body(comp, predicate)
                all_vars += body[1]
                body = body[0]

        for i in list(set(all_vars)):
            if all_vars.count(i) == 1:
                warnings.warn(
                    _("Warning: Singleton variable {0} in {1}".format(i, predicate)),
                    SyntaxWarning
                    )

        return head, body

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
            gols = OrderedDict()
            for gol in self.clausures["gol"]:
                gols[remover_acentos(gol['body']["pred"]["@class"])] = \
                    _parse_li(gol['body']["pred"]["li"])
            return gols

    def get_condictionals(self):
        """Get All conditional"""

        if "conditional" in self.clausures:
            conditionals = OrderedDict()

            for conditional in self.clausures["conditional"]:
                bodyi = conditional['body']["pred"]
                body = OrderedDict()

                if isinstance(bodyi, list):
                    for bi in bodyi:
                        body[bi["@class"]] = _parse_li(bi["li"])
                else:
                    body[bodyi["@class"]] = _parse_li(bodyi["li"])

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
            unconditionals = OrderedDict()
            for unconditional in self.clausures['fact']:
                facts = unconditional['head']["pred"]

                if isinstance(facts, list):
                    for fts in facts:
                        fts_li = _parse_li(fts["li"])
                        unconditionals[remover_acentos(fts["@class"])] = fts_li
                else:
                    fts_li = _parse_li(fts["li"])
                    unconditionals[remover_acentos(unconditional['head']["pred"]["@class"])] = \
                        fts_li
            return unconditionals


if __name__ == "__main__":
    OBJ = Parser("./database/teste_extended.logml")
    print("Predicados : {}".format(OBJ.get_predicates()))
    print("Constants : {}".format(OBJ.constants))
    print("Rules : {}".format(OBJ.conditionals))
    print("Facts : {}".format(OBJ.facts))
