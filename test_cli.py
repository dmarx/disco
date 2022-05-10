import os, sys

PROJECT_DIR = os.getcwd()
import asyncio

sys.path.append(f"{PROJECT_DIR}/lib/glid_3_xl")
sys.path.append(f"{PROJECT_DIR}/lib/CLIP")
sys.path.append(f"{PROJECT_DIR}/lib/MiDaS")
sys.path.append(f"{PROJECT_DIR}/lib/AdaBins")
sys.path.append(f"{PROJECT_DIR}/lib/latent-diffusion")
sys.path.append(f"{PROJECT_DIR}/lib/ResizeRight")
sys.path.append(f"{PROJECT_DIR}/lib/pytorch3d-lite")

import argparse
from types import SimpleNamespace
from modules.manager.chain.chain import Chain
from modules.manager.projects.api import Api
from modules.manager.projects.project import Project


async def run_custom(
    prompt="A scenic view over a landscape of magical architecture, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ.",
):

    project = Project(1)
    project.generators = [
        SimpleNamespace(
            **{
                "id": 0,
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
                "id": 1,
                "type": 2,
                "enabled": True,
                "settings": {
                    "text_prompts": [{"start": 0, "prompt": prompt}],
                    "steps": 40,
                    "width": 640,
                    "height": 380,
                    "ViTB32": True,
                    "ViTB16": True,
                    "ViTL14": False,
                    "ViTL14_336px": False,
                    "RN101": False,
                    "RN50": False,
                    "RN50x4": False,
                    "RN50x16": False,
                    "RN50x64": False,
                    "frames_scale": 1500,
                    "frames_skip_steps": "65%",
                    "turbo_mode": True,
                    "turbo_steps": "3",
                    "skip_steps": 10,
                    "animation_mode": "None",
                    "max_frames": 10000,
                },
            }
        ),
    ]

    print("running project chain...")
    chain = Chain()
    chain.filename = await chain.run_project(project)


async def run_external_project(project_id):
    project = Api.fetch(args.project)
    print("running project chain...")
    chain = Chain()
    chain.filename = await chain.run_project(project)


default_prompt = "A scenic view over a landscape of magical architecture, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=int, default="0", help="project id")
parser.add_argument("--prompt", type=str, default=default_prompt, help="prompt")
args = parser.parse_args()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
if args.project > 0:
    responses = loop.run_until_complete(run_external_project(args.project))
else:
    responses = loop.run_until_complete(run_custom(args.prompt))
