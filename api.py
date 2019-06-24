import fc
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

uploadFolderPath='uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=uploadFolderPath


@app.route('/upload')
def home():
   return render_template('/upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      try:
         checkImage = request.files['check']
         verifyImage = request.files['verify']
         if checkImage== None or verifyImage==None:
          return render_template("result.html",res="Please provide two images")
         checkImage.filename="checkImage.jpg"
         verifyImage.filename="verifyImage.jpg"
         checkImage.save(secure_filename(checkImage.filename))
         verifyImage.save(secure_filename(verifyImage.filename))
         res=fc.checkImage(checkImage,verifyImage)
         return render_template("result.html",res=res[0])
      except Exception as e:
         return render_template("result.html",res="There was some error in comparing the given images")
		
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080,debug = True)
