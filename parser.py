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
import xmltodict
from unicodedata import normalize



IS_PYTHON3 = sys.version_info.major == 3
if IS_PYTHON3:
    unicode = str
    def remover_acentos(txt):
        return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')
else:
    def remover_acentos(txt, codif='utf-8'):
        return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')





class Parser:
    """
    The logml parser.
    """
    def __init__(self, logml_file):
        self.logml_file = logml_file
        self.axioms = self.get_axioms()
        self.clausures = self.get_clausures()
        self.facts = self.get_facts()
        self.gols = self.get_gols()
        self.conditionals = self.get_condictionals()

    def __parse_li(self, arg):
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

    def get_predicates(self):
        """
        Return a list of predicates in the logml file.
        Represent the questions that the sistem can responds.
        """
        predicates = []
        if self.facts is not None:
            predicates += self.facts.keys()

        if self.gols is not None:
            predicates += self.gols.keys()

        if self.conditionals is not None:
            predicates += self.conditionals.keys()
        return [remover_acentos(i) for i in predicates]


    def get_gols(self):
        """Get All gols in the logml file"""
        if 'gol' in self.clausures:
            gols = {}
            for gol in self.clausures["gol"]:
                gols[remover_acentos(gol['body']["pred"]["@class"])] = \
                    self.__parse_li(gol['body']["pred"]["li"])
            return gols


    def get_condictionals(self):
        """Get All conditional"""

        if "conditional" in self.clausures:
            conditionals = {}

            for conditional in self.clausures["conditional"]:
                body = conditional['body']["pred"]

                if isinstance(body, list):
                    body = {bi["@class"]: self.__parse_li(bi["li"]) for bi in body}
                else:
                    body = {body["@class"]: self.__parse_li(body["li"])}



                head_li = self.__parse_li(conditional['head']["pred"]["li"])
                if isinstance(head_li, list):
                    if len(head_li) > 1:
                        raise NameError("Conditional with two predicates in head")

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
                        fts_li = self.__parse_li(fts["li"])
                        unconditionals[remover_acentos(fts["@class"])] = fts_li
                else:
                    unconditionals[remover_acentos(unconditional['head']["pred"]["@class"])] = \
                            self.__parse_li(facts["li"])
            return unconditionals

    def get_axioms(self):
        """
        Return all Axioms from a File
        """
        axioms = None
        with open(self.logml_file, 'r') as logml:
            result = xmltodict.parse(logml.read())
            if "axiom" in result["logml"]:
                axioms = result["logml"]["axiom"]
        return axioms

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
    OBJ = Parser("./teste.logml")
    print("\nFatos: {}\n".format(OBJ.get_facts()))
    print("Condicionais: {}\n".format(OBJ.get_condictionals()))
    print("Clausulas  gol: {}\n".format(OBJ.get_gols()))
    print("Predicados : {}".format(OBJ.get_predicates()))
