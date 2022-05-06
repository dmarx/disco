import io
import json
from types import SimpleNamespace
from PIL import Image
import requests
import numpy as np
from modules.generators.base.generator import GeneratorBase


class GeneratorTest(GeneratorBase):

    default_settings = '{"reflect": True}'
    settings = {"reflect": True}

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

    def do_run(self, prompt, prefix="", input_seed=""):
        if len(prompt) > 0:
            im = Image.open(self.fetch(prompt)).convert("RGB")
        else:
            arr = np.zeros(shape=(512, 512, 3), dtype=np.int16)
            arr[256:, :, 0] = 255
            arr[:, 256:, 1] = 255
            im = Image.fromarray(arr)

        if self.settings["reflect"]:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        filename_out = "test.png"
        im.save(filename_out)
        return filename_out

    def load_models(self):
        pass

    def init_settings(self, override_settings=None):

        settings = self.settings

        if override_settings != None:
            settings = self.json_override(settings, override_settings)

    def __init__(self, chain, load_models=True):
        super().__init__(chain)
        self.title = "Test"

        self.args = json.loads(
            self.default_settings, object_hook=lambda d: SimpleNamespace(**d)
        )

        if load_models:
            self.load_models()
