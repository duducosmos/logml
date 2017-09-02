#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Inference system from logml file.
By: E. S. Pereira
Version: 0.0.1
Date: 01/09/2017
"""

import gettext
import os


LOCALEDIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')


LANGUAGES = ["pt_BR"]

LANGUAGE = gettext.translation("inference", LOCALEDIR,
                               languages=LANGUAGES,
                               fallback=True)

_ = LANGUAGE.gettext
print(_("I know about: "))
