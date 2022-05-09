import datetime
import gc
import json
import math
from types import SimpleNamespace
from PIL import Image, ImageOps
import torch
from torchvision import transforms
from tqdm.notebook import tqdm
from modules.generators.generator_disco.guided_diffusion_disco.guided_diffusion.script_util import (
    create_model_and_diffusion,
    model_and_diffusion_defaults,
)
import os
from modules.generators.base.generator import GeneratorBase
import requests
import json


class GeneratorGoBig(GeneratorBase):

    args = None

    settings = {"init_image": "", "input_width": 512, "input_height": 512}

    model_config = None
    model_path = None
    diffusion_model = None

    # FUNCTIONS FOR GO BIG MODE
    global slices_todo
    slices_todo = 5  # Number of chunks to slice up from the original image

    def do_run(self):

        # curl -i -F files[]=@yourfile.jpeg https://tmp.ninja/upload.php (JSON Response)

        files = {
            "files[]": open(self.settings["init_image"], "rb"),
        }
        response = requests.post("https://tmp.ninja/upload.php", files=files)
        print(response)

        data = {
            "style": "art",
            "noise": "3",
            "x2": "1",
            "input": response.json()["files"][0]["url"],
        }

        r = requests.post(
            url="https://bigjpg.com/api/task/",
            headers={"X-API-KEY": "06838332753e420eb27110b20199b244"},
            data={"conf": json.dumps(data)},
        )

        tid = r.json()["tid"]

        while True:
            r = requests.get(url="https://bigjpg.com/api/task/" + tid)
            if r.json()[tid]["status"] == "success":
                r2 = requests.get(r.json()[tid]["url"], allow_redirects=True)
                open("static/output/output_go_big.png", "wb").write(r2.content)
                break
        #     print(r.json())
        # print(r.json()['tid'])

        return "output_go_big.png"

    def init_settings(self, override_settings=None):

        settings = self.settings

        if override_settings != None:
            settings = self.json_override(settings, override_settings)

        # self.args.steps = settings["steps"]

        # self.update_model_params()

    def __init__(self, chain, load_models=True):
        super().__init__(chain)
        self.title = "Go Big"

        self.args = json.loads(
            json.dumps(self.settings), object_hook=lambda d: SimpleNamespace(**d)
        )
