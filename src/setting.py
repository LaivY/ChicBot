import json
import sys

with open('../settings.json', 'r') as f:
    setting = json.load(f)
if setting is None:
    sys.exit('error')
