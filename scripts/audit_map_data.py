import pyodbc
import os
import datetime

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

def run_audit():
    conn = get_db_connection()
    cursor = conn.cursor()

    print("--- Map Data Audit ---")
    print(f"Time: {datetime.datetime.now()}")
    print("-" * 30)

    # 1. CAD (Incidents)
    # Based on getIncidents in client.js (simplified)
    # It uses /incidents endpoint which queries cadHandler
    sql_cad = "SELECT COUNT(*) as total, SUM(CASE WHEN lat IS NOT NULL AND lon IS NOT NULL THEN 1 ELSE 0 END) as mapped FROM cadHandler"
    cursor.execute(sql_cad)
    row = cursor.fetchone()
    print(f"CAD (Incidents): Total={row.total}, Mapped={row.mapped} ({row.mapped/row.total*100:.1f}%)")

    # 2. Arrests
    # Based on getIncidents with arrestLimit (queries DailyBulletinArrests where key='AR')
    sql_arrest = "SELECT COUNT(*) as total, SUM(CASE WHEN lat IS NOT NULL AND lon IS NOT NULL THEN 1 ELSE 0 END) as mapped FROM DailyBulletinArrests WHERE [key] = 'AR'"
    cursor.execute(sql_arrest)
    row = cursor.fetchone()
    print(f"Arrests: Total={row.total}, Mapped={row.mapped} ({row.mapped/row.total*100:.1f}%)")

    # 3. Crime
    # Based on getIncidents with crimeLimit (queries DailyBulletinArrests where key='LW')
    sql_crime = "SELECT COUNT(*) as total, SUM(CASE WHEN lat IS NOT NULL AND lon IS NOT NULL THEN 1 ELSE 0 END) as mapped FROM DailyBulletinArrests WHERE [key] = 'LW'"
    cursor.execute(sql_crime)
    row = cursor.fetchone()
    print(f"Crime: Total={row.total}, Mapped={row.mapped} ({row.mapped/row.total*100:.1f}%)")

    # 4. Traffic
    # Based on getTraffic (queries DailyBulletinArrests where key != 'AR' and key != 'LW')
    sql_traffic = "SELECT COUNT(*) as total, SUM(CASE WHEN lat IS NOT NULL AND lon IS NOT NULL THEN 1 ELSE 0 END) as mapped FROM DailyBulletinArrests WHERE [key] != 'AR' AND [key] != 'LW'"
    cursor.execute(sql_traffic)
    row = cursor.fetchone()
    print(f"Traffic: Total={row.total}, Mapped={row.mapped} ({row.mapped/row.total*100:.1f}%)")

    # 5. Sex Offenders
    # Based on getSexOffenders (queries sexoffender_registrants)
    sql_so = "SELECT COUNT(*) as total, SUM(CASE WHEN lat IS NOT NULL AND lon IS NOT NULL THEN 1 ELSE 0 END) as mapped FROM sexoffender_registrants"
    cursor.execute(sql_so)
    row = cursor.fetchone()
    print(f"Sex Offenders: Total={row.total}, Mapped={row.mapped} ({row.mapped/row.total*100:.1f}%)")

    print("-" * 30)
    
    # Check recent data (last 7 days) to see if recent events are geocoded
    print("\n--- Recent Data (Last 7 Days) ---")
    
    seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    
    sql_cad_recent = f"SELECT COUNT(*) as total, SUM(CASE WHEN lat IS NOT NULL AND lon IS NOT NULL THEN 1 ELSE 0 END) as mapped FROM cadHandler WHERE starttime >= '{seven_days_ago}'"
    cursor.execute(sql_cad_recent)
    row = cursor.fetchone()
    print(f"CAD (Recent): Total={row.total}, Mapped={row.mapped} ({0 if row.total == 0 else row.mapped/row.total*100:.1f}%)")

    sql_arrest_recent = f"SELECT COUNT(*) as total, SUM(CASE WHEN lat IS NOT NULL AND lon IS NOT NULL THEN 1 ELSE 0 END) as mapped FROM DailyBulletinArrests WHERE [key] = 'AR' AND event_time >= '{seven_days_ago}'"
    cursor.execute(sql_arrest_recent)
    row = cursor.fetchone()
    print(f"Arrests (Recent): Total={row.total}, Mapped={row.mapped} ({0 if row.total == 0 else row.mapped/row.total*100:.1f}%)")
    
    sql_crime_recent = f"SELECT COUNT(*) as total, SUM(CASE WHEN lat IS NOT NULL AND lon IS NOT NULL THEN 1 ELSE 0 END) as mapped FROM DailyBulletinArrests WHERE [key] = 'LW' AND event_time >= '{seven_days_ago}'"
    cursor.execute(sql_crime_recent)
    row = cursor.fetchone()
    print(f"Crime (Recent): Total={row.total}, Mapped={row.mapped} ({0 if row.total == 0 else row.mapped/row.total*100:.1f}%)")

    sql_traffic_recent = f"SELECT COUNT(*) as total, SUM(CASE WHEN lat IS NOT NULL AND lon IS NOT NULL THEN 1 ELSE 0 END) as mapped FROM DailyBulletinArrests WHERE [key] != 'AR' AND [key] != 'LW' AND event_time >= '{seven_days_ago}'"
    cursor.execute(sql_traffic_recent)
    row = cursor.fetchone()
    print(f"Traffic (Recent): Total={row.total}, Mapped={row.mapped} ({0 if row.total == 0 else row.mapped/row.total*100:.1f}%)")

    conn.close()

if __name__ == "__main__":
    run_audit()
