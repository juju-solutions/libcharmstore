
import os
import json


CHARM = None
BUNDLE = None

CWD = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(CWD, 'charm.json')) as f:
    CHARM = json.loads(f.read())

with open(os.path.join(CWD, 'bundle.json')) as f:
    BUNDLE = json.loads(f.read())
