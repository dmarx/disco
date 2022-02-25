import hashlib
import os
from os import path


# Simple create paths taken with modifications from Datamosh's Batch VQGAN+CLIP notebook
def createPath(filepath):
    if path.exists(filepath) == False:
        os.makedirs(filepath)
        print(f'Made {filepath}')
    else:
        print(f'filepath {filepath} exists.')


def download_models2(diffusion_model,model_512_path,model_256_path,check_model_SHA,model_256_SHA,model_512_SHA,use_secondary_model,model_secondary_path,model_secondary_SHA):


      # Download the diffusion model
  if diffusion_model == '256x256_diffusion_uncond':
      if os.path.exists(model_256_path) and check_model_SHA:
          print('Checking 256 Diffusion File')
          with open(model_256_path, "rb") as f:
              bytes = f.read()
              hash = hashlib.sha256(bytes).hexdigest()
          if hash == model_256_SHA:
              print('256 Model SHA matches')
              model_256_downloaded = True
          else:
              print("256 Model SHA doesn't match, redownloading...")
              os.system("wget --continue {model_256_link} -P {model_path}")
              model_256_downloaded = True
      elif os.path.exists(model_256_path) and not check_model_SHA or model_256_downloaded == True:
          print('256 Model already downloaded, check check_model_SHA if the file is corrupt')
      else:
          os.system("wget --continue {model_256_link} -P {model_path}")
          model_256_downloaded = True
  elif diffusion_model == '512x512_diffusion_uncond_finetune_008100':
      if os.path.exists(model_512_path) and check_model_SHA:
          print('Checking 512 Diffusion File')
          with open(model_512_path, "rb") as f:
              bytes = f.read()
              hash = hashlib.sha256(bytes).hexdigest()
          if hash == model_512_SHA:
              print('512 Model SHA matches')
              model_512_downloaded = True
          else:
              print("512 Model SHA doesn't match, redownloading...")
              os.system("wget --continue {model_512_link} -P {model_path}")
              model_512_downloaded = True
      elif os.path.exists(model_512_path) and not check_model_SHA or model_512_downloaded == True:
          print('512 Model already downloaded, check check_model_SHA if the file is corrupt')
      else:
          os.system("wget --continue {model_512_link} -P {model_path}")
          model_512_downloaded = True


  # Download the secondary diffusion model v2
  if use_secondary_model == True:
      if os.path.exists(model_secondary_path) and check_model_SHA:
          print('Checking Secondary Diffusion File')
          with open(model_secondary_path, "rb") as f:
              bytes = f.read()
              hash = hashlib.sha256(bytes).hexdigest()
          if hash == model_secondary_SHA:
              print('Secondary Model SHA matches')
              model_secondary_downloaded = True
          else:
              print("Secondary Model SHA doesn't match, redownloading...")
              os.system("wget --continue {model_secondary_link} -P {model_path}")
              model_secondary_downloaded = True
      elif os.path.exists(model_secondary_path) and not check_model_SHA or model_secondary_downloaded == True:
          print('Secondary Model already downloaded, check check_model_SHA if the file is corrupt')
      else:
          os.system("wget --continue {model_secondary_link} -P {model_path}")
          model_secondary_downloaded = True
