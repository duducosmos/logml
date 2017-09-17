#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Abstract class to create a connector to real time fact update
By: E. S. Pereira
Version: 0.0.1
Date: 08/09/2017
"""
from random import choice

from numpy import array


class Connector(object):
    """
    Dynamic update of a fact
    """

    def __init__(self):
        self.pred_args = None

    def set_args(self, args):
        """
        Set the args of Dynamic facts
        """
        self.pred_args = args

    def gets_args(self):
        """
        Return the new args of a fact.
        """
        tmp = []
        for i in self.pred_args:
            tmp2 = []
            for _ in i:
                tmp2.append(choice(["red", "yellow", "green"]))
            tmp.append(tmp2)

        return array(tmp)
