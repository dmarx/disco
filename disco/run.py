
import gc
import math
import random
import cv2
import numpy as np
from tqdm.notebook import tqdm
import clip
from perlin import create_perlin_noise, regen_perlin
from utils import MakeCutouts, MakeCutoutsDango, alpha_sigma_to_t, fetch, parse_prompt, range_loss, spherical_dist_loss, t_to_alpha_sigma, tv_loss
from PIL import Image, ImageOps
from datetime import datetime

import torch
from torch import nn
from torch.nn import functional as F
import torchvision.transforms as T
import torchvision.transforms.functional as TF

from ipywidgets import Output
from tqdm import trange
from piq import brisque

# clamp_index = [0.03]*50+[0.04]*100+[0.05]*850 #@param {type:'raw'}
# clamp_index = 1*np.array(clamp_index)
# tv_scales = [0]+[2000]*3#@param {type:'raw'}
# tv_scale_2 = 0#@param {type:'raw'}
# sat_index =   [0]*40+[0]*960 #@param {type:'raw'}
# sat_index = np.array(sat_index)
# range_index = [0]*50 +[0]*950 #@param {type:'raw'}

# cc = 6
# bsq_scale = 0
# RGB_min, RGB_max = [-0.95,0.95] #@param {type:'raw'}
# active_function = "softsign"
# grad_scale = 2

# def cond_clamp(image): 
#     #if t >=0:
#         mag=image.square().mean().sqrt()
#         mag = (mag*cc).clamp(1.6,100)
#         image = image.clamp(-mag, mag)
#         return(image)


# @torch.no_grad()
# def cond_sample(model, x, steps, eta, extra_args, cond_fn, number,pace,use_secondary_model,root_path,taskname):
#     """Draws guided samples from a model given starting noise."""
#     global clamp_max
#     ts = x.new_ones([x.shape[0]])

#     # Create the noise schedule
#     alphas, sigmas = t_to_alpha_sigma(steps)

#     lerp = False

#     # The sampling loop
#     for i in trange(len(steps)):
#         # if pace[i%len(pace)]["model_name"]=="cc12m_1":
#         #     extra_args_in = extra_args
#         # else:
#         #     extra_args_in= {}

#         # Get the model output
#         with torch.enable_grad():
#             x = x.detach().requires_grad_()
#             with torch.cuda.amp.autocast():
#                 if lerp:
#                     v=torch.zeros_like(x)
#                     for j in pace:
#                         if j["model_name"]=="cc12m_1":
#                             extra_args_in = extra_args
#                         else:
#                             extra_args_in= {}
#                         v += model[j["model_name"]](x, ts * steps[i], **extra_args_in)
#                     v = v/len(pace)
#                 else:
#                     v = model[pace[i%len(pace)]["model_name"]](x, ts * steps[i], **extra_args_in)
#             v = cond_clamp(v)

#         if use_secondary_model:
#             with torch.no_grad():
#                 if steps[i] < 1 and pace[i%len(pace)]["guided"]:
#                     pred = x * alphas[i] - v * sigmas[i]
#                     cond_grad = cond_fn(x, ts * steps[i],pred, **extra_args).detach()
#                     v = v.detach() - cond_grad * (sigmas[i] / alphas[i]) * pace[i%len(pace)]["mag_adjust"]
#                 else:
#                     v = v.detach()
#                     pred = x * alphas[i] - v * sigmas[i]
#                     clamp_max=torch.tensor([0])

#         else:
#             if steps[i] < 1 and pace[i%len(pace)]["guided"]:
#                 with torch.enable_grad():
#                     pred = x * alphas[i] - v * sigmas[i]
#                     cond_grad = cond_fn(x, ts * steps[i],pred, **extra_args).detach()
#                     v = v.detach() - cond_grad * (sigmas[i] / alphas[i]) * pace[i%len(pace)]["mag_adjust"]
#             else:
#                 with torch.no_grad():
#                     v = v.detach()
#                     pred = x * alphas[i] - v * sigmas[i]
#                     clamp_max=torch.tensor([0])

#         mag = pred.square().mean().sqrt()
#       #  print(mag)
#         if torch.isnan(mag):
#             print("ERROR2")
#             continue
        
#         filename = f'{root_path}/diff/{taskname}_N.jpg'
#         number += 1
#         TF.to_pil_image(pred[0].add(1).div(2).clamp(0, 1)).save(filename,quality=99)
#         # if save_iterations and number % save_every == 0:
#         #   shutil.copy(filename, f'{outDirPath}/{taskname}_{number}.jpg')
#         # textprogress.value = f'{taskname},  step {round(steps[i].item()*1000)}, {pace[i%len(pace)]["model_name"]} :'
#         # file = open(filename, "rb")
#         # image=file.read()
#         # progress.value = image 
#         # file.close()
            
#         # Predict the noise and the denoised image
#         pred = x * alphas[i] - v * sigmas[i]
#         eps = x * sigmas[i] + v * alphas[i]

#         # If we are not on the last timestep, compute the noisy image for the
#         # next timestep.
#         if i < len(steps) - 1:
#             # If eta > 0, adjust the scaling factor for the predicted noise
#             # downward according to the amount of additional noise to add
#             if eta >=0:
#                 ddim_sigma = eta * (sigmas[i + 1]**2 / sigmas[i]**2).sqrt() * \
#                     (1 - alphas[i]**2 / alphas[i + 1]**2).sqrt()
#             else:
#                 ddim_sigma = -eta*sigmas[i+1]
#             adjusted_sigma = (sigmas[i + 1]**2 - ddim_sigma**2).sqrt()

#             # Recombine the predicted noise and predicted denoised image in the
#             # correct proportions for the next step
#             x = pred * alphas[i + 1] + eps * adjusted_sigma
#             x = cond_clamp(x)


#             # Add the correct amount of fresh noise
#             if eta:
#                 x += torch.randn_like(x) * ddim_sigma
            
#          #######   x = sample_a_step(model, x.detach(), steps2, i//2, eta, extra_args)


#     # If we are on the last timestep, output the denoised image
#     return pred

# def log_snr_to_alpha_sigma(log_snr):
#     """Returns the scaling factors for the clean image and for the noise, given
#     the log SNR for a timestep."""
#     return log_snr.sigmoid().sqrt(), log_snr.neg().sigmoid().sqrt()

# def get_ddpm_schedule(ddpm_t):
#     """Returns timesteps for the noise schedule from the DDPM paper."""
#     log_snr = -torch.special.expm1(1e-4 + 10 * ddpm_t**2).log()
#     alpha, sigma = log_snr_to_alpha_sigma(log_snr)
#     return alpha_sigma_to_t(alpha, sigma)

# def get_spliced_ddpm_cosine_schedule(t):
#     """Returns timesteps for a spliced DDPM/cosine noise schedule."""
#     ddpm_crossover = 0.48536712
#     cosine_crossover = 0.80074257
#     big_t = t * (1 + cosine_crossover - ddpm_crossover)
#     ddpm_part = get_ddpm_schedule(big_t + ddpm_crossover - cosine_crossover)
#     return torch.where(big_t < cosine_crossover, big_t, ddpm_part)



def do_run(args, stop_on_next_loop, clip_models, device, model, diffusion, normalize, secondary_model, lpips_model, model_config, use_secondary_model, partialFolder, batchFolder,root_path,pace):  # ,unsharpenFolder):
    #print("Running", clip_models)
    seed = args.seed
    print(range(args.start_frame, args.max_frames))
    for frame_num in range(args.start_frame, args.max_frames):
        if stop_on_next_loop:
            break

        # display.clear_output(wait=True)

        # Print Frame progress if animation mode is on
        if args.animation_mode != "None":
            batchBar = tqdm(range(args.max_frames), desc="Frames")
            batchBar.n = frame_num
            batchBar.refresh()

        # Inits if not video frames
        if args.animation_mode != "Video Input":
            if args.init_image == '':
                init_image = None
            else:
                init_image = args.init_image
            init_scale = args.init_scale
            skip_steps = args.skip_steps

        loss_values = []

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
            torch.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True

        target_embeds, weights = [], []

        if args.prompts_series is not None and frame_num >= len(args.prompts_series):
            frame_prompt = args.prompts_series[-1]
        elif args.prompts_series is not None:
            frame_prompt = args.prompts_series[frame_num]
        else:
            frame_prompt = []

        print(args.image_prompts_series)
        if args.image_prompts_series is not None and frame_num >= len(args.image_prompts_series):
            image_prompt = args.image_prompts_series[-1]
        elif args.image_prompts_series is not None:
            image_prompt = args.image_prompts_series[frame_num]
        else:
            image_prompt = []

        print(f'Frame Prompt: {frame_prompt}')

        model_stats = []
        for clip_model in clip_models:
            cutn = 16
            model_stat = {"clip_model": None, "target_embeds": [],
                          "make_cutouts": None, "weights": []}
            model_stat["clip_model"] = clip_model

            for prompt in frame_prompt:
                txt, weight = parse_prompt(prompt)
                txt = clip_model.encode_text(
                    clip.tokenize(prompt).to(device)).float()

            if args.fuzzy_prompt:
                for i in range(25):
                    model_stat["target_embeds"].append(
                        (txt + torch.randn(txt.shape).cuda() * args.rand_mag).clamp(0, 1))
                    model_stat["weights"].append(weight)
            else:
                model_stat["target_embeds"].append(txt)
                model_stat["weights"].append(weight)

            if image_prompt:
                model_stat["make_cutouts"] = MakeCutouts(
                    clip_model.visual.input_resolution, cutn, skip_augs=args.skip_augs)
                for prompt in image_prompt:
                    path, weight = parse_prompt(prompt)
                    img = Image.open(fetch(path)).convert('RGB')
                    img = TF.resize(
                        img, min(args.side_x, args.side_y, *img.size), T.InterpolationMode.LANCZOS)
                    batch = model_stat["make_cutouts"](TF.to_tensor(
                        img).to(device).unsqueeze(0).mul(2).sub(1))
                    embed = clip_model.encode_image(normalize(batch)).float()
                    if args.fuzzy_prompt:
                        for i in range(25):
                            model_stat["target_embeds"].append(
                                (embed + torch.randn(embed.shape).cuda() * args.rand_mag).clamp(0, 1))
                            weights.extend([weight / cutn] * cutn)
                    else:
                        model_stat["target_embeds"].append(embed)
                        model_stat["weights"].extend([weight / cutn] * cutn)

            model_stat["target_embeds"] = torch.cat(
                model_stat["target_embeds"])
            model_stat["weights"] = torch.tensor(
                model_stat["weights"], device=device)
            if model_stat["weights"].sum().abs() < 1e-3:
                raise RuntimeError('The weights must not sum to 0.')
            model_stat["weights"] /= model_stat["weights"].sum().abs()
            model_stats.append(model_stat)

        init = None
        if init_image is not None:
            init = Image.open(fetch(init_image)).convert('RGB')
            init = init.resize((args.side_x, args.side_y), Image.LANCZOS)
            init = TF.to_tensor(init).to(device).unsqueeze(0).mul(2).sub(1)

        if args.perlin_init:
            if args.perlin_mode == 'color':
                init = create_perlin_noise(
                    [1.5**-i*0.5 for i in range(12)], 1, 1, False)
                init2 = create_perlin_noise(
                    [1.5**-i*0.5 for i in range(8)], 4, 4, False)
            elif args.perlin_mode == 'gray':
                init = create_perlin_noise(
                    [1.5**-i*0.5 for i in range(12)], 1, 1, True)
                init2 = create_perlin_noise(
                    [1.5**-i*0.5 for i in range(8)], 4, 4, True)
            else:
                init = create_perlin_noise(
                    [1.5**-i*0.5 for i in range(12)], 1, 1, False)
                init2 = create_perlin_noise(
                    [1.5**-i*0.5 for i in range(8)], 4, 4, True)
            # init = TF.to_tensor(init).add(TF.to_tensor(init2)).div(2).to(device)
            init = TF.to_tensor(init).add(TF.to_tensor(init2)).div(
                2).to(device).unsqueeze(0).mul(2).sub(1)
            del init2

        cur_t = None

        def cond_fn(x, t, y=None):
            # print("cond_fn",args)
            with torch.enable_grad():
                x_is_NaN = False
                x = x.detach().requires_grad_()
                n = x.shape[0]
                if use_secondary_model is True:
                    alpha = torch.tensor(
                        diffusion.sqrt_alphas_cumprod[cur_t], device=device, dtype=torch.float32)
                    sigma = torch.tensor(
                        diffusion.sqrt_one_minus_alphas_cumprod[cur_t], device=device, dtype=torch.float32)
                    cosine_t = alpha_sigma_to_t(alpha, sigma)
                    out = secondary_model(x, cosine_t[None].repeat([n])).pred
                    fac = diffusion.sqrt_one_minus_alphas_cumprod[cur_t]
                    x_in = out * fac + x * (1 - fac)
                    x_in_grad = torch.zeros_like(x_in)
                else:
                    my_t = torch.ones([n], device=device,
                                      dtype=torch.long) * cur_t
                    out = diffusion.p_mean_variance(
                        model, x, my_t, clip_denoised=False, model_kwargs={'y': y})
                    fac = diffusion.sqrt_one_minus_alphas_cumprod[cur_t]
                    x_in = out['pred_xstart'] * fac + x * (1 - fac)
                    x_in_grad = torch.zeros_like(x_in)
                for model_stat in model_stats:
                    for i in range(args.cutn_batches):
                        # errors on last step without +1, need to find source
                        t_int = int(t.item())+1
                        # when using SLIP Base model the dimensions need to be hard coded to avoid AttributeError: 'VisionTransformer' object has no attribute 'input_resolution'
                        try:
                            input_resolution = model_stat["clip_model"].visual.input_resolution
                        except:
                            input_resolution = 224

                        cuts = MakeCutoutsDango(input_resolution,
                                                Overview=args.cut_overview[1000-t_int],
                                                InnerCrop=args.cut_innercut[1000 -
                                                                            t_int], IC_Size_Pow=args.cut_ic_pow, IC_Grey_P=args.cut_icgray_p[1000-t_int], args=args
                                                )
                        clip_in = normalize(cuts(x_in.add(1).div(2)))
                        image_embeds = model_stat["clip_model"].encode_image(
                            clip_in).float()
                        dists = spherical_dist_loss(image_embeds.unsqueeze(
                            1), model_stat["target_embeds"].unsqueeze(0))
                        dists = dists.view(
                            [args.cut_overview[1000-t_int]+args.cut_innercut[1000-t_int], n, -1])
                        losses = dists.mul(
                            model_stat["weights"]).sum(2).mean(0)
                        # log loss, probably shouldn't do per cutn_batch
                        loss_values.append(losses.sum().item())
                        x_in_grad += torch.autograd.grad(losses.sum() * args.clip_guidance_scale, x_in)[
                            0] / args.cutn_batches
                tv_losses = tv_loss(x_in)
                if use_secondary_model is True:
                    range_losses = range_loss(out)
                else:
                    range_losses = range_loss(out['pred_xstart'])
                sat_losses = torch.abs(x_in - x_in.clamp(min=-1, max=1)).mean()
                loss = tv_losses.sum() * args.tv_scale + range_losses.sum() * \
                    args.range_scale + sat_losses.sum() * args.sat_scale
                if init is not None and args.init_scale:
                    init_losses = lpips_model(x_in, init)
                    loss = loss + init_losses.sum() * args.init_scale
                x_in_grad += torch.autograd.grad(loss, x_in)[0]
                if torch.isnan(x_in_grad).any() == False:
                    grad = -torch.autograd.grad(x_in, x, x_in_grad)[0]
                else:
                    # print("NaN'd")
                    x_is_NaN = True
                    grad = torch.zeros_like(x)
            if args.clamp_grad and x_is_NaN == False:
                magnitude = grad.square().mean().sqrt()
                # min=-0.02, min=-clamp_max,
                return grad * magnitude.clamp(max=args.clamp_max) / magnitude
            return grad


        clamp_start_ = 0


        # def cond_fn2(x, t, x_in, clip_embed=[]):
        #     torch.cuda.empty_cache()
        #     gc.collect()
        #     global test, clamp_start_, clamp_max
        #     t2 = t
        #     t = round(t.item()*1000)
        #     n = x.shape[0]
        #     with torch.enable_grad():
        #         # if use_secondary_model:
        #         #     x = x.detach().requires_grad_()
        #         #     x_in_second = secondary_model(x, t2.repeat([n])).pred
        #         #     if use_original_as_clip_in:
        #         #         x_in = replace_grad(
        #         #             x_in, (1-use_original_as_clip_in)*x_in_second+use_original_as_clip_in*x_in)
        #         #     else:
        #         #         x_in = x_in_second

        #         x_in_grad = torch.zeros_like(x_in)
        #         # clip_guidance_scale = clip_guidance_index[1000-t]
        #         clip_guidance_scale = args.clip_guidance_scale
        # #             clamp_max = clamp_index[1000-t]
        #         make_cutouts = {}
        #         cutn = args.cut_innercut[1000-t] + args.cut_overview[1000-t]
        #         try:
        #             input_resolution = model_stat["clip_model"].visual.input_resolution
        #         except:
        #             input_resolution = 224

        #         for i in clip_models:
        #             make_cutouts[i] = MakeCutoutsDango(input_resolution,
        #                                                 Overview=args.cut_overview[1000-t],
        #                                                 InnerCrop=args.cut_innercut[1000 -
        #                                                                     t], IC_Size_Pow=args.cut_ic_pow, IC_Grey_P=args.cut_icgray_p[1000-t]
        #                                                 )
        #         nscut = MakeCutoutsDango(200, Overview=1)
        #         add_cuts = nscut(x_in.add(1).div(2))
        #         for k in range(args.cutn_batches):
        #             losses = 0
        #             for i in clip_models:
        #                 clip_in = normalize(make_cutouts[i](
        #                     x_in.add(1).div(2)).to("cuda"))
        #                 image_embeds = clip_model[i].encode_image(clip_in).float()
        #                 image_embeds = image_embeds.unsqueeze(1)
        #                 dists = spherical_dist_loss(
        #                     image_embeds, target_embeds[i].unsqueeze(0))
        #                 del image_embeds, clip_in
        #                 dists = dists.view([cutn, n, -1])
        #                 losses = dists.mul(weights[i]).sum(2).mean(0)
        #                 x_in_grad += torch.autograd.grad(losses.sum() * clip_guidance_scale, x_in)[
        #                     0] / args.cutn_batches / len(clip_models)
        #                 del dists, losses
        #             gc.collect()

        #         tv_losses = tv_loss(x_in).sum() * tv_scales[0] +\
        #             tv_loss(F.interpolate(x_in, scale_factor=1/2)).sum() * tv_scales[1] + \
        #             tv_loss(F.interpolate(x_in, scale_factor=1/4)).sum() * tv_scales[2] + \
        #             tv_loss(F.interpolate(x_in, scale_factor=1/8)).sum() * tv_scales[3]
        #         sat_scale = sat_index[1000-t]
        #         range_scale = range_index[1000-t]
        #         range_losses = range_loss(x_in, RGB_min, RGB_max).sum() * range_scale
        #         sat_losses = range_loss(x, -1.0, 1.0).sum() * \
        #             sat_scale + tv_loss(x).sum() * tv_scale_2
        #         try:
        #             bsq_loss = brisque(x_in.add(1).div(2).clamp(0, 1), data_range=1.)
        #         except:
        #             bsq_loss = 0
        #         if bsq_loss <= 10:
        #             bsq_loss = 0

        #         loss = tv_losses + range_losses + \
        #             bsq_loss * bsq_scale

        #         if init is not None and init_scale:
        #             init_losses = lpips_model(x_in, init)
        #             loss = loss + init_losses.sum() * init_scale
        #         loss_grad = torch.autograd.grad(loss, x_in, )[0]
        #         sat_grad = torch.autograd.grad(sat_losses, x, )[0]
        #         x_in_grad += loss_grad + sat_grad
        #         x_in_grad = torch.nan_to_num(x_in_grad, nan=0.0, posinf=0, neginf=0)
        #         grad = -torch.autograd.grad(x_in, x, x_in_grad)[0]
        #         grad = torch.nan_to_num(grad, nan=0.0, posinf=0, neginf=0)
        #         mag = grad.square().mean().sqrt()
        #         if mag == 0:
        #             print("ERROR")
        #             return(grad)
        #         if t >= 0:
        #             if active_function == "softsign":
        #                 grad = F.softsign(grad*grad_scale/mag)
        #             if active_function == "tanh":
        #                 grad = (grad/mag*grad_scale).tanh()
        #             if active_function == "clamp":
        #                 grad = grad.clamp(-mag*grad_scale*2, mag*grad_scale*2)
        #         if grad.abs().max() > 0:
        #             grad = grad/grad.abs().max()
        #             magnitude = grad.square().mean().sqrt()
        #         else:
        #             print(grad)
        #             return(grad)
        #         clamp_max = clamp_index[1000-t]
        #     # return grad* magnitude.clamp(max= clamp_max) /magnitude
        #     return grad * magnitude.clamp(max=0.05) / magnitude

    if model_config['timestep_respacing'].startswith('ddim'):
        sample_fn = diffusion.ddim_sample_loop_progressive
    else:
        sample_fn = diffusion.p_sample_loop_progressive

    image_display = Output()
    for i in range(args.n_batches):
        if args.animation_mode == 'None':
            # display.clear_output(wait=True)
            batchBar = tqdm(range(args.n_batches), desc="Batches")
            batchBar.n = i
            batchBar.refresh()
        print('')
        print('batch ' + str(i))
        # # display.display(image_display)
        gc.collect()
        torch.cuda.empty_cache()
        cur_t = diffusion.num_timesteps - skip_steps - 1
        total_steps = cur_t

        if args.perlin_init:
            init = regen_perlin()

        if model_config['timestep_respacing'].startswith('ddim'):
            print("model_config",1)
            samples = sample_fn(
                model,
                (args.batch_size, 3, args.side_y, args.side_x),
                clip_denoised=args.clip_denoised,
                model_kwargs={},
                cond_fn=cond_fn,
                progress=True,
                skip_timesteps=skip_steps,
                init_image=init,
                randomize_class=args.randomize_class,
                eta=args.eta,
            )
        else:
            print("model_config",2)
            samples = sample_fn(
                model,
                (args.batch_size, 3, args.side_y, args.side_x),
                clip_denoised=args.clip_denoised,
                model_kwargs={},
                cond_fn=cond_fn,
                progress=True,
                skip_timesteps=skip_steps,
                init_image=init,
                randomize_class=args.randomize_class,
            )
        # print("model_config",2)
        

        # taskname="Test"+"_"+str(i)
        # step = 1
        # steps_pow = 1
        # t = torch.linspace(1, 0, step + 1, device=device)[:-1]
        # t=t.pow(steps_pow)
        # x = torch.randn([1, 3, args.side_y, args.side_x], device=device)
        # steps = get_spliced_ddpm_cosine_schedule(t)
        # number = 0
        # extra_args = {}
        # samples = cond_sample(model, x, steps, args.eta, extra_args, cond_fn2, number,pace,use_secondary_model,root_path,taskname)

        samples = sample_fn(
            model,
            (args.batch_size, 3, args.side_y, args.side_x),
            clip_denoised=args.clip_denoised,
            model_kwargs={},
            cond_fn=cond_fn,
            progress=True,
            skip_timesteps=skip_steps,
            init_image=init,
            randomize_class=args.randomize_class,
        )

        # with run_display:
        # display.clear_output(wait=True)
        imgToSharpen = None
        for j, sample in enumerate(samples):
            #print("enumerating samples " + str(j))
            cur_t -= 1
            intermediateStep = False
            if args.steps_per_checkpoint is not None:
                if j % args.steps_per_checkpoint == 0 and j > 0:
                    intermediateStep = True
            elif j in args.intermediate_saves:
                intermediateStep = True
            with image_display:
                if j % args.display_rate == 0 or cur_t == -1 or intermediateStep == True:
                    for k, image in enumerate(sample['pred_xstart']):
                        # tqdm.write(f'Batch {i}, step {j}, output {k}:')
                        current_time = datetime.now().strftime('%y%m%d-%H%M%S_%f')
                        percent = math.ceil(j/total_steps*100)
                        if args.n_batches > 0:
                            # if intermediates are saved to the subfolder, don't append a step or percentage to the name
                            if cur_t == -1 and args.intermediates_in_subfolder is True:
                                save_num = f'{frame_num:04}' if args.animation_mode != "None" else i
                                filename = f'{args.batch_name}({args.batchNum})_{save_num}.png'
                            else:
                                # If we're working with percentages, append it
                                if args.steps_per_checkpoint is not None:
                                    filename = f'{args.batch_name}({args.batchNum})_{i:04}-{percent:02}%.png'
                                # Or else, iIf we're working with specific steps, append those
                                else:
                                    filename = f'{args.batch_name}({args.batchNum})_{i:04}-{j:03}.png'
                        image = TF.to_pil_image(
                            image.add(1).div(2).clamp(0, 1))
                        if j % args.display_rate == 0 or cur_t == -1:
                            if False:
                                image.save('progress.png')
                            # display.clear_output(wait=True)
                            # display.display(display.Image('progress.png'))
                        if args.steps_per_checkpoint is not None:
                            if j % args.steps_per_checkpoint == 0 and j > 0:
                                if args.intermediates_in_subfolder is True:
                                    image.save(
                                        f'{partialFolder}/{filename}')
                                else:
                                    image.save(f'{batchFolder}/{filename}')
                        else:
                            if j in args.intermediate_saves:
                                if args.intermediates_in_subfolder is True:
                                    image.save(
                                        f'{partialFolder}/{filename}')
                                else:
                                    image.save(f'{batchFolder}/{filename}')
                        if cur_t == -1:
                            # if frame_num == 0:
                            #     #save_settings()
                            if args.animation_mode != "None":
                                image.save('prevFrame.png')
                            # if args.sharpen_preset != "Off" and args.animation_mode == "None":
                            #     imgToSharpen = image
                            #     if args.keep_unsharp is True:
                            #         image.save(
                            #             f'{unsharpenFolder}/{filename}')
                            # else:
                            #     image.save(f'{batchFolder}/{filename}')
                            image.save(f'{batchFolder}/{filename}')
                            # if frame_num != args.max_frames-1:
                            #   display.clear_output()

        # with image_display:
        #     if args.sharpen_preset != "Off" and args.animation_mode == "None":
        #         print('Starting Diffusion Sharpening...')
        #         do_superres(imgToSharpen, f'{batchFolder}/{filename}')
        #         display.clear_output()

        # plt.plot(np.array(loss_values), 'r')
