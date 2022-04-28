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
# from modules.manager.chain.chain import Chain

# prompt = "A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."
# chain = Chain()

# # chain.run_ld = False
# filename = chain.run_chain(prompt)

# def run():
#     import datetime


#     print ("updated " + str(datetime.datetime.now()))

#     duration = 1
#     for i in range(100):
#         import time
#         # task.progress = i
#         # task.save()
#         print (str(i))
#         time.sleep(duration)
from modules.manager.chain.chain import Chain
from modules.manager.projects.api import Api
import sys

id = sys.argv[1]
print("Starting project run for project: " + str(id))
project =Api.fetch(id)
#prompt = "A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."
chain = Chain()
filename = chain.run_project(project)
print("Finished project run for project: " + str(project.id))
# chain.run_ld = False

