#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Inference system from logml file.
By: E. S. Pereira
Version: 0.0.1
Date: 08/09/2017
"""

from gettext import gettext as _
from copy import copy
from numpy import where, array, array_equal
import pydot


from .parser import Parser
from .exceptions import InputArgsSizeError, NoDefinedDynamicClass
from .connector import Connector


from .treedata import Node
from .commonsearch import in_common, concatenate_result


def _search_facts(fact, predicate, args, argi):
    subset = []
    for j in args:
        if j in argi:
            index = where(args == j)[0][0]
            seai = where(
                fact[predicate][:, index] == j)[0]
            if not subset:
                subset = set(seai)
            else:
                subset = subset & set(seai)

            if not list(seai):
                argsi = ",".join(list(args))
                neg = _("not({0}({1}))".format(
                    predicate, argsi))
                return False, neg
        else:

            index = where(args == j)[0][0]
            seai = set(range(fact[predicate][:, index].size))

            if not subset:
                subset = set(seai)
            else:
                subset = subset & set(seai)

    if not subset:
        argsi = ",".join(list(args))
        neg = _("not({0}({1}))".format(
            predicate, argsi))
        return False, neg

    return True, fact[predicate][list(subset)]


def plotTree(all_edge, img="test.png"):
    graph = pydot.Dot(graph_type='graph')
    for edi in all_edge:
        edge = pydot.Edge(edi[0], edi[1])
        graph.add_edge(edge)
    graph.write_png(img)


class InferenceMachine(object):
    """
    Inference Machine for logml
    """

    def __init__(self, logml_file):
        self._parser = Parser(logml_file)
        self.facts = self._parser.get_array_facts()
        self.predicates = [list(i.keys())[0] for i in self._parser.predicates]
        self.rules = self._parser.conditionals
        self.dynamic_facts = self._parser.get_dynamic_facts()
        self.dynamic_facts_func = {}
        self.graph = []

    def know_about(self):
        """Return the list of predicates."""

        know = [list(i.keys())[0] for i in self._parser.predicates]
        print(_("I know about: "))

        for pred in self._parser.predicates:
            value = list(pred.items())[0][1]
            mainword = value.split("#")[1].lower()
            print("pred: {0}; meta: {1}".format(
                list(pred.keys())[0], _(mainword)))
        return know

    def _search_facts(self, predicate, args, argi):

        return _search_facts(self.facts, predicate, args, argi)

    def _get_facts(self, predicate, *args, **kwargs):

        if "precise" in kwargs:
            precise = kwargs["precise"]
        else:
            precise = False

        if predicate in self.dynamic_facts:
            self.set_dynamic_fact(predicate)

        args = args[0]

        argi = array(
            [argi for argi in args if argi in self._parser.constants])

        dinfact = self.facts[predicate].shape

        if len(dinfact) == 1:
            self.facts[predicate] = array([list(self.facts[predicate])])

        dinfact = self.facts[predicate].shape

        if len(args) != dinfact[1]:
            raise InputArgsSizeError(_("Input Args not correspondet to: ")
                                     + predicate)
        args = array(args)

        search = where((self.facts[predicate] == args).all(axis=1))
        search = self.facts[predicate][search]
        if search.size:
            return True, search

        else:

            if array_equal(argi, args):
                argsi = ",".join(list(argi))
                neg = _("not({0}({1}))".format(predicate, argsi))
                return False, neg
            else:
                if argi.size:
                    found, ans = self._search_facts(predicate, args, argi)
                    return found, ans

        if precise:
            argsi = ",".join(list(args))
            neg = _("not({0}({1}))".format(predicate, argsi))
            return False, neg

        return True, self.facts[predicate]

    def walk_tree_df_postorder(self, node, visit):
        """
        Depth-first post-order.
        """
        for child in node.children:
            self.walk_tree_df_postorder(child, visit)
        visit(node)

    def visit(self, node):
        """
        Set result in node.
        """
        for key in node.data:
            if node.parente:
                self.graph.append((list(node.parente.data.keys())[0], key))
            if key in self.facts:
                result = self._get_facts(key, node.data[key])
                node.parente.children_result += [result]
                node.parente.children_args += [node.data[key]]
                node.result = result
            else:

                if node.level > 0:
                    node.parente.children_args += [node.data[key]]

                result = [res[1] for res in node.children_result]

                if len(result) == 1 and len(node.data[key]) == 1:
                    node.result = result[0]
                    return

                common, uniao = in_common(
                    result, node.children_args, node.data[key])

                # Falta verificar as variáveis pedidas e qual deve ser o perfil
                # De saída, dado o head.

                if len(node.data[key]) == 1:
                    node.result = common
                else:
                    if not uniao:
                        node.result = common
                    else:
                        concatenate_result(node, result, uniao, common, key)

                if node.level > 0:
                    if node.result.tolist():
                        node.parente.children_result += [(True, node.result)]

    def __compare_to_replace(self, args, genargs, bdi):
        for kbdi, arg in bdi.items():
            if any(k in genargs for k in arg):
                for argi in args:
                    if argi in self._parser.constants:

                        arg_index = args.index(argi)
                        change = genargs[arg_index]
                        if change in bdi[kbdi]:
                            gen_index = bdi[kbdi].index(change)
                            bdi[kbdi][arg_index] = args[gen_index]

    def __replace_const(self, node, pred):
        head, body = self._parser.expanding_rule(pred)

        for key in node.data:
            args = node.data[key]
            genargs = head[key]

            for bdi in body:
                self.__compare_to_replace(args, genargs, bdi)

        return body

    def _add_child(self, node):

        for key in node.data:
            if key not in self.facts:
                print(key, node.data)
                body = self.__replace_const(node, key)
                for bdi in body:
                    for key_j in bdi:
                        if key_j not in self.facts:
                            tmp = Node(bdi)
                            tmp.level = node.level + 1
                            tmp.add_parent(node)
                            node.add_child(tmp)
                            self.__add_child(node)

                        if key_j in self.facts:

                            tmp = Node(bdi)
                            tmp.level = node.level + 1
                            tmp.add_parent(node)
                            node.add_child(tmp)

    def __add_child(self, node):
        if node.children:
            for subnode in node.children:
                self._add_child(subnode)

    def tree_rule(self, predicate):
        """
        Generate three of rule
        """
        self.graph = []

        if predicate in self.facts:
            return self._get_facts(predicate)
        else:
            head, body = self._parser.expanding_rule(predicate)
            with Node(head) as root:
                root = Node(head)
                for data in body:
                    tmp = Node(data)
                    tmp.level = root.level + 1
                    tmp.add_parent(root)
                    root.add_child(tmp)
                self.__add_child(root)

                self.walk_tree_df_postorder(root, self.visit)
                result = copy(root.result)

        return result

    def set_dynamic_fact_interface(self, predicate, connector):
        """
        The function must be return a list of args for a dynamic fact.
        Connector must be a callable Class with the method get_args.
        """
        predargs = self.dynamic_facts[predicate]

        self.dynamic_facts_func[predicate] = connector
        self.dynamic_facts_func[predicate].set_args(args=predargs)

    def set_dynamic_fact(self, predicate):
        """
        Define dynamicaly the current values of fact
        """

        if predicate in self.dynamic_facts_func:
            self.facts[predicate] = \
                self.dynamic_facts_func[predicate].gets_args()
        else:
            raise NoDefinedDynamicClass(
                _("No defined class for dynamic fact: ") + predicate)

    def question(self, predicate, *args, **kwargs):
        """
        Given a text make a query in logml file.
        """

        if "precise" in kwargs:
            precise = kwargs["precise"]
        else:
            precise = False

        if predicate in self.facts:
            facts = None

            if predicate in self.dynamic_facts:
                self.set_dynamic_fact(predicate)

            if args:
                facts = self._get_facts(predicate, args, precise=precise)[1]
            else:
                facts = self.facts[predicate]

            return facts

        if predicate in self.rules:
            return self.tree_rule(predicate)


if __name__ == "__main__":

    OBJ = InferenceMachine("./database/crossroad.json")
    OBJ.set_dynamic_fact_interface("traffic_light", Connector())
    print(OBJ.question("cross_road"))
