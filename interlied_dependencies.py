"""This script downloads all dependencies you require to run the script."""

import sys
import subprocess
import pkg_resources
# 'os-sys'-what's up?

#ADD OS-SYS & PYCOPY-COPY
required = {'numpy','pandas','music21','nltk','matplotlib','python-csv',
            'more-itertools','heapq_max','glob2','tk','Pillow',
            'pyLDAvis==2.1.2','gensim','nltk','notebook', 'ipython','pyoperators',
            'random2', 'tk', 'pathlib', 'pandastable' }

installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',*missing])
