# from generator_disco.generator import GeneratorDisco
# from generator_ld.generator import GeneratorLatentDiffusion
# from manager.chain.chain import Chain


from modules.generators.generator_disco.generator import GeneratorDisco
from modules.manager.chain.chain import Chain


chain = Chain()
# chain.run_ld = False
# chain.run_disco= False

# chain.generator_disco = GeneratorDisco(chain,250,[1280,768])
# chain.generator_disco.settings["prompt"] = ["A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."]
# chain.generator_disco.init_settings()

# output_filename = chain.generator_disco.do_run()


filename = chain.run_chain("A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ.")