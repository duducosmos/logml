#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Verify Nacionalidade.
By: E. S. Pereira
Version: 0.0.1
Date: 08/09/2017
"""


from inferencemachine import InferenceMachine

OBJ = InferenceMachine("./database/nacionalidade.logml")
#print(OBJ.question("estado", "sp", "x"))
#print(OBJ.question("estado", "x", "brasil"))
#print(OBJ.question("nasceu", "x", "sp"))
print(OBJ.question("nacionalidade"))
print("\n")
print(OBJ.question("brasileiro"))
