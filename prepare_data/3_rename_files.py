#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

path = 'data/gempundit_nohands'
# rename files in subfolders to the name of the subfolder + a number
for root, dirs, files in os.walk(path):
    if len(files) > 0:
        for i, f in enumerate(files):
            os.rename(os.path.join(root, f), os.path.join(root, root.split(os.sep)[-1] + '_' + str(i) + '.jpg'))
