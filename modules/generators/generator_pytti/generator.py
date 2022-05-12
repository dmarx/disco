import os
from hydra import initialize, initialize_config_module, initialize_config_dir, compose
from loguru import logger
from omegaconf import OmegaConf
from pytti.workhorse import _main as render_frames

from modules.generators.base.generator import GeneratorBase

CONFIG_BASE_PATH = "config"
CONFIG_DEFAULTS = "default.yaml"

class GeneratorPytti(GeneratorBase):
    """This generator will run the code in settings.code.
    It has access to the 'prompt' and 'init_image' variables.
    Make sure to assign a value to "filename_out" containing
    the location of the image you want to output."""

    settings = dict(OmegaConf.load('config/default.yaml').to_container())
    settings['conf'] = '_empty'
    async def do_run(self, prefix="", input_seed=""):
        logger.debug("pytti generator do_run invoked")
        with initialize(config_path=CONFIG_BASE_PATH):
            for k,v in settings.items():
                cfg = compose(
                    config_name=CONFIG_DEFAULTS, 
                    overrides=[f"{k}={v}"]
                )
                render_frames(cfg)
            return "done"


    def init_settings(self, override_settings=None):

        settings = self.settings

        if override_settings != None:
            settings = self.json_override(settings, override_settings)

    def __init__(self, chain):
        logger.debug(""it's a me! Pytti!)
        super().__init__(chain)
        self.title = "PyTTI-Tools"
