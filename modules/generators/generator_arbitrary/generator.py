from modules.generators.base.generator import GeneratorBase


class GeneratorArbitrary(GeneratorBase):
    """This generator will run the code in settings.code.
    It has access to the 'prompt' and 'init_image' variables.
    Make sure to assign a value to "filename_out" containing
    the location of the image you want to output."""

    settings = {"prompt": "", "code": "", "init_image": "", "i_generator": 0}

    def do_run(self, prefix="", input_seed=""):
        loc = {}
        exec(
            self.settings["code"],
            {
                "prompt": self.settings["prompt"],
                "init_image": self.settings["init_image"],
                "i_generator": self.settings["i_generator"],
            },
            loc,
        )
        return loc["filename_out"]

    def init_settings(self, override_settings=None):

        settings = self.settings

        if override_settings != None:
            settings = self.json_override(settings, override_settings)

    def __init__(self, chain):
        super().__init__(chain)
        self.title = "Arbitrary Code"