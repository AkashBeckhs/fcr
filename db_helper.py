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
        #print(sql)
        #print("excuting sql......!")
        cursor.execute(sql)
        #print("sql executed")
        conn.commit()            
    except Exception as e:
        print("Exception while saving vector "+str(e))
    finally:
        conn.close()


def checkImage(img):
    conn=getDbObject()
    cursor=conn.cursor()
    try:
        sql="SELECT id,unq_id from fcr where (cube(array"+str(img)+") <-> vector)<=0.52 LIMIT 1"
        cursor.execute(sql)
        rows=cursor.fetchall()
        return rows
    except Exception as e:
        print("Exception while fetching "+str(e))
        return None
    finally:
        conn.close()


def insertIntoFcr(enc,img_path,qr_code,unique_id,status):
    conn=getDbObject()
    cursor=conn.cursor()
    try:
        sql="INSERT INTO fcr(vector,img_path,qr_code_path,unq_id,status) values(cube(array"+str(enc)+"),'"+img_path+"','"+qr_code+"',"+str(unique_id)+","+str(status).strip()+")"
        print(sql)
        cursor.execute(sql)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

def fetchDataOnId(id):
    resp=dict()
    conn=getDbObject()
    cursor=conn.cursor()
    try:
        sql="select unq_id,status,img_path,qr_code_path from fcr where unq_id="+str(id)
        cursor.execute(sql)
        rows=cursor.fetchall()
        for row in rows:
            resp['Unique_Id']=row[0]
            resp['status']=row[1]
            resp['image']=row[2]
            resp['qr_code']=row[3]
        return resp
    except Exception as e:
        print(e)
        resp['error']="There was some error"
    finally:
        conn.close()

def saveSixDigitVerificationCode(uid,code):
    conn=getDbObject()
    cursor=conn.cursor()
    try:
        sql="insert into verification_codes (uid,code) values("+uid+",'"+code+"')"
        cursor.execute(sql)
        return {"uid":uid,"code":code}
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

def checkSixDigitVerificationCode(code):
    resp=dict()
    conn=getDbObject()
    cursor=conn.cursor()
    try:
        sql="SELECT uid,code FROM verification_codes WHERE time > now() - interval '30 second' limit 1"
        cursor.execute(sql)
        rows=cursor.fetchall()
        for row in rows:
            resp['Unique_Id']=row[0]
            resp['Code']=row[1]
        return resp
    except Exception as e:
        print(e)
        return resp
    finally:
        conn.close()

        
    

   
