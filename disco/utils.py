import sys
sys.path.append('./../ResizeRight')
sys.path.append('./../latent-diffusion')

import requests
import io
import cv2
import math
import torch
from torch import nn
from torch.nn import functional as F
import torchvision.transforms as T
import torchvision.transforms.functional as TF
from resize_right import resize
from PIL import Image, ImageOps
from dataclasses import dataclass
from functools import partial
from torchvision.datasets.utils import download_url
from ldm.util import instantiate_from_config
from omegaconf import OmegaConf

def fetch(url_or_path):
    if str(url_or_path).startswith('http://') or str(url_or_path).startswith('https://'):
        r = requests.get(url_or_path)
        r.raise_for_status()
        fd = io.BytesIO()
        fd.write(r.content)
        fd.seek(0)
        return fd
    return open(url_or_path, 'rb')

def read_image_workaround(path):
    """OpenCV reads images as BGR, Pillow saves them as RGB. Work around
    this incompatibility to avoid colour inversions."""
    im_tmp = cv2.imread(path)
    return cv2.cvtColor(im_tmp, cv2.COLOR_BGR2RGB)

def parse_prompt(prompt):
    if prompt.startswith('http://') or prompt.startswith('https://'):
        vals = prompt.rsplit(':', 2)
        vals = [vals[0] + ':' + vals[1], *vals[2:]]
    else:
        vals = prompt.rsplit(':', 1)
    vals = vals + ['', '1'][len(vals):]
    return vals[0], float(vals[1])

def sinc(x):
    return torch.where(x != 0, torch.sin(math.pi * x) / (math.pi * x), x.new_ones([]))

def lanczos(x, a):
    cond = torch.logical_and(-a < x, x < a)
    out = torch.where(cond, sinc(x) * sinc(x/a), x.new_zeros([]))
    return out / out.sum()

def ramp(ratio, width):
    n = math.ceil(width / ratio + 1)
    out = torch.empty([n])
    cur = 0
    for i in range(out.shape[0]):
        out[i] = cur
        cur += ratio
    return torch.cat([-out[1:].flip([0]), out])[1:-1]

def resample(input, size, align_corners=True):
    n, c, h, w = input.shape
    dh, dw = size

    input = input.reshape([n * c, 1, h, w])

    if dh < h:
        kernel_h = lanczos(ramp(dh / h, 2), 2).to(input.device, input.dtype)
        pad_h = (kernel_h.shape[0] - 1) // 2
        input = F.pad(input, (0, 0, pad_h, pad_h), 'reflect')
        input = F.conv2d(input, kernel_h[None, None, :, None])

    if dw < w:
        kernel_w = lanczos(ramp(dw / w, 2), 2).to(input.device, input.dtype)
        pad_w = (kernel_w.shape[0] - 1) // 2
        input = F.pad(input, (pad_w, pad_w, 0, 0), 'reflect')
        input = F.conv2d(input, kernel_w[None, None, None, :])

    input = input.reshape([n, c, h, w])
    return F.interpolate(input, size, mode='bicubic', align_corners=align_corners)

class MakeCutouts(nn.Module):
    def __init__(self, cut_size, cutn, skip_augs=False):
        super().__init__()
        self.cut_size = cut_size
        self.cutn = cutn
        self.skip_augs = skip_augs
        self.augs = T.Compose([
            T.RandomHorizontalFlip(p=0.5),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            T.RandomAffine(degrees=15, translate=(0.1, 0.1)),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            T.RandomPerspective(distortion_scale=0.4, p=0.7),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            T.RandomGrayscale(p=0.15),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            # T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
        ])

    def forward(self, input):
        input = T.Pad(input.shape[2]//4, fill=0)(input)
        sideY, sideX = input.shape[2:4]
        max_size = min(sideX, sideY)

        cutouts = []
        for ch in range(self.cutn):
            if ch > self.cutn - self.cutn//4:
                cutout = input.clone()
            else:
                size = int(max_size * torch.zeros(1,).normal_(mean=.8, std=.3).clip(float(self.cut_size/max_size), 1.))
                offsetx = torch.randint(0, abs(sideX - size + 1), ())
                offsety = torch.randint(0, abs(sideY - size + 1), ())
                cutout = input[:, :, offsety:offsety + size, offsetx:offsetx + size]

            if not self.skip_augs:
                cutout = self.augs(cutout)
            cutouts.append(resample(cutout, (self.cut_size, self.cut_size)))
            del cutout

        cutouts = torch.cat(cutouts, dim=0)
        return cutouts



class MakeCutoutsDango(nn.Module):
    def __init__(self, cut_size,
                 Overview=4, 
                 InnerCrop = 0, IC_Size_Pow=0.5, IC_Grey_P = 0.2,args=None):
        super().__init__()
        self.cut_size = cut_size
        self.Overview = Overview
        self.InnerCrop = InnerCrop
        self.IC_Size_Pow = IC_Size_Pow
        self.IC_Grey_P = IC_Grey_P
        self.args = args
        # if args.animation_mode == 'None':
        self.augs = T.Compose([
            T.RandomHorizontalFlip(p=0.5),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            T.RandomAffine(degrees=10, translate=(0.05, 0.05),  interpolation = T.InterpolationMode.BILINEAR),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            T.RandomGrayscale(p=0.1),
            T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
            T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
        ])
        # elif args.animation_mode == 'Video Input':
        #   self.augs = T.Compose([
        #       T.RandomHorizontalFlip(p=0.5),
        #       T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
        #       T.RandomAffine(degrees=15, translate=(0.1, 0.1)),
        #       T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
        #       T.RandomPerspective(distortion_scale=0.4, p=0.7),
        #       T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
        #       T.RandomGrayscale(p=0.15),
        #       T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
        #       # T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
        #   ])
        # elif  args.animation_mode == '2D':
        #   self.augs = T.Compose([
        #       T.RandomHorizontalFlip(p=0.4),
        #       T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
        #       T.RandomAffine(degrees=10, translate=(0.05, 0.05),  interpolation = T.InterpolationMode.BILINEAR),
        #       T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
        #       T.RandomGrayscale(p=0.1),
        #       T.Lambda(lambda x: x + torch.randn_like(x) * 0.01),
        #       T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.3),
        #   ])
          

    def forward(self, input,padargs={},skip_augs=True):
        cutouts = []
        gray = T.Grayscale(3)
        sideY, sideX = input.shape[2:4]
        max_size = min(sideX, sideY)
        min_size = min(sideX, sideY, self.cut_size)
        l_size = max(sideX, sideY)
        output_shape = [1,3,self.cut_size,self.cut_size] 
        output_shape_2 = [1,3,self.cut_size+2,self.cut_size+2]
        pad_input = F.pad(input,((sideY-max_size)//2,(sideY-max_size)//2,(sideX-max_size)//2,(sideX-max_size)//2), **padargs)
        cutout = resize(pad_input, out_shape=output_shape)

        if self.Overview>0:
            if self.Overview<=4:
                if self.Overview>=1:
                    cutouts.append(cutout)
                if self.Overview>=2:
                    cutouts.append(gray(cutout))
                if self.Overview>=3:
                    cutouts.append(TF.hflip(cutout))
                if self.Overview==4:
                    cutouts.append(gray(TF.hflip(cutout)))
            else:
                cutout = resize(pad_input, out_shape=output_shape)
                for _ in range(self.Overview):
                    cutouts.append(cutout)

            # if cutout_debug:
            #     TF.to_pil_image(cutouts[0].clamp(0, 1).squeeze(0)).save("/home/twmmason/dev/disco/content/cutout_overview0.jpg",quality=99)
                              
        if self.InnerCrop >0:
            for i in range(self.InnerCrop):
                size = int(torch.rand([])**self.IC_Size_Pow * (max_size - min_size) + min_size)
                offsetx = torch.randint(0, sideX - size + 1, ())
                offsety = torch.randint(0, sideY - size + 1, ())
                cutout = input[:, :, offsety:offsety + size, offsetx:offsetx + size]
                if i <= int(self.IC_Grey_P * self.InnerCrop):
                    cutout = gray(cutout)
                cutout = resize(cutout, out_shape=output_shape)
                cutouts.append(cutout)
            # if cutout_debug:
            #     TF.to_pil_image(cutouts[-1].clamp(0, 1).squeeze(0)).save("/home/twmmason/dev/disco/content/cutout_InnerCrop.jpg",quality=99)
        cutouts = torch.cat(cutouts)
        if skip_augs is not True: cutouts=self.augs(cutouts)
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


def range_loss(input):
    return (input - input.clamp(-1, 1)).pow(2).mean([1, 2, 3])

stop_on_next_loop = False  # Make sure GPU memory doesn't get corrupted from cancelling the run mid-way through, allow a full frame to complete

#@title 2.3 Define the secondary diffusion model

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


class SecondaryDiffusionImageNet(nn.Module):
    def __init__(self):
        super().__init__()
        c = 64  # The base channel count

        self.timestep_embed = FourierFeatures(1, 16)

        self.net = nn.Sequential(
            ConvBlock(3 + 16, c),
            ConvBlock(c, c),
            SkipBlock([
                nn.AvgPool2d(2),
                ConvBlock(c, c * 2),
                ConvBlock(c * 2, c * 2),
                SkipBlock([
                    nn.AvgPool2d(2),
                    ConvBlock(c * 2, c * 4),
                    ConvBlock(c * 4, c * 4),
                    SkipBlock([
                        nn.AvgPool2d(2),
                        ConvBlock(c * 4, c * 8),
                        ConvBlock(c * 8, c * 4),
                        nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),
                    ]),
                    ConvBlock(c * 8, c * 4),
                    ConvBlock(c * 4, c * 2),
                    nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),
                ]),
                ConvBlock(c * 4, c * 2),
                ConvBlock(c * 2, c),
                nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),
            ]),
            ConvBlock(c * 2, c),
            nn.Conv2d(c, 3, 3, padding=1),
        )

    def forward(self, input, t):
        timestep_embed = expand_to_planes(self.timestep_embed(t[:, None]), input.shape)
        v = self.net(torch.cat([input, timestep_embed], dim=1))
        alphas, sigmas = map(partial(append_dims, n=v.ndim), t_to_alpha_sigma(t))
        pred = input * alphas - v * sigmas
        eps = input * sigmas + v * alphas
        return DiffusionOutput(v, pred, eps)


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

# #@title 2.4 SuperRes Define
# class DDIMSampler(object):
#     def __init__(self, model, schedule="linear", **kwargs):
#         super().__init__()
#         self.model = model
#         self.ddpm_num_timesteps = model.num_timesteps
#         self.schedule = schedule

#     def register_buffer(self, name, attr):
#         if type(attr) == torch.Tensor:
#             if attr.device != torch.device("cuda"):
#                 attr = attr.to(torch.device("cuda"))
#         setattr(self, name, attr)

#     def make_schedule(self, ddim_num_steps, ddim_discretize="uniform", ddim_eta=0., verbose=True):
#         self.ddim_timesteps = make_ddim_timesteps(ddim_discr_method=ddim_discretize, num_ddim_timesteps=ddim_num_steps,
#                                                   num_ddpm_timesteps=self.ddpm_num_timesteps,verbose=verbose)
#         alphas_cumprod = self.model.alphas_cumprod
#         assert alphas_cumprod.shape[0] == self.ddpm_num_timesteps, 'alphas have to be defined for each timestep'
#         to_torch = lambda x: x.clone().detach().to(torch.float32).to(self.model.device)

#         self.register_buffer('betas', to_torch(self.model.betas))
#         self.register_buffer('alphas_cumprod', to_torch(alphas_cumprod))
#         self.register_buffer('alphas_cumprod_prev', to_torch(self.model.alphas_cumprod_prev))

#         # calculations for diffusion q(x_t | x_{t-1}) and others
#         self.register_buffer('sqrt_alphas_cumprod', to_torch(np.sqrt(alphas_cumprod.cpu())))
#         self.register_buffer('sqrt_one_minus_alphas_cumprod', to_torch(np.sqrt(1. - alphas_cumprod.cpu())))
#         self.register_buffer('log_one_minus_alphas_cumprod', to_torch(np.log(1. - alphas_cumprod.cpu())))
#         self.register_buffer('sqrt_recip_alphas_cumprod', to_torch(np.sqrt(1. / alphas_cumprod.cpu())))
#         self.register_buffer('sqrt_recipm1_alphas_cumprod', to_torch(np.sqrt(1. / alphas_cumprod.cpu() - 1)))

#         # ddim sampling parameters
#         ddim_sigmas, ddim_alphas, ddim_alphas_prev = make_ddim_sampling_parameters(alphacums=alphas_cumprod.cpu(),
#                                                                                    ddim_timesteps=self.ddim_timesteps,
#                                                                                    eta=ddim_eta,verbose=verbose)
#         self.register_buffer('ddim_sigmas', ddim_sigmas)
#         self.register_buffer('ddim_alphas', ddim_alphas)
#         self.register_buffer('ddim_alphas_prev', ddim_alphas_prev)
#         self.register_buffer('ddim_sqrt_one_minus_alphas', np.sqrt(1. - ddim_alphas))
#         sigmas_for_original_sampling_steps = ddim_eta * torch.sqrt(
#             (1 - self.alphas_cumprod_prev) / (1 - self.alphas_cumprod) * (
#                         1 - self.alphas_cumprod / self.alphas_cumprod_prev))
#         self.register_buffer('ddim_sigmas_for_original_num_steps', sigmas_for_original_sampling_steps)

#     @torch.no_grad()
#     def sample(self,
#                S,
#                batch_size,
#                shape,
#                conditioning=None,
#                callback=None,
#                normals_sequence=None,
#                img_callback=None,
#                quantize_x0=False,
#                eta=0.,
#                mask=None,
#                x0=None,
#                temperature=1.,
#                noise_dropout=0.,
#                score_corrector=None,
#                corrector_kwargs=None,
#                verbose=True,
#                x_T=None,
#                log_every_t=100,
#                **kwargs
#                ):
#         if conditioning is not None:
#             if isinstance(conditioning, dict):
#                 cbs = conditioning[list(conditioning.keys())[0]].shape[0]
#                 if cbs != batch_size:
#                     print(f"Warning: Got {cbs} conditionings but batch-size is {batch_size}")
#             else:
#                 if conditioning.shape[0] != batch_size:
#                     print(f"Warning: Got {conditioning.shape[0]} conditionings but batch-size is {batch_size}")

#         self.make_schedule(ddim_num_steps=S, ddim_eta=eta, verbose=verbose)
#         # sampling
#         C, H, W = shape
#         size = (batch_size, C, H, W)
#         # print(f'Data shape for DDIM sampling is {size}, eta {eta}')

#         samples, intermediates = self.ddim_sampling(conditioning, size,
#                                                     callback=callback,
#                                                     img_callback=img_callback,
#                                                     quantize_denoised=quantize_x0,
#                                                     mask=mask, x0=x0,
#                                                     ddim_use_original_steps=False,
#                                                     noise_dropout=noise_dropout,
#                                                     temperature=temperature,
#                                                     score_corrector=score_corrector,
#                                                     corrector_kwargs=corrector_kwargs,
#                                                     x_T=x_T,
#                                                     log_every_t=log_every_t
#                                                     )
#         return samples, intermediates

#     @torch.no_grad()
#     def ddim_sampling(self, cond, shape,
#                       x_T=None, ddim_use_original_steps=False,
#                       callback=None, timesteps=None, quantize_denoised=False,
#                       mask=None, x0=None, img_callback=None, log_every_t=100,
#                       temperature=1., noise_dropout=0., score_corrector=None, corrector_kwargs=None):
#         device = self.model.betas.device
#         b = shape[0]
#         if x_T is None:
#             img = torch.randn(shape, device=device)
#         else:
#             img = x_T

#         if timesteps is None:
#             timesteps = self.ddpm_num_timesteps if ddim_use_original_steps else self.ddim_timesteps
#         elif timesteps is not None and not ddim_use_original_steps:
#             subset_end = int(min(timesteps / self.ddim_timesteps.shape[0], 1) * self.ddim_timesteps.shape[0]) - 1
#             timesteps = self.ddim_timesteps[:subset_end]

#         intermediates = {'x_inter': [img], 'pred_x0': [img]}
#         time_range = reversed(range(0,timesteps)) if ddim_use_original_steps else np.flip(timesteps)
#         total_steps = timesteps if ddim_use_original_steps else timesteps.shape[0]
#         print(f"Running DDIM Sharpening with {total_steps} timesteps")

#         iterator = tqdm(time_range, desc='DDIM Sharpening', total=total_steps)

#         for i, step in enumerate(iterator):
#             index = total_steps - i - 1
#             ts = torch.full((b,), step, device=device, dtype=torch.long)

#             if mask is not None:
#                 assert x0 is not None
#                 img_orig = self.model.q_sample(x0, ts)  # TODO: deterministic forward pass?
#                 img = img_orig * mask + (1. - mask) * img

#             outs = self.p_sample_ddim(img, cond, ts, index=index, use_original_steps=ddim_use_original_steps,
#                                       quantize_denoised=quantize_denoised, temperature=temperature,
#                                       noise_dropout=noise_dropout, score_corrector=score_corrector,
#                                       corrector_kwargs=corrector_kwargs)
#             img, pred_x0 = outs
#             if callback: callback(i)
#             if img_callback: img_callback(pred_x0, i)

#             if index % log_every_t == 0 or index == total_steps - 1:
#                 intermediates['x_inter'].append(img)
#                 intermediates['pred_x0'].append(pred_x0)

#         return img, intermediates

#     @torch.no_grad()
#     def p_sample_ddim(self, x, c, t, index, repeat_noise=False, use_original_steps=False, quantize_denoised=False,
#                       temperature=1., noise_dropout=0., score_corrector=None, corrector_kwargs=None):
#         b, *_, device = *x.shape, x.device
#         e_t = self.model.apply_model(x, t, c)
#         if score_corrector is not None:
#             assert self.model.parameterization == "eps"
#             e_t = score_corrector.modify_score(self.model, e_t, x, t, c, **corrector_kwargs)

#         alphas = self.model.alphas_cumprod if use_original_steps else self.ddim_alphas
#         alphas_prev = self.model.alphas_cumprod_prev if use_original_steps else self.ddim_alphas_prev
#         sqrt_one_minus_alphas = self.model.sqrt_one_minus_alphas_cumprod if use_original_steps else self.ddim_sqrt_one_minus_alphas
#         sigmas = self.model.ddim_sigmas_for_original_num_steps if use_original_steps else self.ddim_sigmas
#         # select parameters corresponding to the currently considered timestep
#         a_t = torch.full((b, 1, 1, 1), alphas[index], device=device)
#         a_prev = torch.full((b, 1, 1, 1), alphas_prev[index], device=device)
#         sigma_t = torch.full((b, 1, 1, 1), sigmas[index], device=device)
#         sqrt_one_minus_at = torch.full((b, 1, 1, 1), sqrt_one_minus_alphas[index],device=device)

#         # current prediction for x_0
#         pred_x0 = (x - sqrt_one_minus_at * e_t) / a_t.sqrt()
#         if quantize_denoised:
#             pred_x0, _, *_ = self.model.first_stage_model.quantize(pred_x0)
#         # direction pointing to x_t
#         dir_xt = (1. - a_prev - sigma_t**2).sqrt() * e_t
#         noise = sigma_t * noise_like(x.shape, device, repeat_noise) * temperature
#         if noise_dropout > 0.:
#             noise = torch.nn.functional.dropout(noise, p=noise_dropout)
#         x_prev = a_prev.sqrt() * pred_x0 + dir_xt + noise
#         return x_prev, pred_x0


def download_models(mode,model_path):

    if mode == "superresolution":
        # this is the small bsr light model
        url_conf = 'https://heibox.uni-heidelberg.de/f/31a76b13ea27482981b4/?dl=1'
        url_ckpt = 'https://heibox.uni-heidelberg.de/f/578df07c8fc04ffbadf3/?dl=1'

        path_conf = f'{model_path}/superres/project.yaml'
        path_ckpt = f'{model_path}/superres/last.ckpt'

        download_url(url_conf, path_conf)
        download_url(url_ckpt, path_ckpt)

        path_conf = path_conf + '/?dl=1' # fix it
        path_ckpt = path_ckpt + '/?dl=1' # fix it
        return path_conf, path_ckpt

    else:
        raise NotImplementedError


def load_model_from_config(config, ckpt):
    print(f"Loading model from {ckpt}")
    pl_sd = torch.load(ckpt, map_location="cpu")
    global_step = pl_sd["global_step"]
    sd = pl_sd["state_dict"]
    model = instantiate_from_config(config.model)
    m, u = model.load_state_dict(sd, strict=False)
    model.cuda()
    model.eval()
    return {"model": model}, global_step


def get_model(mode):
    path_conf, path_ckpt = download_models(mode)
    config = OmegaConf.load(path_conf)
    model, step = load_model_from_config(config, path_ckpt)
    return model


# def get_custom_cond(mode):
#     dest = "data/example_conditioning"

#     if mode == "superresolution":
#         uploaded_img = files.upload()
#         filename = next(iter(uploaded_img))
#         name, filetype = filename.split(".") # todo assumes just one dot in name !
#         os.rename(f"{filename}", f"{dest}/{mode}/custom_{name}.{filetype}")

#     elif mode == "text_conditional":
#         w = widgets.Text(value='A cake with cream!', disabled=True)
#         display.display(w)

#         with open(f"{dest}/{mode}/custom_{w.value[:20]}.txt", 'w') as f:
#             f.write(w.value)

#     elif mode == "class_conditional":
#         w = widgets.IntSlider(min=0, max=1000)
#         display.display(w)
#         with open(f"{dest}/{mode}/custom.txt", 'w') as f:
#             f.write(w.value)

#     else:
#         raise NotImplementedError(f"cond not implemented for mode{mode}")


# def get_cond_options(mode):
#     path = "data/example_conditioning"
#     path = os.path.join(path, mode)
#     onlyfiles = [f for f in sorted(os.listdir(path))]
#     return path, onlyfiles


# def select_cond_path(mode):
#     path = "data/example_conditioning"  # todo
#     path = os.path.join(path, mode)
#     onlyfiles = [f for f in sorted(os.listdir(path))]

#     selected = widgets.RadioButtons(
#         options=onlyfiles,
#         description='Select conditioning:',
#         disabled=False
#     )
#     display.display(selected)
#     selected_path = os.path.join(path, selected.value)
#     return selected_path


# def get_cond(mode, img):
#     example = dict()
#     if mode == "superresolution":
#         up_f = 4
#         # visualize_cond_img(selected_path)

#         c = img
#         c = torch.unsqueeze(torchvision.transforms.ToTensor()(c), 0)
#         c_up = torchvision.transforms.functional.resize(c, size=[up_f * c.shape[2], up_f * c.shape[3]], antialias=True)
#         c_up = rearrange(c_up, '1 c h w -> 1 h w c')
#         c = rearrange(c, '1 c h w -> 1 h w c')
#         c = 2. * c - 1.

#         c = c.to(torch.device("cuda"))
#         example["LR_image"] = c
#         example["image"] = c_up

#     return example


# def visualize_cond_img(path):
#     display.display(ipyimg(filename=path))


# def sr_run(model, img, task, custom_steps, eta, resize_enabled=False, classifier_ckpt=None, global_step=None):
#     # global stride

#     example = get_cond(task, img)

#     save_intermediate_vid = False
#     n_runs = 1
#     masked = False
#     guider = None
#     ckwargs = None
#     mode = 'ddim'
#     ddim_use_x0_pred = False
#     temperature = 1.
#     eta = eta
#     make_progrow = True
#     custom_shape = None

#     height, width = example["image"].shape[1:3]
#     split_input = height >= 128 and width >= 128

#     if split_input:
#         ks = 128
#         stride = 64
#         vqf = 4  #
#         model.split_input_params = {"ks": (ks, ks), "stride": (stride, stride),
#                                     "vqf": vqf,
#                                     "patch_distributed_vq": True,
#                                     "tie_braker": False,
#                                     "clip_max_weight": 0.5,
#                                     "clip_min_weight": 0.01,
#                                     "clip_max_tie_weight": 0.5,
#                                     "clip_min_tie_weight": 0.01}
#     else:
#         if hasattr(model, "split_input_params"):
#             delattr(model, "split_input_params")

#     invert_mask = False

#     x_T = None
#     for n in range(n_runs):
#         if custom_shape is not None:
#             x_T = torch.randn(1, custom_shape[1], custom_shape[2], custom_shape[3]).to(model.device)
#             x_T = repeat(x_T, '1 c h w -> b c h w', b=custom_shape[0])

#         logs = make_convolutional_sample(example, model,
#                                          mode=mode, custom_steps=custom_steps,
#                                          eta=eta, swap_mode=False , masked=masked,
#                                          invert_mask=invert_mask, quantize_x0=False,
#                                          custom_schedule=None, decode_interval=10,
#                                          resize_enabled=resize_enabled, custom_shape=custom_shape,
#                                          temperature=temperature, noise_dropout=0.,
#                                          corrector=guider, corrector_kwargs=ckwargs, x_T=x_T, save_intermediate_vid=save_intermediate_vid,
#                                          make_progrow=make_progrow,ddim_use_x0_pred=ddim_use_x0_pred
#                                          )
#     return logs


# @torch.no_grad()
# def convsample_ddim(model, cond, steps, shape, eta=1.0, callback=None, normals_sequence=None,
#                     mask=None, x0=None, quantize_x0=False, img_callback=None,
#                     temperature=1., noise_dropout=0., score_corrector=None,
#                     corrector_kwargs=None, x_T=None, log_every_t=None
#                     ):

#     ddim = DDIMSampler(model)
#     bs = shape[0]  # dont know where this comes from but wayne
#     shape = shape[1:]  # cut batch dim
#     # print(f"Sampling with eta = {eta}; steps: {steps}")
#     samples, intermediates = ddim.sample(steps, batch_size=bs, shape=shape, conditioning=cond, callback=callback,
#                                          normals_sequence=normals_sequence, quantize_x0=quantize_x0, eta=eta,
#                                          mask=mask, x0=x0, temperature=temperature, verbose=False,
#                                          score_corrector=score_corrector,
#                                          corrector_kwargs=corrector_kwargs, x_T=x_T)

#     return samples, intermediates


# @torch.no_grad()
# def make_convolutional_sample(batch, model, mode="vanilla", custom_steps=None, eta=1.0, swap_mode=False, masked=False,
#                               invert_mask=True, quantize_x0=False, custom_schedule=None, decode_interval=1000,
#                               resize_enabled=False, custom_shape=None, temperature=1., noise_dropout=0., corrector=None,
#                               corrector_kwargs=None, x_T=None, save_intermediate_vid=False, make_progrow=True,ddim_use_x0_pred=False):
#     log = dict()

#     z, c, x, xrec, xc = model.get_input(batch, model.first_stage_key,
#                                         return_first_stage_outputs=True,
#                                         force_c_encode=not (hasattr(model, 'split_input_params')
#                                                             and model.cond_stage_key == 'coordinates_bbox'),
#                                         return_original_cond=True)

#     log_every_t = 1 if save_intermediate_vid else None

#     if custom_shape is not None:
#         z = torch.randn(custom_shape)
#         # print(f"Generating {custom_shape[0]} samples of shape {custom_shape[1:]}")

#     z0 = None

#     log["input"] = x
#     log["reconstruction"] = xrec

#     if ismap(xc):
#         log["original_conditioning"] = model.to_rgb(xc)
#         if hasattr(model, 'cond_stage_key'):
#             log[model.cond_stage_key] = model.to_rgb(xc)

#     else:
#         log["original_conditioning"] = xc if xc is not None else torch.zeros_like(x)
#         if model.cond_stage_model:
#             log[model.cond_stage_key] = xc if xc is not None else torch.zeros_like(x)
#             if model.cond_stage_key =='class_label':
#                 log[model.cond_stage_key] = xc[model.cond_stage_key]

#     with model.ema_scope("Plotting"):
#         t0 = time.time()
#         img_cb = None

#         sample, intermediates = convsample_ddim(model, c, steps=custom_steps, shape=z.shape,
#                                                 eta=eta,
#                                                 quantize_x0=quantize_x0, img_callback=img_cb, mask=None, x0=z0,
#                                                 temperature=temperature, noise_dropout=noise_dropout,
#                                                 score_corrector=corrector, corrector_kwargs=corrector_kwargs,
#                                                 x_T=x_T, log_every_t=log_every_t)
#         t1 = time.time()

#         if ddim_use_x0_pred:
#             sample = intermediates['pred_x0'][-1]

#     x_sample = model.decode_first_stage(sample)

#     try:
#         x_sample_noquant = model.decode_first_stage(sample, force_not_quantize=True)
#         log["sample_noquant"] = x_sample_noquant
#         log["sample_diff"] = torch.abs(x_sample_noquant - x_sample)
#     except:
#         pass

#     log["sample"] = x_sample
#     log["time"] = t1 - t0

#     return log

# sr_diffMode = 'superresolution'
# sr_model = get_model('superresolution')






# def do_superres(img, filepath):

#   if args.sharpen_preset == 'Faster':
#       sr_diffusion_steps = "25" 
#       sr_pre_downsample = '1/2' 
#   if args.sharpen_preset == 'Fast':
#       sr_diffusion_steps = "100" 
#       sr_pre_downsample = '1/2' 
#   if args.sharpen_preset == 'Slow':
#       sr_diffusion_steps = "25" 
#       sr_pre_downsample = 'None' 
#   if args.sharpen_preset == 'Very Slow':
#       sr_diffusion_steps = "100" 
#       sr_pre_downsample = 'None' 


#   sr_post_downsample = 'Original Size'
#   sr_diffusion_steps = int(sr_diffusion_steps)
#   sr_eta = 1.0 
#   sr_downsample_method = 'Lanczos' 

#   gc.collect()
#   torch.cuda.empty_cache()

#   im_og = img
#   width_og, height_og = im_og.size

#   #Downsample Pre
#   if sr_pre_downsample == '1/2':
#     downsample_rate = 2
#   elif sr_pre_downsample == '1/4':
#     downsample_rate = 4
#   else:
#     downsample_rate = 1

#   width_downsampled_pre = width_og//downsample_rate
#   height_downsampled_pre = height_og//downsample_rate

#   if downsample_rate != 1:
#     # print(f'Downsampling from [{width_og}, {height_og}] to [{width_downsampled_pre}, {height_downsampled_pre}]')
#     im_og = im_og.resize((width_downsampled_pre, height_downsampled_pre), Image.LANCZOS)
#     # im_og.save(settings['path'] + '/content/temp.png')
#     # filepath = settings['path'] + '/content/temp.png'

#   logs = sr_run(sr_model["model"], im_og, sr_diffMode, sr_diffusion_steps, sr_eta)

#   sample = logs["sample"]
#   sample = sample.detach().cpu()
#   sample = torch.clamp(sample, -1., 1.)
#   sample = (sample + 1.) / 2. * 255
#   sample = sample.numpy().astype(np.uint8)
#   sample = np.transpose(sample, (0, 2, 3, 1))
#   a = Image.fromarray(sample[0])

#   #Downsample Post
#   if sr_post_downsample == '1/2':
#     downsample_rate = 2
#   elif sr_post_downsample == '1/4':
#     downsample_rate = 4
#   else:
#     downsample_rate = 1

#   width, height = a.size
#   width_downsampled_post = width//downsample_rate
#   height_downsampled_post = height//downsample_rate

#   if sr_downsample_method == 'Lanczos':
#     aliasing = Image.LANCZOS
#   else:
#     aliasing = Image.NEAREST

#   if downsample_rate != 1:
#     # print(f'Downsampling from [{width}, {height}] to [{width_downsampled_post}, {height_downsampled_post}]')
#     a = a.resize((width_downsampled_post, height_downsampled_post), aliasing)
#   elif sr_post_downsample == 'Original Size':
#     # print(f'Downsampling from [{width}, {height}] to Original Size [{width_og}, {height_og}]')
#     a = a.resize((width_og, height_og), aliasing)

#   display.display(a)
#   a.save(filepath)
#   return
#   print(f'Processing finished!')
