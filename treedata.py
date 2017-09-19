#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Suport module to InferenceMachine
By: E. S. Pereira
Version: 0.0.1
Date: 12/09/2017
"""


class Node(object):
    """
    Tree of rule
    """
    level = 0

    def __init__(self, data):
        self.data = data
        self.result = None
        self.children = []
        self.parente = None
        self.children_result = []
        self.children_args = []

    def __enter__(self):
        pass

    def __exit__(self, type_, value, traceback):
        self.children = []
        self.parente = None
        self.children_result = []
        self.children_args = []

    def add_child(self, obj):
        """
        add child
        """
        self.children.append(obj)

    def add_parent(self, obj):
        """
        Set the parent reference
        """
        self.parente = obj
