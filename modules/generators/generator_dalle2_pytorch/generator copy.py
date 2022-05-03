# # import click
# import json
# from types import SimpleNamespace
# from dalle2_pytorch.cli import get_pkg_version, safeget, simple_slugify
# from dalle2_pytorch.dalle2_pytorch import DALLE2, Decoder, DiffusionPrior
# import torch
# # import torchvision.transforms as T
# from pathlib import Path
# import torchvision.transforms as T

# # from dalle2_pytorch import DALLE2, Decoder, DiffusionPrior

# from functools import reduce, partial
# from modules.generators.base.generator import GeneratorBase


# class GeneratorDALLE2Pytorch(GeneratorBase):

#     args = None

#     def safeget(dictionary, keys, default = None):
#         return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split('.'), dictionary)

#     def simple_slugify(text, max_length = 255):
#         return text.replace("-", "_").replace(",", "").replace(" ", "_").replace("|", "--").strip('-_')[:max_length]

#     def get_pkg_version():
#         from pkg_resources import get_distribution
#         return get_distribution('dalle2_pytorch').version


#     def do_run(self,  model,cond_scale=1,text="Hello I am a string"):
    
#         model_path = Path(model)
#         full_model_path = str(model_path.resolve())
#         assert model_path.exists(), f'model not found at {full_model_path}'
#         loaded = torch.load(str(model_path))

#         version = safeget(loaded, 'version')
#         print(f'loading DALL-E2 from {full_model_path}, saved at version {version} - current package version is {get_pkg_version()}')

#         prior_init_params = safeget(loaded, 'init_params.prior')
#         decoder_init_params = safeget(loaded, 'init_params.decoder')
#         model_params = safeget(loaded, 'model_params')

#         prior = DiffusionPrior(**prior_init_params)
#         decoder = Decoder(**decoder_init_params)

#         dalle2 = DALLE2(prior, decoder)
#         dalle2.load_state_dict(model_params)

#         image = dalle2(text, cond_scale = cond_scale)

#         pil_image = T.ToPILImage()(image)
#         return pil_image.save(f'./{simple_slugify(text)}.png')

#         filename_gen = self.args.prefix + "00000.png"
#         filename_out = self.args.prefix + "_" + str(self.args.seed) + "_00000.png"
#         os.system("cp content/output/" + filename_gen +
#                 " static/output/" + filename_out)

#         return filename_out

#     def load_models(self):
#         print("Loading models")
        
#     def init_settings(self, override_settings=None):
                
#         settings = self.settings
#         if override_settings!=None:
#             settings = self.json_override(settings, override_settings)
            

#     def __init__(self,chain, load_models=True):
#         super().__init__(chain)
#         self.title = "Latent Diffusion"
     
#         try:
#             self.args = json.loads(self.default_settings, object_hook=lambda d: SimpleNamespace(**d))
#         except Exception:
#             pass
        
# #         self.args.width = 256
# #         self.args.height = 256
# #         self.args.clip_guidance = True

  
#         if load_models:
#             self.load_models()
