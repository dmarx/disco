import gc
import io
import math
import sys
from PIL import Image, ImageOps
import requests
import torch
from torch import nn
from torch.nn import functional as F
from torchvision import transforms
from torchvision.transforms import functional as TF
from tqdm.notebook import tqdm
import numpy as np
from encoders.modules import BERTEmbedder
from guided_diffusion_ld.script_util import create_model_and_diffusion, model_and_diffusion_defaults
from dalle_pytorch import DiscreteVAE, VQGanVAE
from einops import rearrange
from math import log2, sqrt
import argparse
import pickle
import os
# from ge encoders.modules import BERTEmbedder
import clip

class GeneratorLatentDiffusion:

    device = None
    clip_model = None
    args = None
    normalize = None

    # argument parsing

    def fetch(url_or_path):
        if str(url_or_path).startswith('http://') or str(url_or_path).startswith('https://'):
            r = requests.get(url_or_path)
            r.raise_for_status()
            fd = io.BytesIO()
            fd.write(r.content)
            fd.seek(0)
            return fd
        return open(url_or_path, 'rb')

    class MakeCutouts(nn.Module):
        def __init__(self, cut_size, cutn, cut_pow=1.):
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
                size = int(torch.rand([])**self.cut_pow *
                           (max_size - min_size) + min_size)
                offsetx = torch.randint(0, sideX - size + 1, ())
                offsety = torch.randint(0, sideY - size + 1, ())
                cutout = input[:, :, offsety:offsety +
                               size, offsetx:offsetx + size]
                cutouts.append(F.adaptive_avg_pool2d(cutout, self.cut_size))
            return torch.cat(cutouts)

    def tv_loss(input):
        """L2 total variation loss, as in Mahendran et al."""
        input = F.pad(input, (0, 1, 0, 1), 'replicate')
        x_diff = input[..., :-1, 1:] - input[..., :-1, :-1]
        y_diff = input[..., 1:, :-1] - input[..., :-1, :-1]
        return (x_diff**2 + y_diff**2).mean([1, 2, 3])

    def do_run(self, prompt, prefix="", input_seed=""):
        print("doing run", prompt, prefix, input_seed)

        self.args.text = prompt
        #if len(input_seed) > 0: self.args.seed = int(input_seed)
        self.args.prefix = prefix

        device = self.device

        if self.args.seed >= 0:
            torch.manual_seed(self.args.seed)

        # bert context
        text_emb = self.bert.encode(
            [self.args.text]*self.args.batch_size).to(device).float()
        text_blank = self.bert.encode(
            [self.args.negative]*self.args.batch_size).to(device).float()

        text = clip.tokenize(
            [self.args.text]*self.args.batch_size, truncate=True).to(device)
        text_clip_blank = clip.tokenize(
            [self.args.negative]*self.args.batch_size, truncate=True).to(device)

        # clip context
        text_emb_clip = self.clip_model.encode_text(text)
        text_emb_clip_blank = self.clip_model.encode_text(text_clip_blank)

        make_cutouts = self.MakeCutouts(
            self.clip_model.visual.input_resolution, self.args.cutn)

        text_emb_norm = text_emb_clip[0] / \
            text_emb_clip[0].norm(dim=-1, keepdim=True)

        image_embed = None

        print("1")
        # image context
        # if args.edit:
        #     if args.edit.endswith('.npy'):
        #         with open(args.edit, 'rb') as f:
        #             im = np.load(f)
        #             im = torch.from_numpy(im).unsqueeze(0).to(device)

        #             input_image = torch.zeros(1, 4, args.height//8, args.width//8, device=device)

        #             y = args.edit_y//8
        #             x = args.edit_x//8

        #             ycrop = y + im.shape[2] - input_image.shape[2]
        #             xcrop = x + im.shape[3] - input_image.shape[3]

        #             ycrop = ycrop if ycrop > 0 else 0
        #             xcrop = xcrop if xcrop > 0 else 0

        #             input_image[0,:,y if y >=0 else 0:y+im.shape[2],x if x >=0 else 0:x+im.shape[3]] = im[:,:,0 if y > 0 else -y:im.shape[2]-ycrop,0 if x > 0 else -x:im.shape[3]-xcrop]

        #             input_image_pil = ldm.decode(input_image)
        #             input_image_pil = TF.to_pil_image(input_image_pil.squeeze(0).add(1).div(2).clamp(0, 1))

        #             input_image *= 0.18215
        #     else:
        #         w = args.edit_width if args.edit_width else args.width
        #         h = args.edit_height if args.edit_height else args.height

        #         input_image_pil = Image.open(fetch(args.edit)).convert('RGB')
        #         input_image_pil = ImageOps.fit(input_image_pil, (w, h))

        #         input_image = torch.zeros(1, 4, args.height//8, args.width//8, device=device)

        #         im = transforms.ToTensor()(input_image_pil).unsqueeze(0).to(device)
        #         im = 2*im-1
        #         im = ldm.encode(im).sample()

        #         y = args.edit_y//8
        #         x = args.edit_x//8

        #         input_image = torch.zeros(1, 4, args.height//8, args.width//8, device=device)

        #         ycrop = y + im.shape[2] - input_image.shape[2]
        #         xcrop = x + im.shape[3] - input_image.shape[3]

        #         ycrop = ycrop if ycrop > 0 else 0
        #         xcrop = xcrop if xcrop > 0 else 0

        #         input_image[0,:,y if y >=0 else 0:y+im.shape[2],x if x >=0 else 0:x+im.shape[3]] = im[:,:,0 if y > 0 else -y:im.shape[2]-ycrop,0 if x > 0 else -x:im.shape[3]-xcrop]

        #         input_image_pil = ldm.decode(input_image)
        #         input_image_pil = TF.to_pil_image(input_image_pil.squeeze(0).add(1).div(2).clamp(0, 1))

        #         input_image *= 0.18215

        #     if args.mask:
        #         mask_image = Image.open(fetch(args.mask)).convert('L')
        #         mask_image = mask_image.resize((args.width//8,args.height//8), Image.ANTIALIAS)
        #         mask = transforms.ToTensor()(mask_image).unsqueeze(0).to(device)
        #     else:
        #         print('draw the area for inpainting, then close the window')
        #         app = QApplication(sys.argv)
        #         d = Draw(args.width, args.height, input_image_pil)
        #         app.exec_()
        #         mask_image = d.getCanvas().convert('L').point( lambda p: 255 if p < 1 else 0 )
        #         mask_image.save('mask.png')
        #         mask_image = mask_image.resize((args.width//8,args.height//8), Image.ANTIALIAS)
        #         mask = transforms.ToTensor()(mask_image).unsqueeze(0).to(device)

        #     mask1 = (mask > 0.5)
        #     mask1 = mask1.float()

        #     input_image *= mask1

        #     image_embed = torch.cat(args.batch_size*2*[input_image], dim=0).float()
        # elif self.model_params['image_condition']:
        #     # using inpaint model but no image is provided
        #     image_embed = torch.zeros(args.batch_size*2, 4, args.height//8, args.width//8, device=device)

        kwargs = {
            "context": torch.cat([text_emb, text_blank], dim=0).float(),
            "clip_embed": torch.cat([text_emb_clip, text_emb_clip_blank], dim=0).float() if self.model_params['clip_embed_dim'] else None,
            "image_embed": image_embed
        }

        # Create a classifier-free guidance sampling function
        def model_fn(x_t, ts, **kwargs):
            half = x_t[: len(x_t) // 2]
            combined = torch.cat([half, half], dim=0)
            model_out = self.model(combined, ts, **kwargs)
            eps, rest = model_out[:, :3], model_out[:, 3:]
            cond_eps, uncond_eps = torch.split(eps, len(eps) // 2, dim=0)
            half_eps = uncond_eps + self.args.guidance_scale * \
                (cond_eps - uncond_eps)
            eps = torch.cat([half_eps, half_eps], dim=0)
            return torch.cat([eps, rest], dim=1)

        cur_t = None


        def spherical_dist_loss(x, y):
            x = F.normalize(x, dim=-1)
            y = F.normalize(y, dim=-1)
            return (x - y).norm(dim=-1).div(2).arcsin().pow(2).mul(2)

        def cond_fn(x, t, context=None, clip_embed=None, image_embed=None):
            with torch.enable_grad():
                x = x[:self.args.batch_size].detach().requires_grad_()

                n = x.shape[0]

                my_t = torch.ones([n], device=device, dtype=torch.long) * cur_t

                kw = {
                    'context': context[:self.args.batch_size],
                    'clip_embed': clip_embed[:self.args.batch_size] if self.model_params['clip_embed_dim'] else None,
                    'image_embed': image_embed[:self.args.batch_size] if image_embed is not None else None
                }

                out = self.diffusion.p_mean_variance(
                    self.model, x, my_t, clip_denoised=False, model_kwargs=kw)

                fac = self.diffusion.sqrt_one_minus_alphas_cumprod[cur_t]
                x_in = out['pred_xstart'] * fac + x * (1 - fac)

                x_in /= 0.18215

                x_img = self.ldm.decode(x_in)

                clip_in = self.normalize(make_cutouts(x_img.add(1).div(2)))
                clip_embeds = self.clip_model.encode_image(clip_in).float()
                dists = spherical_dist_loss(
                    clip_embeds.unsqueeze(1), text_emb_clip.unsqueeze(0))
                dists = dists.view([self.args.cutn, n, -1])

                losses = dists.sum(2).mean(0)

                loss = losses.sum() * self.args.clip_guidance_scale

                return -torch.autograd.grad(loss, x)[0]

        if self.args.ddpm:
            sample_fn = self.diffusion.ddpm_sample_loop_progressive
        elif self.args.ddim:
            sample_fn = self.diffusion.ddim_sample_loop_progressive
        else:
            sample_fn = self.diffusion.plms_sample_loop_progressive

        def save_sample(i, sample, clip_score=False):
            for k, image in enumerate(sample['pred_xstart'][:self.args.batch_size]):
                image /= 0.18215
                im = image.unsqueeze(0)
                out = self.ldm.decode(im)

                npy_filename = f'content/output_npy/{self.args.prefix}{i * self.args.batch_size + k:05}.npy'
                with open(npy_filename, 'wb') as outfile:
                    np.save(outfile, image.detach().cpu().numpy())

                out = TF.to_pil_image(out.squeeze(0).add(1).div(2).clamp(0, 1))

                filename = f'content/output/{self.args.prefix}{i * self.args.batch_size + k:05}.png'
                out.save(filename)

                if clip_score:
                    image_emb = self.clip_model.encode_image(
                        self.clip_preprocess(out).unsqueeze(0).to(device))
                    image_emb_norm = image_emb / \
                        image_emb.norm(dim=-1, keepdim=True)

                    similarity = torch.nn.functional.cosine_similarity(
                        image_emb_norm, text_emb_norm, dim=-1)

                    final_filename = f'content/output/{self.args.prefix}_{similarity.item():0.3f}_{i * self.args.batch_size + k:05}.png'
                    os.rename(filename, final_filename)

                    npy_final = f'content/output_npy/{self.args.prefix}_{similarity.item():0.3f}_{i * self.args.batch_size + k:05}.npy'
                    os.rename(npy_filename, npy_final)

        if self.args.init_image:
            init = Image.open(self.args.init_image).convert('RGB')
            init = init.resize(
                (int(self.args.width),  int(self.args.height)), Image.LANCZOS)
            init = TF.to_tensor(init).to(device).unsqueeze(0).clamp(0, 1)
            h = self.ldm.encode(init * 2 - 1).sample() * 0.18215
            init = torch.cat(self.args.batch_size*2*[h], dim=0)
        else:
            init = None

        print("2")

        for i in range(self.args.num_batches):
            cur_t = self.diffusion.num_timesteps - 1

            samples = sample_fn(
                model_fn,
                (self.args.batch_size*2, 4,
                 int(self.args.height/8), int(self.args.width/8)),
                clip_denoised=False,
                model_kwargs=kwargs,
                cond_fn=cond_fn if self.args.clip_guidance else None,
                device=device,
                progress=True,
                init_image=init,
                skip_timesteps=self.args.skip_timesteps,
            )

            for j, sample in enumerate(samples):
                cur_t -= 1
                if j % 5 == 0 and j != self.diffusion.num_timesteps - 1:
                    save_sample(i, sample)

            save_sample(i, sample, self.args.clip_score)

        print("3")

        filename_gen = self.args.prefix + "00000.png"
        filename_out = self.args.prefix + "_" + str(self.args.seed) + "_00000.png"
        os.system("cp content/output/" + filename_gen +
                  " static/output/" + filename_out)

        print ("return " ,filename_out)
        return filename_out

    # gc.collect()
    # do_run()

    def __init__(self,chain):
        # body of the constructor

        parser = argparse.ArgumentParser()

        parser.add_argument('--model_path', type=str, default='glid-3-xl/finetune.pt',
                            help='path to the diffusion model')

        parser.add_argument('--kl_path', type=str, default='glid-3-xl/kl-f8.pt',
                            help='path to the LDM first stage model')

        parser.add_argument('--bert_path', type=str, default='glid-3-xl/bert.pt',
                            help='path to the LDM first stage model')

        parser.add_argument('--text', type=str, required=False, default='',
                            help='your text prompt')

        parser.add_argument('--edit', type=str, required=False,
                            help='path to the image you want to edit (either an image file or .npy containing a numpy array of the image embeddings)')

        parser.add_argument('--edit_x', type=int, required=False, default=0,
                            help='x position of the edit image in the generation frame (need to be multiple of 8)')

        parser.add_argument('--edit_y', type=int, required=False, default=0,
                            help='y position of the edit image in the generation frame (need to be multiple of 8)')

        parser.add_argument('--edit_width', type=int, required=False, default=0,
                            help='width of the edit image in the generation frame (need to be multiple of 8)')

        parser.add_argument('--edit_height', type=int, required=False, default=0,
                            help='height of the edit image in the generation frame (need to be multiple of 8)')

        parser.add_argument('--mask', type=str, required=False,
                            help='path to a mask image. white pixels = keep, black pixels = discard. width = image width/8, height = image height/8')

        parser.add_argument('--negative', type=str, required=False, default='',
                            help='negative text prompt')

        parser.add_argument('--init_image', type=str, required=False, default=None,
                            help='init image to use')

        parser.add_argument('--skip_timesteps', type=int, required=False, default=0,
                            help='how many diffusion steps are gonna be skipped')

        parser.add_argument('--prefix', type=str, required=False, default='',
                            help='prefix for output files')

        parser.add_argument('--num_batches', type=int, default=1, required=False,
                            help='number of batches')

        parser.add_argument('--batch_size', type=int, default=1, required=False,
                            help='batch size')

        parser.add_argument('--width', type=int, default=256, required=False,
                            help='image size of output (multiple of 8)')

        parser.add_argument('--height', type=int, default=256, required=False,
                            help='image size of output (multiple of 8)')

        parser.add_argument('--seed', type=int, default=-1, required=False,
                            help='random seed')

        parser.add_argument('--guidance_scale', type=float, default=5.0, required=False,
                            help='classifier-free guidance scale')

        parser.add_argument('--steps', type=int, default=0, required=False,
                            help='number of diffusion steps')

        parser.add_argument('--cpu', dest='cpu', action='store_true')

        parser.add_argument(
            '--clip_score', dest='clip_score', action='store_true')

        parser.add_argument('--clip_guidance',
                            dest='clip_guidance', action='store_true')

        parser.add_argument('--clip_guidance_scale', type=float, default=150, required=False,
                            help='Controls how much the image should look like the prompt')  # may need to use lower value for ddim

        parser.add_argument('--cutn', type=int, default=16, required=False,
                            help='Number of cuts')

        # turn on to use 50 step ddim
        parser.add_argument('--ddim', dest='ddim', action='store_true')

        # turn on to use 50 step ddim
        parser.add_argument('--ddpm', dest='ddpm', action='store_true')

        self.args = parser.parse_args()

        #self.args.clip_guidance = True

        # self.device = torch.device('cuda:0' if (
        #     torch.cuda.is_available() and not self.args.cpu) else 'cpu')
        # print('Using device:', self.device)
        self.device = chain.device

        self.model_state_dict = torch.load(
            self.args.model_path, map_location='cpu')

        self.model_params = {
            'attention_resolutions': '32,16,8',
            'class_cond': False,
            'diffusion_steps': 1000,
            'rescale_timesteps': True,
            'timestep_respacing': '27',  # Modify this value to decrease the number of
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
            'image_condition': True if self.model_state_dict['input_blocks.0.0.weight'].shape[1] == 8 else False,
            'super_res_condition': True if 'external_block.0.0.weight' in self.model_state_dict else False,
        }

        if self.args.ddpm:
            self.model_params['timestep_respacing'] = 1000
        if self.args.ddim:
            if self.args.steps:
                self.model_params['timestep_respacing'] = 'ddim' + \
                    str(self.args.steps)
            else:
                self.model_params['timestep_respacing'] = 'ddim50'
        elif self.args.steps:
            self.model_params['timestep_respacing'] = str(self.args.steps)

        self.model_config = model_and_diffusion_defaults()
        self.model_config.update(self.model_params)

        if self.args.cpu:
            self.model_config['use_fp16'] = False

        # Load models
        self.model, self.diffusion = create_model_and_diffusion(
            **self.model_config)
        self.model.load_state_dict(self.model_state_dict, strict=False)
        self.model.requires_grad_(
            self.args.clip_guidance).eval().to(self.device)

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
        sd = torch.load(self.args.bert_path, map_location="cpu")
        self.bert.load_state_dict(sd)

        self.bert.to(self.device)
        self.bert.half().eval()
        set_requires_grad(self.bert, False)

        # clip
        self.clip_model, self.clip_preprocess = clip.load(
            'ViT-L/14', device=self.device, jit=False)
        self.clip_model.eval().requires_grad_(False)
        self.normalize = transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[
                                              0.26862954, 0.26130258, 0.27577711])

        print("ready")
