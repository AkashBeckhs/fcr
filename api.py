import fc
import json
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask import jsonify
from flask import Response


uploadFolderPath='uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=uploadFolderPath


@app.route('/upload')
def home():
   return render_template('/upload.html')
	
@app.route('/uploader', methods = ['POST'])
def upload_file():
   resp=dict()
   if request.method == 'POST':
      try:
         checkImage = request.files['check']
         verifyImage = request.files['verify']
         if checkImage== None or verifyImage==None:
          resp['Message']="Please provide valid images."  
          return Response(json.dumps(resp),mimetype="application/json",status=403)
         checkImage.filename="checkImage.jpg"
         verifyImage.filename="verifyImage.jpg"
         checkImage.save(secure_filename(checkImage.filename))
         verifyImage.save(secure_filename(verifyImage.filename))
         resp['Message']=str(fc.checkImage(checkImage,verifyImage)[0])
         return Response(json.dumps(resp),mimetype="application/json",status=200)
      except Exception as e:
         resp['Message']="There is some exception "+str(e)
         return Response(json.dumps(resp),mimetype="application/json",status=500)
		
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080,debug = True)
