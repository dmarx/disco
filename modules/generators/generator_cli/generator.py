from modules.generators.base.generator import GeneratorBase

import subprocess

class GeneratorCLI(GeneratorBase):
    """This generator will run the code in settings.code.
    It has access to the 'prompt' and 'init_image' variables.
    Make sure to assign a value to "filename_out" containing
    the location of the image you want to output."""

    settings = {"command": ""}

    async def do_run(self, prefix="", input_seed=""):
        cmd = self.settings["command"]
        subprocess.run(cmd.split(' '), shell=False)
        return "Done"


    def init_settings(self, override_settings=None):

        settings = self.settings

        if override_settings != None:
            settings = self.json_override(settings, override_settings)

    def __init__(self, chain):
        super().__init__(chain)
        self.title = "Arbitrary CLI Command"
