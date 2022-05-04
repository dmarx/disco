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


# def configure_paths(root_path):

#   initDirPath = f'{root_path}/content/init_images'
#   createPath(initDirPath)
#   outDirPath = f'{root_path}/content/images_out'
#   createPath(outDirPath)
#   model_path = f'{root_path}/content/models'
#   createPath(model_path)


def load_models():
    print("load models")
    # @title ### 1.4 Define Midas functions

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


def configure_sys_paths(PROJECT_DIR, model_path, USE_ADABINS):

    try:
        from CLIP import clip
    except:
        if os.path.exists("lib/CLIP") is not True:
            gitclone("https://github.com/openai/CLIP", path=f"{PROJECT_DIR}/lib/")
    sys.path.append(f"{PROJECT_DIR}/lib/CLIP")

    # try:
    #   from guided_diffusion.script_util import create_model_and_diffusion
    # except:
    #   if os.path.exists("guided-diffusion") is not True:
    #     gitclone("https://github.com/crowsonkb/guided-diffusion")
    # sys.path.append(f'{PROJECT_DIR}/guided-diffusion')

    try:
        from ResizeRight import resize
    except:
        if os.path.exists("lib/ResizeRight") is not True:
            gitclone(
                "https://github.com/assafshocher/ResizeRight.git",
                path=f"{PROJECT_DIR}/lib/",
            )
    sys.path.append(f"{PROJECT_DIR}/lib/ResizeRight")

    try:
        import py3d_tools
    except:
        if os.path.exists("lib/pytorch3d-lite") is not True:
            gitclone(
                "https://github.com/MSFTserver/pytorch3d-lite.git",
                path=f"{PROJECT_DIR}/lib/",
            )
    sys.path.append(f"{PROJECT_DIR}/lib/pytorch3d-lite")

    try:
        from midas.dpt_depth import DPTDepthModel
    except:
        if os.path.exists("lib/MiDaS") is not True:
            gitclone("https://github.com/isl-org/MiDaS.git", path=f"{PROJECT_DIR}/lib/")
        if os.path.exists("lib/MiDaS/midas_utils.py") is not True:
            shutil.move("lib/MiDaS/utils.py", "lib/MiDaS/midas_utils.py")
        if not os.path.exists(f"{model_path}/dpt_large-midas-2f21e586.pt"):
            wget(
                "https://github.com/intel-isl/DPT/releases/download/1_0/dpt_large-midas-2f21e586.pt",
                model_path,
            )
    sys.path.append(f"{PROJECT_DIR}/lib/MiDaS")

    try:
        from glid_3_xl.encoders.modules import BERTEmbedder
    except:
        if os.path.exists("lib/glid_3_xl") is not True:
            gitclone(
                "https://github.com/Jack000/glid-3-xl.git", path=f"{PROJECT_DIR}/lib/"
            )
            shutil.move("lib/glid-3-xl", "lib/glid_3_xl")

        import fileinput

        def replace_in_file(file_path, search_text, new_text):
            with fileinput.input(file_path, inplace=True) as file:
                for line in file:
                    new_line = line.replace(search_text, new_text)
                    print(new_line, end="")

        replace_in_file(
            "lib/glid_3_xl/encoders/modules.py",
            "from encoders.x_transformer import Encoder, TransformerWrapper",
            "from lib.glid_3_xl.encoders.x_transformer import Encoder, TransformerWrapper",
        )

        # Should be pip install -e .
        sys.path.append(f"{PROJECT_DIR}/lib/glid_3_xl")

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
    if USE_ADABINS:
        try:
            from infer import InferenceHelper
        except:
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
        sys.path.append(f"{PROJECT_DIR}/lib/AdaBins")
        from infer import InferenceHelper
