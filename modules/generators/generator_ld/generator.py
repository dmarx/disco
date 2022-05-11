import asyncio
import gc
import io
import json
import math
from random import randint
import sys
from types import SimpleNamespace
from PIL import Image, ImageOps
import requests
import torch
from torch import nn
from torch.nn import functional as F
from torchvision import transforms
from torchvision.transforms import functional as TF
from tqdm.notebook import tqdm
import numpy as np
from lib.dalle_flow_glid3.encoders.modules import BERTEmbedder
from lib.dalle_flow_glid3.guided_diffusion_ld2.script_util import (
    create_model_and_diffusion,
    model_and_diffusion_defaults,
)
from einops import rearrange
from math import log2, sqrt
import os
# import clip
from modules.generators.base.generator import GeneratorBase
from functools import reduce  # py3

from clip_client import Client

class GeneratorLatentDiffusion(GeneratorBase):

    clip_model = None
    args = None
    normalize = None

    ldm = None

    default_settings = '{"model_path": "lib/glid_3_xl/finetune.pt", "kl_path": "lib/glid_3_xl/kl-f8.pt", "bert_path": "lib/glid_3_xl/bert.pt", "text": "", "edit": null, "edit_x": 0, "edit_y": 0, "edit_width": 0, "edit_height": 0, "mask": null, "negative": "", "init_image": null, "skip_timesteps": 0, "prefix": "", "num_batches": 1, "batch_size": 1, "width": 256, "height": 256, "seed": -1, "guidance_scale": 5.0, "steps": 0, "cpu": false, "clip_score": false, "clip_guidance": false, "clip_guidance_scale": 150, "cutn": 16, "ddim": false, "ddpm": false}'
    settings = {
        "model_path": "lib/glid_3_xl/finetune.pt",
        "kl_path": "lib/glid_3_xl/kl-f8.pt",
        "bert_path": "lib/glid_3_xl/bert.pt",
        "prompt": "",
        "edit": None,
        "edit_x": 0,
        "edit_y": 0,
        "edit_width": 0,
        "edit_height": 0,
        "mask": None,
        "negative": "",
        "init_image": None,
        "skip_timesteps": 0,
        "prefix": "",
        "num_batches": 1,
        "batch_size": 1,
        "width": 256,
        "height": 256,
        "seed": -1,
        "guidance_scale": 5.0,
        "steps": 0,
        "cpu": False,
        "clip_score": False,
        "clip_guidance": False,
        "clip_guidance_scale": 150,
        "cutn": 16,
        "ddim": False,
        "ddpm": False,
    }

    def fetch(url_or_path):
        if str(url_or_path).startswith("http://") or str(url_or_path).startswith(
            "https://"
        ):
            r = requests.get(url_or_path)
            r.raise_for_status()
            fd = io.BytesIO()
            fd.write(r.content)
            fd.seek(0)
            return fd
        return open(url_or_path, "rb")

    class MakeCutouts(nn.Module):
        def __init__(self, cut_size, cutn, cut_pow=1.0):
            super().__init__()

            self.cut_size = cut_size
            self.cutn = cutn
            self.cut_pow = cut_pow

        def forward(self, input):
            sideY, sideX = input.shape[2:4]
            max_size = min(sideX, sideY)
            min_size = min(sideX, sideY, self.cut_size)
            cutouts = []
            for _ in range(self.cutn):
                size = int(
                    torch.rand([]) ** self.cut_pow * (max_size - min_size) + min_size
                )
                offsetx = torch.randint(0, sideX - size + 1, ())
                offsety = torch.randint(0, sideY - size + 1, ())
                cutout = input[:, :, offsety : offsety + size, offsetx : offsetx + size]
                cutouts.append(F.adaptive_avg_pool2d(cutout, self.cut_size))
            return torch.cat(cutouts)

    def tv_loss(input):
        """L2 total variation loss, as in Mahendran et al."""
        input = F.pad(input, (0, 1, 0, 1), "replicate")
        x_diff = input[..., :-1, 1:] - input[..., :-1, :-1]
        y_diff = input[..., 1:, :-1] - input[..., :-1, :-1]
        return (x_diff ** 2 + y_diff ** 2).mean([1, 2, 3])

    # async def get_embeds(self):
    #     self.args.negative = " "
    #     clip_c = AsyncGRPCClient(server='grpc://demo-cas.jina.ai:51000')
    #     #text_emb_clip = clip_c.encode([self.args.prompt] * self.args.batch_size)
        
        
    #     t2 = asyncio.create_task(clip_c.aencode([self.args.prompt] * self.args.batch_size))
    #     t3 = asyncio.create_task(clip_c.aencode([self.args.negative] * self.args.batch_size))
    #     tasks = t2, t3
    #     self.text_emb_clip, self.text_emb_clip_blank = asyncio.gather(*tasks)

    #     # self.text_emb_clip = await clip_c.encode([self.args.prompt] * self.args.batch_size)
    #     # self.text_emb_clip_blank = await clip_c.encode([self.args.negative] * self.args.batch_size)

    #     # responses = loop.run_until_complete(self.get_embeds())
        
        
    #     # asyncio.gather(t2,t3)
    #     # assert t2.result()
    #     # self.text_emb_clip = t2.result()
    #     # assert t3.result()
    #     # self.text_emb_clip_blank = t3.result()
    #     # assert t2.result().
       
    # async def get_embeds(self):
    #     self.args.negative = " "
    #     t1 = asyncio.create_task(self.chain.clip_c.encode([self.args.prompt] * self.args.batch_size))
    #     t2 = asyncio.create_task(self.chain.clip_c.encode([self.args.negative] * self.args.batch_size))
    #     # t2 = asyncio.create_task(c.aencode(['hello world'] * 100))
    #     await asyncio.gather(t1, t2)
    #     print(t1,t2)
     
    async def do_run(self, prefix="", input_seed=""):
        
        self.args.output_path = os.getcwd() + "/content/output"
        
        if self.args.seed >= 0:
            torch.manual_seed(self.args.seed)

        # bert context
        text_emb = (
            self.bert.encode([self.args.prompt] * self.args.batch_size).to(self.device).float()
        )
        text_blank = (
            self.bert.encode([self.args.negative] * self.args.batch_size)
            .to(self.device)
            .float()
        )


        # text = clip.tokenize([self.args.prompt] * self.args.batch_size, truncate=True).to(
        #     device
        # )
        # text_clip_blank = clip.tokenize(
        #     [self.args.negative] * self.args.batch_size, truncate=True
        # ).to(device)

        # # clip context
        # text_emb_clip = self.clip_model.encode_text(text)
        # text_emb_clip_blank = self.clip_model.encode_text(text_clip_blank)

        # clip context
       
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # responses = loop.run_until_complete(self.get_embeds())
        
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # responses = loop.run_until_complete(self.get_embeds())
        # self.get_embeds()
 
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # responses = loop.run_until_complete(self.get_embeds())
        
        # clip_c = Client(server='grpc://demo-cas.jina.ai:51000')
        # self.args.negative = " "
        # t1 = asyncio.create_task(clip_c.aencode([self.args.prompt] * self.args.batch_size))
        # t2 = asyncio.create_task(clip_c.aencode([self.args.negative] * self.args.batch_size))
        # # t2 = asyncio.create_task(c.aencode(['hello world'] * 100))
        # self.text_emb_clip, self.text_emb_clip_blank = asyncio.gather(t1, t2).result()
        
        clip_c = Client(server='grpc://demo-cas.jina.ai:51000')
        # clip_c._async_client.post
        self.args.negative = " "
        self.text_emb_clip = await clip_c.aencode([self.args.prompt] * self.args.batch_size)
        self.text_emb_clip_blank = await clip_c.aencode([self.args.negative] * self.args.batch_size)
        
        # asyncio.run(self.get_embeds())
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # responses = loop.run_until_complete(self.get_embeds())
        # self.get_embeds()
        
        # torch.Size([8, 77, 1280]) torch.Size([8, 77, 1280]) (1, 768) (1, 768)

        print(self.text_emb_clip.shape, type(self.text_emb_clip))
        image_embed = None

        # image context
        if self.model_params['image_condition']:
            # using inpaint model but no image is provided
            image_embed = torch.zeros(
                self.args.batch_size * 2,
                4,
                self.args.height // 8,
                self.args.width // 8,
                device=self.device,
            )

        kwargs = {
            "context": torch.cat([text_emb, text_blank], dim=0).float(),
            "clip_embed": torch.cat(
                [torch.from_numpy(self.text_emb_clip), torch.from_numpy(self.text_emb_clip_blank)],
                dim=0,
            )
            .to(self.device)
            .float()
            if self.model_params['clip_embed_dim']
            else None,
            "image_embed": image_embed,
        }

        # Create a classifier-free guidance sampling function
        def model_fn(x_t, ts, **kwargs):
            half = x_t[: len(x_t) // 2]
            combined = torch.cat([half, half], dim=0)
            model_out = self.model(combined, ts, **kwargs)
            eps, rest = model_out[:, :3], model_out[:, 3:]
            cond_eps, uncond_eps = torch.split(eps, len(eps) // 2, dim=0)
            half_eps = uncond_eps + self.args.guidance_scale * (cond_eps - uncond_eps)
            eps = torch.cat([half_eps, half_eps], dim=0)
            return torch.cat([eps, rest], dim=1)

        if self.args.ddpm:
            sample_fn = self.diffusion.ddpm_sample_loop_progressive
        elif self.args.ddim:
            sample_fn = self.diffusion.ddim_sample_loop_progressive
        else:
            sample_fn = self.diffusion.plms_sample_loop_progressive

        def save_sample(i, sample):
            for k, image in enumerate(sample['pred_xstart'][: self.args.batch_size]):
                image /= 0.18215
                im = image.unsqueeze(0)
                out = self.ldm.decode(im)

                out = TF.to_pil_image(out.squeeze(0).add(1).div(2).clamp(0, 1))

                # self.Path(self.args.output_path).mkdir(exist_ok=True)

                filename = os.path.join(
                    self.args.output_path,
                    f'{self.args.prefix}{i * self.args.batch_size + k:05}.png',
                )
                out.save(filename)

        if self.args.init_image:
            init = Image.open(self.args.init_image).convert('RGB')
            init = init.resize(
                (int(self.args.width), int(self.args.height)), Image.LANCZOS
            )
            init = TF.to_tensor(init).to(self.device).unsqueeze(0).clamp(0, 1)
            h = self.ldm.encode(init * 2 - 1).sample() * 0.18215
            init = torch.cat(self.args.batch_size * 2 * [h], dim=0)
        else:
            init = None

        for i in range(self.args.num_batches):
            cur_t = self.diffusion.num_timesteps - 1

            samples = sample_fn(
                model_fn,
                (
                    self.args.batch_size * 2,
                    4,
                    int(self.args.height / 8),
                    int(self.args.width / 8),
                ),
                clip_denoised=False,
                model_kwargs=kwargs,
                cond_fn=None,
                device=self.device,
                progress=True,
                init_image=init,
                skip_timesteps=self.args.skip_timesteps,
            )

            for j, sample in enumerate(samples):
                cur_t -= 1
                if j % 5 == 0 and j != self.diffusion.num_timesteps - 1:
                    save_sample(i, sample)

            save_sample(i, sample)
        
        filename_gen = self.args.prefix + "00000.png"
        filename_out = self.args.prefix + "_" + str(self.args.seed) + "_00000.png"
        os.system(
            "cp content/output/" + filename_gen + " static/output/" + filename_out
        )

        return filename_out

    # gc.collect()
    # do_run()

    def load_models(self):

            
        self.model_state_dict = torch.load(self.args.model_path, map_location='cpu')

        self.model_params = {
            'attention_resolutions': '32,16,8',
            'class_cond': False,
            'diffusion_steps': 1000,
            'rescale_timesteps': True,
            'timestep_respacing': '30',  # Modify this value to decrease the number of
            # timesteps.
            'image_size': 32,
            'learn_sigma': False,
            'noise_schedule': 'linear',
            'num_channels': 320,
            'num_heads': 8,
            'num_res_blocks': 2,
            'resblock_updown': False,
            'use_fp16': False,
            'use_scale_shift_norm': False,
            'clip_embed_dim': 768 if 'clip_proj.weight' in self.model_state_dict else None,
            'image_condition': True
            if self.model_state_dict['input_blocks.0.0.weight'].shape[1] == 8
            else False,
            'super_res_condition': True
            if 'external_block.0.0.weight' in self.model_state_dict
            else False,
        }

        if self.args.ddpm:
            self.model_params['timestep_respacing'] = 1000
        if self.args.ddim:
            if self.args.steps:
                self.model_params['timestep_respacing'] = 'ddim' + os.environ.get(
                    'GLID3_STEPS', str(self.args.steps)
                )
            else:
                self.model_params['timestep_respacing'] = 'ddim50'
        elif self.args.steps:
            self.model_params['timestep_respacing'] = os.environ.get(
                'GLID3_STEPS', str(self.args.steps)
            )

        self.model_config = model_and_diffusion_defaults()
        self.model_config.update(self.model_params)

        if self.args.cpu:
            self.model_config['use_fp16'] = False

        # Load models
        self.model, self.diffusion = create_model_and_diffusion(**self.model_config)
        self.model.load_state_dict(self.model_state_dict, strict=False)
        self.model.requires_grad_(self.args.clip_guidance).eval().to(self.device)

        if self.model_config['use_fp16']:
            self.model.convert_to_fp16()
        else:
            self.model.convert_to_fp32()


        def set_requires_grad(model, value):
            for param in model.parameters():
                param.requires_grad = value


        # vae
        self.ldm = torch.load(self.args.kl_path, map_location="cpu")
        self.ldm.to(self.device)
        self.ldm.eval()
        self.ldm.requires_grad_(self.args.clip_guidance)
        set_requires_grad(self.ldm, self.args.clip_guidance)

        self.bert = BERTEmbedder(1280, 32)
        self.sd = torch.load(self.args.bert_path, map_location="cpu")
        self.bert.load_state_dict(self.sd)

        self.bert.to(self.device)
        self.bert.half().eval()
        set_requires_grad(self.bert, False)


    #def update_model_params(self):
        # self.model_params = {
        #     "attention_resolutions": "32,16,8",
        #     "class_cond": False,
        #     "diffusion_steps": 1000,
        #     "rescale_timesteps": True,
        #     "timestep_respacing": "45",  # Modify this value to decrease the number of
        #     # timesteps.
        #     "image_size": 32,
        #     "learn_sigma": False,
        #     "noise_schedule": "linear",
        #     "num_channels": 320,
        #     "num_heads": 8,
        #     "num_res_blocks": 2,
        #     "resblock_updown": False,
        #     "use_fp16": False,
        #     "use_scale_shift_norm": False,
        #     "clip_embed_dim": 768
        #     if "clip_proj.weight" in self.model_state_dict
        #     else None,
        #     "image_condition": True
        #     if self.model_state_dict["input_blocks.0.0.weight"].shape[1] == 8
        #     else False,
        #     "super_res_condition": True
        #     if "external_block.0.0.weight" in self.model_state_dict
        #     else False,
        # }

        # if self.args.ddpm:
        #     self.model_params["timestep_respacing"] = 1000
        # if self.args.ddim:
        #     if self.args.steps:
        #         self.model_params["timestep_respacing"] = "ddim" + str(self.args.steps)
        #     else:
        #         self.model_params["timestep_respacing"] = "ddim50"
        # elif self.args.steps:
        #     self.model_params["timestep_respacing"] = str(self.args.steps)

        # self.model_config = model_and_diffusion_defaults()
        # self.model_config.update(self.model_params)

    def init_settings(self, override_settings=None):

        settings = self.settings

        if override_settings != None:
            settings = self.json_override(settings, override_settings)

        self.args.steps = settings["steps"]

        self.args.prompt = settings["prompt"]
        self.args.width = settings["width"]
        self.args.height = settings["height"]

        #self.update_model_params()

    def __init__(self, chain, load_models=True):
        super().__init__(chain)
        self.title = "Latent Diffusion"


        # parser = argparse.ArgumentParser()

        # parser.add_argument('--model_path', type=str, default='glid_3_xl/finetune.pt',
        #                     help='path to the diffusion model')

        # parser.add_argument('--kl_path', type=str, default='glid_3_xl/kl-f8.pt',
        #                     help='path to the LDM first stage model')

        # parser.add_argument('--bert_path', type=str, default='glid_3_xl/bert.pt',
        #                     help='path to the LDM first stage model')

        # parser.add_argument('--text', type=str, required=False, default='',
        #                     help='your text prompt')

        # parser.add_argument('--edit', type=str, required=False,
        #                     help='path to the image you want to edit (either an image file or .npy containing a numpy array of the image embeddings)')

        # parser.add_argument('--edit_x', type=int, required=False, default=0,
        #                     help='x position of the edit image in the generation frame (need to be multiple of 8)')

        # parser.add_argument('--edit_y', type=int, required=False, default=0,
        #                     help='y position of the edit image in the generation frame (need to be multiple of 8)')

        # parser.add_argument('--edit_width', type=int, required=False, default=0,
        #                     help='width of the edit image in the generation frame (need to be multiple of 8)')

        # parser.add_argument('--edit_height', type=int, required=False, default=0,
        #                     help='height of the edit image in the generation frame (need to be multiple of 8)')

        # parser.add_argument('--mask', type=str, required=False,
        #                     help='path to a mask image. white pixels = keep, black pixels = discard. width = image width/8, height = image height/8')

        # parser.add_argument('--negative', type=str, required=False, default='',
        #                     help='negative text prompt')

        # parser.add_argument('--init_image', type=str, required=False, default=None,
        #                     help='init image to use')

        # parser.add_argument('--skip_timesteps', type=int, required=False, default=0,
        #                     help='how many diffusion steps are gonna be skipped')

        # parser.add_argument('--prefix', type=str, required=False, default='',
        #                     help='prefix for output files')

        # parser.add_argument('--num_batches', type=int, default=1, required=False,
        #                     help='number of batches')

        # parser.add_argument('--batch_size', type=int, default=1, required=False,
        #                     help='batch size')

        # parser.add_argument('--width', type=int, default=256, required=False,
        #                     help='image size of output (multiple of 8)')

        # parser.add_argument('--height', type=int, default=256, required=False,
        #                     help='image size of output (multiple of 8)')

        # parser.add_argument('--seed', type=int, default=-1, required=False,
        #                     help='random seed')

        # parser.add_argument('--guidance_scale', type=float, default=5.0, required=False,
        #                     help='classifier-free guidance scale')

        # parser.add_argument('--steps', type=int, default=0, required=False,
        #                     help='number of diffusion steps')

        # parser.add_argument('--cpu', dest='cpu', action='store_true')

        # parser.add_argument(
        #     '--clip_score', dest='clip_score', action='store_true')

        # parser.add_argument('--clip_guidance',
        #                     dest='clip_guidance', action='store_true')

        # parser.add_argument('--clip_guidance_scale', type=float, default=150, required=False,
        #                     help='Controls how much the image should look like the prompt')  # may need to use lower value for ddim

        # parser.add_argument('--cutn', type=int, default=16, required=False,
        #                     help='Number of cuts')

        # # turn on to use 50 step ddim
        # parser.add_argument('--ddim', dest='ddim', action='store_true')

        # # turn on to use 50 step ddim
        # parser.add_argument('--ddpm', dest='ddpm', action='store_true')

        # self.args = parser.parse_args(args = [],namespace=None)
        # strj = json.dumps(self.args, default=lambda obj: obj.__dict__)
        self.args = json.loads(
            self.default_settings, object_hook=lambda d: SimpleNamespace(**d)
        )

        self.args.width = 256
        self.args.height = 256
        self.args.clip_guidance = True

        self.args.prefix = str(randint(0, 1000000))

        # self.device = torch.device('cuda:0' if (
        #     torch.cuda.is_available() and not self.args.cpu) else 'cpu')
        # self.chain.output_message('Using device:', self.device)

        if load_models:
            self.load_models()
