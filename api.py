import fc
import json
from flask import Flask, render_template, request,send_from_directory
from werkzeug.utils import secure_filename
from flask import jsonify
from flask import Response
import qrcode_qpi as qr
import time


uploadFolderPath='uploads/'
app = Flask(__name__)


@app.route('/upload')
def home():
   return render_template('/upload.html')
	
@app.route('/uploader', methods = ['POST'])
def upload_file():
   print("Inside upload method")
   resp=dict()
   if request.method == 'POST':
      try:
         checkImage = request.files['check']
         verifyImage = request.files['verify']
         print(checkImage)
         print(verifyImage)
         if checkImage== None or verifyImage==None:
          resp['Message']="Please provide valid images."  
          return Response(json.dumps(resp),mimetype="application/json",status=403)
         checkImage.filename="checkImage.jpg"
         verifyImage.filename="verifyImage.jpg"
         checkImage.save(secure_filename(checkImage.filename))
         verifyImage.save(secure_filename(verifyImage.filename))
         startTime=time.time()
         resp['Message']=str(fc.checkImage(checkImage,verifyImage)[0])
         endTime=time.time()
         print(endTime-startTime)
         return Response(json.dumps(resp),mimetype="application/json",status=200)
      except Exception as e:
         resp['Message']="There is some exception "+str(e)
         return Response(json.dumps(resp),mimetype="application/json",status=500)

@app.route('/qrcode')
def getQrCodePath():
   resp= dict()
   try:
      resp['Message']="data/%s" %(qr.generateQrCode())
      return Response(json.dumps(resp),mimetype="application/json",status=200)
   except Exception as e:
      print(e)
      resp['Message']="There was some error"
      return Response(json.dumps(resp),mimetype="application/json",status=500)


@app.route('/data/<path:filepath>')
def getQrCode(filepath):
   return send_from_directory('data', filepath)

   
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080,debug = True)
