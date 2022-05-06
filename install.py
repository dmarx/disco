import io
import shutil
import subprocess, os, sys, ipykernel
import requests
import fileinput


def gitclone(url, path=None):
    if path is None:
        res = subprocess.run(
            ["git", "clone", url], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
    else:
        if not os.path.exists(path):
            os.makedirs(path)
        res = subprocess.run(
            ["git", "-C", path, "clone", url], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
    print(res)

def pipi(modulestr):
    res = subprocess.run(
        ["pip", "install", modulestr], stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    print(res)


def pipie(modulestr):
    res = subprocess.run(
        ["git", "install", "-e", modulestr], stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    print(res)


def wget(url, outputdir):
    res = subprocess.run(
        ["wget", url, "-P", f"{outputdir}"], stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    print(res)


def createPath(filepath):
    os.makedirs(filepath, exist_ok=True)


def fetch(url_or_path):
    if str(url_or_path).startswith("http://") or str(url_or_path).startswith(
        "https://"
    ):
        r = requests.get(url_or_path)
        r.raise_for_status()
        fd = io.BytesIO()
        fd.write(r.content)
        fd.seek(0)
        return fd
    return open(url_or_path, "rb")


def replace_in_file(file_path, search_text, new_text):
    with fileinput.input(file_path, inplace=True) as file:
        for line in file:
            new_line = line.replace(search_text, new_text)
            print(new_line, end="")


def configure_paths(PROJECT_DIR):

   createPath(f'{PROJECT_DIR}/content/output')
   createPath(f'{PROJECT_DIR}/content/output_npy')
   createPath(f'{PROJECT_DIR}/static/output')
#   outDirPath = f'{root_path}/content/images_out'
#   createPath(outDirPath)
#   model_path = f'{root_path}/content/models'
#   createPath(model_path)


def configure_libs(PROJECT_DIR, model_path, USE_ADABINS):

    if os.path.exists("lib/CLIP") is not True:
        gitclone("https://github.com/openai/CLIP", path=f"{PROJECT_DIR}/lib/")
        os.system("cd lib/CLIP && pip install -e .")
        os.system("cd ..")

    if os.path.exists("lib/ResizeRight") is not True:
        gitclone(
            "https://github.com/assafshocher/ResizeRight.git",
            path=f"{PROJECT_DIR}/lib/",
        )

    if os.path.exists("lib/pytorch3d-lite") is not True:
        gitclone(
            "https://github.com/MSFTserver/pytorch3d-lite.git",
            path=f"{PROJECT_DIR}/lib/",
        )

    if os.path.exists("lib/MiDaS") is not True:
        gitclone("https://github.com/isl-org/MiDaS.git", path=f"{PROJECT_DIR}/lib/")
    if os.path.exists("lib/MiDaS/midas_utils.py") is not True:
        shutil.move("lib/MiDaS/utils.py", "lib/MiDaS/midas_utils.py")
    if not os.path.exists(f"{model_path}/dpt_large-midas-2f21e586.pt"):
        wget(
            "https://github.com/intel-isl/DPT/releases/download/1_0/dpt_large-midas-2f21e586.pt",
            model_path,
        )
        
        
    # if os.path.exists("lib/pytorch3d") is not True:
    #     gitclone(
    #         "https://github.com/facebookresearch/pytorch3d.git", path=f"{PROJECT_DIR}/lib/"
    #     )
    #     os.system("cd lib/pytorch3d && python3 setup.py install")
    #     os.system("cd " + PROJECT_DIR)

    if os.path.exists("lib/latent-diffusion") is not True:
        gitclone(
            "https://github.com/CompVis/latent-diffusion", path=f"{PROJECT_DIR}/lib/"
        )
        os.system("cd lib/latent-diffusion && pip install -e .")
        os.system("cd ..")

    if os.path.exists("lib/glid_3_xl") is not True:
        gitclone(
            "https://github.com/Jack000/glid-3-xl.git", path=f"{PROJECT_DIR}/lib/"
        )
        shutil.move("lib/glid-3-xl", "lib/glid_3_xl")
        shutil.move("lib/glid_3_xl/guided_diffusion", "lib/glid_3_xl/guided_diffusion_ld")

        replace_in_file(
            "lib/glid_3_xl/encoders/modules.py",
            "from encoders.x_transformer import Encoder, TransformerWrapper",
            "from lib.glid_3_xl.encoders.x_transformer import Encoder, TransformerWrapper",
        )
        
        os.system("wget https://dall-3.com/models/glid-3-xl/bert.pt -P lib/glid_3_xl")
        os.system("wget https://dall-3.com/models/glid-3-xl/kl-f8.pt -P lib/glid_3_xl")
        os.system("wget https://dall-3.com/models/glid-3-xl/finetune.pt -P lib/glid_3_xl")

        os.system("cd lib/latent-diffusion && pip install -e .")
        os.system("cd ..")
        
    # try:
    # sys.path.append(PROJECT_DIR)
    # import disco_xform_utils as dxf
    # except:
    #   if os.path.exists("disco-diffusion") is not True:
    #     gitclone("https://github.com/alembics/disco-diffusion.git")
    #   # Rename a file to avoid a name conflict..
    #   if os.path.exists('disco_xform_utils.py') is not True:
    #     shutil.move('disco-diffusion/disco_xform_utils.py', 'disco_xform_utils.py')
    # sys.path.append(PROJECT_DIR)

    # AdaBins stuff

    if os.path.exists("lib/AdaBins") is not True:
        gitclone(
            "https://github.com/shariqfarooq123/AdaBins.git",
            path=f"{PROJECT_DIR}/lib/",
        )
    if not os.path.exists(
        f"{PROJECT_DIR}/content/models/pretrained/AdaBins_nyu.pt"
    ):
        createPath(f"{PROJECT_DIR}/content/models/pretrained")
        wget(
            "https://cloudflare-ipfs.com/ipfs/Qmd2mMnDLWePKmgfS8m6ntAg4nhV5VkUyAydYBp8cWWeB7/AdaBins_nyu.pt",
            f"{PROJECT_DIR}/content/models/pretrained",
        )



    # try:
    #   from guided_diffusion.script_util import create_model_and_diffusion
    # except:
    #   if os.path.exists("guided-diffusion") is not True:
    #     gitclone("https://github.com/crowsonkb/guided-diffusion")
    # sys.path.append(f'{PROJECT_DIR}/guided-diffusion')

PROJECT_DIR=os.getcwd()
model_path = f"{PROJECT_DIR}/content/models"
USE_ADABINS = True

configure_libs(PROJECT_DIR, model_path, USE_ADABINS)
configure_paths(PROJECT_DIR)

