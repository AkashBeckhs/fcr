import qrcode
from PIL import Image
import datetime


face = Image.open('logo.png').crop((45,50,80,80))
qr_big = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

def generateQrCode(status,id):
    timestamp=datetime.datetime.now()
    timestampStr = timestamp.strftime(" %d-%b-%Y (%H:%M:%S.%f)")
    qr_big.add_data(timestampStr)
    qr_big.add_data(id)
    qr_big.add_data(status)
    qr_big.make()
    img_qr_big = qr_big.make_image().convert('RGB')
    pos = ((img_qr_big.size[0] - face.size[0]) // 2, (img_qr_big.size[1] - face.size[1]) // 2)
    img_qr_big.paste(face, pos)
    fileName=timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)").replace('-','_').replace(' ','_').replace('.','_').replace(':',"_").replace('(','').replace(')','')
    fileName='%s.png' %fileName
    img_qr_big.save('data/%s' %fileName)
    return fileName


if(__name__=="__main__"):
    print(generateQrCode("#v","#"+str(2)))


   
        
