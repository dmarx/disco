# # from generator_disco.generator import GeneratorDisco
# # from generator_ld.generator import GeneratorLatentDiffusion
# # from manager.chain.chain import Chain


# from modules.generators.generator_disco.generator import GeneratorDisco
# from modules.manager.chain.chain import Chain


# chain = Chain()
# # chain.run_ld = False
# # chain.run_disco= False

# # chain.generator_disco = GeneratorDisco(chain,250,[1280,768])
# # chain.generator_disco.settings["prompt"] = ["A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."]
# # chain.generator_disco.init_settings()

# # output_filename = chain.generator_disco.do_run()


# filename = chain.run_chain("A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ.")


# from generator_disco.generator import GeneratorDisco
# from generator_ld.generator import GeneratorLatentDiffusion
# from manager.chain.chain import Chain


# from modules.manager.chain.chain import Chain

# prompt = "A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."
# chain = Chain()
# filename = chain.run_chain(prompt)

# from modules.generators.generator_disco.generator import GeneratorDisco




import argparse
import json
from types import SimpleNamespace
from modules.manager.chain.chain import Chain
from modules.manager.projects.api import Api
from modules.manager.projects.project import Project


def run_custom():
    prompt = "A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."

    project = Project(-1)
    project.generators = [
        # SimpleNamespace(**
        # {
        #     "id":0,
        #     "type":1,
        #     "settings":{
        #         "prompt":prompt,
        #         "steps":150,
        #         "width":512,
        #         "height":512,
        #         # 'ViTB32': True,
        #         # 'ViTB16': True,
        #         # 'ViTL14': False, # True
        #         # 'ViTL14_336px':False,
        #         # 'RN101': False,
        #         # 'RN50': False,
        #         # 'RN50x4': False,
        #         # 'RN50x16': False,
        #         # 'RN50x64': False,
        #     }
        # }),
        # SimpleNamespace(**{
        #     "id":3,
        #     "type":3,
        #     "settings":{
        #     "width":512,
        #         "height":512,
        #         }
        # # }),
        #      SimpleNamespace(**{
        #     "id":3
        #     "type":3,
        #     "settings":{
        #     "width":512,
        #         "height":512,
        #         }
        #     # ),
        #      SimpleNamespace(**{
        #     "id":4
        #     "type":4,
        #     "settings":{
        #     "width":512,
        # # #         "height":512,
        # #         }
        # })
        {
            id:0,
            type:4,
            'settings':{
                prompt:prompt,
                'steps':150,
                'width':512,
                'height':512,
                # 'ViTB32': True,
                # 'ViTB16': True,
                # 'ViTL14': False, # True
                # 'ViTL14_336px':False,
                # 'RN101': False,
                # 'RN50': False,
                # 'RN50x4': False,
                # 'RN50x16': False,
                # 'RN50x64': False,
            }
        }
    ]
    chain = Chain()
    filename = chain.run_project(project)
    # filename = chain.run_chain(prompt)
    

parser = argparse.ArgumentParser()

parser.add_argument('--project', type=int, default='0',
                    help='project id')

args = parser.parse_args(args = [],namespace=None)

args.project = 0
if args.project > 0:
    project =Api.fetch(args.project)
    chain = Chain()
    chain.output = ""
    filename = chain.run_project(project)
else:
    run_custom()
    
    
    