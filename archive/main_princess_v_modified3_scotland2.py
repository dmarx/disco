# -*- coding: utf-8 -*-
"""Diffusion_V_Princess_Generator_Victoria.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nk6l2Q_paC1J8p4gW-__Me26DtZETFkd

# Princess Generator: Ver. Victoria
## Attention: Not colab ready. You have to install dependencies and download the models, put them in right position by yourself.
### It would be great if someone could get this to a colab ready state... 

Originally by Katherine Crowson (https://github.com/crowsonkb, https://twitter.com/RiversHaveWings). It uses a 512x512 unconditional ImageNet diffusion model fine-tuned from OpenAI's 512x512 class-conditional ImageNet diffusion model (https://github.com/openai/guided-diffusion) together with CLIP (https://github.com/openai/CLIP) to connect text prompts with images. 

Now updated using V-diffusion by Katherine Crowson. (https://github.com/crowsonkb/v-diffusion-pytorch)

@Nshepperd, @DaneilRussruss also have contribution in this code.
I may missed some of the contributors of specific functions. If you found your credit is missing, let me know and I 'll add it as soon as possible.
"""

settings = {
    #'prompt': "A scenic view of Venice, by Canaletto, matte painting trending on artstation",
    'prompt': "A scenic view of a Scottish loch in the Isle of Skye, matte painting trending on artstation",
    'path':'/notebooks/dev/disco',
    'cut_ic_pow':0.3,
    'w' : 1024
} 

from dataclasses import dataclass
from functools import partial
import gc
import io
import math
import sys
import random
import numpy as np
from piq import brisque
from itertools import product
import lpips
from PIL import Image, ImageOps
import requests
import torch
from torch import nn
from torch.nn import functional as F
from torchvision import transforms
from torchvision import transforms as T
from torchvision.transforms import functional as TF
from tqdm.notebook import tqdm
from numpy import nan

sys.path.append('./CLIP')
sys.path.append('./v-diffusion-pytorch')
sys.path.append('./guided-diffusion')
sys.path.append('./ResizeRight/')

from resize_right import resize, calc_pad_sz


import clip

# Define necessary functions
class ReplaceGrad(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x_forward, x_backward):
        ctx.shape = x_backward.shape
        return x_forward

    @staticmethod
    def backward(ctx, grad_in):
        return None, grad_in.sum_to_size(ctx.shape)


replace_grad = ReplaceGrad.apply

        
def fetch(url_or_path):
    if str(url_or_path).startswith('http://') or str(url_or_path).startswith('https://'):
        r = requests.get(url_or_path)
        r.raise_for_status()
        fd = io.BytesIO()
        fd.write(r.content)
        fd.seek(0)
        return fd
    return open(url_or_path, 'rb')


def parse_prompt(prompt):
    if prompt.startswith('http://') or prompt.startswith('https://') or prompt.startswith("E:") or prompt.startswith("C:") or prompt.startswith("D:"):
        vals = prompt.rsplit(':', 2)
        vals = [vals[0] + ':' + vals[1], *vals[2:]]
    else:
        vals = prompt.rsplit(':', 1)
    vals = vals + ['', '1'][len(vals):]
    return vals[0], float(vals[1])


class MakeCutoutsVDango(nn.Module):
    def __init__(self, cut_size,
                 Overview=4, 
                 WholeCrop = 0, WC_Allowance = 10, WC_Grey_P=0.2,
                 InnerCrop = 0, IC_Size_Pow=0.5, IC_Grey_P = 0.2
                 ):
        super().__init__()
        self.cut_size = cut_size
        self.Overview = Overview
        self.WholeCrop= WholeCrop
        self.WC_Allowance = WC_Allowance
        self.WC_Grey_P = WC_Grey_P
        self.InnerCrop = InnerCrop
        self.IC_Size_Pow = IC_Size_Pow
        self.IC_Grey_P = IC_Grey_P
        self.augs = T.Compose([
            T.RandomHorizontalFlip(p=0.5),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            T.RandomAffine(degrees=5, 
                           translate=(0.05, 0.05), 
                           #scale=(0.9,0.95),
                           fill=-1,  interpolation = T.InterpolationMode.BILINEAR, ),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            #T.RandomPerspective(p=1, interpolation = T.InterpolationMode.BILINEAR, fill=-1,distortion_scale=0.2),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            T.RandomGrayscale(p=0.1),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            T.ColorJitter(brightness=0.05, contrast=0.05, saturation=0.05),
        ])

    def forward(self, input):
        gray = transforms.Grayscale(3)
        sideY, sideX = input.shape[2:4]
        max_size = min(sideX, sideY)
        min_size = min(sideX, sideY, self.cut_size)
        l_size = max(sideX, sideY)
        output_shape = [1,3,self.cut_size,self.cut_size] 
        output_shape_2 = [1,3,self.cut_size+2,self.cut_size+2]
        pad_input = F.pad(input,((sideY-max_size)//2+round(max_size*0.05),(sideY-max_size)//2+round(max_size*0.05),(sideX-max_size)//2+round(max_size*0.05),(sideX-max_size)//2+round(max_size*0.05)), **padargs)
        cutouts_list = []
        
        if self.Overview>0:
            cutouts = []
            cutout = resize(pad_input, out_shape=output_shape)
            if self.Overview in [1,2,4]:
                if self.Overview>=2:
                    cutout=torch.cat((cutout,gray(cutout)))
                if self.Overview==4:
                    cutout = torch.cat((cutout, TF.hflip(cutout)))
            else:
                output_shape_all = list(output_shape)
                output_shape_all[0]=self.Overview
                cutout = resize(pad_input, out_shape=output_shape_all)
                if aug: cutout=self.augs(cutout)
            cutouts_list.append(cutout)
            
        if self.InnerCrop >0:
            cutouts=[]
            for i in range(self.InnerCrop):
                size = int(torch.rand([])**self.IC_Size_Pow * (max_size - min_size) + min_size)
                offsetx = torch.randint(0, sideX - size + 1, ())
                offsety = torch.randint(0, sideY - size + 1, ())
                cutout = input[:, :, offsety:offsety + size, offsetx:offsetx + size]
                if i <= int(self.IC_Grey_P * self.InnerCrop):
                    cutout = gray(cutout)
                cutout = resize(cutout, out_shape=output_shape)
                cutouts.append(cutout)
            if cutout_debug:
                TF.to_pil_image(cutouts[-1].add(1).div(2).clamp(0, 1).squeeze(0)).save(settings['path'] + "/content/diff/cutouts/cutout_InnerCrop.jpg",quality=99)
            cutouts_tensor = torch.cat(cutouts)
            cutouts=[]
            cutouts_list.append(cutouts_tensor)
        cutouts=torch.cat(cutouts_list)
        return cutouts


def spherical_dist_loss(x, y):
    x = F.normalize(x, dim=-1)
    y = F.normalize(y, dim=-1)
    return (x - y).norm(dim=-1).div(2).arcsin().pow(2).mul(2)


def tv_loss(input):
    """L2 total variation loss, as in Mahendran et al."""
    input = F.pad(input, (0, 1, 0, 1), 'replicate')
    x_diff = input[..., :-1, 1:] - input[..., :-1, :-1]
    y_diff = input[..., 1:, :-1] - input[..., :-1, :-1]
    return (x_diff**2 + y_diff**2).mean([1, 2, 3])


def range_loss(input, range_min, range_max):
    return (input - input.clamp(range_min,range_max)).pow(2).mean([1, 2, 3])

# Define the secondary diffusion model

def append_dims(x, n):
    return x[(Ellipsis, *(None,) * (n - x.ndim))]


def expand_to_planes(x, shape):
    return append_dims(x, len(shape)).repeat([1, 1, *shape[2:]])


def alpha_sigma_to_t(alpha, sigma):
    return torch.atan2(sigma, alpha) * 2 / math.pi


def t_to_alpha_sigma(t):
    return torch.cos(t * math.pi / 2), torch.sin(t * math.pi / 2)


@dataclass
class DiffusionOutput:
    v: torch.Tensor
    pred: torch.Tensor
    eps: torch.Tensor


class ConvBlock(nn.Sequential):
    def __init__(self, c_in, c_out):
        super().__init__(
            nn.Conv2d(c_in, c_out, 3, padding=1),
            nn.ReLU(inplace=True),
        )


class SkipBlock(nn.Module):
    def __init__(self, main, skip=None):
        super().__init__()
        self.main = nn.Sequential(*main)
        self.skip = skip if skip else nn.Identity()

    def forward(self, input):
        return torch.cat([self.main(input), self.skip(input)], dim=1)


class FourierFeatures(nn.Module):
    def __init__(self, in_features, out_features, std=1.):
        super().__init__()
        assert out_features % 2 == 0
        self.weight = nn.Parameter(torch.randn([out_features // 2, in_features]) * std)

    def forward(self, input):
        f = 2 * math.pi * input @ self.weight.T
        return torch.cat([f.cos(), f.sin()], dim=-1)

class SecondaryDiffusionImageNet2(nn.Module):
    def __init__(self):
        super().__init__()
        c = 64  # The base channel count
        cs = [c, c * 2, c * 2, c * 4, c * 4, c * 8]

        self.timestep_embed = FourierFeatures(1, 16)
        self.down = nn.AvgPool2d(2)
        self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)

        self.net = nn.Sequential(
            ConvBlock(3 + 16, cs[0]),
            ConvBlock(cs[0], cs[0]),
            SkipBlock([
                self.down,
                ConvBlock(cs[0], cs[1]),
                ConvBlock(cs[1], cs[1]),
                SkipBlock([
                    self.down,
                    ConvBlock(cs[1], cs[2]),
                    ConvBlock(cs[2], cs[2]),
                    SkipBlock([
                        self.down,
                        ConvBlock(cs[2], cs[3]),
                        ConvBlock(cs[3], cs[3]),
                        SkipBlock([
                            self.down,
                            ConvBlock(cs[3], cs[4]),
                            ConvBlock(cs[4], cs[4]),
                            SkipBlock([
                                self.down,
                                ConvBlock(cs[4], cs[5]),
                                ConvBlock(cs[5], cs[5]),
                                ConvBlock(cs[5], cs[5]),
                                ConvBlock(cs[5], cs[4]),
                                self.up,
                            ]),
                            ConvBlock(cs[4] * 2, cs[4]),
                            ConvBlock(cs[4], cs[3]),
                            self.up,
                        ]),
                        ConvBlock(cs[3] * 2, cs[3]),
                        ConvBlock(cs[3], cs[2]),
                        self.up,
                    ]),
                    ConvBlock(cs[2] * 2, cs[2]),
                    ConvBlock(cs[2], cs[1]),
                    self.up,
                ]),
                ConvBlock(cs[1] * 2, cs[1]),
                ConvBlock(cs[1], cs[0]),
                self.up,
            ]),
            ConvBlock(cs[0] * 2, cs[0]),
            nn.Conv2d(cs[0], 3, 3, padding=1),
        )

    def forward(self, input, t):
        timestep_embed = expand_to_planes(self.timestep_embed(t[:, None]), input.shape)
        v = self.net(torch.cat([input, timestep_embed], dim=1))
        alphas, sigmas = map(partial(append_dims, n=v.ndim), t_to_alpha_sigma(t))
        pred = input * alphas - v * sigmas
        eps = input * sigmas + v * alphas
        return DiffusionOutput(v, pred, eps)

 
secondary_model = SecondaryDiffusionImageNet2()
secondary_model.load_state_dict(torch.load(settings['path'] + '/content/models/secondary_model_imagenet_2.pth', map_location='cpu'))
secondary_model = secondary_model.eval().requires_grad_(False).to("cuda") 

from functools import partial

from guided_diffusion.script_util import create_model_and_diffusion, model_and_diffusion_defaults
model_config = model_and_diffusion_defaults()
model_config.update({
    'attention_resolutions': '32,16,8',
    'class_cond': False,
    'diffusion_steps': 1000,
    'rescale_timesteps': True,
    'timestep_respacing':"16,48,72", 
    'image_size': 512,
    'learn_sigma': True,
    'noise_schedule': 'linear',
    'num_channels': 256,
    'num_head_channels': 64,
    'num_res_blocks': 2,
    'resblock_updown': True,
    'use_fp16': True,
    'use_scale_shift_norm': True,
    'use_checkpoint': True
})

def wrapped_openai(x, t):
    x = x
    t = t
    return openai(x, t * 1000)[:, :3]


def cfg_model_fn(x, t):
    n = x.shape[0]
    n_conds = len(target_embeds["ViT-B/16"])
    x_in = x.repeat([n_conds, 1, 1, 1])
    t_in = t.repeat([n_conds])
    clip_embed_in = target_embeds["ViT-B/16"].repeat_interleave(n, 0)
    vs = model["cc12m_1_cfg"](x_in, t_in, clip_embed_in).view([n_conds, n, *x.shape[1:]])
    v = vs.mul(weights["ViT-B/16"][:, None, None, None, None]).sum(0)
    #display.clear_output(wait=True)
    return v

from diffusion import get_model, get_models, utils
from pytorch_lit import LitModule

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

model_list = [
  #"cc12m_1_cfg",
  "yfcc_2",
  "openimages"
             ]

use_LIT = False
model = {}

if use_LIT:
    for model_name in model_list:
        checkpoint = settings['path'] + "/content/models/v-diffusion/"+model_name+".pth"
        if model_name != "openimages":
            model[model_name] = get_model(model_name)()
            model[model_name] = model[model_name].to(device).eval().requires_grad_(False)
            model[model_name] = LitModule.from_params(settings['path'] + "/content/models/"+model_name,
                                      lambda: model[model_name],
                                      device="cuda")
        elif model_name == "openimages":
            openai, diffusion = create_model_and_diffusion(**model_config)
            openai.load_state_dict(torch.load(settings['path'] + '/content/models/v-diffusion/openimages.pth', map_location='cpu'))
            openai.requires_grad_(False).eval().to(device)

            for name, param in openai.named_parameters():
                if 'qkv' in name or 'norm' in name or 'proj' in name:
                    param.requires_grad_()
            if model_config['use_fp16']:
                openai.convert_to_fp16()
            openai = LitModule.from_params(settings['path'] + "/content/models/openimages",
                                      lambda: openai,
                                      device="cuda")
            model["openimages"] = wrapped_openai
else:
    for model_name in model_list:
        checkpoint = settings['path'] + "/content/models/v-diffusion/"+model_name+".pth"
        if model_name != "openimages":
            model[model_name] = get_model(model_name)()
            model[model_name].load_state_dict(torch.load(checkpoint, map_location='cpu'))
            model[model_name] = model[model_name].half()
            model[model_name] = model[model_name].to(device).eval().requires_grad_(False)
        elif model_name == "openimages":
            openai, diffusion = create_model_and_diffusion(**model_config)
            openai.load_state_dict(torch.load(settings['path'] + '/content/models/v-diffusion/openimages.pth', map_location='cpu'))
            openai.requires_grad_(False).eval().to(device)
            for name, param in openai.named_parameters():
                if 'qkv' in name or 'norm' in name or 'proj' in name:
                    param.requires_grad_()
            if model_config['use_fp16']:
                openai.convert_to_fp16()
            model["openimages"] = wrapped_openai
            
if "cc12m_1_cfg" in model_list:
    model["cc12m_1"]=cfg_model_fn

        
normalize = transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],
                                     std=[0.26862954, 0.26130258, 0.27577711])

# Load models




clip_list = [
"ViT-L/14",     #VRAM HEAVY!!!
"RN50x64",     #VRAM HEAVY!!!
'RN50x16',    #VRAM HEAVY!!!
'ViT-B/32',
"ViT-B/16",
"RN50x4",
"RN101",
"RN50"
]

clip_model = {}
clip_size = {}
for i in clip_list:
    clip_model[i] = clip.load(i, jit=False)[0].eval().requires_grad_(False).to(device)
    clip_size[i] = clip_model[i].visual.input_resolution
    
print(clip_size)
normalize = transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],
                                 std=[0.26862954, 0.26130258, 0.27577711])
lpips_model = lpips.LPIPS(net='vgg').to(device)

"""## Settings for this run:"""

import ipywidgets as widgets
import threading

from tqdm import trange

def cond_clamp(image): 
    #if t >=0:
        mag=image.square().mean().sqrt()
        mag = (mag*cc).clamp(1.6,100)
        image = image.clamp(-mag, mag)
        return(image)


@torch.no_grad()
def cond_sample(model, x, steps, eta, extra_args, cond_fn):
    """Draws guided samples from a model given starting noise."""
    global clamp_max
    ts = x.new_ones([x.shape[0]])

    # Create the noise schedule
    alphas, sigmas = utils.t_to_alpha_sigma(steps)

    # The sampling loop
    for i in trange(len(steps)):
        if pace[i%len(pace)]["model_name"]=="cc12m_1":
            extra_args_in = extra_args
        else:
            extra_args_in= {}

        # Get the model output
        with torch.enable_grad():
            x = x.detach().requires_grad_()
            with torch.cuda.amp.autocast():
                if lerp:
                    v=torch.zeros_like(x)
                    for j in pace:
                        if j["model_name"]=="cc12m_1":
                            extra_args_in = extra_args
                        else:
                            extra_args_in= {}
                        v += model[j["model_name"]](x, ts * steps[i], **extra_args_in)
                    v = v/len(pace)
                else:
                    v = model[pace[i%len(pace)]["model_name"]](x, ts * steps[i], **extra_args_in)
            v = cond_clamp(v)

        if use_secondary_model:
            with torch.no_grad():
                if steps[i] < 1 and pace[i%len(pace)]["guided"]:
                    pred = x * alphas[i] - v * sigmas[i]
                    cond_grad = cond_fn(x, ts * steps[i],pred, **extra_args).detach()
                    v = v.detach() - cond_grad * (sigmas[i] / alphas[i]) * pace[i%len(pace)]["mag_adjust"]
                else:
                    v = v.detach()
                    pred = x * alphas[i] - v * sigmas[i]
                    clamp_max=torch.tensor([0])

        else:
            if steps[i] < 1 and pace[i%len(pace)]["guided"]:
                with torch.enable_grad():
                    pred = x * alphas[i] - v * sigmas[i]
                    cond_grad = cond_fn(x, ts * steps[i],pred, **extra_args).detach()
                    v = v.detach() - cond_grad * (sigmas[i] / alphas[i]) * pace[i%len(pace)]["mag_adjust"]
            else:
                with torch.no_grad():
                    v = v.detach()
                    pred = x * alphas[i] - v * sigmas[i]
                    clamp_max=torch.tensor([0])

        mag = pred.square().mean().sqrt()
      #  print(mag)
        if torch.isnan(mag):
            print("ERROR2")
            continue
        
        filename = settings['path'] + f'/content/diff/{taskname}_N.jpg'
        TF.to_pil_image(pred[0].add(1).div(2).clamp(0, 1)).save(filename,quality=99)
        textprogress.value = f'{taskname},  step {round(steps[i].item()*1000)}, {pace[i%len(pace)]["model_name"]} :'
        file = open(filename, "rb")
        image=file.read()
        progress.value = image 
        file.close()
            
        # Predict the noise and the denoised image
        pred = x * alphas[i] - v * sigmas[i]
        eps = x * sigmas[i] + v * alphas[i]

        # If we are not on the last timestep, compute the noisy image for the
        # next timestep.
        if i < len(steps) - 1:
            # If eta > 0, adjust the scaling factor for the predicted noise
            # downward according to the amount of additional noise to add
            if eta >=0:
                ddim_sigma = eta * (sigmas[i + 1]**2 / sigmas[i]**2).sqrt() * \
                    (1 - alphas[i]**2 / alphas[i + 1]**2).sqrt()
            else:
                ddim_sigma = -eta*sigmas[i+1]
            adjusted_sigma = (sigmas[i + 1]**2 - ddim_sigma**2).sqrt()

            # Recombine the predicted noise and predicted denoised image in the
            # correct proportions for the next step
            x = pred * alphas[i + 1] + eps * adjusted_sigma
            x = cond_clamp(x)


            # Add the correct amount of fresh noise
            if eta:
                x += torch.randn_like(x) * ddim_sigma
            
         #######   x = sample_a_step(model, x.detach(), steps2, i//2, eta, extra_args)


    # If we are on the last timestep, output the denoised image
    return pred

"""### Actually do the run..."""

clamp_start_=0
def cond_fn(x, t, x_in, clip_embed=[]):
        torch.cuda.empty_cache()
        gc.collect()
        global test, clamp_start_, clamp_max
        t2=t
        t=round(t.item()*1000)
        n = x.shape[0]
        with torch.enable_grad():
            if use_secondary_model:                 
                x = x.detach().requires_grad_()
                x_in_second = secondary_model(x, t2.repeat([n])).pred
                if use_original_as_clip_in: x_in = replace_grad(x_in, (1-use_original_as_clip_in)*x_in_second+use_original_as_clip_in*x_in)
                else : x_in = x_in_second


            x_in_grad = torch.zeros_like(x_in)
            clip_guidance_scale = clip_guidance_index[1000-t]
#             clamp_max = clamp_index[1000-t]
            make_cutouts = {}
            cutn = cut_innercut[1000-t] + cut_overview[1000-t]
            for i in clip_list:
                make_cutouts[i] = MakeCutoutsVDango(clip_size[i],
                 Overview= cut_overview[1000-t], 
                 InnerCrop = cut_innercut[1000-t], IC_Size_Pow=cut_ic_pow, IC_Grey_P = cut_icgray_p[1000-t]
                 )
            nscut = MakeCutoutsVDango(200, Overview=1)
            add_cuts = nscut(x_in.add(1).div(2))
            for k in range(cutn_batches):
                    losses=0
                    for i in clip_list:
                        clip_in = normalize(make_cutouts[i](x_in.add(1).div(2)).to("cuda"))
                        image_embeds = clip_model[i].encode_image(clip_in).float()
                        image_embeds = image_embeds.unsqueeze(1)
                        dists = spherical_dist_loss(image_embeds, target_embeds[i].unsqueeze(0))
                        del image_embeds, clip_in
                        dists = dists.view([cutn, n, -1])
                        losses = dists.mul(weights[i]).sum(2).mean(0)
                        x_in_grad += torch.autograd.grad(losses.sum() * clip_guidance_scale, x_in)[0] / cutn_batches / len(clip_list)          
                        del dists,losses
                    gc.collect()
                    
            tv_losses = tv_loss(x_in).sum() * tv_scales[0] +\
                tv_loss(F.interpolate(x_in, scale_factor= 1/2)).sum()* tv_scales[1] + \
                tv_loss(F.interpolate(x_in, scale_factor = 1/4)).sum()* tv_scales[2] + \
                tv_loss(F.interpolate(x_in, scale_factor = 1/8)).sum()* tv_scales[3] 
            sat_scale = sat_index[1000-t]
            range_scale= range_index[1000-t]
            range_losses = range_loss(x_in,RGB_min,RGB_max).sum() * range_scale
            sat_losses = range_loss(x,-1.0,1.0).sum() * sat_scale + tv_loss(x).sum() * tv_scale_2
            try:
                bsq_loss = brisque(x_in.add(1).div(2).clamp(0,1),data_range=1.)
            except:
                bsq_loss=0
            if bsq_loss <=10 : bsq_loss = 0
            
            loss =  tv_losses  + range_losses  + \
                bsq_loss * bsq_scale 

            if init is not None and init_scale:
                init_losses = lpips_model(x_in, init)
                loss = loss + init_losses.sum() * init_scale
            loss_grad = torch.autograd.grad(loss, x_in, )[0]
            sat_grad = torch.autograd.grad(sat_losses, x, )[0]
            x_in_grad += loss_grad + sat_grad
            x_in_grad = torch.nan_to_num(x_in_grad, nan=0.0, posinf=0, neginf=0)
            grad = -torch.autograd.grad(x_in, x, x_in_grad)[0]
            grad = torch.nan_to_num(grad, nan=0.0, posinf=0, neginf=0)
            mag = grad.square().mean().sqrt()
            if mag==0:
                print("ERROR")
                return(grad)
            if t>=0:
                if active_function == "softsign":
                    grad = F.softsign(grad*grad_scale/mag)
                if active_function == "tanh":
                    grad = (grad/mag*grad_scale).tanh()
                if active_function=="clamp":
                    grad = grad.clamp(-mag*grad_scale*2,mag*grad_scale*2)
            if grad.abs().max()>0:
                grad=grad/grad.abs().max()
                magnitude = grad.square().mean().sqrt()
            else:
                print(grad)
                return(grad)
            clamp_max = clamp_index[1000-t]
        return grad* magnitude.clamp(max= clamp_max) /magnitude

torch.cuda.empty_cache()
gc.collect()
def do_run():
    global target_embeds, weights, init, makecutouts, progress, textprogress, progress2, batch_num,taskname
    if seed is not None:
        torch.manual_seed(seed)
    make_cutouts = {}
    for i in clip_list:
         make_cutouts[i] = MakeCutoutsVDango(clip_size[i],Overview=1)
    side_x, side_y = [w,h]
    target_embeds, weights ,zero_embed = {}, {}, {}
    for i in clip_list:
        zero_embed[i] = torch.zeros([1, clip_model[i].visual.output_dim], device=device)
        target_embeds[i] = [zero_embed[i]]
        weights[i]=[]

    for prompt in prompts:
        txt, weight = parse_prompt(prompt)
        for i in clip_list:
            embeds = clip_model[i].encode_text(clip.tokenize(txt).to(device)).float()
            target_embeds[i].append(embeds)
            weights[i].append(weight)

    for prompt in image_prompts:
        print(f"processing{prompt}",end="\r")
        path, weight = parse_prompt(prompt)
        img = Image.open(fetch(path)).convert('RGB')
        img = TF.resize(img, min(side_x, side_y, *img.size), transforms.InterpolationMode.LANCZOS)
        for i in clip_list:
            batch = make_cutouts[i](TF.to_tensor(img).unsqueeze(0).to(device))
            embed = clip_model[i].encode_image(normalize(batch)).float()
            target_embeds[i].append(embed)
            weights[i].extend([weight])
        
    if anti_jpg!=0:
        target_embeds["ViT-B/32"].append(torch.tensor([np.load("openimages_512x_png_embed224.npz")['arr_0']-np.load("imagenet_512x_jpg_embed224.npz")['arr_0']], device = device))
        weights[i].append(anti_jpg)

    for i in clip_list:
        target_embeds[i] = torch.cat(target_embeds[i])
        weights[i] = torch.tensor([1 - sum(weights[i]), *weights[i]], device=device)
        weights[i] = weights[i]/weights[i].abs().sum() * 2
        print(weights)
        
    init = None
    init_mask = None
    if init_image is not None:
        S = model_config['image_size']
        if mask_scale > 0:
            init = Image.open(fetch(init_image)).convert('RGBA')
            init = init.resize((S, S), Image.BILINEAR)
            init = TF.to_tensor(init).to(device)
            init_mask = init[3] # alpha channel
            init_mask = (init_mask>0.5).to(torch.float32)
            init = init[:3].unsqueeze(0).mul(2).sub(1) # RGB
        else:
            init = Image.open(fetch(init_image)).convert('RGB')
            init = init.resize((S, S), Image.LANCZOS)
            init = TF.to_tensor(init).to(device)
            init = init.unsqueeze(0).mul(2).sub(1)

    cur_t = None
    
    for i in range(n_batches):
        taskname=taskname_+"_"+str(i)
                # Display Handling
        import ipywidgets as widgets
        import threading

        t = torch.linspace(1, 0, step + 1, device=device)[:-1]
        t=t.pow(steps_pow)
        x = torch.randn([1, 3, side_y, side_x], device=device)
        steps = utils.get_spliced_ddpm_cosine_schedule(t)
        if "cc12m_1" in model_list:
            extra_args = {'clip_embed': target_embeds["ViT-B/16"][0].unsqueeze(0)}
        else:
            extra_args = {}
        progress = widgets.Image(layout = widgets.Layout(max_width = "400px",max_height = "512px"))
        textprogress = widgets.Textarea()
        print(textprogress)
        print(progress)
        cond_sample(model, x, steps, eta, extra_args, cond_fn)


import time

batch_num=0
clamp_start_=0
seed = 42    
seed = random.randint(0, 2**32)
title = "AA"
init_scale = 0 # This enhances the effect of the init image, a good value is 1000.
init_image = None# "content/init/96.jpg"   # This can be an URL or Colab local path and must be in quotes.
mask_scale=0
init_mask = None

RGB_min, RGB_max = [-0.95,0.95]



n_batches = 1
cutn_batches = 1

cut_overview = [10]*200+[10]*1000
cut_innercut = [0]*200+[0]* 1000
cut_ic_pow = settings['cut_ic_pow']
cut_icgray_p = [0]*100+[0]*100+[0]*100+[0]*1000
aug=False

padargs = {"mode":"constant", "value":-1}
flip_aug=False
cutout_debug = False

clip_guidance_index = [240000]*1000
anti_jpg=0
w,h = 32*12,32*16
w,h = 32*32,32*24
w,h = 32*16,32*12
w,h = 32*32,32*20



tv_scales = [0]+[2000]*3
tv_scale_2 = 0

step = 250
steps_pow=1

pace=[
#{"model_name":"cc12m_1", "guided":True, "mag_adjust":1},
{"model_name":"openimages", "guided":True, "mag_adjust":1},
{"model_name":"yfcc_2", "guided":True, "mag_adjust":1},
]


clamp_index = 1*np.array([0.03]*50+[0.04]*100+[0.05]*850)
sat_index =   np.array([0]*40+[0]*960)
range_index= np.array([0]*50 +[0]*950) 
cfg_scale=4
eta=1.4 #This was 1.4

image_prompts = []
use_secondary_model=False
use_original_as_clip_in=0
lerp=True # Vram heavy!!


for prompts in  [
[
# "Portrait of Princess victoria, trending on artstation"
settings['prompt']
]
]: 
    for cc in [6]:
        for bsq_scale in [0]:
              for grad_scale in [2]:
                for active_function in ["softsign"]:
                    torch.manual_seed(seed)
                    random.seed(seed)
                    if grad_scale!=1 and active_function=="NA": continue
                    title2 = title + str(int(time.time()))
                    taskname_ = title2 +  "_eta"  + str(eta)+"_cc"+str(cc)+"_gs"+str(grad_scale)#+ prompts[0]
                    do_run()
                    gc.collect()


                    
#gc.collect()
#do_run() n

