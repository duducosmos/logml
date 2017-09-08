#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Especifc exeptions of logml file.
By: E. S. Pereira
Version: 0.0.1
Date: 22/08/2017
"""


class InputArgsSizeError(Exception):
    """
    Return Error when try to search facts or rules using no correspondet number of args.
    """
    pass

class OnlyOneClausure(Exception):
    """
    Return Error when it is use more than one Clausure in comman  in class.
    """
    pass

class OnVarNeed(Exception):
    """
    Return Error when no var is found in head of rule.
    """
    pass

class OnlyOneFactBySide(Exception):
    """
    Return Error when it is use more than one Clausure in comman  in class.
    """
    pass

class EmptyFact(Exception):
    """
    Return Error when it is use more than one Clausure in comman  in class.
    """
    pass

class NoVarConstFound(Exception):
    """
    Return Error when no var os constant found in Clausure.
    """
    pass

class InconsistenNumberOfArgsIFacts(Exception):
    """
    Return Error when it is use more than one Clausure in comman  in class.
    """
    pass


class NoKeyExpressionFounded(Exception):
    """
    Return Error when it is use more than one Clausure in comman  in class.
    """
    pass


class InvalidKeyExpressionFounded(Exception):
    """
    Return Error when it is use more than one Clausure in comman  in class.
    """
    pass


class NoClosedKeyExpression(Exception):
    """
    Return Error when it is use more than one Clausure in comman  in class.
    """
    pass
