#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
The validate functions of meta-language.
Given a logml file, return the sintatic structure.
By: E. S. Pereira
Version: 0.0.1
Date: 31/08/2017
"""

from .exceptions import NoKeyExpressionFounded, InvalidKeyExpressionFounded
from .exceptions import InconsistenNumberOfArgsIFacts, EmptyFact
from .exceptions import NoClosedKeyExpression


def validate_meta(frase, predicate):
    """
    Validate main text in meta-language
    """
    if "#" not in frase:
        raise NoKeyExpressionFounded(
            "No # simbol found in {}".format(predicate))
    if frase.count("#") > 2:
        raise InvalidKeyExpressionFounded(
            "More than 2 # simbol found in {}".format(predicate))
    if frase.count("#") == 1:
        raise NoClosedKeyExpression(
            "No closed # simbol found in {}".format(predicate))

def validate_meta_star(frase, predicate, args):
    """
    Validade change simbol in meta-language
    """
    if isinstance(args, list):
        tmp = list(set([len(ai["dynamic"]) for ai in args if "dynamic" in ai]))
        args = tmp + list(set([len(ai["1"]) for ai in args if "1" in ai]))
    else:
        args = list(set([len(args["1"])]))

    if len(args) > 1:
        raise InconsistenNumberOfArgsIFacts(
            "Number of args inconsisten in {}".format(predicate)
        )

    if not args:
        raise EmptyFact(
            "No args found in {}".format(predicate)
        )


    if "*" not in frase:
        raise NoKeyExpressionFounded(
            "No * simbol found in {}".format(predicate))
    if frase.count("*") > args[0]:
        raise InvalidKeyExpressionFounded(
            "More * than constants in {}".format(predicate))
    if frase.count("*") < args[0]:
        raise InvalidKeyExpressionFounded(
            "Less * than constants in {}".format(predicate))
