import gc
import json
import os, sys
from random import randint, seed
from regex import P
import torch
from modules.generators.generator_disco.generator import GeneratorDisco
from modules.generators.generator_go_big.generator import GeneratorGoBig
from modules.generators.generator_ld.generator import GeneratorLatentDiffusion
from modules.generators.generator_loader.generator import GeneratorLoader
# from modules.generators.generator_arbitrary.generator import GeneratorArbitrary
# from modules.generators.generator_vqgan.generator import GeneratorVQGAN

# import asyncio
# from clip_client import Client

class Chain:

    DEVICE = None
    device = None
    output_filename = None
    output = ""
    progress = 0
    busy = False

    project = None

    generator_disco = None
    generator_ld = None
    generator_go_big = None
    generator_dalle_pytorch = None
    generator_loader = None
    generator_arbitrary = None
    generator_vqgan = None
    # clip_c = None

    def load_cuda(self,cudaDeviceOverride=""):

        # self.clip_c = Client(server='grpc://demo-cas.jina.ai:51000')
        
        cudaDevice = "cuda:0" if torch.cuda.is_available() else "cpu"
        print (cudaDevice,torch.cuda.is_available())
        #if (cudaDeviceOverride!=""): cudaDevice = cudaDeviceOverride

        self.DEVICE = torch.device(cudaDevice)
        print("Using device:", self.DEVICE)
        self.device = self.DEVICE  # At least one of the modules expects this name.

        if torch.cuda.is_available():
            if torch.cuda.get_device_capability(self.DEVICE) == (
                8,
                0,
            ):  # A100 fix thanks to Emad
                print("Disabling CUDNN for A100 gpu", file=sys.stderr)
                torch.backends.cudnn.enabled = False

    def run_chain(self, prompt):
        return self.output_filename

    def fetch_instanced_generator(self, generator_type):
        if generator_type == 0:
            if self.generator_loader == None:
                self.generator_loader = GeneratorLoader(self)
            return self.generator_loader

        if generator_type == 1:
            if self.generator_ld == None:
                self.generator_ld = GeneratorLatentDiffusion(self)
            return self.generator_ld

        if generator_type == 2:
            if self.generator_disco == None:
                self.generator_disco = GeneratorDisco(self)
            return self.generator_disco

        if generator_type == 4:
            if self.generator_go_big == None:
                self.generator_go_big = GeneratorGoBig(self)
            return self.generator_go_big

        # if generator_type == 4:
        #     if self.generator_dalle_pytorch == None:
        #         self.generator_dalle_pytorch = GeneratorDALLE2Pytorch(self)
        #     return self.generator_dalle_pytorch

        # if generator_type == 5:
        #     if self.generator_arbitrary == None:
        #         self.generator_arbitrary = GeneratorArbitrary(self)
        #     return self.generator_arbitrary

        # if generator_type == 6:
        #     if self.generator_vqgan == None:
        #         self.generator_vqgan = GeneratorVQGAN(self)
        #     return self.generator_vqgan

                        
    async def run_project(self, project):
        self.output_message("Running project " + str(project.id) + ": " + project.title)
        self.progress = 0
        self.busy = True
        self.project = project
        self.output_filename = ""

        for i_generator, generator in enumerate(project.generators):
            if generator.enabled:
                if i_generator == 0:
                    # Clear if running for a second time so init_image isn't
                    # left over from previous run
                    generator.settings["init_image"] = ""
                generator.settings = json.loads(
                    json.dumps(generator.settings, default=lambda obj: obj.__dict__)
                )
                generator.settings["i_generator"] = i_generator

                if self.output_filename != None and len(self.output_filename) > 0:
                    generator.settings["skip_steps"] = 25
                    generator.settings["init_image"] = (
                        os.getcwd() + "/static/output/" + self.output_filename
                    )

                instanced_generator = self.fetch_instanced_generator(generator.type)
                instanced_generator.init_settings(generator.settings)
                self.output_filename = await instanced_generator.do_run()
                self.output_project_image(project, generator)

        self.output_message(
            "Finished project " + str(project.id) + ": " + project.title
        )
        self.busy = False
        self.progress = 0

        return self.output_filename

    def run_project_preview(self, project, frame=0):
        self.output_message(
            "Running project preview " + str(project.id) + ": " + project.title
        )
        self.progress = 0
        self.busy = True
        self.project = project
        self.output_filename = ""

        for generator in project.generators:

            if generator.type == 2:
                generator.settings = json.loads(
                    json.dumps(generator.settings, default=lambda obj: obj.__dict__)
                )
                generator.settings["steps"] = 5
                generator.settings["diffusion_steps"] = 20
                generator.settings["width"] = 640
                generator.settings["height"] = 376
                generator.settings["start_frame"] = frame
                generator.settings["animation_mode"] = "None"
                if self.generator_disco == None:
                    self.generator_disco = GeneratorDisco(
                        self,
                        generator.settings["steps"],
                        [
                            int(generator.settings["width"]),
                            int(generator.settings["height"]),
                        ],
                        load_models=False,
                    )
                    self.generator_disco.load_models(self.generator_disco.settings)
                    self.generator_disco.init_settings(generator.settings)
                else:
                    self.generator_disco.init_settings(generator.settings)
                self.output_filename = self.generator_disco.do_run()
                self.output_project_image(
                    project, generator, "preview/" + str(frame), "preview.png"
                )

        self.output_message(
            "Finished project " + str(project.id) + ": " + project.title
        )
        self.busy = False
        self.progress = 0

        return self.output_filename

    def output_project_image(self, project, generator, slug="", filename=""):
        out_filename = self.output_filename if len(filename) == 0 else filename
        out_path = (
            "static/data/projects/"
            + str(project.id)
            + "/output/"
            + str(generator.type)
            + "/"
            + (slug + "/" if slug != "" else "")
        )
        os.system("mkdir -p " + out_path)
        print(generator, self.output_filename, out_path, out_filename)
        os.system(
            'cp "static/output/'
            + self.output_filename
            + '" "'
            + os.path.join(out_path, out_filename)
            + '"'
        )
        os.system(
            'cp "static/output/'
            + self.output_filename
            + '" "'
            + os.path.join("content/output", out_filename)
            + '"'
        )
        generator.output_path = os.path.join(
            out_path.replace("static/", ""), out_filename
        )
        project.save()

    def output_message(self, msg):
        print(msg)
        self.output += msg + "\n"

    def __init__(self,cudaDeviceOverride=""):
        seed(1)
        self.load_cuda(cudaDeviceOverride)
