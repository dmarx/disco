import io
import os
from PIL import Image
import requests
import numpy as np
from modules.generators.base.generator import GeneratorBase


class GeneratorLoader(GeneratorBase):
    """If prompt is the URL or filepath of an image, this generator will download
    and output the path to that image.
    If prompt is empty, or does not resolve to a loadable image, it will output a
    4-color grid with black in the top left corner."""

    settings = {"prompt": "", "init_image": "", "i_generator": 0}

    def fetch(self, url_or_path):
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

    async def do_run(self, prefix="", input_seed=""):
        try:
            im = Image.open(self.fetch(self.settings["prompt"])).convert("RGB")
        except (FileNotFoundError, requests.exceptions.ConnectionError):
            arr = np.zeros(shape=(512, 512, 3), dtype=np.uint8)
            arr[256:, :, 0] = 255
            arr[:, 256:, 1] = 255
            im = Image.fromarray(arr)

        filename_out = f"{self.settings['i_generator']}_loader.png"
        im.save(os.path.join("content/output", filename_out))
        im.save(os.path.join("static/output", filename_out))
        return filename_out

    def init_settings(self, override_settings=None):
        settings = self.settings

        if override_settings != None:
            settings = self.json_override(settings, override_settings)

    def __init__(self, chain):
        super().__init__(chain)
        self.title = "Image Loader"
