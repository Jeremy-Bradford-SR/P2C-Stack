import sys, os, pyodbc
conn_str = "Driver={ODBC Driver 18 for SQL Server};Server=localhost,1433;Database=P2C;UID=sa;PWD=P2CSecurePassword2026!;TrustServerCertificate=yes;"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM DailyBulletinArrests")
total = cursor.fetchone()[0]
print(f"Total records in DB: {total}")

cursor.execute("SELECT [key], COUNT(*) FROM DailyBulletinArrests GROUP BY [key]")
print("\nBreakdown by key:")
for row in cursor.fetchall():
    print(f"Key: {row[0]}, Count: {row[1]}")

cursor.execute("SELECT COUNT(*) FROM DailyBulletinArrests WHERE id = '&nbsp;'")
nbsp_count = cursor.fetchone()[0]
print(f"\nRecords with '&nbsp;' as ID: {nbsp_count}")
