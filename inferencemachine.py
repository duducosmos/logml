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
import sys

from parser import Parser
from exceptions import InputArgsSizeError, NoDefinedDynamicClass
from connector import Connector

from numpy import where, array, array_equal

from treedata import Node, in_common, concatenate_result

IS_PYTHON3 = sys.version_info.major == 3
if IS_PYTHON3:
    from functools import lru_cache as memoize
else:
    from functools import wraps

    def memoize(function):
        '''
        Create a cache for function
        '''
        memo = {}

        @wraps(function)
        def wrapper(*args):
            '''
            Wrapper
            '''
            if args in memo:
                return memo[args]

            rvi = function(*args)
            memo[args] = rvi
            return rvi
        return wrapper


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

    def know_about(self):
        """
        Return the list of predicates.
        """
        know = [list(i.keys())[0] for i in self._parser.predicates]
        print(_("I know about: "))

        for pred in self._parser.predicates:
            value = list(pred.items())[0][1]
            mainword = value.split("#")[1].lower()
            print("pred: {0}; meta: {1}".format(
                list(pred.keys())[0], _(mainword)))
        return know

    def _search_facts(self, predicate, args, argi):
        subset = []
        for j in args:
            if j in argi:
                index = where(argi == j)[0][0]
                seai = where(
                    self.facts[predicate][:, index] == j)[0]
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
                seai = set(range(self.facts[predicate][:, index].size))

                if not subset:
                    subset = set(seai)
                else:
                    subset = subset & set(seai)

        if not subset:
            argsi = ",".join(list(args))
            neg = _("not({0}({1}))".format(
                predicate, argsi))
            return False, neg

        return True, self.facts[predicate][list(subset)]

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
        Depth-first post-order
        """
        for child in node.children:
            self.walk_tree_df_postorder(child, visit)
        visit(node)

    def visit(self, node):
        """
        Set result in node
        """
        for key in node.data:
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

                common, uniao = in_common(result, node.children_args)
                if len(node.data[key]) == 1:
                    node.result = common
                else:
                    concatenate_result(node, result, uniao, common, key)

                if node.level > 0:
                    if node.result.tolist():
                        node.parente.children_result += [(True, node.result)]

    def _add_child(self, node):
        for key in node.data:
            if key not in self.facts:
                body = self._parser.expanding_rule(key)[1]
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

    @memoize(maxsize=32)
    def tree_rule(self, predicate):
        """
        Generate three of rule
        """

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
            self.facts[predicate] = self.dynamic_facts_func[predicate].gets_args()
        else:
            raise NoDefinedDynamicClass(_("No defined class for dynamic fact: ") + predicate)


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
                facts = self._get_facts(predicate, args, precise=precise)
            else:
                facts = self.facts[predicate]

            return facts

        if predicate in self.rules:
            return self.tree_rule(predicate)


if __name__ == "__main__":




    OBJ = InferenceMachine("./database/teste_extended.logml")
    OBJ.set_dynamic_fact_interface("farol", Connector())


    '''
    print(OBJ.question("mulher", "marta"))
    print(OBJ.question("mulher", "mariano"))
    print(OBJ.question("parente", "tony", "x"))
    print(OBJ.question("parente", "tony", "sara"))
    print(OBJ.question("parente", "tony", "dino"))
    print(OBJ.question("quadrado"))
    print(OBJ.question("quadrado", "3", "2", "x"))
    print(OBJ.question("quadrado", "2", "3", "25"))
    print(OBJ.question("quadrado", "3", "2", "25"))
    '''

    #print(OBJ.question("parente", "y", "x"))
    # print(OBJ.question("avo"))
    '''
    print("\ngripe")
    print(OBJ.question("gripe"))
    print("\npai")
    print(OBJ.question("pai"))
    print("\nmae")
    print(OBJ.question("mae"))
    print("\nfilho")
    print(OBJ.question("filho"))
    print("\nmortal")
    print(OBJ.question("mortal"))
    print("\navoh")
    print(OBJ.question("avoh"))
    print("\nbisavo")
    print(OBJ.question("bisavo"))
    print("\nbisavoh")
    print(OBJ.question("bisavoh"))
    print("\ntataravo")
    print(OBJ.question("tataravo"))
    print("\ntetraravoh")
    print(OBJ.question("tataravoh"))
    print("\ntetraravo")
    print(OBJ.question("tetraravo"))
    '''

    print("\nfarol")
    print(OBJ.question("farol"))
    print("\nmudar_estado")
    print(OBJ.question("mudar_estado"))
