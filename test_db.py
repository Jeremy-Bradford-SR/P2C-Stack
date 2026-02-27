import sys, os
sys.path.append(os.path.join(os.getcwd(), 'P2CScripts'))
import shared_utils

api = shared_utils.APIClient()
res = api.get("tools/dab-time/candidates?count=10")
for r in res:
    print(r.get("TimeText"))
