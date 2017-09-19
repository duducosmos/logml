#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Search for common elements in matrix.
The search is based in logical programming filosophy
By: E. S. Pereira
Version: 0.0.1
Date: 12/09/2017
"""
from collections import OrderedDict

from functools import reduce
from itertools import product
from numpy import where, array, intersect1d, in1d, concatenate


def _sub_common(result, common, match, args, hargs):
    if len(hargs) == 1:
        for i in match:
            if match[i][1] == hargs:
                return common[i], []

    for j, argi in enumerate(args):
        if all(k in argi for k in hargs):
            for i in match:
                if match[i][0] == j:
                    to_get = [argi.index(hi) for hi in hargs]
                    to_search = argi.index(match[i][1][0])
                    lines = in1d(result[j][:, to_search], common[i]).nonzero()
                    finalr = concatenate([result[j][lines, tgi]
                                          for tgi in to_get]).T
                    break
    return finalr, []


def _in_common(result, args, hargs):
    common = []
    match = OrderedDict()

    for i, vali in enumerate(args):
        tmp = []
        for j, valj in enumerate(args[i + 1:], start=i + 1):
            if any(k in valj for k in vali):
                uniao = list(set(valj) & set(vali))
                match[i] = [j, uniao]
                to_search = [where(array(l) == uniao)[0] for l in [vali, valj]]
                tmp.append(result[i][:, to_search[0]])
                tmp.append(result[j][:, to_search[1]])
        if tmp:

            in_array = array(reduce(intersect1d, tmp))
            common.append(in_array)

    # if we have 4 inputs, and, we are compare each by each, the max size of the
    # Common list will be input size less one
    # If the size of common is lower than the size of args less one, for
    # some predicate, no value was found, and the rule is not true for all body component.

    if len(common) < len(args) - 1:
        return [], []

    return _sub_common(result, common, match, args, hargs)


def in_common(result, args, hargs):
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
    if uniao:
        to_search = [where(array(i) == uniao)[0] for i in args]
        tmp = [result[j][:, to_search[j]] for j in range(len(result))]
        common = array(reduce(intersect1d, tmp))

        return common, uniao

    return _in_common(result, args, hargs)


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
                    tmp2 += item[:,
                                 to_get][where(item[:, to_search] == cmi)[0]].T.tolist()

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
