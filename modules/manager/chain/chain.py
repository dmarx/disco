import gc
import json
import os, sys
from random import randint, seed
from regex import P
import torch
from modules.generators.generator_disco.generator import GeneratorDisco
from modules.generators.generator_go_big.generator import GeneratorGoBig
from modules.generators.generator_ld.generator import GeneratorLatentDiffusion
# from modules.generators.generator_dalle2_pytorch.generator import GeneratorDALLE2Pytorch

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

    # clip_c = None


    # run_disco = True
    # run_ld = True

    def load_cuda(self):

        # self.clip_c = Client(server='grpc://demo-cas.jina.ai:51000')
        
        self.DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print("Using device:", self.DEVICE)
        self.device = self.DEVICE  # At least one of the modules expects this name..

        if torch.cuda.get_device_capability(self.DEVICE) == (
            8,
            0,
        ):  ## A100 fix thanks to Emad
            print("Disabling CUDNN for A100 gpu", file=sys.stderr)
            torch.backends.cudnn.enabled = False

    def run_chain(self, prompt):
        # print (prompt)

        # if self.run_ld:
        #     if self.generator_ld == None: self.generator_ld =  GeneratorLatentDiffusion(self)
        #     self.generator_ld.args.prefix = str(randint(0,1000000))
        #     self.output_filename = self.generator_ld.do_run(prompt,self.generator_ld.args.prefix,str(100))

        # if self.run_disco:
        # if self.generator_disco == None: self.generator_disco = GeneratorDisco(self,150,[512,512])
        # self.generator_disco.settings["prompt"] = [prompt]
        # if self.run_ld:
        #     self.generator_disco.settings["skip_steps"] = 25
        #     self.generator_disco.settings["init_image"] = os.getcwd() + "/static/output/" + self.output_filename
        # self.generator_disco.init_settings()
        # self.output_filename = self.generator_disco.do_run()

        return self.output_filename

    def fetch_instanced_generator(self, generator_type):
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
        
        
                        
    async def run_project(self, project):
        self.output_message("Running project " + str(project.id) + ": " + project.title)
        self.progress = 0
        self.busy = True
        self.project = project
        self.output_filename = ""

    
        for generator in project.generators:
            if generator.enabled:
                generator.settings = json.loads(
                    json.dumps(generator.settings, default=lambda obj: obj.__dict__)
                )
                
                if self.output_filename != None and len(self.output_filename) > 0:
                    generator.settings["skip_steps"] = 25
                    generator.settings["init_image"] = (os.getcwd() + "/static/output/" + self.output_filename)
        
                instanced_generator = self.fetch_instanced_generator(generator.type)
                instanced_generator.init_settings(generator.settings)
                self.output_filename = await instanced_generator.do_run()
                self.output_project_image(project, generator)

            # #disco
            # if generator.type == 2:
            #     if self.generator_disco == None:
            #         self.generator_disco = GeneratorDisco(
            #             self,
            #             generator.settings["steps"],
            #             [
            #                 int(generator.settings["width"]),
            #                 int(generator.settings["height"]),
            #             ],
            #         )
            #     if self.output_filename != None and len(self.output_filename) > 0:
            #         generator.settings["skip_steps"] = 25
            #         generator.settings["init_image"] = (
            #             os.getcwd() + "/static/output/" + self.output_filename
            #         )
            #     self.generator_disco.init_settings(generator.settings)
            #     self.output_filename = self.generator_disco.do_run()

            # #upscaler
            # if generator.type == 3:
            #     if self.generator_go_big == None:
            #         self.generator_go_big = GeneratorGoBig(self)
            #     # self.generator_disco.settings["prompt"] = generator.settings["prompt"]
            #     self.generator_go_big.init_settings(generator.settings)
            #     if self.output_filename != None and len(self.output_filename) > 0:
            #         self.generator_go_big.settings["init_image"] = (
            #             os.getcwd() + "/static/output/" + self.output_filename
            #         )
            #     self.output_filename = self.generator_go_big.do_run()

            # #dalle2
            # if generator.type == 4:
            #     if self.generator_dalle_pytorch == None:
            #         self.generator_dalle_pytorch = GeneratorDALLE2Pytorch(self)
            #     self.output_filename = self.generator_dalle_pytorch.do_run(
            #         generator.settings["prompt"]
            #     )

            #clean gpu memory
            # del self.generator_ld
            # # del self.generator_ld.diffusion
            # gc.collect()
            # torch.cuda.empty_cache()



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
                # generator.settings['RN50x16']=False
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
                # self.generator_disco.settings["prompt"] = generator.settings["prompt"]

                # if self.output_filename != None and len(self.output_filename) > 0:
                #     self.generator_disco.settings["skip_steps"] = 25
                #     self.generator_disco.settings["init_image"] = os.getcwd() + "/static/output/" + self.output_filename
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
            + out_path
            + "/"
            + out_filename
            + '"'
        )
        generator.output_path = out_path.replace("static/", "") + "/" + out_filename
        project.save()

    def output_message(self, msg):
        print(msg)
        self.output += msg + "\n"

    def __init__(self):
        seed(1)
        self.load_cuda()
