import psycopg2 as ps

host='127.0.0.1'
port="5432"
db="postgres"
user="pg"
password="admin"

def getDbObject():
    connection=ps.connect(database=db, user=user, password=password, host=host, port=port)
    return connection


def insert(img1):
    try:
        conn=getDbObject()
        cursor=conn.cursor()
        sql="insert into vectors(vector) values(cube(array"+str(img1)+"))"
        print(sql)
        cursor.execute(sql)
    except Exception as e:
        print("Exception while saving vector "+str(e))

   
