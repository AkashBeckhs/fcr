#!/usr/bin/env python
# coding: utf-8

# In[1]:


import qrcode
from PIL import Image
import datetime

face = Image.open('lena.png').crop((75, 90, 150, 150))


qr_big = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
qr_big.add_data('Name-Akshay  Unique id-123456')

timestamp=datetime.datetime.now()
timestampStr = timestamp.strftime(" %d-%b-%Y (%H:%M:%S.%f)")


timestampnew=qr_big.add_data(timestampStr)

qr_big.make()
img_qr_big = qr_big.make_image().convert('RGB')

pos = ((img_qr_big.size[0] - face.size[0]) // 2, (img_qr_big.size[1] - face.size[1]) // 2)

img_qr_big.paste(face, pos)
img_qr_big.save('final_lena11.png')


# In[ ]:




