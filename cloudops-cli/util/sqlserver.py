import pyodbc

def get_connection(server, username, password):
    return pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=%s;'
                          'uid=%s;'
                          'pwd=%s;' % (server, username, password))

def execute_sql(conn, sql, *args):
    with conn.execute(sql, *args) as cursor:
        # Each row is an array, convert each to a dictionary using column information from the cursor
        return [dict(zip([column[0] for column in cursor.description], row))
                for row in cursor.fetchall()]