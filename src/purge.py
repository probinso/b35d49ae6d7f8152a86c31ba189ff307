#!/usr/bin/env python3

import shutil
from utility import _path_resource

PATH = _path_resource()
shutil.rmtree(PATH)
