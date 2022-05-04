import os, sys
PROJECT_DIR=os.getcwd()
sys.path.append(f'{PROJECT_DIR}/CLIP')
sys.path.append(f'{PROJECT_DIR}/MiDaS')
sys.path.append(f'{PROJECT_DIR}/AdaBins')
sys.path.append(f'{PROJECT_DIR}/latent-diffusion')
sys.path.append(f'{PROJECT_DIR}/ResizeRight')
sys.path.append(f'{PROJECT_DIR}/pytorch3d-lite')
sys.path.append(f'{PROJECT_DIR}/gl_3_xl')

# # from generator_disco.generator import GeneratorDisco
# from modules.generators.generator_ld.generator import GeneratorLatentDiffusion
# # from manager.chain.chain import Chain

import argparse
import json
from types import SimpleNamespace
from modules.manager.chain.chain import Chain
from modules.manager.projects.api import Api
from modules.manager.projects.project import Project


def run_custom():
    prompt = "A scenic view underwater of pearlescent hypervisors gleaming in the ethereal interdimensional space, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."

    project = Project(1)
    project.generators = [
        #SimpleNamespace(**{
       #     'id':0,
         #   'type':1,
        #    'settings':{
        #        "prompt":prompt,
          #      "steps":150,
          #      "width":512,
        #        "height":512,
         #   }
        #}),
        
        #Disco
         SimpleNamespace(**{
            'id':0,
            'type':2,
            'settings':{
                "text_prompts": [{
                    "start": 0,
                    "prompt": prompt
                }], 
                "steps":150,
                "width":512,
                "height":512,
                'ViTB32': True,
                'ViTB16': True,
                #'ViTL14': False,
                'ViTL14_336px':False,
               # 'RN101': False,
               # 'RN50': False,
              #  'RN50x4': False,
              #  'RN50x16': False,
               # 'RN50x64': False,
            }
        }),
        
        #SimpleNamespace(**{
           # 'id':0,
           # 'type':4,
         #   'settings':{
           #     'prompt':prompt,
                #'steps':150,
               # 'width':512,
              #  'height':512,
                # 'ViTB32': True,
                # 'ViTB16': True,
                # 'ViTL14': False, # True
                # 'ViTL14_336px':False,
                # 'RN101': False,
                # 'RN50': False,
                # 'RN50x4': False,
                # 'RN50x16': False,
                # 'RN50x64': False,
        #   }
      #  })
    ]
    print("running project chain...")
    chain = Chain()
    chain.filename = chain.run_project(project)



parser = argparse.ArgumentParser()
parser.add_argument('--project', type=int, default='0',
                    help='project id')

args = parser.parse_args(args = [],namespace=None)

args.project = 0
if args.project > 0:
    project = Api.fetch(args.project)
    chain = Chain()
    chain.output = ""
    filename = chain.run_project(project)
else:
    run_custom()

    

