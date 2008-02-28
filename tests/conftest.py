import sys
import os
import shutil
import pkg_resources

here = os.path.dirname(__file__)
base = os.path.dirname(here)

sys.path.append(here)
sys.path.insert(0, base)

here = os.path.dirname(__file__)

pkg_resources.working_set.add_entry(base)

