#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Verify Criminal.
By: E. S. Pereira
Version: 0.0.1
Date: 08/09/2017
"""


from inferencemachine import InferenceMachine

OBJ = InferenceMachine("./database/criminal.logml")
#print(OBJ.rules)
print(OBJ.question("produce"))
print(OBJ.question("sells"))
print(OBJ.question("criminal"))
