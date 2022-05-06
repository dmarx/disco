# import click
import json
import os
from types import SimpleNamespace
import PIL
from dalle2_pytorch.dalle2_pytorch import (
    DALLE2,
    Decoder,
    DiffusionPrior,
    DiffusionPriorNetwork,
    OpenAIClipAdapter,
    Unet,
)
import torch

# import torchvision.transforms as T
from pathlib import Path
import torchvision.transforms as T

# from dalle2_pytorch import DALLE2, Decoder, DiffusionPrior
from functools import reduce, partial
from modules.generators.base.generator import GeneratorBase
import click

# https://huggingface.co/krish240574/Dalle2-Diffusion-Prior


class GeneratorDALLE2Pytorch(GeneratorBase):

    args = None

    def safeget(self, dictionary, keys, default=None):
        return reduce(
            lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
            keys.split("."),
            dictionary,
        )

    def simple_slugify(self, text, max_length=255):
        return (
            text.replace("-", "_")
            .replace(",", "")
            .replace(" ", "_")
            .replace("|", "--")
            .strip("-_")[:max_length]
        )

    def get_pkg_version(self):
        from pkg_resources import get_distribution

        return get_distribution("dalle2_pytorch").version

    def do_run(self, prompt, prefix="", input_seed=""):

        # filename_gen = self.args.prefix + "00000.png"
        # filename_out = self.args.prefix + "_" + str(self.args.seed) + "_00000.png"
        # os.system("cp content/output/" + filename_gen +
        #         " static/output/" + filename_out)

        filename_gen = self.dream(
            "content/models/dalle2/1651473037.600823_saved_model.pth", 2, prompt
        )
        # filename_gen = self.do_run_openai(prompt)

        # filename_gen = self.args.prefix + "00000.png"
        filename_out = (
            filename_gen  # self.args.prefix + "_" + str(self.args.seed) + "_00000.png"
        )
        os.system(
            "cp content/output/" + filename_gen + " static/output/" + filename_out
        )

        return filename_out

    def dream(self, model, cond_scale, text):
        model_path = Path(model)
        full_model_path = str(model_path.resolve())
        assert model_path.exists(), f"model not found at {full_model_path}"
        loaded = torch.load(str(model_path))

        version = self.safeget(loaded, "version")
        print(
            f"loading DALL-E2 from {full_model_path}, saved at version {version} - current package version is {self.get_pkg_version()}"
        )

        prior_init_params = self.safeget(loaded, "init_params.prior")
        decoder_init_params = self.safeget(loaded, "init_params.decoder")
        model_params = self.safeget(loaded, "model_params")

        prior = DiffusionPrior(**prior_init_params)
        decoder = Decoder(**decoder_init_params)

        dalle2 = DALLE2(prior, decoder)
        dalle2.load_state_dict(model_params)

        image = dalle2(text, cond_scale=cond_scale)

        pil_image = T.ToPILImage()(image)
        return pil_image.save(f"./{simple_slugify(text)}.png")

    def do_run_openai(self, prompt):

        # filename_gen = self.args.prefix + "00000.png"
        # filename_out = self.args.prefix + "_" + str(self.args.seed) + "_00000.png"
        # os.system("cp content/output/" + filename_gen +
        #         " static/output/" + filename_out)
        clip = OpenAIClipAdapter()

        # mock data

        text = torch.randint(0, 49408, (4, 256)).cuda()
        images = torch.randn(4, 3, 256, 256).cuda()

        # prior networks (with transformer)

        prior_network = DiffusionPriorNetwork(
            dim=512, depth=6, dim_head=64, heads=8
        ).cuda()

        diffusion_prior = DiffusionPrior(
            net=prior_network, clip=clip, timesteps=100, cond_drop_prob=0.2
        ).cuda()

        loss = diffusion_prior(text, images)
        loss.backward()

        # do above for many steps ...

        # decoder (with unet)

        unet1 = Unet(
            dim=128,
            image_embed_dim=512,
            cond_dim=128,
            channels=3,
            dim_mults=(1, 2, 4, 8),
        ).cuda()

        unet2 = Unet(
            dim=16,
            image_embed_dim=512,
            cond_dim=128,
            channels=3,
            dim_mults=(1, 2, 4, 8, 16),
        ).cuda()

        decoder = Decoder(
            unet=(unet1, unet2),
            image_sizes=(128, 256),
            clip=clip,
            timesteps=100,
            image_cond_drop_prob=0.1,
            text_cond_drop_prob=0.5,
            # set this to True if you wish to condition on text during training and sampling
            condition_on_text_encodings=False,
        ).cuda()

        for unet_number in (1, 2):
            # this can optionally be decoder(images, text) if you wish to condition on the text encodings as well, though it was hinted in the paper it didn't do much
            loss = decoder(images, unet_number=unet_number)
            loss.backward()

        # do above for many steps

        dalle2 = DALLE2(prior=diffusion_prior, decoder=decoder)

        images = dalle2(
            [prompt],
            # classifier free guidance strength (> 1 would strengthen the condition)
            cond_scale=2.0,
        )

        filename_gen = f"dalle_out.png"
        for img in images:

            try:
                pil_image = T.ToPILImage()(img)
                pil_image.save("content/output/" + filename_gen)
                # return pil_image.save(f'/home/twmmason/dev/disco/content/{simple_slugify(text)}.png')

            except Exception as inst:
                print(inst)  # __str__ allows args to be printed directly,

            #  T.ToPILImage()("/homw/twmmason/dev/discpoimg)
            # PIPpil_image.save(f'./{simple_slugify(text)}.png')

        return filename_gen

    def do_run_cli(self, prompt):
        print("cli")

    def load_models(self):
        print("Loading models")

    def init_settings(self, override_settings=None):

        settings = self.settings
        if override_settings != None:
            settings = self.json_override(settings, override_settings)

    def __init__(self, chain, load_models=True):
        super().__init__(chain)
        self.title = "Latent Diffusion"

        try:
            self.args = json.loads(
                self.default_settings, object_hook=lambda d: SimpleNamespace(**d)
            )
        except Exception:
            pass

        #         self.args.width = 256
        #         self.args.height = 256
        #         self.args.clip_guidance = True

        if load_models:
            self.load_models()
