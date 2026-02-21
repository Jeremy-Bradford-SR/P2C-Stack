with open('/Users/jeremy/devroot/P2C-Stack/P2CScripts/scripts/ETL/backfill_geocoding.py', 'r') as f:
    lines = f.readlines()

for i in range(175, 289):
    if lines[i].strip():
        lines[i] = '    ' + lines[i]

with open('/Users/jeremy/devroot/P2C-Stack/P2CScripts/scripts/ETL/backfill_geocoding.py', 'w') as f:
    f.writelines(lines)
