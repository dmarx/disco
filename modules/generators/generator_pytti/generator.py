import os
from hydra import initialize, initialize_config_module, initialize_config_dir, compose
from loguru import logger
from omegaconf import OmegaConf
from pytti.workhorse import _main as render_frames

from pathlib import Path

from copy import deepcopy

from modules.generators.base.generator import GeneratorBase

CONFIG_BASE_PATH = "../../../config"
CONFIG_DEFAULTS = "default.yaml"

NON_PYTTI_SETTINGS_KEYS = ['i_generator']

def rand_string(length):
    import random
    import string
    import time
    random.seed(time.time())
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

class GeneratorPytti(GeneratorBase):
    """This generator will run the code in settings.code.
    It has access to the 'prompt' and 'init_image' variables.
    Make sure to assign a value to "filename_out" containing
    the location of the image you want to output."""

    async def do_run(self, prefix="", input_seed=""):
        logger.debug("pytti generator do_run invoked")
        logger.debug(self.settings)
        with initialize(config_path=CONFIG_BASE_PATH):
            overrides = [f"{k}={v}" for k,v in self.settings.items()]
            logger.debug(f"overrides: {overrides}")
            cfg = compose(
                config_name=CONFIG_DEFAULTS, 
                overrides=overrides,
            )
            render_frames(cfg)

            im_path = Path("images_out") / cfg.file_namespace 
            images = list(im_path.glob('*.png'))
            images.sort(key=lambda x: os.path.getmtime(x))
            out_fpath = images[-1].resolve()

            logger.debug(f"out_fpath: {out_fpath}")
            return out_fpath


    def init_settings(self, override_settings=None):
        logger.debug(f"init_settings: {override_settings}")
        #self.settings = override_settings.get('settings', dict())
        self.settings = deepcopy(override_settings)
        if 'file_namespace' not in self.settings:
            self.settings['file_namespace'] = rand_string(10)

        for k in NON_PYTTI_SETTINGS_KEYS:
            if k in self.settings:
                self.settings.pop(k)

        logger.debug(self.settings)

    def __init__(self, chain):
        logger.debug("it's a me! Pytti!")
        super().__init__(chain)
        self.title = "PyTTI-Tools"
