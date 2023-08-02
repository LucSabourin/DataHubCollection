import pyodbc, os

server_name = os.getenv('SQL_DB_SERVER')
server = f'{server_name}.database.windows.net'
database = os.getenv('SQL_DB_DATABASE')
username = os.getenv('SQL_DB_USERNAME')
password = os.getenv('SQL_DB_PASSWORD')
driver = '{ODBC Driver 17 for SQL Server}'

"""
conn_str = 'DRIVER{0}'
conn_str += ';SERVER=' + server
#conn_str += ',1433'
#conn_str += ';POST=1433'
conn_str += ';DATABASE=' + database
conn_str += ';UID=' + username
conn_str += ';PWD=' + password
#conn_str += ';Encrypt=True'
#conn_str += ';TrustServerCertificate=no'
#conn_str += ';Connection Timeout=30'

for driver in pyodbc.drivers():
"""

print(pyodbc.drivers())

print(server)
print(database)
print(username)
print(password)
print()

conn_str = 'DRIVER=' + driver
conn_str += ';SERVER=' + server
#conn_str += ',1433'
#conn_str += ';POST=1433'
conn_str += ';DATABASE=' + database
conn_str += ';UID=' + username
conn_str += ';PWD=' + password
#conn_str += ';Encrypt=True'
#conn_str += ';TrustServerCertificate=no'
#conn_str += ';Connection Timeout=30'

print(conn_str)
print()

with pyodbc.connect(conn_str) as sql_conn:
    with sql_conn.cursor() as cursor:
        cursor.execute('SELECT TOP 3 name, collation_name FROM sys.databases')
        row = cursor.fetchone()
        while row:
            print(str(row[0]) + ' ' + str(row[1]))
            row = cursor.fetchone()