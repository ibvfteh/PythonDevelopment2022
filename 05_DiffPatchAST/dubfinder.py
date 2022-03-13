from importlib import import_module
import inspect
import sys
from textwrap import dedent
import ast
from ast import unparse
from itertools import combinations
from difflib import SequenceMatcher

atribs = ['name', 'id', 'arg', 'attr']
prepared = {}

def recursion(pname, module):
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if not name.startswith('__'):
                recursion(pname + '.' + name, obj)
        elif inspect.isfunction(obj) or inspect.ismethod(obj):
            tree = ast.parse(dedent(inspect.getsource(obj)))
            for node in ast.walk(tree):
                for attr in atribs:
                    if hasattr(node, attr):
                        setattr(node, attr, '_')
            prepared[pname + "." + name] = ast.unparse(tree)


for module_name in sys.argv[1:]:
    module = import_module(module_name)
    recursion(module_name, module)

for prep1, prep2 in combinations(prepared.items(), r = 2):
    if SequenceMatcher(None, prep1[1], prep2[1]).ratio() > 0.95:
        print(prep1[0],":",prep2[0])
