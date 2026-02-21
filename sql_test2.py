import pyodbc
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=mssql,1433;DATABASE=P2C_Dashboard;UID=sa;PWD=MyP@ssword!2024;TrustServerCertificate=yes')
cursor = conn.cursor()
cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'DailyBulletinArrests'")
columns = cursor.fetchall()
for col in columns: print(col[0], col[1])
