import os, sys
import argparse, asyncio
import json
from types import SimpleNamespace

os.system("export TOKENIZERS_PARALLELISM=false")

PROJECT_DIR = os.getcwd()
sys.path.append(f"{PROJECT_DIR}/lib/glid_3_xl")
sys.path.append(f"{PROJECT_DIR}/lib/CLIP")
sys.path.append(f"{PROJECT_DIR}/lib/MiDaS")
sys.path.append(f"{PROJECT_DIR}/lib/AdaBins")
sys.path.append(f"{PROJECT_DIR}/lib/latent-diffusion")
sys.path.append(f"{PROJECT_DIR}/lib/ResizeRight")
sys.path.append(f"{PROJECT_DIR}/lib/pytorch3d-lite")

from modules.manager.chain.chain import Chain
from modules.manager.projects.api import Api
from modules.manager.projects.project import Project


async def run_custom():
    prompt = "A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."

    arbitrary_code_to_run = """
# Converts output of previous generator to black and white (dithering)
# and adds prompt as text in top left corner
import numpy as np
import os
from PIL import Image
from PIL import ImageDraw

im = Image.open(init_image)
im = im.convert('1')
draw = ImageDraw.Draw(im)
draw.text((0, 0), prompt, (255))

filename_out = f"{i_generator}_arbitrary.png"
im.save(os.path.join("content/output", filename_out))
im.save(os.path.join("static/output", filename_out))
    """

    project = Project(1)
    project.generators = [
        SimpleNamespace(
            **{
                "type": 0,
                "enabled": False,
                "settings": {
                    "prompt": "https://cdn.discordapp.com/attachments/970060442774958151/970073453052985445/BeepleBrandingConsultancy-PANCE-9.png",
                },
            }
        ),
        SimpleNamespace(
            **{
                "type": 1,
                "enabled": False,
                "settings": {
                    "prompt": prompt,
                    "steps": 30,
                    "width": 256,
                    "height": 256,
                },
            }
        ),
        SimpleNamespace(
            **{
                "type": 2,
                "enabled": False,
                "settings": {
                    "text_prompts": [{"start": 0, "prompt": prompt}],
                    "steps": 25,
                    "width": 640,
                    "height": 512,
                    # 'ViTB32': True,
                    # 'ViTB16': True,
                    # 'ViTL14': False,
                    # 'ViTL14_336px':False,
                    # 'RN101': False,
                    # 'RN50': False,
                    # 'RN50x4': False,
                    # 'RN50x16': False,
                    # 'RN50x64': False,
                },
            }
        ),
        SimpleNamespace(
            **{
                "type": 5,
                "enabled": False,
                "settings": {
                    "code": arbitrary_code_to_run,
                    "prompt": "",
                },
            }
        ),
        SimpleNamespace(
            **{
                "type": 7,
                "enabled": True,
                "settings": {
                    "command": "python -m pytti.warmup",
                },
            }
        ),
    ]

    print("running custom chain...")
    chain = Chain()
    await chain.run_project(project)

async def run_external_project(project_id):
    project = Api.fetch(args.project)
    print("running project chain...")
    chain = Chain()
    await chain.run_project(project)

# default run
default_prompt = "A scenic view over a landscape of magical architecture, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."
parser = argparse.ArgumentParser()
parser.add_argument("--project", type=int, default="0", help="project id")
parser.add_argument("--prompt", type=str, default=default_prompt, help="prompt")
args = parser.parse_args()

# args.project = 0
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
if args.project > 0:
    responses = loop.run_until_complete(run_external_project(args.project))
else:
    responses = loop.run_until_complete(run_custom())


