import pyodbc
import os
import re
from collections import Counter

def get_db_connection():
    """Establishes a database connection using settings from .env-db."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env-db')
    
    conn_str_raw = ""
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("ConnectionStrings__Default="):
                    conn_str_raw = line.strip().split("=", 1)[1]
                    break
    
    if not conn_str_raw:
        raise Exception("Could not find ConnectionStrings__Default in .env-db")

    parts = [p for p in conn_str_raw.split(';') if p]
    params = {}
    for p in parts:
        if '=' in p:
            k, v = p.split('=', 1)
            params[k.strip()] = v.strip()

    driver = "{ODBC Driver 18 for SQL Server}"
    server = params.get('Server')
    database = params.get('Database')
    uid = params.get('User Id')
    pwd = params.get('Password')
    trust_cert = params.get('TrustServerCertificate', 'no')
    if trust_cert.lower() == 'true':
        trust_cert = 'yes'
    
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={uid};PWD={pwd};TrustServerCertificate={trust_cert};"
    
    return pyodbc.connect(conn_str)

def analyze_misses():
    conn = get_db_connection()
    cursor = conn.cursor()

    print("Fetching sample of un-geocoded addresses from DailyBulletinArrests...")
    
    # Fetch samples from Arrests (Recent first to see what's failing now)
    sql = "SELECT TOP 2000 location FROM DailyBulletinArrests WHERE lat IS NULL AND location IS NOT NULL ORDER BY event_time DESC"
    cursor.execute(sql)
    addresses = [row.location for row in cursor.fetchall()]

    print(f"Analyzing {len(addresses)} addresses...")

    categories = Counter()
    examples = {}

    for addr in addresses:
        cat = "Unknown"
        
        # 1. Block Numbers
        if "BLK" in addr or re.search(r'\d+-', addr):
            cat = "Block Number"
        
        # 2. Intersections
        elif "/" in addr:
            cat = "Intersection"
            
        # 3. Mile Markers
        elif "MM " in addr or "MILE MARKER" in addr:
            cat = "Mile Marker"
            
        # 4. Highways
        elif "HWY" in addr or "US " in addr or "IA " in addr:
            cat = "Highway"
            
        # 5. Coordinates?
        elif re.search(r'-?\d+\.\d+', addr):
            cat = "Contains Coordinates"
            
        # 6. Short / Place Names
        elif len(addr) < 10:
            cat = "Short/Place Name"
            
        # 7. Standard Street Address (starts with digit, no slash)
        elif addr[0].isdigit():
            cat = "Standard Address"
            
        categories[cat] += 1
        if cat not in examples:
            examples[cat] = []
        if len(examples[cat]) < 5:
            examples[cat].append(addr)

    print("\n--- Categories of Misses ---")
    for cat, count in categories.most_common():
        print(f"{cat}: {count} ({count/len(addresses)*100:.1f}%)")
        for ex in examples[cat]:
            print(f"  - {ex}")
        print()

    conn.close()

if __name__ == "__main__":
    analyze_misses()
