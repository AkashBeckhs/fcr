import qrcode
from PIL import Image
import datetime
import os
from enc import AESCipher 

face = Image.open('logo.png').crop((0,0,56,56))

key='aiypwzqphesoyamaaiypwzqphesoyama'

def generateQrCode(status,id):
    qr_big = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    data=dict()
    timestamp=datetime.datetime.now()
    timestampStr = timestamp.strftime(" %d-%b-%Y (%H:%M:%S.%f)")
    data['time']=timestampStr
    data['unique_id']=id
    data['status']=str(status).strip()
    d=str(data)
    print("before encryption  :-"+d)
    cipher=AESCipher(key)
    d=str(cipher.encrypt(d))
    print("after ecncryption   :-"+ d)
    qr_big.add_data(d)
    qr_big.make()
    img_qr_big = qr_big.make_image().convert('RGB')
    pos = ((img_qr_big.size[0] - face.size[0]) // 2, (img_qr_big.size[1] - face.size[1]) // 2)
    img_qr_big.paste(face, pos)
    #fileName=timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)").replace('-','_').replace(' ','_').replace('.','_').replace(':',"_").replace('(','').replace(')','')
    fileName="qr_code_"+str(id)
    fileName='%s.png' %fileName
    if os.path.exists("data/%s" %fileName):
        os.remove("data/%s" %fileName)
    img_qr_big.save('data/%s' %fileName)
    img_qr_big.close()
    return fileName





   
        
