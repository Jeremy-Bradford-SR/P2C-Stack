import sys, os
sys.path.append(os.path.join(os.getcwd(), 'P2CScripts'))
import shared_utils
api = shared_utils.APIClient()

print("Initial Counts:")
q1 = api.post("data/query", "SELECT COUNT(*) as c FROM DailyBulletinArrests")
print("Total rows:", q1.get("data", [{}])[0].get("c"))

q2 = api.post("data/query", "SELECT COUNT(*) as c FROM DailyBulletinArrests WHERE event_time = '1900-01-01 00:00:00.0000000'")
print("1900-01-01 rows:", q2.get("data", [{}])[0].get("c"))

print("\nUpdating...")
api.post("data/query", "UPDATE DailyBulletinArrests SET event_time = NULL WHERE event_time = '1900-01-01 00:00:00.0000000'")

q3 = api.post("data/query", "SELECT COUNT(*) as c FROM DailyBulletinArrests WHERE event_time IS NULL")
print("NULL rows after update:", q3.get("data", [{}])[0].get("c"))
