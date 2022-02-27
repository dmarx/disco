# -*- coding: utf-8 -*-
"""3D-Photo-Inpainting-multiple-download.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/mrm8488/shared_colab_notebooks/blob/master/3D_Photo_Inpainting_multiple_download.ipynb

# 3D Photography using Context-aware Layered Depth Inpainting (CVPR 2020)

[project website](https://shihmengli.github.io/3D-Photo-Inpainting/)

> Colab adapted version by [Manuel Romero/@mrm8488](https://twitter.com/mrm8488)

## 1. Install required packages
"""

!pip3 install -q torch==1.4.0+cu100 torchvision==0.5.0+cu100 -f https://download.pytorch.org/whl/torch_stable.html
!pip3 install -q opencv-python==4.2.0.32
!pip3 install -q vispy==0.6.4
!pip3 install -q moviepy==1.0.2
!pip3 install -q transforms3d==0.3.1
!pip3 install -q networkx==2.3
!pip install -q PyDrive

"""## 2. Download script and pretrained model
- It will ask for you a verification code

"""

![ -e 3d-photo-inpainting-master ] && rm -r 3d-photo-inpainting-master

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
downloaded = drive.CreateFile({'id':"1Jmiq1-hSIsHiq_GCcmiNXtrs_T62AY_z"})
downloaded.GetContentFile('3d-photo-inpainting-master.zip')

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# unzip 3d-photo-inpainting-master.zip
# rm 3d-photo-inpainting-master.zip
# [ -e /content/3d-photo-inpainting-master/image/moon.jpg ] && rm -rf /content/3d-photo-inpainting-master/image/moon.jpg

cd 3d-photo-inpainting-master

# Disable PLY generation
!sed -i 's/save_ply: True/save_ply: False/' argument.yml

# Switch off screen rendering
!sed -i 's/offscreen_rendering: True/offscreen_rendering: False/g' argument.yml

"""## 3. Upload a picture from your filesystem with jpg extension"""

!rm -rf /content/3d-photo-inpainting-master/image/*

import os
import shutil
from google.colab import files

uploaded = files.upload()
pic_name = list(uploaded.keys())[0]

if(pic_name.split(".")[1].lower() != "jpg"):
  print("YOU MUST UPLOAD A .jpg FILE!! Re-run this cell and upload a pic with jpg extension")
  os.remove("./" + pic_name)
else:
  shutil.move("./" + pic_name, "/content/3d-photo-inpainting-master/image/" + pic_name)

"""## 4. Execute the 3D Photo Inpainting
  - Note: The 3D photo generation process usually takes about 2-3 minutes or more depending on the available computing resources.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# !python main.py --config argument.yml

"""- **The results are stored in the following directories**
  - Corresponding depth map estimated by [MiDaS](https://github.com/intel-isl/MiDaS.git) 
      - E.g. ```/content/3d-photo-inpainting-master/depth/moon.npy```
  - Inpainted 3D mesh
      - E.g. ```/content/3d-photo-inpainting-master/mesh/moon.ply```
  - Rendered videos with circular motion
      - E.g. ```/content/3d-photo-inpainting-master/mesh/moon.mp4```

## 5. Visualize results
### 5.1 Swing effect
"""

from IPython.display import HTML
from base64 import b64encode
mp4 = open('/content/3d-photo-inpainting-master/video/' + pic_name.split(".")[0] +  '_swing.mp4','rb').read()
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
HTML("""
<video width=600 controls autoplay>
      <source src="%s" type="video/mp4">
</video>
""" % data_url)

"""### 5.2 Straight line effect"""

mp4 = open('/content/3d-photo-inpainting-master/video/' + pic_name.split(".")[0] +  '_straight-line.mp4','rb').read()
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
HTML("""
<video width=600 controls autoplay>
      <source src="%s" type="video/mp4">
</video>
""" % data_url)

"""## Download it!
### Download all!
"""

directory = '/content/3d-photo-inpainting-master/video'
for filename in os.listdir(directory):
    if (filename.endswith(".mp4")): 
         files.download(os.path.join(directory, filename))

"""### Download the one with the effect you want (or both)"""

files.download('/content/3d-photo-inpainting-master/video/' + pic_name.split(".")[0] +  '_swing.mp4')

files.download('/content/3d-photo-inpainting-master/video/' + pic_name.split(".")[0] +  '_straight-line.mp4')

"""### Download 3D generated file (PLY)"""

files.download('/content/3d-photo-inpainting-master/mesh/' + + pic_name.split(".")[0] + '.ply')

"""### If you want to try with another picture go to step 3

<p>Did you enjoy? Buy me a coffe :)</p>
<p><a href="https://ko-fi.com/Y8Y3VYYE"><img src="https://camo.githubusercontent.com/c8a9d4f1653d599167ef09852550c6810a7306bc/68747470733a2f2f7777772e6b6f2d66692e636f6d2f696d672f676974687562627574746f6e5f736d2e737667" alt="ko-fi" data-canonical-src="https://www.ko-fi.com/img/githubbutton_sm.svg"></a></p>
"""