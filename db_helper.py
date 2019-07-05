import psycopg2 as ps


host='127.0.0.1'
port="5432"
db="test"
user="pg"
password="admin"

def getDbObject():
    connection=ps.connect(database=db, user=user, password=password, host=host, port=port)
    return connection
