#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Inference system from logml file.
By: E. S. Pereira
Version: 0.0.1
Date: 08/09/2017
"""


from inferencemachine import InferenceMachine
from connector import Connector


OBJ = InferenceMachine("./database/crossroad.json")
OBJ.set_dynamic_fact_interface("traffic_light", Connector())
print(OBJ.question("cross_road"))


OBJ = InferenceMachine("./database/teste_extended.json")
print(OBJ.question("mulher", "marta"))
print(OBJ.question("mulher", "mariano"))
print(OBJ.question("parente", "tony", "x"))
print(OBJ.question("parente", "tony", "sara"))
print(OBJ.question("parente", "tony", "dino"))
print(OBJ.question("quadrado"))
print(OBJ.question("quadrado", "3", "2", "x"))
print(OBJ.question("quadrado", "2", "3", "25"))
print(OBJ.question("quadrado", "3", "2", "25"))


print(OBJ.question("parente", "y", "x"))
print(OBJ.question("avo"))

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
print("\ntataravoh")
print(OBJ.question("tataravoh"))
print("\ntetraravo")
print(OBJ.question("tetraravo"))


print("\nfarol")
#OBJ.set_dynamic_fact_interface("farol", Connector())
#print(OBJ.question("farol"))
#print("\nmudar_estado")
#print(OBJ.question("mudar_estado"))
