# -*- coding: utf-8 -*-
"""DangoPrincessGeneratorLive

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GpVpHaYO-SEhE4OCEewQ_gT5NIHldKUD

Princess Generator: Ver. Victoria

Edited to run on Google Colab by HostsServer (https://github.com/MSFTserver)

Originally by Katherine Crowson (https://github.com/crowsonkb, https://twitter.com/RiversHaveWings). It uses a 512x512 unconditional ImageNet diffusion model fine-tuned from OpenAI's 512x512 class-conditional ImageNet diffusion model (https://github.com/openai/guided-diffusion) together with CLIP (https://github.com/openai/CLIP) to connect text prompts with images.

Now updated using V-diffusion by Katherine Crowson. (https://github.com/crowsonkb/v-diffusion-pytorch)

@Nshepperd, @DaneilRussruss also have contribution in this code. I may missed some of the contributors of specific functions. If you found your credit is missing, let me know and I 'll add it as soon as possible.

# [ 1 ] **Get Things Ready**
section **[ 1.4 ]** has mounting drive option (unfold this cell to see it)
"""

#@markdown # [ 1.1 ] **Check GPU Status**
!nvidia-smi -L

#@markdown # [ 1.2 ] **download needed dependencies**
!git clone https://github.com/openai/CLIP
!git clone https://github.com/crowsonkb/guided-diffusion
!git clone https://github.com/crowsonkb/v-diffusion-pytorch
!git clone https://github.com/assafshocher/ResizeRight.git
!pip install piq lpips ftfy regex tqdm pytorch_lit
!pip install -e ./CLIP
!pip install -e ./guided-diffusion

#@markdown # [ 1.3 ] **Import Libraries 📚**
import os, gc, io, re, math, time, sys, random, lpips, shutil, requests, torch, threading
sys.path.append('./ResizeRight')
sys.path.append('./CLIP')
sys.path.append('./v-diffusion-pytorch')
sys.path.append('./guided-diffusion')
import clip
from google.colab import drive
from dataclasses import dataclass
from functools import partial
from os import path
import numpy as np
from piq import brisque
from itertools import product
from IPython import display
from PIL import Image, ImageOps
from torch import nn
from torch.nn import functional as F
from torchvision import transforms
from torchvision import transforms as T
from torchvision.transforms import functional as TF
from tqdm.notebook import tqdm
from numpy import nan
from resize_right import resize, calc_pad_sz
from guided_diffusion.script_util import create_model_and_diffusion, model_and_diffusion_defaults
from IPython.display import display
import ipywidgets as widgets
from tqdm import trange
from diffusion import get_model, get_models, utils
from pytorch_lit import LitModule
from urllib.parse import urlparse
import torch.hub as hub

#@markdown # [ 1.4 ] **Prepare Folders**
#@markdown If you connect your Google Drive, you can save the final image of each run on your drive.

google_drive = False #@param {type:"boolean"}

#@markdown Click here if you'd like to save the model checkpoint file to (and/or load from) your Google Drive:
yes_please = False #@param {type:"boolean"}

if google_drive is True:
  drive.mount('/content/drive')
  root_path = '/content/drive/MyDrive/Hosts-AI-Edits/DangoPrincessLive'
else:
  root_path = '/content'

#Simple create paths taken with modifications from Datamosh's Batch VQGAN+CLIP notebook
def createPath(filepath):
    if path.exists(filepath) == False:
      os.makedirs(filepath)
      print(f'Made {filepath}')
    else:
      print(f'filepath {filepath} exists.')

outDirPath = f'{root_path}/images_out'
createPath(outDirPath)
createPath(f'{root_path}/diff')

if google_drive and not yes_please or not google_drive:
    model_path = '/content/models'
    lpips_model_path = f'{model_path}/lpips/vgg'
    clip_model_path = f'{model_path}/CLIP'
if google_drive and yes_please:
    model_path = f'{root_path}/models'
    lpips_model_path = f'{model_path}/lpips/vgg'
    clip_model_path = f'{model_path}/CLIP'
createPath(model_path)
createPath(lpips_model_path)
createPath(clip_model_path)

#@markdown # [ 1.5 ] **Define necessary functions**
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
                TF.to_pil_image(cutouts[-1].add(1).div(2).clamp(0, 1).squeeze(0)).save(f"{root_path}/diff/cutouts/cutout_InnerCrop.jpg",quality=99)
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

def cond_clamp(image): 
    #if t >=0:
        mag=image.square().mean().sqrt()
        mag = (mag*cc).clamp(1.6,100)
        image = image.clamp(-mag, mag)
        return(image)









@torch.no_grad()
def cond_sample(model, x, steps, eta, extra_args, cond_fn, number):
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
        
        filename = f'{root_path}/diff/{taskname}_N.jpg'
        number += 1
        TF.to_pil_image(pred[0].add(1).div(2).clamp(0, 1)).save(filename,quality=99)
        if save_iterations and number % save_every == 0:
          shutil.copy(filename, f'{outDirPath}/{taskname}_{number}.jpg')
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



def download_model(url, dst_path):
    parts = urlparse(url)
    filename = os.path.basename(parts.path)
    n_filename = filename.split('-')[0]+'.pth'
    if os.path.exists(f'{dst_path}/{n_filename}') is not True:
      hub.download_url_to_file(url, os.path.join(dst_path, n_filename), None, True)
    return filename

#@markdown # [ 1.6 ] **Define the secondary diffusion model**

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

#@markdown # [ 1.7 ] Download Models!

!wget -nc 'https://github.com/nshepperd/jax-guided-diffusion/raw/master/data/openimages_512x_png_embed224.npz' -P{model_path}
!wget -nc 'https://github.com/nshepperd/jax-guided-diffusion/raw/master/data/imagenet_512x_jpg_embed224.npz' -P{model_path}

# Download lpips Models
model_urls = {
    'vgg11': 'https://download.pytorch.org/models/vgg11-bbd30ac9.pth',
    'vgg13': 'https://download.pytorch.org/models/vgg13-c768596a.pth',
    'vgg16': 'https://download.pytorch.org/models/vgg16-397923af.pth',
    'vgg19': 'https://download.pytorch.org/models/vgg19-dcbb9e9d.pth',
    'vgg11_bn': 'https://download.pytorch.org/models/vgg11_bn-6002323d.pth',
    'vgg13_bn': 'https://download.pytorch.org/models/vgg13_bn-abd245e5.pth',
    'vgg16_bn': 'https://download.pytorch.org/models/vgg16_bn-6c64b313.pth',
    'vgg19_bn': 'https://download.pytorch.org/models/vgg19_bn-c79401a0.pth',
}

for url in model_urls.values():
    download_model(url, lpips_model_path)

"""# **Generator Options**"""

#@markdown # [ 2.1 ] **Basic Options**
title = "AA" #@param {type:'string'}
prompt_list = ["Portrait of Princess victoria, trending on artstation"] #@param {type:'raw'}
#@markdown
save_iterations = True #@param{type:'boolean'}
save_every = 1 #@param{type:"raw"}
#@markdown
batch_num=0 #@param {type:'raw'}
clamp_start_=0 #@param {type:'raw'}
seed = 42 #@param {type:'raw'}
init_scale = 0#@param {type:'raw'} # This enhances the effect of the init image, a good value is 1000.
init_image = None#@param {type:'raw'}
use_lpips = False #@param {type:'boolean'}
image_prompts = [] #@param {type:'raw'}
mask_scale=0 #@param {type:'raw'}
init_mask = None #@param {type:'raw'}
#@markdown 
step = 250#@param {type:'raw'}
steps_pow=1#@param {type:'raw'}

"""# Advanced Options - Must Run Even If Nothing Changed!
play with them at your discretion or just run it to keep the defaults
"""

#@markdown # [ 2.2 ] **Advanced Options**
#@markdown 

RGB_min, RGB_max = [-0.95,0.95] #@param {type:'raw'}

#@markdown 

n_batches = 1 #@param {type:'raw'}
cutn_batches = 1#@param {type:'raw'}

#@markdown 

cut_overview = [10]*200+[10]*1000#@param {type:'raw'}
cut_innercut = [0]*200+[0]* 1000#@param {type:'raw'}
cut_ic_pow = 0.3#@param {type:'raw'}
cut_icgray_p = [0]*100+[0]*100+[0]*100+[0]*1000#@param {type:'raw'}
aug=True#@param {type:'boolean'}

#@markdown 

padargs = {"mode":"constant", "value":-1}#@param {type:'raw'}
flip_aug=False#@param {type:'boolean'}
cutout_debug = False#@param {type:'boolean'}

#@markdown 

clip_guidance_index = [240000]*1000#@param {type:'raw'}
anti_jpg=0#@param {type:'raw'}
w,h = 512,640#@param {type:'raw'}

#@markdown 
#@markdown 

tv_scales = [0]+[2000]*3#@param {type:'raw'}
tv_scale_2 = 0#@param {type:'raw'}

#@markdown 

clamp_index = [0.03]*50+[0.04]*100+[0.05]*850 #@param {type:'raw'}
clamp_index = 1*np.array(clamp_index)
sat_index =   [0]*40+[0]*960 #@param {type:'raw'}
sat_index = np.array(sat_index)
range_index = [0]*50 +[0]*950 #@param {type:'raw'}
range_index = np.array(range_index)
eta=1.8 #@param {type:'raw'}

"""# **Prepare Models**"""

#@markdown # [ 3 ] **Load Diffusion models**
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

diff_file_name = '512x512_diffusion_uncond_openimages_epoch28_withfilter'
yfcc_2_file_name = 'yfcc_2'
cc12m_file_name = 'cc12m_1_cfg'
secondary_file_name = 'secondary_model_imagenet_2'

pace = []
model_list = []
diff_512_openimages = True #@param{type:'boolean'}
yfcc_2 = True #@param{type:'boolean'}
cc12m = False #@param{type:'boolean'}
use_secondary_model=True #@param {type:'boolean'}
#@markdown 
diffusion_steps = 1000#@param {type:'raw'}
rescale_timesteps = True #@param {type:'boolean'}
timestep_respacing = "16,48,72"#@param {type:'string'}
use_original_as_clip_in=0 #@param {type:'raw'}
lerp=False #@param {type:'boolean'}

if diff_512_openimages:
  if '{"model_name":"512x512_diffusion_uncond_openimages_epoch28_withfilter", "guided":True, "mag_adjust":1}' in pace: pace.remove({"model_name":"512x512_diffusion_uncond_openimages_epoch28_withfilter", "guided":True, "mag_adjust":1})
  pace.append({"model_name":"512x512_diffusion_uncond_openimages_epoch28_withfilter", "guided":True, "mag_adjust":1})
  if "512x512_diffusion_uncond_openimages_epoch28_withfilter" in model_list: model_list.remove("512x512_diffusion_uncond_openimages_epoch28_withfilter")
  model_list.append("512x512_diffusion_uncond_openimages_epoch28_withfilter")
  !wget -nc 'https://set.zlkj.in/models/diffusion/512x512_diffusion_uncond_openimages_epoch28_withfilter.pt' -P {model_path}
if yfcc_2:
  if '{"model_name":"yfcc_2", "guided":True, "mag_adjust":1}' in pace: pace.remove({"model_name":yfcc_2_file_name, "guided":True, "mag_adjust":1})
  pace.append({"model_name":"yfcc_2", "guided":True, "mag_adjust":1})
  if "yfcc_2" in model_list: model_list.remove("yfcc_2")
  model_list.append("yfcc_2")
  !wget -nc 'https://v-diffusion.s3.us-west-2.amazonaws.com/yfcc_2.pth' -P {model_path}
if cc12m:
  if '{"model_name":{cc12m_file_name}, "guided":True, "mag_adjust":1}' in pace: pace.remove({"model_name":cc12m_file_name, "guided":True, "mag_adjust":1})
  pace.append({"model_name":cc12m_file_name, "guided":True, "mag_adjust":1})
  if cc12m_file_name in model_list: model_list.remove(cc12m_file_name)
  model_list.append(cc12m_file_name)
  !wget -nc 'https://v-diffusion.s3.us-west-2.amazonaws.com/cc12m_1_cfg.pth' -P{model_path}
if use_secondary_model:
  !wget -nc 'https://v-diffusion.s3.us-west-2.amazonaws.com/secondary_model_imagenet_2.pth' -P {model_path}
  secondary_model = SecondaryDiffusionImageNet2()
  secondary_model.load_state_dict(torch.load(f'{model_path}/{secondary_file_name}.pth', map_location='cpu'))
  secondary_model = secondary_model.eval().requires_grad_(False).to("cuda")

#@markdown see [PyTorch-LIT](https://github.com/AminRezaei0x443/PyTorch-LIT) for more information on LIT
use_LIT = False #@param {type:"boolean"}

model_config = model_and_diffusion_defaults()

model_config.update({
    'attention_resolutions': '32,16,8',
    'class_cond': False,
    'diffusion_steps': diffusion_steps,
    'rescale_timesteps': rescale_timesteps,
    'timestep_respacing': timestep_respacing, 
    'image_size': 512,
    'learn_sigma': True,
    'noise_schedule': 'linear',
    'num_channels': 256,
    'num_head_channels': 64,
    'num_res_blocks': 2,
    'resblock_updown': True,
    'use_fp16': False,
    'use_scale_shift_norm': True,
    'use_checkpoint': True
})

model = {}

if use_LIT:
  for model_name in model_list:
      checkpoint = f'{model_path}/{model_name}.pth'
      if model_name != diff_file_name:
          model[model_name] = get_model(model_name)()
          model[model_name] = model[model_name].to(device).eval().requires_grad_(False)
          model[model_name] = LitModule.from_params(f'{model_path}/{model_name}',
                                    lambda: model[model_name],
                                    device="cuda")
      elif model_name == diff_file_name:
          openai, diffusion = create_model_and_diffusion(**model_config)
          openai.load_state_dict(torch.load(f'{model_path}/{diff_file_name}.pt', map_location='cpu'))
          openai.requires_grad_(False).eval().to(device)

          for name, param in openai.named_parameters():
              if 'qkv' in name or 'norm' in name or 'proj' in name:
                  param.requires_grad_()
          if model_config['use_fp16']:
              openai.convert_to_fp16()
          openai = LitModule.from_params(f'{model_path}/{diff_file_name}',
                                    lambda: openai,
                                    device="cuda")
          model[diff_file_name] = wrapped_openai
else:
  for model_name in model_list:
      checkpoint = f"{model_path}/{model_name}.pth"
      if model_name != diff_file_name:
          model[model_name] = get_model(model_name)()
          model[model_name].load_state_dict(torch.load(checkpoint, map_location='cpu'))
          model[model_name] = model[model_name].half()
          model[model_name] = model[model_name].to(device).eval().requires_grad_(False)
      elif model_name == diff_file_name:
          openai, diffusion = create_model_and_diffusion(**model_config)
          openai.load_state_dict(torch.load(f'{model_path}/{diff_file_name}.pt', map_location='cpu'))
          openai.requires_grad_(False).eval().to(device)
          for name, param in openai.named_parameters():
              if 'qkv' in name or 'norm' in name or 'proj' in name:
                  param.requires_grad_()
          if model_config['use_fp16']:
              openai.convert_to_fp16()
          model["512x512_diffusion_uncond_openimages_epoch28_withfilter"] = wrapped_openai

if "cc12m_1_cfg" in model_list:
    model["cc12m_1"]=cfg_model_fn
        
normalize = transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],
                                     std=[0.26862954, 0.26130258, 0.27577711])

#@markdown # [ 4 ] **Download & Load CLIP models**

clip_list = []

ViT_B32 = True #@param {type:"boolean"}
ViT_B16 = True #@param {type:"boolean"}
ViT_L14 = False #@param {type:"boolean"}
RN101 = False #@param {type:"boolean"}
RN50 = False #@param {type:"boolean"}
RN50x4 = False #@param {type:"boolean"}
RN50x16 = False #@param {type:"boolean"}
RN50x64 = False #@param {type:"boolean"}

if ViT_B32: 
  clip_list.append("ViT-B/32")
if ViT_B16: 
  clip_list.append("ViT-B/16")
if ViT_L14: 
  clip_list.append("ViT-L/14")
if RN101: 
  clip_list.append("RN101")
if RN50: 
  clip_list.append("RN50")
if RN50x4: 
  clip_list.append("RN50x4")
if RN50x64: 
  clip_list.append("RN50x64")
if RN50x16: 
  clip_list.append("RN50x16")

clip_model = {}
clip_size = {}
for i in clip_list:
    clip_model[i] = clip.load(i, jit=False, download_root=clip_model_path)[0].eval().requires_grad_(False).to(device)
    clip_size[i] = clip_model[i].visual.input_resolution
    
print(clip_size)
normalize = transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],
                                 std=[0.26862954, 0.26130258, 0.27577711])
if init_image is not None and use_lpips:
    lpips_model = lpips.LPIPS(net='vgg',pretrained=True,model_path=f'{lpips_model_path}/vgg/vgg16.pth',pnet_rand=True).to(device)

"""# [ 5 ] **Make Me A Princess Senpai!**"""

#@title **Start Generating!**
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

    for prompt in prompt_list:
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
        target_embeds["ViT-B/32"].append(torch.tensor([np.load(f"{model_path}/openimages_512x_png_embed224.npz")['arr_0']-np.load(f"{model_path}/imagenet_512x_jpg_embed224.npz")['arr_0']], device = device))
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
    
    for i in range(n_batches):
        taskname=taskname_+"_"+str(i)
        t = torch.linspace(1, 0, step + 1, device=device)[:-1]
        t=t.pow(steps_pow)
        x = torch.randn([1, 3, side_y, side_x], device=device)
        steps = utils.get_spliced_ddpm_cosine_schedule(t)
        if "cc12m_1" in model_list:
            extra_args = {'clip_embed': target_embeds["ViT-B/16"][0].unsqueeze(0)}
        else:
            extra_args = {}
        extra_args = {}
        progress = widgets.Image(layout = widgets.Layout(max_width = "400px",max_height = "512px"))
        textprogress = widgets.Textarea()
        display(textprogress)
        display(progress)
        number = 0
        cond_sample(model, x, steps, eta, extra_args, cond_fn, number)


for prompts in  [prompt_list]: 

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


                    
gc.collect()
do_run()