#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Especifc exeptions of logml file.
By: E. S. Pereira
Version: 0.0.1
Date: 22/08/2017
"""


class OnlyOneClausure(Exception):
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