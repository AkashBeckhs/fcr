import fc
import json
from flask import Flask, render_template, request,send_from_directory
from werkzeug.utils import secure_filename
from flask import jsonify
from flask import Response
import qrcode_qpi as qr
import time
from random import randint
import db_helper as db
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER']='data/uploads/'

@app.route('/upload')
def home():
   return render_template('/upload.html')


@app.route('/unlock')
def unlock():
   return render_template('/check.html')
	
def saveImage(image,name):
      try:
         image.filename="img_"+str(name)+".png"
         fileName=secure_filename(image.filename)
         imageFilePath="/data/uploads/"+str(image.filename)
         image.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
         return imageFilePath
      except Exception as e:
         print(e)
         return "FileNotSaved"

def getUniqueId():
   return randint(99999,1000000)


def registerImage(encodings,imageFilePath,unique_id,status):
   resp= dict()
   try:
      if status ==True:
         id=str(unique_id)
         st=str(status)
         qr_code="/data/"+qr.generateQrCode(st,id)
         db.insertIntoFcr(enc=encodings.tolist(),img_path=imageFilePath,qr_code=qr_code,unique_id=unique_id,status=status)
         resp['unique_id']=unique_id
         resp['error']="None"
         return resp
      else:
         resp['unique_id']="Not verified"
         resp['error']="None"
         return resp
   except Exception as e:
      print("inside register image")
      print(e)
      resp['error']=str(e)
      return resp

@app.route('/uploader/<flag>', methods = ['POST'])
def upload_file(flag="register"):
   print("Inside upload method")
   resp=dict()
   if request.method == 'POST':
      try:
         checkImage = request.files['check']
         verifyImage = request.files['verify']
         assert flag == request.view_args['flag']
         if flag =="register":
            uid=getUniqueId()
            imageFilePath=saveImage(checkImage,uid)
            startTime=time.time()
            result,encodings=fc.checkImage(checkImage,verifyImage)
            resp=registerImage(encodings,imageFilePath,uid,result[0])
            resp['Message']=str(result[0])
            endTime=time.time()
            print(endTime-startTime)
            return Response(json.dumps(resp),mimetype="application/json",status=200)
         else:
            result,encodings=fc.checkImage(checkImage,verifyImage)
            resp['Message']=str(result[0])
            return Response(json.dumps(resp),mimetype="application/json",status=200)
      except Exception as e:
         print(e)
         resp['Message']="There is some exception "+str(e)
         return Response(json.dumps(resp),mimetype="application/json",status=500)
      finally:
         checkImage.close()
         verifyImage.close()



@app.route("/fetch/<uid>",methods=['GET'])
def fetchData(uid):
    assert uid == request.view_args['uid']
    if uid is not None:
       resp=db.fetchDataOnId(uid)
       return Response(json.dumps(resp),mimetype="application/json",status=200)
    else:
      resp=dict()
      resp['Message']='No user found'
      return Response(json.dumps(resp),mimetype="application/json",status=200)
      
@app.route('/verify', methods = ['GET'])
def verifyImagePage():
   return render_template('/verify.html')

@app.route('/verify', methods = ['POST'])
def checkImage():
   print("Inside upload method")
   resp=dict()
   if request.method == 'POST':
      try:
         checkImage = request.files['check']
         if checkImage== None:
          resp['Message']="Please provide valid images."  
          return Response(json.dumps(resp),mimetype="application/json",status=403)
         rows=fc.verifyImage(checkImage)
         return Response(json.dumps(rows),mimetype="application/json",status=200)
      except Exception as e:
         resp['Message']="There is some exception "+str(e)
         return Response(json.dumps(resp),mimetype="application/json",status=500)


@app.route('/qrcode/<uid>',methods=['GET'])
def getQrCodePath(uid):
   assert uid == request.view_args['uid']
   resp= dict()
   try:
      fileName="qr_code_"+str(uid)
      fileName='%s.png' %fileName
      res=db.fetchDataOnId(uid)
      filePath=qr.generateQrCode(res['status'],res['Unique_Id'])
      print(filePath)
      return send_from_directory('data', filePath)
   except Exception as e:
      print(e)
      resp['Message']="There was some error"
      return Response(json.dumps(resp),mimetype="application/json",status=500)


@app.route('/data/<path:filepath>')
def getQrCode(filepath):
   return send_from_directory('data', filepath)
   

   
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080,debug = True)
