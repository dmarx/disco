# # import click
# import json
# import os
# from types import SimpleNamespace

# import PIL
# from dalle2_pytorch.cli import get_pkg_version, safeget, simple_slugify
# from dalle2_pytorch.dalle2_pytorch import DALLE2, Decoder, DiffusionPrior, DiffusionPriorNetwork, OpenAIClipAdapter, Unet
# import torch
# # import torchvision.transforms as T
# from pathlib import Path
# import torchvision.transforms as T

# # from dalle2_pytorch import DALLE2, Decoder, DiffusionPrior

# from functools import reduce, partial
# from modules.generators.base.generator import GeneratorBase


# class GeneratorDALLE2Pytorch(GeneratorBase):

#     args = None

#     def do_run(self, prompt, prefix="", input_seed=""):


#         # filename_gen = self.args.prefix + "00000.png"
#         # filename_out = self.args.prefix + "_" + str(self.args.seed) + "_00000.png"
#         # os.system("cp content/output/" + filename_gen +
#         #         " static/output/" + filename_out)
#         clip = OpenAIClipAdapter()

#         # mock data

#         text = torch.randint(0, 49408, (4, 256)).cuda()
#         images = torch.randn(4, 3, 256, 256).cuda()

#         # prior networks (with transformer)

#         prior_network = DiffusionPriorNetwork(
#             dim=512,
#             depth=6,
#             dim_head=64,
#             heads=8
#         ).cuda()

#         diffusion_prior = DiffusionPrior(
#             net=prior_network,
#             clip=clip,
#             timesteps=100,
#             cond_drop_prob=0.2
#         ).cuda()

#         loss = diffusion_prior(text, images)
#         loss.backward()

#         # do above for many steps ...

#         # decoder (with unet)

#         unet1 = Unet(
#             dim=128,
#             image_embed_dim=512,
#             cond_dim=128,
#             channels=3,
#             dim_mults=(1, 2, 4, 8)
#         ).cuda()

#         unet2 = Unet(
#             dim=16,
#             image_embed_dim=512,
#             cond_dim=128,
#             channels=3,
#             dim_mults=(1, 2, 4, 8, 16)
#         ).cuda()

#         decoder = Decoder(
#             unet=(unet1, unet2),
#             image_sizes=(128, 256),
#             clip=clip,
#             timesteps=100,
#             image_cond_drop_prob=0.1,
#             text_cond_drop_prob=0.5,
#             # set this to True if you wish to condition on text during training and sampling
#             condition_on_text_encodings=False
#         ).cuda()

#         for unet_number in (1, 2):
#             # this can optionally be decoder(images, text) if you wish to condition on the text encodings as well, though it was hinted in the paper it didn't do much
#             loss = decoder(images, unet_number=unet_number)
#             loss.backward()

#         # do above for many steps

#         dalle2 = DALLE2(
#             prior=diffusion_prior,
#             decoder=decoder
#         )

#         images = dalle2(
#             [prompt],
#             # classifier free guidance strength (> 1 would strengthen the condition)
#             cond_scale=2.
#         )


#         out_path = "content/dalle.png"

#         return    PIL.save(out_path)

# # save your image (in this example, of size 256x256)


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
