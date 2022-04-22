import os
from disco.guided_diffusion_disco.guided_diffusion.script_util import create_model_and_diffusion, model_and_diffusion_defaults

import generator_disco.common.envutils as envutils
envutils.configure_sys_paths(os.getcwd(),os.getcwd()+"/content/models",True)

from disco.prompt import get_inbetweens, parse_key_frames, split_prompts
from generator_disco.common import models, utils
from generator_disco.common.cutouts import MakeCutouts, MakeCutoutsDango

import gc
import subprocess
import torch
import numpy as np
import math
import pathlib, shutil, os, sys
import torch
import cv2
import gc
import math
import lpips
from PIL import Image
from glob import glob
import json
from types import SimpleNamespace
import torchvision.transforms as T
import torchvision.transforms.functional as TF
from tqdm.notebook import tqdm
from CLIP import clip
# from guided_diffusion.script_util import create_model_and_diffusion, model_and_diffusion_defaults
from datetime import datetime
import numpy as np
import random
from ipywidgets import Output
import hashlib
from IPython.display import Image as ipyimg
import torch
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class GeneratorDisco:

    #default settings
    settings = {
        'prompt':
            [
                "A scenic view of a mystical place, by Felix Kahn, matte painting trending on artstation artstation HQ.",
            ],
        'clip_guidance_scale':5000,
        'steps':100,
        'cut_ic_pow':1,
        'range_scale':150,
        'n_batches':5,
        'eta' : 0.8,
        'diffusion_steps':1000,
        'tv_scale':0,
        'sat_scale':0,
        'clamp_max':0.05,
        'rand_mag':0.05,
        'cutn_batches':4, #2
        'path':os.getcwd(),
        'ViTB32': True,
        'ViTB16': True,
        'ViTL14': False, # True
        'RN101': False,
        'RN50': False,
        'RN50x4': False,
        'RN50x16': False,
        'RN50x64': False,
        'use_secondary_model':False,
        'skip_augs':False,
        'soft_limiter_on': True,#@param{type: 'boolean'}\n",
        'soft_limiter_knee': .98, #@param{type: 'number'}\n",
        'frames_scale': 1500, #@param{type: 'integer'}
        'frames_skip_steps':'65%',
        'turbo_mode':True,
        'turbo_steps':"3",
        'turbo_preroll':2,
        'init_image':"",
        'skip_steps':0, # was 20
        'vr_mode':False,
        'vr_eye_angle':0.5,
        'vr_ipd':5.0,
        'intermediate_saves': 0,
        'animation_mode':'None',
        'max_frames':10000,
        #'wh':[512, 512],  
        #'wh':[1024,1024],
        'wh':[640,384],
        #'wh':[1024,1024],
    } 

    args = None
    root_path = settings['path']
    model_path = ""
    clip_models = None
    os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

    device = None
    DEVICE = None

    stop_on_next_loop = False  # Make sure GPU memory doesn't get corrupted from cancelling the run mid-way through, allow a full frame to complete
    trans_scale = 1.0/200.0
    MAX_ADABINS_AREA = 500000

    text_prompts = None
    image_prompts = None
    clip_guidance_scale = None
    tv_scale = None
    range_scale = None
    sat_scale = None
    cutn_batches = None
    max_frames = None
    interp_spline = None
    init_image = None
    init_scale = None
    skip_steps = None
    frames_scale = None
    frames_skip_steps = None
    perlin_init = None
    perlin_mode = None
    skip_augs = None
    randomize_class = None
    clip_denoised = None
    clamp_grad = None
    clamp_max = None
    seed = None
    fuzzy_prompt = None
    rand_mag = None
    eta = None
    width_height = None
    diffusion_model = None
    use_secondary_model = None
    steps = None
    diffusion_steps = None
    diffusion_sampling_mode = None
    ViTB32 = None
    ViTB16 = None
    ViTL14 = None
    RN101 = None
    RN50 = None
    RN50x4 = None
    RN50x16 = None
    RN50x64 = None
    cut_overview = None
    cut_innercut = None
    cut_ic_pow = None
    cut_icgray_p = None
    key_frames = None
    max_frames = None
    animation_mode = None
    angle = None
    zoom = None
    translation_x = None
    translation_y = None
    translation_z = None
    rotation_3d_x = None
    rotation_3d_y = None
    rotation_3d_z = None
    midas_depth_model = None
    midas_weight = None
    near_plane = None
    far_plane = None
    fov = None
    padding_mode = None
    sampling_mode = None
    resume_run = None
    video_init_path = None
    extract_nth_frame = None
    video_init_seed_continuity = None
    turbo_mode = None
    turbo_steps = None
    turbo_preroll = None
    batchNum = None
    
    def render_frames(self):
        args = self.args
        seed = args.seed
        last_path  ="" #f'{batchFolder}/{filename}'
        filename = ""
        if (args.animation_mode == "3D") and (args.midas_weight > 0.0):
            midas_model, midas_transform, midas_net_w, midas_net_h, midas_resize_mode, midas_normalization = utils.init_midas_depth_model(args.midas_depth_model,DEVICE = self.DEVICE,default_models = self.default_models)
        for self.frame_num in range(args.start_frame, args.max_frames):
            if self.stop_on_next_loop:
                break
            # display.clear_output(wait=True)
            
            # Print Frame progress if animation mode is on
            if args.animation_mode != "None":
                batchBar = tqdm(range(args.max_frames), desc ="Frames")
                batchBar.n = self.frame_num
                batchBar.refresh()

            # Inits if not video frames
            if args.animation_mode != "Video Input":
                if args.init_image == '':
                    init_image = None
                else:
                    init_image = args.init_image
                self.init_scale = args.init_scale
                self.skip_steps = args.skip_steps

            if args.animation_mode == "2D":
                if args.key_frames:
                    angle = args.angle_series[self.frame_num]
                    zoom = args.zoom_series[self.frame_num]
                    translation_x = args.translation_x_series[self.frame_num]
                    translation_y = args.translation_y_series[self.frame_num]
                    print(
                        f'angle: {angle}',
                        f'zoom: {zoom}',
                        f'translation_x: {translation_x}',
                        f'translation_y: {translation_y}',
                    )
                
                if self.frame_num > 0:
                    seed += 1
                    if self.resume_run and self.frame_num == self.start_frame:
                        img_0 = cv2.imread(self.batchFolder+f"/{self.batch_name}({self.batchNum})_{self.start_frame-1:04}.png")
                    else:
                        img_0 = cv2.imread('content/prevFrame.png')
                    center = (1*img_0.shape[1]//2, 1*img_0.shape[0]//2)
                    trans_mat = np.float32(
                        [[1, 0, translation_x],
                        [0, 1, translation_y]]
                    )
                    rot_mat = cv2.getRotationMatrix2D( center, angle, zoom )
                    trans_mat = np.vstack([trans_mat, [0,0,1]])
                    rot_mat = np.vstack([rot_mat, [0,0,1]])
                    transformation_matrix = np.matmul(rot_mat, trans_mat)
                    img_0 = cv2.warpPerspective(
                        img_0,
                        transformation_matrix,
                        (img_0.shape[1], img_0.shape[0]),
                        borderMode=cv2.BORDER_WRAP
                    )

                    cv2.imwrite('content/prevFrameScaled.png', img_0)
                    init_image = 'content/prevFrameScaled.png'
                    self.init_scale = args.frames_scale
                    self.skip_steps = args.calc_frames_skip_steps

            if args.animation_mode == "3D":
                if self.frame_num > 0:
                    seed += 1    
                    if self.resume_run and self.frame_num == self.start_frame:
                        img_filepath = self.batchFolder+f"/{self.batch_name}({self.batchNum})_{self.start_frame-1:04}.png"
                        if self.turbo_mode and self.frame_num > self.turbo_preroll:
                            shutil.copyfile(img_filepath, 'content/oldFrameScaled.png')
                    else:
                        img_filepath = 'content/prevFrame.png'

                    next_step_pil = utils.do_3d_step(img_filepath, self.frame_num, midas_model, midas_transform,args,trans_scale=self.trans_scale,device=self.device,DEVICE=self.DEVICE)
                    next_step_pil.save('content/prevFrameScaled.png')

                    ### Turbo mode - skip some diffusions, use 3d morph for clarity and to save time
                    if self.turbo_mode:
                        if self.frame_num == self.turbo_preroll: #start tracking oldframe
                            next_step_pil.save('content/oldFrameScaled.png')#stash for later blending          
                        elif self.frame_num > self.turbo_preroll:
                        #set up 2 warped image sequences, old & new, to blend toward new diff image
                            old_frame = utils.do_3d_step('content/oldFrameScaled.png', self.frame_num, midas_model, midas_transform,args,trans_scale=self.trans_scale,device=self.device,DEVICE=self.DEVICE)
                            old_frame.save('content/oldFrameScaled.png')
                            if self.frame_num % int(self.turbo_steps) != 0: 
                                print('turbo skip this frame: skipping clip diffusion steps')
                                filename = f'{args.batch_name}({args.batchNum})_{self.frame_num:04}.png'
                                blend_factor = ((self.frame_num % int(self.turbo_steps))+1)/int(self.turbo_steps)
                                print('turbo skip this frame: skipping clip diffusion steps and saving blended frame')
                                newWarpedImg = cv2.imread('content/prevFrameScaled.png')#this is already updated..
                                oldWarpedImg = cv2.imread('content/oldFrameScaled.png')
                                blendedImage = cv2.addWeighted(newWarpedImg, blend_factor, oldWarpedImg,1-blend_factor, 0.0)
                                cv2.imwrite(f'{self.batchFolder}/{filename}',blendedImage)
                                next_step_pil.save(f'{img_filepath}') # save it also as prev_frame to feed next iteration
                                continue
                            else:
                                #if not a skip frame, will run diffusion and need to blend.
                                oldWarpedImg = cv2.imread('prevFrameScaled.png')
                                cv2.imwrite(f'oldFrameScaled.png',oldWarpedImg)#swap in for blending later 
                                print('clip/diff this frame - generate clip diff image')

                    init_image = 'content/prevFrameScaled.png'
                    self.init_scale = args.frames_scale
                    self.skip_steps = args.calc_frames_skip_steps

            if  args.animation_mode == "Video Input":
                if not self.video_init_seed_continuity:
                    seed += 1
                    init_image = f'{self.videoFramesFolder}/{self.frame_num+1:04}.jpg'
                    self.init_scale = args.frames_scale
                    self.skip_steps = args.calc_frames_skip_steps

            loss_values = []
        
            if seed is not None:
                np.random.seed(seed)
                random.seed(seed)
                torch.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)
                torch.backends.cudnn.deterministic = True
        
            target_embeds, weights = [], []
            
            if args.prompts_series is not None and self.frame_num >= len(args.prompts_series):
                frame_prompt = args.prompts_series[-1]
            elif args.prompts_series is not None:
                frame_prompt = args.prompts_series[self.frame_num]
            else:
                frame_prompt = []
            
            print(args.image_prompts_series)
            if args.image_prompts_series is not None and self.frame_num >= len(args.image_prompts_series):
                image_prompt = args.image_prompts_series[-1]
            elif args.image_prompts_series is not None:
                image_prompt = args.image_prompts_series[self.frame_num]
            else:
                image_prompt = []

            print(f'Frame {self.frame_num} Prompt: {frame_prompt}')

            model_stats = []
            for clip_model in self.clip_models:
                cutn = 16
                model_stat = {"clip_model":None,"target_embeds":[],"make_cutouts":None,"weights":[]}
                model_stat["clip_model"] = clip_model
                
                
                for prompt in frame_prompt:
                    txt, weight = utils.parse_prompt(prompt)
                    txt = clip_model.encode_text(clip.tokenize(prompt).to(self.device)).float()
                    
                    if args.fuzzy_prompt:
                        for i in range(25):
                            model_stat["target_embeds"].append((txt + torch.randn(txt.shape).cuda() * args.rand_mag).clamp(0,1))
                            model_stat["weights"].append(weight)
                    else:
                        model_stat["target_embeds"].append(txt)
                        model_stat["weights"].append(weight)
            
                if image_prompt:
                    model_stat["make_cutouts"] = MakeCutouts(clip_model.visual.input_resolution, cutn, skip_augs=self.skip_augs) 
                    for prompt in image_prompt:
                        path, weight = utils.parse_prompt(prompt)
                        img = Image.open(envutils.fetch(path)).convert('RGB')
                        img = TF.resize(img, min(self.side_x, self.side_y, *img.size), T.InterpolationMode.LANCZOS)
                        batch = model_stat["make_cutouts"](TF.to_tensor(img).to(self.device).unsqueeze(0).mul(2).sub(1))
                        embed = clip_model.encode_image(self.normalize(batch)).float()
                        if self.fuzzy_prompt:
                            for i in range(25):
                                model_stat["target_embeds"].append((embed + torch.randn(embed.shape).cuda() * self.rand_mag).clamp(0,1))
                                weights.extend([weight / cutn] * cutn)
                        else:
                            model_stat["target_embeds"].append(embed)
                            model_stat["weights"].extend([weight / cutn] * cutn)
                
                model_stat["target_embeds"] = torch.cat(model_stat["target_embeds"])
                model_stat["weights"] = torch.tensor(model_stat["weights"], device=self.device)
                if model_stat["weights"].sum().abs() < 1e-3:
                    raise RuntimeError('The weights must not sum to 0.')
                model_stat["weights"] /= model_stat["weights"].sum().abs()
                model_stats.append(model_stat)
    
            init = None
            if init_image is not None:
                init = Image.open(envutils.fetch(init_image)).convert('RGB')
                init = init.resize((args.side_x, args.side_y), Image.LANCZOS)
                init = TF.to_tensor(init).to(self.device).unsqueeze(0).mul(2).sub(1)
            
            if args.perlin_init:
                if args.perlin_mode == 'color':
                    init = utils.create_perlin_noise([1.5**-i*0.5 for i in range(12)], 1, 1, False)
                    init2 = utils.create_perlin_noise([1.5**-i*0.5 for i in range(8)], 4, 4, False)
                elif args.perlin_mode == 'gray':
                    init = utils.create_perlin_noise([1.5**-i*0.5 for i in range(12)], 1, 1, True)
                    init2 = utils.create_perlin_noise([1.5**-i*0.5 for i in range(8)], 4, 4, True)
                else:
                    init = utils.create_perlin_noise([1.5**-i*0.5 for i in range(12)], 1, 1, False)
                    init2 = utils.create_perlin_noise([1.5**-i*0.5 for i in range(8)], 4, 4, True)
                # init = TF.to_tensor(init).add(TF.to_tensor(init2)).div(2).to(device)
                init = TF.to_tensor(init).add(TF.to_tensor(init2)).div(2).to(self.device).unsqueeze(0).mul(2).sub(1)
                del init2
        
            cur_t = None
        
            def cond_fn(x, t, y=None):
                with torch.enable_grad():
                    x_is_NaN = False
                    x = x.detach().requires_grad_()
                    n = x.shape[0]
                    if self.use_secondary_model is True:
                        alpha = torch.tensor(self.diffusion.sqrt_alphas_cumprod[cur_t], device=self.device, dtype=torch.float32)
                        sigma = torch.tensor(self.diffusion.sqrt_one_minus_alphas_cumprod[cur_t], device=self.device, dtype=torch.float32)
                        cosine_t = utils.alpha_sigma_to_t(alpha, sigma)
                        out = self.secondary_model(x, cosine_t[None].repeat([n])).pred
                        fac = self.diffusion.sqrt_one_minus_alphas_cumprod[cur_t]
                        x_in = out * fac + x * (1 - fac)
                        x_in_grad = torch.zeros_like(x_in)
                    else:
                        my_t = torch.ones([n], device=self.device, dtype=torch.long) * cur_t
                        out = self.diffusion.p_mean_variance(self.model, x, my_t, clip_denoised=False, model_kwargs={'y': y})
                        fac = self.diffusion.sqrt_one_minus_alphas_cumprod[cur_t]
                        x_in = out['pred_xstart'] * fac + x * (1 - fac)
                        x_in_grad = torch.zeros_like(x_in)
                    for model_stat in model_stats:
                        for i in range(args.cutn_batches):
                            t_int = int(t.item())+1 #errors on last step without +1, need to find source
                            #when using SLIP Base model the dimensions need to be hard coded to avoid AttributeError: 'VisionTransformer' object has no attribute 'input_resolution'
                            try:
                                input_resolution=model_stat["clip_model"].visual.input_resolution
                            except:
                                input_resolution=224

                            cuts = MakeCutoutsDango(input_resolution,
                                    Overview= args.cut_overview[1000-t_int], 
                                    InnerCrop = args.cut_innercut[1000-t_int], IC_Size_Pow=args.cut_ic_pow, IC_Grey_P = args.cut_icgray_p[1000-t_int]
                                    )
                            #TODO
                            clip_in = self.normalize(cuts(x_in.add(1).div(2)))
                            image_embeds = model_stat["clip_model"].encode_image(clip_in).float()
                            dists = utils.spherical_dist_loss(image_embeds.unsqueeze(1), model_stat["target_embeds"].unsqueeze(0))
                            dists = dists.view([args.cut_overview[1000-t_int]+args.cut_innercut[1000-t_int], n, -1])
                            losses = dists.mul(model_stat["weights"]).sum(2).mean(0)
                            loss_values.append(losses.sum().item()) # log loss, probably shouldn't do per cutn_batch
                            x_in_grad += torch.autograd.grad(losses.sum() * self.clip_guidance_scale, x_in)[0] / self.cutn_batches
                    tv_losses = utils.tv_loss(x_in)
                    if self.use_secondary_model is True:
                        range_losses = utils.range_loss(out)
                    else:
                        range_losses = utils.range_loss(out['pred_xstart'])
                    sat_losses = torch.abs(x_in - x_in.clamp(min=-1,max=1)).mean()
                    loss = tv_losses.sum() * self.tv_scale + range_losses.sum() * self.range_scale + sat_losses.sum() * self.sat_scale 
                    if init is not None and args.init_scale:
                        init_losses = self.lpips_model(x_in, init)
                        loss = loss + init_losses.sum() * args.init_scale
                    x_in_grad += torch.autograd.grad(loss, x_in)[0]
                    if torch.isnan(x_in_grad).any()==False:
                        grad = -torch.autograd.grad(x_in, x, x_in_grad)[0]
                    else:
                        # print("NaN'd")
                        x_is_NaN = True
                        grad = torch.zeros_like(x)
                if args.clamp_grad and x_is_NaN == False:
                    magnitude = grad.square().mean().sqrt()
                    return grad * magnitude.clamp(max=args.clamp_max) / magnitude  #min=-0.02, min=-clamp_max, 
                return grad
        
            if args.diffusion_sampling_mode == 'ddim':
                sample_fn = self.diffusion.ddim_sample_loop_progressive
            else:
                sample_fn = self.diffusion.plms_sample_loop_progressive

            image_display = Output()
            for i in range(args.n_batches):
                if args.animation_mode == 'None':
                    batchBar = tqdm(range(args.n_batches), desc ="Batches")
                    batchBar.n = i
                    batchBar.refresh()
                print('')
                gc.collect()
                torch.cuda.empty_cache()
                cur_t = self.diffusion.num_timesteps - self.skip_steps - 1
                total_steps = cur_t

                if self.perlin_init:
                    init = utils.regen_perlin()

                if args.diffusion_sampling_mode == 'ddim':
                    samples = sample_fn(
                        self.model,
                        (self.batch_size, 3, args.side_y, args.side_x),
                        clip_denoised=self.clip_denoised,
                        model_kwargs={},
                        cond_fn=cond_fn,
                        progress=True,
                        skip_timesteps=self.skip_steps,
                        init_image=init,
                        randomize_class=self.randomize_class,
                        eta=self.eta,
                    )
                else:
                    samples = sample_fn(
                        self.model,
                        (self.batch_size, 3, args.side_y, args.side_x),
                        clip_denoised=self.clip_denoised,
                        model_kwargs={},
                        cond_fn=cond_fn,
                        progress=True,
                        skip_timesteps=self.skip_steps,
                        init_image=init,
                        randomize_class=self.randomize_class,
                        order=2,
                    )
                
                for j, sample in enumerate(samples):    
                    cur_t -= 1
                    intermediateStep = False
                    if args.steps_per_checkpoint is not None:
                        if j % self.steps_per_checkpoint == 0 and j > 0:
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
                                    #if intermediates are saved to the subfolder, don't append a step or percentage to the name
                                    if cur_t == -1 and args.intermediates_in_subfolder is True:
                                        save_num = f'{self.frame_num:04}' if self.animation_mode != "None" else i
                                        filename = f'{args.batch_name}({args.batchNum})_{save_num}.png'
                                    else:
                                    #If we're working with percentages, append it
                                        if args.steps_per_checkpoint is not None:
                                            filename = f'{args.batch_name}({args.batchNum})_{i:04}-{percent:02}%.png'
                                        # Or else, iIf we're working with specific steps, append those
                                        else:
                                            filename = f'{args.batch_name}({args.batchNum})_{i:04}-{j:03}.png'
                                image = TF.to_pil_image(image.add(1).div(2).clamp(0, 1))
                                if j % args.display_rate == 0 or cur_t == -1:
                                    image.save('content/progress.png')
                                if args.steps_per_checkpoint is not None:
                                    if j % args.steps_per_checkpoint == 0 and j > 0:
                                        if args.intermediates_in_subfolder is True:
                                            image.save(f'{self.partialFolder}/{filename}')
                                        else:
                                            image.save(f'{self.batchFolder}/{filename}')
                                else:
                                    if j in args.intermediate_saves:
                                        if args.intermediates_in_subfolder is True:
                                            image.save(f'{self.partialFolder}/{filename}')
                                        else:
                                            image.save(f'{self.batchFolder}/{filename}')
                                if cur_t == -1:
                                    if self.frame_num == 0:
                                        self.save_settings()
                                    if args.animation_mode != "None":
                                        image.save('content/prevFrame.png')
                                    image.save(f'{self.batchFolder}/{filename}')
                                    last_path  = f'{self.batchFolder}/{filename}'
                                    
                                    if args.animation_mode == "3D":
                                    # If turbo, save a blended image
                                        if self.turbo_mode and self.frame_num > 0:
                                            # Mix new image with prevFrameScaled
                                            blend_factor = (1)/int(self.turbo_steps)
                                            newFrame = cv2.imread('content/prevFrame.png') # This is already updated..
                                            prev_frame_warped = cv2.imread('content/prevFrameScaled.png')
                                            blendedImage = cv2.addWeighted(newFrame, blend_factor, prev_frame_warped, (1-blend_factor), 0.0)
                                            cv2.imwrite(f'{self.batchFolder}/{filename}',blendedImage)
                                        else:
                                            image.save(f'{self.batchFolder}/{filename}')
                                            
        os.system("cp \"" + last_path + "\" \"" + os.getcwd() + "/static/output/" + filename + "\"")
        return filename
                        
    def do_run(self):

        self.resume_run = False #@param{type: 'boolean'}
        run_to_resume = 'latest' #@param{type: 'string'}
        resume_from_frame = 'latest' #@param{type: 'string'}
        retain_overwritten_frames = False #@param{type: 'boolean'}
        if retain_overwritten_frames is True:
            retainFolder = f'{self.batchFolder}/retained'
            envutils.createPath(retainFolder)

        skip_step_ratio = int(self.frames_skip_steps.rstrip("%")) / 100
        calc_frames_skip_steps = math.floor(self.steps * skip_step_ratio)

        if self.steps <= calc_frames_skip_steps:
            sys.exit("ERROR: You can't skip more steps than your total steps")

        if self.resume_run:
            if run_to_resume == 'latest':
                try:
                    self.batchNum
                except:
                    self.batchNum = len(glob(f"{self.batchFolder}/{self.batch_name}(*)_settings.txt"))-1
            else:
                self.batchNum = int(run_to_resume)
            if resume_from_frame == 'latest':
                self.start_frame = len(glob(self.batchFolder+f"/{self.batch_name}({self.batchNum})_*.png"))
                if self.animation_mode != '3D' and self.turbo_mode == True and self.start_frame > self.turbo_preroll and self.start_frame % int(self.turbo_steps) != 0:
                    self.start_frame = self.start_frame - (self.start_frame % int(self.turbo_steps))
            else:
                self.start_frame = int(resume_from_frame)+1
                if self.animation_mode != '3D' and self.turbo_mode == True and self.start_frame > self.turbo_preroll and self.start_frame % int(self.turbo_steps) != 0:
                    self.start_frame = self.start_frame - (self.start_frame % int(self.turbo_steps))
                if retain_overwritten_frames is True:
                    existing_frames = len(glob(self.batchFolder+f"/{self.batch_name}({self.batchNum})_*.png"))
                    frames_to_save = existing_frames - self.start_frame
                    print(f'Moving {frames_to_save} frames to the Retained folder')
                    self.move_files(self.start_frame, existing_frames, self.batchFolder, retainFolder)
        else:
            self.start_frame = 0
            self.batchNum = len(glob(self.batchFolder+"/*.txt"))
            while os.path.isfile(f"{self.batchFolder}/{self.batch_name}({self.batchNum})_settings.txt") is True or os.path.isfile(f"{self.batchFolder}/{self.batch_name}-{self.batchNum}_settings.txt") is True:
                self.batchNum += 1

        print(f'Init Run: {self.batch_name}({self.batchNum}) at frame {self.start_frame}')

        if self.set_seed == 'random_seed':
            random.seed()
            seed = random.randint(0, 2**32)
            print(f'Using seed: {seed}')
        else:
            seed = int(self.set_seed)

        self.args = {
            'batchNum': self.batchNum,
            'prompts_series':split_prompts(self.text_prompts) if self.text_prompts else None,
            'image_prompts_series':split_prompts(self.image_prompts) if self.image_prompts else None,
            'seed': seed,
            'display_rate':self.display_rate,
            'n_batches':self.n_batches if self.animation_mode == 'None' else 1,
            'batch_size':self.batch_size,
            'batch_name': self.batch_name,
            'steps': self.steps,
            'diffusion_sampling_mode': self.diffusion_sampling_mode,
            'width_height': self.width_height,
            'clip_guidance_scale': self.clip_guidance_scale,
            'tv_scale': self.tv_scale,
            'range_scale': self.range_scale,
            'sat_scale': self.sat_scale,
            'cutn_batches': self.cutn_batches,
            'init_image': self.init_image,
            'init_scale': self.init_scale,
            'skip_steps': self.skip_steps,
            'side_x': self.side_x,
            'side_y': self.side_y,
            'timestep_respacing': self.timestep_respacing,
            'diffusion_steps': self.diffusion_steps,
            'animation_mode': self.animation_mode,
            'video_init_path': self.video_init_path,
            'extract_nth_frame': self.extract_nth_frame,
            'video_init_seed_continuity': self.video_init_seed_continuity,
            'key_frames': self.key_frames,
            'max_frames': self.max_frames if self.animation_mode != "None" else 1,
            'interp_spline': self.interp_spline,
            'start_frame': self.start_frame,
            'angle': self.angle,
            'zoom': self.zoom,
            'translation_x': self.translation_x,
            'translation_y': self.translation_y,
            'translation_z': self.translation_z,
            'rotation_3d_x': self.rotation_3d_x,
            'rotation_3d_y': self.rotation_3d_y,
            'rotation_3d_z': self.rotation_3d_z,
            'midas_depth_model': self.midas_depth_model,
            'midas_weight': self.midas_weight,
            'near_plane': self.near_plane,
            'far_plane': self.far_plane,
            'fov': self.fov,
            'padding_mode': self.padding_mode,
            'sampling_mode': self.sampling_mode,
            'angle_series':self.angle_series,
            'zoom_series':self.zoom_series,
            'translation_x_series':self.translation_x_series,
            'translation_y_series':self.translation_y_series,
            'translation_z_series':self.translation_z_series,
            'rotation_3d_x_series':self.rotation_3d_x_series,
            'rotation_3d_y_series':self.rotation_3d_y_series,
            'rotation_3d_z_series':self.rotation_3d_z_series,
            'frames_scale': self.frames_scale,
            'calc_frames_skip_steps': calc_frames_skip_steps,
            'skip_step_ratio': skip_step_ratio,
            'calc_frames_skip_steps': calc_frames_skip_steps,
            'text_prompts': self.text_prompts,
            'image_prompts': self.image_prompts,
            'cut_overview': eval(self.cut_overview),
            'cut_innercut': eval(self.cut_innercut),
            'cut_ic_pow': self.cut_ic_pow,
            'cut_icgray_p': eval(self.cut_icgray_p),
            'intermediate_saves': self.intermediate_saves,
            'intermediates_in_subfolder': self.intermediates_in_subfolder,
            'steps_per_checkpoint': self.steps_per_checkpoint,
            'perlin_init': self.perlin_init,
            'perlin_mode': self.perlin_mode,
            'set_seed': self.set_seed,
            'eta': self.eta,
            'clamp_grad': self.clamp_grad,
            'clamp_max': self.clamp_max,
            'skip_augs': self.skip_augs,
            'randomize_class': self.randomize_class,
            'clip_denoised': self.clip_denoised,
            'fuzzy_prompt': self.fuzzy_prompt,
            'rand_mag': self.rand_mag,
            'soft_limiter_on': self.soft_limiter_on,
            'soft_limiter_knee': self.soft_limiter_knee,
        }

        self.args = SimpleNamespace(**self.args)

        # self.load_models()
        
        filename = ""
        gc.collect()
        torch.cuda.empty_cache()
        try:
            filename = self.render_frames()
        except KeyboardInterrupt:
            pass
        finally:
            print('Seed used:', seed)
            gc.collect()
            torch.cuda.empty_cache()
        return filename

    def init_settings(self):
                
        settings = self.settings

        """# 3. Settings"""

        #@markdown ####**Basic Settings:**
        self.batch_name = 'TimeToDisco' #@param{type: 'string'}
        self.clip_guidance_scale = settings['clip_guidance_scale'] #@param{type: 'number'}
        self.tv_scale =  settings['tv_scale']#@param{type: 'number'}
        self.range_scale =   settings['range_scale']#@param{type: 'number'}
        self.sat_scale =   settings['sat_scale'] #0#@param{type: 'number'}
        self.cutn_batches = settings['cutn_batches']   #@param{type: 'number'}
        self.skip_augs =  settings['skip_augs'] #@param{type: 'boolean'}

        #@markdown ####**Soft Limiter (Use 0.97 - 0.995 range):**\n",
                #@markdown *Experimental! ...may help mitigate color clipping.*\n",
        self.soft_limiter_on = settings['soft_limiter_on'] #@param{type: 'boolean'}\n",
        self.soft_limiter_knee = settings['soft_limiter_knee'] #@param{type: 'number'}\n",
        if self.soft_limiter_knee < 0.5 or self.soft_limiter_knee > .999:
            self.soft_limiter_knee = .98
            print('soft_limiter_knee out of range. Automatically reset to 0.98')
                
                    
        #@markdown ---

        #@markdown ####**Init Settings:**
        self.init_image = settings["init_image"] #@param{type: 'string'}
        self.init_scale = 1000 #@param{type: 'integer'}
        self.skip_steps = settings['skip_steps'] #@param{type: 'integer'}
        #@markdown *Make sure you set skip_steps to ~50% of your steps if you want to use an init image.*

        #Make folder for batch
        self.batchFolder = f'{self.outDirPath}/{self.batch_name}'
        envutils.createPath(self.batchFolder)

        """### Animation Settings"""

        #@markdown ####**Animation Mode:**
        self.animation_mode = settings['animation_mode'] #@param ['None', '2D', '3D', 'Video Input'] {type:'string'}
        #@markdown *For animation, you probably want to turn `cutn_batches` to 1 to make it quicker.*


        #@markdown ---

        #@markdown ####**Video Input Settings:**
        self.video_init_path = "training.mp4" #@param {type: 'string'}
        self.extract_nth_frame = 2 #@param {type: 'number'}
        self.video_init_seed_continuity = True #@param {type: 'boolean'}

        if self.animation_mode == "Video Input":
            self.videoFramesFolder = f'videoFrames'
            envutils.createPath(self.videoFramesFolder)
            print(f"Exporting Video Frames (1 every {self.extract_nth_frame})...")
            try:
                for f in pathlib.Path(f'{self.videoFramesFolder}').glob('*.jpg'):
                    f.unlink()
            except:
                print('')
            vf = f'"select=not(mod(n\,{self.extract_nth_frame}))"'
            subprocess.run(['ffmpeg', '-i', f'{self.video_init_path}', '-vf', f'{vf}', '-vsync', 'vfr', '-q:v', '2', '-loglevel', 'error', '-stats', f'{self.videoFramesFolder}/%04d.jpg'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            #!ffmpeg -i {video_init_path} -vf {vf} -vsync vfr -q:v 2 -loglevel error -stats {videoFramesFolder}/%04d.jpg

        #@markdown ---

        #@markdown ####**2D Animation Settings:**
        #@markdown `zoom` is a multiplier of dimensions, 1 is no zoom.
        #@markdown All rotations are provided in degrees.
        self.create_animation_data()

        self.midas_depth_model = "dpt_large"#@param {type:"string"}
        self.midas_weight = 0.3#@param {type:"number"}
        self.near_plane = 200#@param {type:"number"}
        self.far_plane = 10000#@param {type:"number"}
        self.fov = 40#@param {type:"number"}
        self.padding_mode = 'border'#@param {type:"string"}
        self.sampling_mode = 'bicubic'#@param {type:"string"}

        #======= TURBO MODE
        #@markdown ---
        #@markdown ####**Turbo Mode (3D anim only):**
        #@markdown (Starts after frame 10,) skips diffusion steps and just uses depth map to warp images for skipped frames.
        #@markdown Speeds up rendering by 2x-4x, and may improve image coherence between frames. frame_blend_mode smooths abrupt texture changes across 2 frames.
        #@markdown For different settings tuned for Turbo Mode, refer to the original Disco-Turbo Github: https://github.com/zippy731/disco-diffusion-turbo

        self.turbo_mode = settings['turbo_mode'] #@param {type:"boolean"}
        self.turbo_steps = settings['turbo_steps'] #@param ["2","3","4","5","6"] {type:"string"}
        self.turbo_preroll = settings['turbo_preroll'] # frames

        #insist turbo be used only w 3d anim.
        if self.turbo_mode and self.animation_mode != '3D':
            print('=====')
            print('Turbo mode only available with 3D animations. Disabling Turbo.')
            print('=====')
            self.turbo_mode = False

        #@markdown ---

        #@markdown ####**Coherency Settings:**
        #@markdown `frame_scale` tries to guide the new frame to looking like the old one. A good default is 1500.
        self.frames_scale = settings['frames_scale'] #@param{type: 'integer'}
        #@markdown `frame_skip_steps` will blur the previous frame - higher values will flicker less but struggle to add enough new detail to zoom into.
        self.frames_skip_steps = settings['frames_skip_steps'] #@param ['40%', '50%', '60%', '70%', '80%'] {type: 'string'}



        if self.key_frames:
            try:
                self.angle_series = get_inbetweens(parse_key_frames(self.angle),max_frames=self.max_frames,interp_spline = self.interp_spline)
            except RuntimeError as e:
                print(
                    "WARNING: You have selected to use key frames, but you have not "
                    "formatted `angle` correctly for key frames.\n"
                    "Attempting to interpret `angle` as "
                    f'"0: ({self.angle})"\n'
                    "Please read the instructions to find out how to use key frames "
                    "correctly.\n"
                )
                self.angle = f"0: ({self.angle})"
                self.angle_series = get_inbetweens(parse_key_frames(self.angle),max_frames=self.max_frames,interp_spline = self.interp_spline)

            try:
                self.zoom_series = get_inbetweens(parse_key_frames(self.zoom),max_frames=self.max_frames,interp_spline = self.interp_spline)
            except RuntimeError as e:
                print(
                    "WARNING: You have selected to use key frames, but you have not "
                    "formatted `zoom` correctly for key frames.\n"
                    "Attempting to interpret `zoom` as "
                    f'"0: ({self.zoom})"\n'
                    "Please read the instructions to find out how to use key frames "
                    "correctly.\n"
                )
                self.zoom = f"0: ({self.zoom})"
                self.zoom_series = get_inbetweens(parse_key_frames(self.zoom),max_frames=self.max_frames,interp_spline = self.interp_spline)

            try:
                self.translation_x_series = get_inbetweens(parse_key_frames(self.translation_x),max_frames=self.max_frames,interp_spline = self.interp_spline)
            except RuntimeError as e:
                print(
                    "WARNING: You have selected to use key frames, but you have not "
                    "formatted `translation_x` correctly for key frames.\n"
                    "Attempting to interpret `translation_x` as "
                    f'"0: ({self.translation_x})"\n'
                    "Please read the instructions to find out how to use key frames "
                    "correctly.\n"
                )
                self.translation_x = f"0: ({self.translation_x})"
                self.translation_x_series = get_inbetweens(parse_key_frames(self.translation_x),max_frames=self.max_frames,interp_spline = self.interp_spline)

            try:
                self.translation_y_series = get_inbetweens(parse_key_frames(self.translation_y),max_frames=self.max_frames,interp_spline = self.interp_spline)
            except RuntimeError as e:
                print(
                    "WARNING: You have selected to use key frames, but you have not "
                    "formatted `translation_y` correctly for key frames.\n"
                    "Attempting to interpret `translation_y` as "
                    f'"0: ({self.translation_y})"\n'
                    "Please read the instructions to find out how to use key frames "
                    "correctly.\n"
                )
                self.translation_y = f"0: ({self.translation_y})"
                self.translation_y_series = get_inbetweens(parse_key_frames(self.translation_y),max_frames=self.max_frames,interp_spline = self.interp_spline)

            try:
                self.translation_z_series = get_inbetweens(parse_key_frames(self.translation_z),max_frames=self.max_frames,interp_spline = self.interp_spline)
            except RuntimeError as e:
                print(
                    "WARNING: You have selected to use key frames, but you have not "
                    "formatted `translation_z` correctly for key frames.\n"
                    "Attempting to interpret `translation_z` as "
                    f'"0: ({self.translation_z})"\n'
                    "Please read the instructions to find out how to use key frames "
                    "correctly.\n"
                )
                self.translation_z = f"0: ({self.translation_z})"
                self.translation_z_series = get_inbetweens(parse_key_frames(self.translation_z),max_frames=self.max_frames,interp_spline = self.interp_spline)

            try:
                self.rotation_3d_x_series = get_inbetweens(parse_key_frames(self.rotation_3d_x),max_frames=self.max_frames,interp_spline = self.interp_spline)
            except RuntimeError as e:
                print(
                    "WARNING: You have selected to use key frames, but you have not "
                    "formatted `rotation_3d_x` correctly for key frames.\n"
                    "Attempting to interpret `rotation_3d_x` as "
                    f'"0: ({self.rotation_3d_x})"\n'
                    "Please read the instructions to find out how to use key frames "
                    "correctly.\n"
                )
                self.rotation_3d_x = f"0: ({self.rotation_3d_x})"
                self.rotation_3d_x_series = get_inbetweens(parse_key_frames(self.rotation_3d_x),max_frames=self.max_frames,interp_spline = self.interp_spline)

            try:
                self.rotation_3d_y_series = get_inbetweens(parse_key_frames(self.rotation_3d_y),max_frames=self.max_frames,interp_spline = self.interp_spline)
            except RuntimeError as e:
                print(
                    "WARNING: You have selected to use key frames, but you have not "
                    "formatted `rotation_3d_y` correctly for key frames.\n"
                    "Attempting to interpret `rotation_3d_y` as "
                    f'"0: ({self.rotation_3d_y})"\n'
                    "Please read the instructions to find out how to use key frames "
                    "correctly.\n"
                )
                self.rotation_3d_y = f"0: ({self.rotation_3d_y})"
                self.rotation_3d_y_series = get_inbetweens(parse_key_frames(self.rotation_3d_y),max_frames=self.max_frames,interp_spline = self.interp_spline)

            try:
                self.rotation_3d_z_series = get_inbetweens(parse_key_frames(self.rotation_3d_z),max_frames=self.max_frames,interp_spline = self.interp_spline)
            except RuntimeError as e:
                print(
                    "WARNING: You have selected to use key frames, but you have not "
                    "formatted `rotation_3d_z` correctly for key frames.\n"
                    "Attempting to interpret `rotation_3d_z` as "
                    f'"0: ({self.rotation_3d_z})"\n'
                    "Please read the instructions to find out how to use key frames "
                    "correctly.\n"
                )
                self.rotation_3d_z = f"0: ({self.rotation_3d_z})"
                self.rotation_3d_z_series = get_inbetweens(parse_key_frames(self.rotation_3d_z),max_frames=self.max_frames,interp_spline = self.interp_spline)

        else:
            self.angle = float(self.angle)
            self.zoom = float(self.zoom)
            self.translation_x = float(self.translation_x)
            self.translation_y = float(self.translation_y)
            self.translation_z = float(self.translation_z)
            self.rotation_3d_x = float(self.rotation_3d_x)
            self.rotation_3d_y = float(self.rotation_3d_y)
            self.rotation_3d_z = float(self.rotation_3d_z)

        """### Extra Settings
        Partial Saves, Advanced Settings, Cutn Scheduling
        """

        #@markdown ####**Saving:**

        self.intermediate_saves = 10#@param{type: 'raw'}
        self.intermediates_in_subfolder = True #@param{type: 'boolean'}
        #@markdown Intermediate steps will save a copy at your specified intervals. You can either format it as a single integer or a list of specific steps 

        #@markdown A value of `2` will save a copy at 33% and 66%. 0 will save none.

        #@markdown A value of `[5, 9, 34, 45]` will save at steps 5, 9, 34, and 45. (Make sure to include the brackets)


        if type(self.intermediate_saves) is not list:
            if self.intermediate_saves:
                self.steps_per_checkpoint = math.floor((self.steps - self.skip_steps - 1) // (self.intermediate_saves+1))
                self.steps_per_checkpoint = self.steps_per_checkpoint if self.steps_per_checkpoint > 0 else 1
                print(f'Will save every {self.steps_per_checkpoint} steps')
            else:
                self.steps_per_checkpoint = self.steps+10
        else:
            self.steps_per_checkpoint = None

        if self.intermediate_saves and self.intermediates_in_subfolder is True:
            self.partialFolder = f'{self.batchFolder}/partials'
            envutils.createPath(self.partialFolder)

            #@markdown ---

            #@markdown ####**Advanced Settings:**
            #@markdown *There are a few extra advanced settings available if you double click this cell.*

            #@markdown *Perlin init will replace your init, so uncheck if using one.*

            self.perlin_init = False  #@param{type: 'boolean'}
            self.perlin_mode = 'mixed' #@param ['mixed', 'color', 'gray']
            self.set_seed = 'random_seed' #'3545594394' #'random_seed' #@param{type: 'string'}
            self.eta = settings['eta'] #8#@param{type: 'number'}
            self.clamp_grad = True #@param{type: 'boolean'}
            self.clamp_max = settings['clamp_max'] #@param{type: 'number'}


            ### EXTRA ADVANCED SETTINGS:
            self.randomize_class = True
            self.clip_denoised = False
            self.fuzzy_prompt = False
            self.rand_mag = settings['rand_mag']


            #@markdown ---

            #@markdown ####**Cutn Scheduling:**
            #@markdown Format: `[40]*400+[20]*600` = 40 cuts for the first 400 /1000 steps, then 20 for the last 600/1000

            #@markdown cut_overview and cut_innercut are cumulative for total cutn on any given step. Overview cuts see the entire image and are good for early structure, innercuts are your standard cutn.

            self.cut_overview = "[12]*400+[4]*600" #@param {type: 'string'}       
            self.cut_innercut ="[4]*400+[12]*600"#@param {type: 'string'}  
            self.cut_ic_pow = 1#@param {type: 'number'}  
            self.cut_icgray_p = "[0.2]*400+[0]*600"#@param {type: 'string'}

            """### Prompts
            `animation_mode: None` will only use the first set. `animation_mode: 2D / Video` will run through them per the set frames and hold on the last one.
            """

            self.text_prompts = {
                0: settings['prompt'],
                #100: ["This set of prompts start at frame 100","This prompt has weight five:5"],
            }

            self.image_prompts = {
                # 0:['ImagePromptsWorkButArentVeryGood.png:2',],
            }

            """# 4. Diffuse!"""

            #@title Do the Run!
            #@markdown `n_batches` ignored with animation modes.
            self.display_rate =  10 #@param{type: 'number'}
            self.n_batches =  1 #@param{type: 'number'}

            #Update Model Settings
            self.timestep_respacing = f'ddim{self.steps}'
            self.diffusion_steps = (1000//self.steps)*self.steps if self.steps < 1000 else self.steps
            self.model_config.update({
                'timestep_respacing': self.timestep_respacing,
                'diffusion_steps': self.diffusion_steps,
            })

            self.batch_size = 1 

    def load_models(self,settings):
        
        model_256_downloaded = False
        model_512_downloaded = False
        model_secondary_downloaded = False

        multipip_res = subprocess.run(['pip', 'install', 'lpips', 'datetime', 'timm', 'ftfy', 'einops', 'pytorch-lightning', 'omegaconf'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(multipip_res)


        """# 2. Diffusion and CLIP model settings"""

        #@markdown ####**Models Settings:**
        self.diffusion_model = "512x512_diffusion_uncond_finetune_008100" #@param ["256x256_diffusion_uncond", "512x512_diffusion_uncond_finetune_008100"]
        self.use_secondary_model = settings['use_secondary_model'] #@param {type: 'boolean'}
        self.diffusion_sampling_mode = 'ddim' #@param ['plms','ddim']  


        use_checkpoint = True #@param {type: 'boolean'}
        self.ViTB32 = settings['ViTB32'] #@param{type:"boolean"}
        self.ViTB16 = settings['ViTB16'] #@param{type:"boolean"}
        self.ViTL14 = settings['ViTL14'] #@param{type:"boolean"}
        self.RN101 = settings['RN101'] #@param{type:"boolean"}
        self.RN50 = settings['RN50'] #@param{type:"boolean"}
        self.RN50x4 = settings['RN50x4'] #@param{type:"boolean"}
        self.RN50x16 = settings['RN50x16'] #@param{type:"boolean"}
        self.RN50x64 = settings['RN50x64'] #@param{type:"boolean"}

        #@markdown If you're having issues with model downloads, check this to compare SHA's:
        check_model_SHA = False #@param{type:"boolean"}

        model_256_SHA = '983e3de6f95c88c81b2ca7ebb2c217933be1973b1ff058776b970f901584613a'
        model_512_SHA = '9c111ab89e214862b76e1fa6a1b3f1d329b1a88281885943d2cdbe357ad57648'
        model_secondary_SHA = '983e3de6f95c88c81b2ca7ebb2c217933be1973b1ff058776b970f901584613a'

        model_256_link = 'https://openaipublic.blob.core.windows.net/diffusion/jul-2021/256x256_diffusion_uncond.pt'
        model_512_link = 'https://v-diffusion.s3.us-west-2.amazonaws.com/512x512_diffusion_uncond_finetune_008100.pt'
        model_secondary_link = 'https://v-diffusion.s3.us-west-2.amazonaws.com/secondary_model_imagenet_2.pth'

        model_256_path = f'{self.model_path}/256x256_diffusion_uncond.pt'
        model_512_path = f'{self.model_path}/512x512_diffusion_uncond_finetune_008100.pt'
        model_secondary_path = f'{self.model_path}/secondary_model_imagenet_2.pth'

        # Download the diffusion model
        if self.diffusion_model == '256x256_diffusion_uncond':
            if os.path.exists(model_256_path) and check_model_SHA:
                print('Checking 256 Diffusion File')
                with open(model_256_path,"rb") as f:
                    bytes = f.read() 
                    hash = hashlib.sha256(bytes).hexdigest();
                if hash == model_256_SHA:
                    print('256 Model SHA matches')
                    model_256_downloaded = True
                else: 
                    print("256 Model SHA doesn't match, redownloading...")
                    envutils.wget(model_256_link, self.model_path)
                    model_256_downloaded = True
            elif os.path.exists(model_256_path) and not check_model_SHA or model_256_downloaded == True:
                print('256 Model already downloaded, check check_model_SHA if the file is corrupt')
            else:  
                envutils.wget(model_256_link, self.model_path)
                model_256_downloaded = True
        elif self.diffusion_model == '512x512_diffusion_uncond_finetune_008100':
            if os.path.exists(model_512_path) and check_model_SHA:
                print('Checking 512 Diffusion File')
                with open(model_512_path,"rb") as f:
                    bytes = f.read() 
                    hash = hashlib.sha256(bytes).hexdigest();
                if hash == model_512_SHA:
                    print('512 Model SHA matches')
                    model_512_downloaded = True
                else:  
                    print("512 Model SHA doesn't match, redownloading...")
                    envutils.wget(model_512_link, envutils.model_path)
                    model_512_downloaded = True
            elif os.path.exists(model_512_path) and not check_model_SHA or model_512_downloaded == True:
                print('512 Model already downloaded, check check_model_SHA if the file is corrupt')
            else:  
                envutils.wget(model_512_link, self.model_path)
                model_512_downloaded = True


        # Download the secondary diffusion model v2
        if self.use_secondary_model == True:
            if os.path.exists(model_secondary_path) and check_model_SHA:
                print('Checking Secondary Diffusion File')
                with open(model_secondary_path,"rb") as f:
                    bytes = f.read() 
                    hash = hashlib.sha256(bytes).hexdigest();
                if hash == model_secondary_SHA:
                    print('Secondary Model SHA matches')
                    model_secondary_downloaded = True
                else:  
                    print("Secondary Model SHA doesn't match, redownloading...")
                    envutils.wget(model_secondary_link, self.model_path)
                    model_secondary_downloaded = True
            elif os.path.exists(model_secondary_path) and not check_model_SHA or model_secondary_downloaded == True:
                print('Secondary Model already downloaded, check check_model_SHA if the file is corrupt')
            else:  
                envutils.wget(model_secondary_link, self.model_path)
                model_secondary_downloaded = True

        self.model_config = model_and_diffusion_defaults()
        if self.diffusion_model == '512x512_diffusion_uncond_finetune_008100':
            self.model_config.update({
                'attention_resolutions': '32, 16, 8',
                'class_cond': False,
                'diffusion_steps': 1000, #No need to edit this, it is taken care of later.
                'rescale_timesteps': True,
                'timestep_respacing': 250, #No need to edit this, it is taken care of later.
                'image_size': 512,
                'learn_sigma': True,
                'noise_schedule': 'linear',
                'num_channels': 256,
                'num_head_channels': 64,
                'num_res_blocks': 2,
                'resblock_updown': True,
                'use_checkpoint': use_checkpoint,
                'use_fp16': True,
                'use_scale_shift_norm': True,
            })
        elif self.diffusion_model == '256x256_diffusion_uncond':
            self.model_config.update({
                'attention_resolutions': '32, 16, 8',
                'class_cond': False,
                'diffusion_steps': 1000, #No need to edit this, it is taken care of later.
                'rescale_timesteps': True,
                'timestep_respacing': 250, #No need to edit this, it is taken care of later.
                'image_size': 256,
                'learn_sigma': True,
                'noise_schedule': 'linear',
                'num_channels': 256,
                'num_head_channels': 64,
                'num_res_blocks': 2,
                'resblock_updown': True,
                'use_checkpoint': use_checkpoint,
                'use_fp16': True,
                'use_scale_shift_norm': True,
            })

        model_default = self.model_config['image_size']

        if self.use_secondary_model:
            secondary_model = models.SecondaryDiffusionImageNet2()
            secondary_model.load_state_dict(torch.load(f'{self.model_path}/secondary_model_imagenet_2.pth', map_location='cpu'))
            secondary_model.eval().requires_grad_(False).to(self.device)

        self.clip_models = []
        if self.ViTB32 is True: self.clip_models.append(clip.load('ViT-B/32', jit=False)[0].eval().requires_grad_(False).to(self.device)) 
        if self.ViTB16 is True: self.clip_models.append(clip.load('ViT-B/16', jit=False)[0].eval().requires_grad_(False).to(self.device) ) 
        if self.ViTL14 is True: self.clip_models.append(clip.load('ViT-L/14', jit=False)[0].eval().requires_grad_(False).to(self.device) ) 
        if self.RN50 is True: self.clip_models.append(clip.load('RN50', jit=False)[0].eval().requires_grad_(False).to(self.device))
        if self.RN50x4 is True: self.clip_models.append(clip.load('RN50x4', jit=False)[0].eval().requires_grad_(False).to(self.device)) 
        if self.RN50x16 is True: self.clip_models.append(clip.load('RN50x16', jit=False)[0].eval().requires_grad_(False).to(self.device)) 
        if self.RN50x64 is True: self.clip_models.append(clip.load('RN50x64', jit=False)[0].eval().requires_grad_(False).to(self.device)) 
        if self.RN101 is True: self.clip_models.append(clip.load('RN101', jit=False)[0].eval().requires_grad_(False).to(self.device)) 

        self.normalize = T.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[0.26862954, 0.26130258, 0.27577711])
        self.lpips_model = lpips.LPIPS(net='vgg').to(self.device)



        
        #Get corrected sizes
        self.steps = settings['steps'] #@param [25,50,100,150,250,500,1000]{type: 'raw', allow-input: true}
        self.width_height = settings['wh'] #@param{type: 'raw'}
        self.side_x = (self.width_height[0]//64)*64
        self.side_y = (self.width_height[1]//64)*64
        if self.side_x != self.width_height[0] or self.side_y != self.width_height[1]:
            print(f'Changing output size to {self.side_x}x{self.side_y}. Dimensions must by multiples of 64.')

        #Update Model Settings
        self.timestep_respacing = f'ddim{self.steps}'
        self.diffusion_steps = (1000//self.steps)*self.steps if self.steps < 1000 else self.steps
        self.model_config.update({
            'timestep_respacing': self.timestep_respacing,
            'diffusion_steps': self.diffusion_steps,
        })

        
        
        print('Prepping model...')
        self.model, self.diffusion = create_model_and_diffusion(**self.model_config)
        self.model.load_state_dict(torch.load(f'{self.model_path}/{self.diffusion_model}.pt', map_location='cpu'))
        self.model.requires_grad_(False).eval().to(self.device)
        for name, param in self.model.named_parameters():
            if 'qkv' in name or 'norm' in name or 'proj' in name:
                param.requires_grad_()
        if self.model_config['use_fp16']:
            self.model.convert_to_fp16()

    def save_settings(self):
        setting_list = {
            'text_prompts': self.text_prompts,
            'image_prompts': self.image_prompts,
            'clip_guidance_scale': self.clip_guidance_scale,
            'tv_scale': self.tv_scale,
            'range_scale': self.range_scale,
            'sat_scale': self.sat_scale,
            # 'cutn': self.cutn,
            'cutn_batches': self.cutn_batches,
            'max_frames': self.max_frames,
            'interp_spline': self.interp_spline,
            # 'rotation_per_frame': self.rotation_per_frame,
            'init_image': self.init_image,
            'init_scale': self.init_scale,
            'skip_steps': self.skip_steps,
            # 'zoom_per_frame': self.zoom_per_frame,
            'frames_scale': self.frames_scale,
            'frames_skip_steps': self.frames_skip_steps,
            'perlin_init': self.perlin_init,
            'perlin_mode': self.perlin_mode,
            'skip_augs': self.skip_augs,
            'randomize_class': self.randomize_class,
            'clip_denoised': self.clip_denoised,
            'clamp_grad': self.clamp_grad,
            'clamp_max': self.clamp_max,
            'seed': self.seed,
            'fuzzy_prompt': self.fuzzy_prompt,
            'rand_mag': self.rand_mag,
            'eta': self.eta,
            'width': self.width_height[0],
            'height': self.width_height[1],
            'diffusion_model': self.diffusion_model,
            'use_secondary_model': self.use_secondary_model,
            'steps': self.steps,
            'diffusion_steps': self.diffusion_steps,
            'diffusion_sampling_mode': self.diffusion_sampling_mode,
            'ViTB32': self.ViTB32,
            'ViTB16': self.ViTB16,
            'ViTL14': self.ViTL14,
            'RN101': self.RN101,
            'RN50': self.RN50,
            'RN50x4': self.RN50x4,
            'RN50x16': self.RN50x16,
            'RN50x64': self.RN50x64,
            'cut_overview': str(self.cut_overview),
            'cut_innercut': str(self.cut_innercut),
            'cut_ic_pow': self.cut_ic_pow,
            'cut_icgray_p': str(self.cut_icgray_p),
            'key_frames': self.key_frames,
            'max_frames': self.max_frames,
            'angle': self.angle,
            'zoom': self.zoom,
            'translation_x': self.translation_x,
            'translation_y': self.translation_y,
            'translation_z': self.translation_z,
            'rotation_3d_x': self.rotation_3d_x,
            'rotation_3d_y': self.rotation_3d_y,
            'rotation_3d_z': self.rotation_3d_z,
            'midas_depth_model': self.midas_depth_model,
            'midas_weight': self.midas_weight,
            'near_plane': self.near_plane,
            'far_plane': self.far_plane,
            'fov': self.fov,
            'padding_mode': self.padding_mode,
            'sampling_mode': self.sampling_mode,
            'video_init_path':self.video_init_path,
            'extract_nth_frame':self.extract_nth_frame,
            'video_init_seed_continuity': self.video_init_seed_continuity,
            'turbo_mode':self.turbo_mode,
            'turbo_steps':self.turbo_steps,
            'turbo_preroll':self.turbo_preroll,
        }
        # print('Settings:', setting_list)
        with open(f"{self.batchFolder}/{self.batch_name}({self.batchNum})_settings.txt", "w+") as f:   #save settings
            json.dump(setting_list, f, ensure_ascii=False, indent=4)

    def create_animation_data(self):
        self.key_frames = True #@param {type:"boolean"}
        self.max_frames = self.settings["max_frames"]  #@param {type:"number"}

        if self.animation_mode == "Video Input":
            self.max_frames = len(glob(f'{self.videoFramesFolder}/*.jpg'))

        sx = ""
        sz = ""
        sr = ""

        r=7.0
        px = 0.0
        pz = 0.0

        frame=360
        theta = -(math.pi*2) / (frame) #  -(math.pi / 180)
        for i in range(self.max_frames):

            px = 0.0
            pz = -r

            p1 = np.array([px,pz])
            p2 = np.array([r*math.cos(theta/2),r*math.sin(theta/2)])
            tv=  np.tan(np.flip(p1.copy())) 
            newpos = np.add(p1.copy(),np.multiply(tv.copy(),(math.pi*r*2)/frame))
            v = np.subtract(p2.copy(),newpos)

            sx = str(i) +": (" + str(v[0]) + "),"
            sz = str(i) +": (" + str(v[1]) + "),"
            sr = str(i) +": (" + str((theta)) + "),"
            
            sz = str(i) +": (" + str(2.0) + "),"
            

        self.interp_spline = 'Linear' #Do not change, currently will not look good. param ['Linear','Quadratic','Cubic']{type:"string"}
        self.angle = "0:(0.0)" #sa #@param {type:"string"}
        self.zoom = "0:(1.0)"#", 50: (1.05)"#@param {type:"string"} # was 10

        self.translation_x = "0: (0.0)" #"0: (0)"#@param {type:"string"}
        self.translation_y ="0: (0.0)" #"#@param {type:"string"}
        self.translation_z = sz #"0: (0.0)" #sz #"0: (0.0)" #0: (-10.0), 360: (-10)" #"0: (0.0)" #0: (1.0),360: (1.0)" # #"0: (10.0)"#@param {type:"string"}
        self.rotation_3d_x = "0: (0)"#@param {type:"string"}
        self.rotation_3d_y = "0: (0)" ##@param {type:"string"}
        self.rotation_3d_z = "0: (0)"#@param {type:"string"}
        
    def create_video(self):
        """# 5. Create the video"""

        # @title ### **Create video**
        #@markdown Video file will save in the same folder as your images.

        skip_video_for_run_all = True #@param {type: 'boolean'}

        if skip_video_for_run_all == True:
            print('Skipping video creation, uncheck skip_video_for_run_all if you want to run it')

        else:
            # import subprocess in case this cell is run without the above cells
            import subprocess
            from base64 import b64encode

        latest_run = self.batchNum

        folder = self.batch_name #@param
        run = latest_run #@param
        final_frame = 'final_frame'


        init_frame = 1#@param {type:"number"} This is the frame where the video will start
        last_frame = final_frame#@param {type:"number"} You can change i to the number of the last frame you want to generate. It will raise an error if that number of frames does not exist.
        fps = 12#@param {type:"number"}
        # view_video_in_cell = True #@param {type: 'boolean'}

        frames = []
        # tqdm.write('Generating video...')

        if last_frame == 'final_frame':
            last_frame = len(glob(self.batchFolder+f"/{folder}({run})_*.png"))
            print(f'Total frames: {last_frame}')

        image_path = f"{self.outDirPath}/{folder}/{folder}({run})_%04d.png"
        filepath = f"{self.outDirPath}/{folder}/{folder}({run}).mp4"


        cmd = [
            'ffmpeg',
            '-y',
            '-vcodec',
            'png',
            '-r',
            str(fps),
            '-start_number',
            str(init_frame),
            '-i',
            image_path,
            '-frames:v',
            str(last_frame+1),
            '-c:v',
            'libx264',
            '-vf',
            f'fps={fps}',
            '-pix_fmt',
            'yuv420p',
            '-crf',
            '17',
            '-preset',
            'veryslow',
            filepath
        ]

        process = subprocess.Popen(cmd, cwd=f'{self.batchFolder}', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(stderr)
            raise RuntimeError(stderr)
        else:
            print("The video is ready and saved to the images folder")
            
    def __init__(self,chain,steps,wh):
        self.device = chain.device
        self.DEVICE = chain.DEVICE
                
        self.settings["steps"] = steps
        self.settings["wh"] = wh

        self.root_path = os.getcwd()
        self.initDirPath = f'{self.root_path}/content/init_images'
        #createPath(initDirPath)
        self.outDirPath = f'{self.root_path}/content/images_out'
        #createPath(outDirPath)
        self.model_path = f'{self.root_path}/content/models'
        #createPath(model_path)
        self.PROJECT_DIR = os.path.abspath(os.getcwd())
        self.USE_ADABINS = True
                


        #@title ### 1.4 Define Midas functions

        # from midas.dpt_depth import DPTDepthModel
        # from midas.midas_net import MidasNet
        # from midas.midas_net_custom import MidasNet_small
        # from midas.transforms import Resize, NormalizeImage, PrepareForNet

        # # Initialize MiDaS depth model.
        # # It remains resident in VRAM and likely takes around 2GB VRAM.
        # # You could instead initialize it for each frame (and free it after each frame) to save VRAM.. but initializing it is slow.
        self.default_models = {
            "midas_v21_small": f"{self.model_path}/midas_v21_small-70d6b9c8.pt",
            "midas_v21": f"{self.model_path}/midas_v21-f6b98070.pt",
            "dpt_large": f"{self.model_path}/dpt_large-midas-2f21e586.pt",
            "dpt_hybrid": f"{self.model_path}/dpt_hybrid-midas-501f0c75.pt",
            "dpt_hybrid_nyu": f"{self.model_path}/dpt_hybrid_nyu-2ce69ec7.pt",}
        
        self.load_models(self.settings)
        

