import sys

sys.path.append('./../ResizeRight')
sys.path.append('./../CLIP')
sys.path.append('./../guided-diffusion')
sys.path.append('./../latent-diffusion')

from setup import download_models2
from datetime import datetime
from perlin import create_perlin_noise, regen_perlin
import run
import setup
import hashlib
from ipywidgets import Output
import random
import matplotlib.pyplot as plt
import numpy as np
from guided_diffusion.script_util import create_model_and_diffusion, model_and_diffusion_defaults
import clip
from tqdm.notebook import tqdm
import torchvision.transforms.functional as TF
import torchvision.transforms as T
from torch.nn import functional as F
import torch
from types import SimpleNamespace
from PIL import Image, ImageOps
import lpips
from IPython import display
import math
import gc
import cv2
import os
from prompt import get_inbetweens, parse_key_frames, split_prompts
from setup import createPath
from utils import MakeCutouts, MakeCutoutsDango, SecondaryDiffusionImageNet2, alpha_sigma_to_t, fetch, parse_prompt, range_loss, spherical_dist_loss, tv_loss


clip_list = [
    #"ViT-L/14",  # VRAM HEAVY!!!
    # "RN50x64",     #VRAM HEAVY!!!
    'RN50x16',  # VRAM HEAVY!!!
    'ViT-B/32',
    "ViT-B/16",
    #"RN50x4",
     #"RN101",
     #"RN50"
]

settings = {
    # 'prompt': "A scenic view of an Alpine landscape in summer, matte painting trending on artstation",
    # 'prompt': "The Gateway to the Great Temple at Baalbec, matte painting trending on artstation",
    # 'prompt':'A scenic view of Torres del Paine National Park at Patagonia, matte painting trending on artstation',
   'prompt': "A scenic view of a Scottish loch in the Isle of Skye, matte painting trending on artstation",
    #  'prompt':'Astronaut in vale of tears and locusts attack by Gustav Dore. Rendered in Unreal Engine, Trending on Artstation',
    'clip_guidance_scale': 10000,
    'steps': 250,
    'cut_ic_pow': 1,
    'range_scale': 150,
    'cutn_batches': 4,
    'diffusion_steps': 1000,
    'path': '/home/twmmason/dev/disco',
    # 'RN101': False,
    # 'RN50': True,
    # 'RN50x4': False,
    # 'RN50x16': False,
    # 'RN50x64': False,
    # 'ViTB32': False,
    # 'ViTB16': False,
    # 'ViTL14': False,
}
print(settings)

skip_for_run_all = True  # @param {type: 'boolean'}
root_path = settings['path'] + '/content'

initDirPath = f'{root_path}/init_images'
setup.createPath(initDirPath)
outDirPath = f'{root_path}/images_out'
setup.createPath(outDirPath)
print("Created paths...")


model_path = settings['path'] + '/content/models'

model_256_downloaded = False
model_512_downloaded = False
model_secondary_downloaded = False

stop_on_next_loop = False
rescale_timesteps = True

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

# A100 fix thanks to Emad
if torch.cuda.get_device_capability(device) == (8, 0):
    print('Disabling CUDNN for A100 gpu', file=sys.stderr)
    torch.backends.cudnn.enabled = False


cutout_debug = False
padargs = {}

# @param ["256x256_diffusion_uncond", "512x512_diffusion_uncond_finetune_008100"]
diffusion_model = "512x512_diffusion_uncond_finetune_008100"
# diffusion_model = "512x512_diffusion_uncond_openimages_epoch28_withfilter"
use_secondary_model = False  # @param {type: 'boolean'}

# param ['25','50','100','150','250','500','1000','ddim25','ddim50', 'ddim75', 'ddim100','ddim150','ddim250','ddim500','ddim1000']
timestep_respacing = '50'
diffusion_steps = settings['diffusion_steps']  # param {type: 'number'}
use_checkpoint = True  # @param {type: 'boolean'}

SLIPB16 = False  # param{type:"boolean"}
SLIPL16 = False  # param{type:"boolean"}

# @markdown If you're having issues with model downloads, check this to compare SHA's:
check_model_SHA = False  # @param{type:"boolean"}

model_256_SHA = '983e3de6f95c88c81b2ca7ebb2c217933be1973b1ff058776b970f901584613a'
model_512_SHA = '9c111ab89e214862b76e1fa6a1b3f1d329b1a88281885943d2cdbe357ad57648'
model_secondary_SHA = '983e3de6f95c88c81b2ca7ebb2c217933be1973b1ff058776b970f901584613a'

model_256_link = 'https://openaipublic.blob.core.windows.net/diffusion/jul-2021/256x256_diffusion_uncond.pt'
model_512_link = 'http://batbot.tv/ai/models/guided-diffusion/512x512_diffusion_uncond_finetune_008100.pt'
model_secondary_link = 'https://v-diffusion.s3.us-west-2.amazonaws.com/secondary_model_imagenet_2.pth'

model_256_path = f'{model_path}/256x256_diffusion_uncond.pt'
model_512_path = f'{model_path}/512x512_diffusion_uncond_finetune_008100.pt'
model_secondary_path = f'{model_path}/secondary_model_imagenet_2.pth'

download_models2(diffusion_model, model_512_path, model_256_path, check_model_SHA, model_256_SHA,
                 model_512_SHA, use_secondary_model, model_secondary_path, model_secondary_SHA)

pace = []
model_list = []
# diff_512_openimages=True
# yfcc_2=True
# yfcc_2_file_name = 'yfcc_2'

# if diff_512_openimages:
#   if '{"model_name":"512x512_diffusion_uncond_openimages_epoch28_withfilter", "guided":True, "mag_adjust":1}' in pace: pace.remove({"model_name":"512x512_diffusion_uncond_openimages_epoch28_withfilter", "guided":True, "mag_adjust":1})
#   pace.append({"model_name":"512x512_diffusion_uncond_openimages_epoch28_withfilter", "guided":True, "mag_adjust":1})
#   if "512x512_diffusion_uncond_openimages_epoch28_withfilter" in model_list: model_list.remove("512x512_diffusion_uncond_openimages_epoch28_withfilter")
#   model_list.append("512x512_diffusion_uncond_openimages_epoch28_withfilter")
#   os.system("wget -nc 'https://set.zlkj.in/models/diffusion/512x512_diffusion_uncond_openimages_epoch28_withfilter.pt' -P " + model_path + "")
# if yfcc_2:
#   if '{"model_name":"yfcc_2", "guided":True, "mag_adjust":1}' in pace: pace.remove({"model_name":yfcc_2_file_name, "guided":True, "mag_adjust":1})
#   pace.append({"model_name":"yfcc_2", "guided":True, "mag_adjust":1})
#   if "yfcc_2" in model_list: model_list.remove("yfcc_2")
#   model_list.append("yfcc_2")
#   os.system("wget -nc 'https://v-diffusion.s3.us-west-2.amazonaws.com/yfcc_2.pth' -P " + model_path + "")
# # if cc12m:
# #   if '{"model_name":{cc12m_file_name}, "guided":True, "mag_adjust":1}' in pace: pace.remove({"model_name":cc12m_file_name, "guided":True, "mag_adjust":1})
# #   pace.append({"model_name":cc12m_file_name, "guided":True, "mag_adjust":1})
# #   if cc12m_file_name in model_list: model_list.remove(cc12m_file_name)
# #   model_list.append(cc12m_file_name)
# #   os.system("wget -nc 'https://v-diffusion.s3.us-west-2.amazonaws.com/cc12m_1_cfg.pth' -P " + model_path + "")
# # if use_secondary_model:
# #   os.system("wget -nc 'https://v-diffusion.s3.us-west-2.amazonaws.com/secondary_model_imagenet_2.pth' -P " + model_path + "")
# #   secondary_model = SecondaryDiffusionImageNet2()
# #   secondary_model.load_state_dict(torch.load(f'{model_path}/{secondary_file_name}.pth', map_location='cpu'))
# #   secondary_model = secondary_model.eval().requires_grad_(False).to("cuda")


model_config = model_and_diffusion_defaults()
if diffusion_model == '512x512_diffusion_uncond_finetune_008100':
    model_config.update({
        'attention_resolutions': '32, 16, 8',
        'class_cond': False,
        'diffusion_steps': diffusion_steps,
        'rescale_timesteps': True,
        'timestep_respacing': timestep_respacing,
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
elif diffusion_model == '512x512_diffusion_uncond_openimages_epoch28_withfilter':
    timestep_respacing = "16,48,72"
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
elif diffusion_model == '256x256_diffusion_uncond':
    model_config.update({
        'attention_resolutions': '32, 16, 8',
        'class_cond': False,
        'diffusion_steps': diffusion_steps,
        'rescale_timesteps': True,
        'timestep_respacing': timestep_respacing,
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

secondary_model_ver = 2
model_default = model_config['image_size']


if secondary_model_ver == 2:
    secondary_model = SecondaryDiffusionImageNet2()
    secondary_model.load_state_dict(torch.load(
        f'{model_path}/secondary_model_imagenet_2.pth', map_location='cpu'))
secondary_model.eval().requires_grad_(False).to(device)

print("clip models", clip.available_models())

clip_models = []

# clip_model = {}
# clip_size = {}
for i in clip_list:
    # clip_model[i] = clip.load(i, jit=False)[
    #     0].eval().requires_grad_(False).to(device)
    # clip_size[i] = clip_model[i].visual.input_resolution
    clip_models.append(clip.load(i, jit=False)[0].eval().requires_grad_(False).to(device))
    # print("clip_size", clip_size[i])

normalize = T.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[
                        0.26862954, 0.26130258, 0.27577711])
lpips_model = lpips.LPIPS(net='vgg').to(device)

"""# 3. Settings"""

# @markdown ####**Basic Settings:**
batch_name = 'TimeToDisco'  # @param{type: 'string'}
# @param [25,50,100,150,250,500,1000]{type: 'raw', allow-input: true}
steps = settings['steps']
width_height = [1280, 768]  # @param{type: 'raw'}
clip_guidance_scale = settings['clip_guidance_scale']  # @param{type: 'number'}
tv_scale = 0  # @param{type: 'number'}
range_scale = settings['range_scale']  # @param{type: 'number'}
sat_scale = 0  # @param{type: 'number'}
cutn_batches = settings['cutn_batches']  # @param{type: 'number'}
skip_augs = True  # @param{type: 'boolean'}

# @markdown ---

# @markdown ####**Init Settings:**
init_image = None  # @param{type: 'string'}
init_scale = 1000  # @param{type: 'integer'}
skip_steps = 0  # @param{type: 'integer'}

# Get corrected sizes
side_x = (width_height[0]//64)*64
side_y = (width_height[1]//64)*64
if side_x != width_height[0] or side_y != width_height[1]:
    print(
        f'Changing output size to {side_x}x{side_y}. Dimensions must by multiples of 64.')

# Update Model Settings
timestep_respacing = f'ddim{steps}'
diffusion_steps = (1000//steps)*steps if steps < 1000 else steps
model_config.update({
    'timestep_respacing': timestep_respacing,
    'diffusion_steps': diffusion_steps,
})

# Make folder for batch
batchFolder = f'{outDirPath}/{batch_name}'
setup.createPath(batchFolder)

animation_mode = "None"  # @param['None', '2D', 'Video Input']
extract_nth_frame = 2  # @param {type:"number"}

key_frames = True  # @param {type:"boolean"}
max_frames = 10000  # @param {type:"number"}


# Do not change, currently will not look good. param ['Linear','Quadratic','Cubic']{type:"string"}
interp_spline = 'Linear'
angle = "0:(0)"  # @param {type:"string"}
zoom = "0: (1), 10: (1.05)"  # @param {type:"string"}
translation_x = "0: (0)"  # @param {type:"string"}
translation_y = "0: (0)"  # @param {type:"string"}

# @markdown ####**Coherency Settings:**
# @markdown `frame_scale` tries to guide the new frame to looking like the old one. A good default is 1500.
frames_scale = 1500  # @param{type: 'integer'}
# @markdown `frame_skip_steps` will blur the previous frame - higher values will flicker less but struggle to add enough new detail to zoom into.
# @param ['40%', '50%', '60%', '70%', '80%'] {type: 'string'}
frames_skip_steps = '60%'

if key_frames:
    try:
        angle_series = get_inbetweens(parse_key_frames(angle))
    except RuntimeError as e:
        print(
            "WARNING: You have selected to use key frames, but you have not "
            "formatted `angle` correctly for key frames.\n"
            "Attempting to interpret `angle` as "
            f'"0: ({angle})"\n'
            "Please read the instructions to find out how to use key frames "
            "correctly.\n"
        )
        angle = f"0: ({angle})"
        angle_series = get_inbetweens(parse_key_frames(angle))

    try:
        zoom_series = get_inbetweens(parse_key_frames(zoom))
    except RuntimeError as e:
        print(
            "WARNING: You have selected to use key frames, but you have not "
            "formatted `zoom` correctly for key frames.\n"
            "Attempting to interpret `zoom` as "
            f'"0: ({zoom})"\n'
            "Please read the instructions to find out how to use key frames "
            "correctly.\n"
        )
        zoom = f"0: ({zoom})"
        zoom_series = get_inbetweens(parse_key_frames(zoom))

    try:
        translation_x_series = get_inbetweens(parse_key_frames(translation_x))
    except RuntimeError as e:
        print(
            "WARNING: You have selected to use key frames, but you have not "
            "formatted `translation_x` correctly for key frames.\n"
            "Attempting to interpret `translation_x` as "
            f'"0: ({translation_x})"\n'
            "Please read the instructions to find out how to use key frames "
            "correctly.\n"
        )
        translation_x = f"0: ({translation_x})"
        translation_x_series = get_inbetweens(parse_key_frames(translation_x))

    try:
        translation_y_series = get_inbetweens(parse_key_frames(translation_y))
    except RuntimeError as e:
        print(
            "WARNING: You have selected to use key frames, but you have not "
            "formatted `translation_y` correctly for key frames.\n"
            "Attempting to interpret `translation_y` as "
            f'"0: ({translation_y})"\n'
            "Please read the instructions to find out how to use key frames "
            "correctly.\n"
        )
        translation_y = f"0: ({translation_y})"
        translation_y_series = get_inbetweens(parse_key_frames(translation_y))

else:
    angle = float(angle)
    zoom = float(zoom)
    translation_x = float(translation_x)
    translation_y = float(translation_y)

"""### Extra Settings
 Partial Saves, Diffusion Sharpening, Advanced Settings, Cutn Scheduling
"""

# @markdown ####**Saving:**

intermediate_saves = 50  # @param{type: 'raw'}
intermediates_in_subfolder = True  # @param{type: 'boolean'}
# @markdown Intermediate steps will save a copy at your specified intervals. You can either format it as a single integer or a list of specific steps
# @markdown A value of `2` will save a copy at 33% and 66%. 0 will save none.
# @markdown A value of `[5, 9, 34, 45]` will save at steps 5, 9, 34, and 45. (Make sure to include the brackets)


if type(intermediate_saves) is not list:
    if intermediate_saves:
        steps_per_checkpoint = math.floor(
            (steps - skip_steps - 1) // (intermediate_saves+1))
        steps_per_checkpoint = steps_per_checkpoint if steps_per_checkpoint > 0 else 1
        print(f'Will save every {steps_per_checkpoint} steps')
    else:
        steps_per_checkpoint = steps+10
else:
    steps_per_checkpoint = None

if intermediate_saves and intermediates_in_subfolder is True:
    partialFolder = f'{batchFolder}/partials'
    createPath(partialFolder)

    # @markdown ---

# @markdown ####**SuperRes Sharpening:**
# @markdown *Sharpen each image using latent-diffusion. Does not run in animation mode. `keep_unsharp` will save both versions.*
sharpen_preset = 'Off'  # @param ['Off', 'Faster', 'Fast', 'Slow', 'Very Slow']
keep_unsharp = True  # @param{type: 'boolean'}

if sharpen_preset != 'Off' and keep_unsharp is True:
    unsharpenFolder = f'{batchFolder}/unsharpened'
    createPath(unsharpenFolder)

    # @markdown ---

# @markdown ####**Advanced Settings:**
# @markdown *There are a few extra advanced settings available if you double click this cell.*

# @markdown *Perlin init will replace your init, so uncheck if using one.*

perlin_init = False  # @param{type: 'boolean'}
perlin_mode = 'mixed'  # @param ['mixed', 'color', 'gray']
set_seed = 'random_seed'  # @param{type: 'string'}
eta = 0.9  # @param{type: 'number'}
clamp_grad = True  # @param{type: 'boolean'}
clamp_max = 0.05  # @param{type: 'number'}


# EXTRA ADVANCED SETTINGS:
randomize_class = True
clip_denoised = False
fuzzy_prompt = False
rand_mag = 0.05

# @markdown ---
# @markdown ####**Cutn Scheduling:**
# @markdown Format: `[40]*400+[20]*600` = 40 cuts for the first 400 /1000 steps, then 20 for the last 600/1000
# @markdown cut_overview and cut_innercut are cumulative for total cutn on any given step. Overview cuts see the entire image and are good for early structure, innercuts are your standard cutn.

cut_overview = "[12]*400+[4]*600"  # @param {type: 'string'}
cut_innercut = "[4]*400+[12]*600"  # @param {type: 'string'}
cut_ic_pow = 1  # @param {type: 'number'}
cut_icgray_p = "[0.2]*400+[0]*600"  # @param {type: 'string'}


text_prompts = {
    0: [settings['prompt']],
    100: ["This set of prompts start at frame 100", "This prompt has weight five:5"],
}

image_prompts = {
    # 0:['ImagePromptsWorkButArentVeryGood.png:2',],
}

display_rate = 50  # @param{type: 'number'}
n_batches = 1  # @param{type: 'number'}

batch_size = 1

resume_run = False  # @param{type: 'boolean'}
run_to_resume = 'latest'  # @param{type: 'string'}
resume_from_frame = 'latest'  # @param{type: 'string'}
retain_overwritten_frames = False  # @param{type: 'boolean'}
if retain_overwritten_frames is True:
    retainFolder = f'{batchFolder}/retained'
    setup.createPath(retainFolder)


skip_step_ratio = int(frames_skip_steps.rstrip("%")) / 100
calc_frames_skip_steps = math.floor(steps * skip_step_ratio)

if steps <= calc_frames_skip_steps:
    sys.exit("ERROR: You can't skip more steps than your total steps")

batchNum = 0

random.seed()
seed = random.randint(0, 2**32)

args = {
    'batchNum': batchNum,
    'prompts_series': split_prompts(text_prompts) if text_prompts else None,
    'image_prompts_series': split_prompts(image_prompts) if image_prompts else None,
    'seed': seed,
    'display_rate': display_rate,
    'n_batches': n_batches if animation_mode == 'None' else 1,
    'batch_size': batch_size,
    'batch_name': batch_name,
    'steps': steps,
    'width_height': width_height,
    'clip_guidance_scale': clip_guidance_scale,
    'tv_scale': tv_scale,
    'range_scale': range_scale,
    'sat_scale': sat_scale,
    'cutn_batches': cutn_batches,
    'init_image': init_image,
    'init_scale': init_scale,
    'skip_steps': skip_steps,
    'sharpen_preset': sharpen_preset,
    'keep_unsharp': keep_unsharp,
    'side_x': side_x,
    'side_y': side_y,
    'timestep_respacing': timestep_respacing,
    'diffusion_steps': diffusion_steps,
    'animation_mode': animation_mode,
    'video_init_path': "",
    'extract_nth_frame': extract_nth_frame,
    'key_frames': key_frames,
    'max_frames': max_frames if animation_mode != "None" else 1,
    'interp_spline': interp_spline,
    'start_frame': 0,
    'angle': angle,
    'zoom': zoom,
    'translation_x': translation_x,
    'translation_y': translation_y,
    'angle_series': angle_series,
    'zoom_series': zoom_series,
    'translation_x_series': translation_x_series,
    'translation_y_series': translation_y_series,
    'frames_scale': frames_scale,
    'calc_frames_skip_steps': calc_frames_skip_steps,
    'skip_step_ratio': skip_step_ratio,
    'calc_frames_skip_steps': calc_frames_skip_steps,
    'text_prompts': text_prompts,
    'image_prompts': image_prompts,
    'cut_overview': eval(cut_overview),
    'cut_innercut': eval(cut_innercut),
    'cut_ic_pow': cut_ic_pow,
    'cut_icgray_p': eval(cut_icgray_p),
    'intermediate_saves': intermediate_saves,
    'intermediates_in_subfolder': intermediates_in_subfolder,
    'steps_per_checkpoint': steps_per_checkpoint,
    'perlin_init': perlin_init,
    'perlin_mode': perlin_mode,
    'set_seed': set_seed,
    'eta': eta,
    'clamp_grad': clamp_grad,
    'clamp_max': clamp_max,
    'skip_augs': skip_augs,
    'randomize_class': randomize_class,
    'clip_denoised': clip_denoised,
    'fuzzy_prompt': fuzzy_prompt,
    'rand_mag': rand_mag,
}

args = SimpleNamespace(**args)

print('Prepping model...')
model, diffusion = create_model_and_diffusion(**model_config)
model.load_state_dict(torch.load(
    f'{model_path}/{diffusion_model}.pt', map_location='cpu'))
model.requires_grad_(False).eval().to(device)
for name, param in model.named_parameters():
    if 'qkv' in name or 'norm' in name or 'proj' in name:
        param.requires_grad_()
if model_config['use_fp16']:
    model.convert_to_fp16()


gc.collect()
torch.cuda.empty_cache()
try:
    # do_run()
    run.do_run(args, stop_on_next_loop, clip_models, device, model, diffusion, normalize, secondary_model,
               lpips_model, model_config, use_secondary_model, partialFolder, batchFolder,root_path,pace)  # ,unsharpenFolder)
except KeyboardInterrupt:
    pass
finally:
    print('Seed used:', seed)
    gc.collect()
    torch.cuda.empty_cache()
