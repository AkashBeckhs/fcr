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
    conn=getDbObject()
    cursor=conn.cursor()
    try:
        sql="insert into vectors(vector) values(cube(array"+str(img1)+"))"
        print(sql)
        print("excuting sql......!")
        cursor.execute(sql)
        print("sql executed")
        conn.commit()            
    except Exception as e:
        print("Exception while saving vector "+str(e))
    finally:
        conn.close()


def checkImage(img):
    conn=getDbObject()
    cursor=conn.cursor()
    try:
        sql="SELECT id from vectors where (cube(array"+str(img)+") <-> vector)<=0.52 limit 1"
        print(sql)
        cursor.execute(sql)
        rows=cursor.fetchall()
        return rows
    except Exception as e:
        print("Exception while fetching "+str(e))
        return None
    finally:
        conn.close()


def insertIntoFcr(enc,img_path,qr_code,unique_id):
    conn=getDbObject()
    cursor=conn.cursor()
    try:
        sql="INSERT INTO fcr(encodings,img_path,qr_code_path,unq_id) values(array"+str(enc)+",'"+img_path+"','"+qr_code+"',"+str(unique_id)+")"
        print(sql)
        cursor.execute(sql)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()
    

   
