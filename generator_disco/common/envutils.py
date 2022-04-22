import io
import shutil
import subprocess, os, sys, ipykernel
import requests

# simple_nvidia_smi_display = False#@param {type:"boolean"}
# if simple_nvidia_smi_display:
#   #!nvidia-smi
#   nvidiasmi_output = subprocess.run(['nvidia-smi', '-L'], stdout=subprocess.PIPE).stdout.decode('utf-8')
#   print(nvidiasmi_output)
# else:
#   #!nvidia-smi -i 0 -e 0
#   nvidiasmi_output = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE).stdout.decode('utf-8')
#   print(nvidiasmi_output)
#   nvidiasmi_ecc_note = subprocess.run(['nvidia-smi', '-i', '0', '-e', '0'], stdout=subprocess.PIPE).stdout.decode('utf-8')
#   print(nvidiasmi_ecc_note)

def gitclone(url):
  res = subprocess.run(['git', 'clone', url], stdout=subprocess.PIPE).stdout.decode('utf-8')
  print(res)

def pipi(modulestr):
  res = subprocess.run(['pip', 'install', modulestr], stdout=subprocess.PIPE).stdout.decode('utf-8')
  print(res)

def pipie(modulestr):
  res = subprocess.run(['git', 'install', '-e', modulestr], stdout=subprocess.PIPE).stdout.decode('utf-8')
  print(res)

def wget(url, outputdir):
  res = subprocess.run(['wget', url, '-P', f'{outputdir}'], stdout=subprocess.PIPE).stdout.decode('utf-8')
  print(res)

def createPath(filepath):
    os.makedirs(filepath, exist_ok=True)

def fetch(url_or_path):
    if str(url_or_path).startswith('http://') or str(url_or_path).startswith('https://'):
        r = requests.get(url_or_path)
        r.raise_for_status()
        fd = io.BytesIO()
        fd.write(r.content)
        fd.seek(0)
        return fd
    return open(url_or_path, 'rb')
  
# def configure_paths(root_path):
    
#   initDirPath = f'{root_path}/content/init_images'
#   createPath(initDirPath)
#   outDirPath = f'{root_path}/content/images_out'
#   createPath(outDirPath)
#   model_path = f'{root_path}/content/models'
#   createPath(model_path)

def load_models():
    print("load models")
    #@title ### 1.4 Define Midas functions

    # from midas.dpt_depth import DPTDepthModel
    # from midas.midas_net import MidasNet
    # from midas.midas_net_custom import MidasNet_small
    # from midas.transforms import Resize, NormalizeImage, PrepareForNet

    # Initialize MiDaS depth model.
    # It remains resident in VRAM and likely takes around 2GB VRAM.
    # You could instead initialize it for each frame (and free it after each frame) to save VRAM.. but initializing it is slow.
    # self.default_models = {
    #     "midas_v21_small": f"{self.model_path}/midas_v21_small-70d6b9c8.pt",
    #     "midas_v21": f"{self.model_path}/midas_v21-f6b98070.pt",
    #     "dpt_large": f"{self.model_path}/dpt_large-midas-2f21e586.pt",
    #     "dpt_hybrid": f"{self.model_path}/dpt_hybrid-midas-501f0c75.pt",
    #     "dpt_hybrid_nyu": f"{self.model_path}/dpt_hybrid_nyu-2ce69ec7.pt",}
    
def configure_sys_paths(PROJECT_DIR,model_path,USE_ADABINS):

    try:
      from CLIP import clip
    except:
      if os.path.exists("CLIP") is not True:
        gitclone("https://github.com/openai/CLIP")
    sys.path.append(f'{PROJECT_DIR}/CLIP')

    # try:
    #   from guided_diffusion.script_util import create_model_and_diffusion
    # except:
    #   if os.path.exists("guided-diffusion") is not True:
    #     gitclone("https://github.com/crowsonkb/guided-diffusion")
    # sys.path.append(f'{PROJECT_DIR}/guided-diffusion')

    try:
      from ResizeRight import resize
    except:
      if os.path.exists("ResizeRight") is not True:
        gitclone("https://github.com/assafshocher/ResizeRight.git")
    sys.path.append(f'{PROJECT_DIR}/ResizeRight')

    try:
      import py3d_tools
    except:
      if os.path.exists('pytorch3d-lite') is not True:
        gitclone("https://github.com/MSFTserver/pytorch3d-lite.git")
    sys.path.append(f'{PROJECT_DIR}/pytorch3d-lite')

    try:
      from midas.dpt_depth import DPTDepthModel
    except:
      if os.path.exists('MiDaS') is not True:
        gitclone("https://github.com/isl-org/MiDaS.git")
      if os.path.exists('MiDaS/midas_utils.py') is not True:
        shutil.move('MiDaS/utils.py', 'MiDaS/midas_utils.py')
      if not os.path.exists(f'{model_path}/dpt_large-midas-2f21e586.pt'):
        wget("https://github.com/intel-isl/DPT/releases/download/1_0/dpt_large-midas-2f21e586.pt", model_path)
    sys.path.append(f'{PROJECT_DIR}/MiDaS')

    # try:
    #sys.path.append(PROJECT_DIR)
    #import disco_xform_utils as dxf
    # except:
    #   if os.path.exists("disco-diffusion") is not True:
    #     gitclone("https://github.com/alembics/disco-diffusion.git")
    #   # Rename a file to avoid a name conflict..
    #   if os.path.exists('disco_xform_utils.py') is not True:
    #     shutil.move('disco-diffusion/disco_xform_utils.py', 'disco_xform_utils.py')
    # sys.path.append(PROJECT_DIR)

    # AdaBins stuff
    if USE_ADABINS:
        try:
            from infer import InferenceHelper
        except:
            if os.path.exists("AdaBins") is not True:
                gitclone("https://github.com/shariqfarooq123/AdaBins.git")
            if not os.path.exists(f'{PROJECT_DIR}/pretrained/AdaBins_nyu.pt'):
                createPath(f'{PROJECT_DIR}/pretrained')
                wget("https://cloudflare-ipfs.com/ipfs/Qmd2mMnDLWePKmgfS8m6ntAg4nhV5VkUyAydYBp8cWWeB7/AdaBins_nyu.pt", f'{PROJECT_DIR}/pretrained')
        sys.path.append(f'{PROJECT_DIR}/AdaBins')
        from infer import InferenceHelper