import pyodbc, os

#from models.exceptions.exceptions import ServerError

server_name = os.getenv('SQL_DB_SERVER')
server = f'{server_name}.database.windows.net'
database = os.getenv('SQL_DB_DATABASE')
username = os.getenv('SQL_DB_USERNAME')
password = os.getenv('SQL_DB_PASSWORD')

def generate_connect_str() -> str:
    connect_str = 'SERVER=' + server + ';'
    connect_str += 'DATABASE=' + database + ';'
    connect_str += 'UID=' + username + ';'
    connect_str += 'PWD=' + password
    for driver in pyodbc.drivers():
        if 'ODBC' in driver:
            connect_str = 'DRIVER={' + driver + '};' + connect_str
            return connect_str

def connect_sql(autocommit = False) -> pyodbc.Connection:
    connect_str = generate_connect_str()
    try:
        return pyodbc.connect(connect_str, autocommit=autocommit)
    except pyodbc.ProgrammingError as msg:
        #raise ServerError('99 -> Could not connect to server.')
        raise Exception('99 -> Could not connect to server.')

def create_db(db_name: str):
    sql_command = f"CREATE DATABASE [{db_name}]"
    try:
        connection = connect_sql(autocommit=True)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        cursor.close()
        connection.close()
    except pyodbc.ProgrammingError as msg:
        #raise ServerError('99 -> Tried to make database that already exists.')
        raise Exception('99 -> Tried to make a database that already exists.')

def drop_db(db_name: str):
    sql_command = f"DROP DATABASE [{db_name}]"
    try:
        connection = connect_sql(autocommit=True)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        cursor.close()
        connection.close()
    except pyodbc.OperationalError as msg:
        #raise ServerError('99 -> Tried to delete a database that does not exist')
        raise Exception('99 -> Tried to delete a database that does not exist')

def create_table(db_name: str, table_name: str):
    sql_command = f""
    connect_sql().execute(sql_command)

def get_from_sql(location):
    pass

if __name__ == '__main__':
    #connect_sql()
    create_db('TEST_DB2')
    print('Database Created!')

    drop_db('TEST_DB2')
    print('Database Dropped!')
