#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Suport module to InferenceMachine
By: E. S. Pereira
Version: 0.0.1
Date: 12/09/2017
"""

from functools import reduce
from itertools import product
from numpy import where, array, intersect1d, concatenate


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


def in_common(result, args):
    """
    Given a list o result and a list of args, return the common elements
    where the relation is mapping by args.
    """
    uniao = None
    if len(args) == 1:
        return result[0]

    for i in args:
        if uniao is None:
            uniao = set(i)
        else:
            uniao = uniao & set(i)
    uniao = list(uniao)
    to_search = [where(array(i) == uniao)[0] for i in args]
    tmp = [result[j][:, to_search[j]] for j in range(len(result))]
    common = array(reduce(intersect1d, tmp))
    print(common)

    return common, uniao


def concatenate_result(node, result, uniao, common, predicate):
    '''
    Given a array of results, the union args, the common values and a predicate
    concatenete the body result in a new result.
    '''

    tmp = []
    for i, item in enumerate(result):
        test = node.children_args[i][:]
        for uni in uniao:
            if uni in test:
                test.remove(uni)

        if test:
            tmp2 = []
            for cmi in common:
                for uni in uniao:
                    to_get = where(~(array(node.children_args[i]) == uni))[0]
                    to_search = where(array(node.children_args[i]) == uni)[0]
                    tmp2 += item[:, to_get][where(item[:, to_search] == cmi)[0]].T.tolist()

            tmp.append(tmp2)
        else:

            if [node.data[predicate].index(uni) for uni in uniao
                    if uni in node.data[predicate]]:
                listcommon = [[cmk] for cmk in common.T.tolist()]
                tmp.append(listcommon)
    tmp2 = []

    for i in range(len(tmp[0])):
        tmp2.append(
            array(list(product(*[tmp[j][i] for j in range(len(tmp))]))))
    if tmp2:
        node.result = concatenate(tmp2)
