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
import json
from types import SimpleNamespace
from modules.manager.chain.chain import Chain
from modules.manager.projects.project import Project

prompt = "A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."

project = Project(-1)
project.generators = [
    SimpleNamespace(**
    {
        "id":0,
        "type":1,
        "settings":{
            "prompt":prompt,
            "steps":150,
            "width":512,
            "height":512,
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
    }),
    SimpleNamespace(**{
        "id":1,
        "type":3,
        "settings":{
        "width":512,
            "height":512,
            }
    })
]
chain = Chain()
filename = chain.run_project(project)
# filename = chain.run_chain(prompt)
