


import math
import os
import torch
from midas.dpt_depth import DPTDepthModel
from midas.midas_net import MidasNet
from midas.midas_net_custom import MidasNet_small
from midas.transforms import NormalizeImage, PrepareForNet, Resize
import py3d_tools as p3dT
import disco_xform_utils as dxf
import cv2
from torch.nn import functional as F
import torchvision.transforms.functional as TF
import numpy as np
from PIL import ImageOps
import pandas as pd
import torchvision.transforms as T


def init_midas_depth_model(midas_model_type="dpt_large", optimize=True,DEVICE = None,default_models=None):
    midas_model = None
    net_w = None
    net_h = None
    resize_mode = None
    normalization = None

    print(f"Initializing MiDaS '{midas_model_type}' depth model...")
    # load network
    midas_model_path = default_models[midas_model_type]

    if midas_model_type == "dpt_large": # DPT-Large
        midas_model = DPTDepthModel(
            path=midas_model_path,
            backbone="vitl16_384",
            non_negative=True,
        )
        net_w, net_h = 384, 384
        resize_mode = "minimal"
        normalization = NormalizeImage(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    elif midas_model_type == "dpt_hybrid": #DPT-Hybrid
        midas_model = DPTDepthModel(
            path=midas_model_path,
            backbone="vitb_rn50_384",
            non_negative=True,
        )
        net_w, net_h = 384, 384
        resize_mode="minimal"
        normalization = NormalizeImage(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    elif midas_model_type == "dpt_hybrid_nyu": #DPT-Hybrid-NYU
        midas_model = DPTDepthModel(
            path=midas_model_path,
            backbone="vitb_rn50_384",
            non_negative=True,
        )
        net_w, net_h = 384, 384
        resize_mode="minimal"
        normalization = NormalizeImage(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    elif midas_model_type == "midas_v21":
        midas_model = MidasNet(midas_model_path, non_negative=True)
        net_w, net_h = 384, 384
        resize_mode="upper_bound"
        normalization = NormalizeImage(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        )
    elif midas_model_type == "midas_v21_small":
        midas_model = MidasNet_small(midas_model_path, features=64, backbone="efficientnet_lite3", exportable=True, non_negative=True, blocks={'expand': True})
        net_w, net_h = 256, 256
        resize_mode="upper_bound"
        normalization = NormalizeImage(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        )
    else:
        print(f"midas_model_type '{midas_model_type}' not implemented")
        assert False

    midas_transform = T.Compose(
        [
            Resize(
                net_w,
                net_h,
                resize_target=None,
                keep_aspect_ratio=True,
                ensure_multiple_of=32,
                resize_method=resize_mode,
                image_interpolation_method=cv2.INTER_CUBIC,
            ),
            normalization,
            PrepareForNet(),
        ]
    )

    midas_model.eval()
    
    if optimize==True:
        if DEVICE == torch.device("cuda"):
            midas_model = midas_model.to(memory_format=torch.channels_last)  
            midas_model = midas_model.half()

    midas_model.to(DEVICE)

    print(f"MiDaS '{midas_model_type}' depth model initialized.")
    return midas_model, midas_transform, net_w, net_h, resize_mode, normalization

def interp(t):
    return 3 * t**2 - 2 * t ** 3

def perlin(self, width, height, scale=10, device=None):
    gx, gy = torch.randn(2, width + 1, height + 1, 1, 1, device=device)
    xs = torch.linspace(0, 1, scale + 1)[:-1, None].to(device)
    ys = torch.linspace(0, 1, scale + 1)[None, :-1].to(device)
    wx = 1 - self.interp(xs)
    wy = 1 - self.interp(ys)
    dots = 0
    dots += wx * wy * (gx[:-1, :-1] * xs + gy[:-1, :-1] * ys)
    dots += (1 - wx) * wy * (-gx[1:, :-1] * (1 - xs) + gy[1:, :-1] * ys)
    dots += wx * (1 - wy) * (gx[:-1, 1:] * xs - gy[:-1, 1:] * (1 - ys))
    dots += (1 - wx) * (1 - wy) * (-gx[1:, 1:] * (1 - xs) - gy[1:, 1:] * (1 - ys))
    return dots.permute(0, 2, 1, 3).contiguous().view(width * scale, height * scale)

def perlin_ms(octaves, width, height, grayscale, device=None):
    out_array = [0.5] if grayscale else [0.5, 0.5, 0.5]
    # out_array = [0.0] if grayscale else [0.0, 0.0, 0.0]
    for i in range(1 if grayscale else 3):
        scale = 2 ** len(octaves)
        oct_width = width
        oct_height = height
        for oct in octaves:
            p = perlin(oct_width, oct_height, scale, device)
            out_array[i] += p * oct
            scale //= 2
            oct_width *= 2
            oct_height *= 2
    return torch.cat(out_array)

def create_perlin_noise(side_x,side_y,octaves=[1, 1, 1, 1], width=2, height=2, grayscale=True):
    out = perlin_ms(octaves, width, height, grayscale)
    if grayscale:
        out = TF.resize(size=(side_y, side_x), img=out.unsqueeze(0))
        out = TF.to_pil_image(out.clamp(0, 1)).convert('RGB')
    else:
        out = out.reshape(-1, 3, out.shape[0]//3, out.shape[1])
        out = TF.resize(size=(side_y, side_x), img=out)
        out = TF.to_pil_image(out.clamp(0, 1).squeeze())

    out = ImageOps.autocontrast(out)
    return out

def regen_perlin(perlin_mode,device,batch_size):
    if perlin_mode == 'color':
        init = create_perlin_noise([1.5**-i*0.5 for i in range(12)], 1, 1, False)
        init2 = create_perlin_noise([1.5**-i*0.5 for i in range(8)], 4, 4, False)
    elif perlin_mode == 'gray':
        init = create_perlin_noise([1.5**-i*0.5 for i in range(12)], 1, 1, True)
        init2 = create_perlin_noise([1.5**-i*0.5 for i in range(8)], 4, 4, True)
    else:
        init = create_perlin_noise([1.5**-i*0.5 for i in range(12)], 1, 1, False)
        init2 = create_perlin_noise([1.5**-i*0.5 for i in range(8)], 4, 4, True)

    init = TF.to_tensor(init).add(TF.to_tensor(init2)).div(2).to(device).unsqueeze(0).mul(2).sub(1)
    del init2
    return init.expand(batch_size, -1, -1, -1)


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

def soft_limit(x,soft_limiter_knee):
    #value from -n to n, always return a value -1<x<1\n",
    #soft_limiter_knee set in params = 0.97 # where does compression start?\n",
    soft_sign = x/abs(x)
    soft_overage = ((abs(x)-soft_limiter_knee)+(abs(abs(x)-soft_limiter_knee)))/2
    soft_base = abs(x)-soft_overage
    soft_limited_x = soft_base + torch.tanh(soft_overage/(1-soft_limiter_knee))*(1-soft_limiter_knee)
    return soft_limited_x*soft_sign
        
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

def do_3d_step(img_filepath, frame_num, midas_model, midas_transform,args,trans_scale,device,DEVICE):
    if args.key_frames:
        translation_x = args.translation_x_series[frame_num]
        translation_y = args.translation_y_series[frame_num]
        translation_z = args.translation_z_series[frame_num]
        rotation_3d_x = args.rotation_3d_x_series[frame_num]
        rotation_3d_y = args.rotation_3d_y_series[frame_num]
        rotation_3d_z = args.rotation_3d_z_series[frame_num]
        print(
            f'translation_x: {translation_x}',
            f'translation_y: {translation_y}',
            f'translation_z: {translation_z}',
            f'rotation_3d_x: {rotation_3d_x}',
            f'rotation_3d_y: {rotation_3d_y}',
            f'rotation_3d_z: {rotation_3d_z}',
        )

    translate_xyz = [-translation_x*trans_scale, translation_y*trans_scale, -translation_z*trans_scale]
    rotate_xyz_degrees = [rotation_3d_x, rotation_3d_y, rotation_3d_z]
    print('translation:',translate_xyz)
    print('rotation:',rotate_xyz_degrees)
    rotate_xyz = [math.radians(rotate_xyz_degrees[0]), math.radians(rotate_xyz_degrees[1]), math.radians(rotate_xyz_degrees[2])]
    rot_mat = p3dT.euler_angles_to_matrix(torch.tensor(rotate_xyz, device=device), "XYZ").unsqueeze(0)
    print("rot_mat: " + str(rot_mat))
    next_step_pil = dxf.transform_image_3d(img_filepath, midas_model, midas_transform, DEVICE,
                                            rot_mat, translate_xyz, args.near_plane, args.far_plane,
                                            args.fov, padding_mode=args.padding_mode,
                                            sampling_mode=args.sampling_mode, midas_weight=args.midas_weight)
    return next_step_pil

def generate_eye_views(trans_scale,batchFolder,filename,frame_num,midas_model, midas_transform,vr_ipd,vr_eye_angle,DEVICE,device,args):
    for i in range(2):
        theta = vr_eye_angle * (math.pi/180) #x * 2 * pi ­ pi
        #   phi = pi / 2 ­ y * pi
        ipd = vr_ipd
        ray_origin = math.cos(theta) * ipd / 2 * (-1.0 if i==0 else 1.0)
        ray_rotation = (theta if i==0 else -theta)
        # translate_xyz = [-(translation_x+ray_origin)*trans_scale, translation_y*trans_scale, -translation_z*trans_scale]
        translate_xyz = [-(ray_origin)*trans_scale, 0,0]
        rotate_xyz = [0, (ray_rotation), 0]
        rot_mat = p3dT.euler_angles_to_matrix(torch.tensor(rotate_xyz, device=device), "XYZ").unsqueeze(0)
        transformed_image = dxf.transform_image_3d(f'{batchFolder}/{filename}', midas_model, midas_transform, DEVICE,
                                                        rot_mat, translate_xyz, args.near_plane, args.far_plane,
                                                        args.fov, padding_mode=args.padding_mode,
                                                        sampling_mode=args.sampling_mode, midas_weight=args.midas_weight,spherical=True)
        eye_file_path = batchFolder+f"/frame_{frame_num:04}" + ('_l' if i==0 else '_r')+'.png'
        transformed_image.save(eye_file_path)
    
    
    def append_dims(x, n):
        return x[(Ellipsis, *(None,) * (n - x.ndim))]


    def alpha_sigma_to_t(alpha, sigma):
        return torch.atan2(sigma, alpha) * 2 / math.pi


    def t_to_alpha_sigma(t):
        return torch.cos(t * math.pi / 2), torch.sin(t * math.pi / 2)


    def parse_key_frames(string, prompt_parser=None):
        """Given a string representing frame numbers paired with parameter values at that frame,
        return a dictionary with the frame numbers as keys and the parameter values as the values.

        Parameters
        ----------
        string: string
            Frame numbers paired with parameter values at that frame number, in the format
            'framenumber1: (parametervalues1), framenumber2: (parametervalues2), ...'
        prompt_parser: function or None, optional
            If provided, prompt_parser will be applied to each string of parameter values.
        
        Returns
        -------
        dict
            Frame numbers as keys, parameter values at that frame number as values

        Raises
        ------
        RuntimeError
            If the input string does not match the expected format.
        
        Examples
        --------
        >>> parse_key_frames("10:(Apple: 1| Orange: 0), 20: (Apple: 0| Orange: 1| Peach: 1)")
        {10: 'Apple: 1| Orange: 0', 20: 'Apple: 0| Orange: 1| Peach: 1'}

        >>> parse_key_frames("10:(Apple: 1| Orange: 0), 20: (Apple: 0| Orange: 1| Peach: 1)", prompt_parser=lambda x: x.lower()))
        {10: 'apple: 1| orange: 0', 20: 'apple: 0| orange: 1| peach: 1'}
        """
        import re
        pattern = r'((?P<frame>[0-9]+):[\s]*[\(](?P<param>[\S\s]*?)[\)])'
        frames = dict()
        for match_object in re.finditer(pattern, string):
            frame = int(match_object.groupdict()['frame'])
            param = match_object.groupdict()['param']
            if prompt_parser:
                frames[frame] = prompt_parser(param)
            else:
                frames[frame] = param

        if frames == {} and len(string) != 0:
            raise RuntimeError('Key Frame string not correctly formatted')
        return frames

    def get_inbetweens(interp_spline,max_frames,key_frames, integer=False):
        """Given a dict with frame numbers as keys and a parameter value as values,
        return a pandas Series containing the value of the parameter at every frame from 0 to max_frames.
        Any values not provided in the input dict are calculated by linear interpolation between
        the values of the previous and next provided frames. If there is no previous provided frame, then
        the value is equal to the value of the next provided frame, or if there is no next provided frame,
        then the value is equal to the value of the previous provided frame. If no frames are provided,
        all frame values are NaN.

        Parameters
        ----------
        key_frames: dict
            A dict with integer frame numbers as keys and numerical values of a particular parameter as values.
        integer: Bool, optional
            If True, the values of the output series are converted to integers.
            Otherwise, the values are floats.
        
        Returns
        -------
        pd.Series
            A Series with length max_frames representing the parameter values for each frame.
        
        Examples
        --------
        >>> max_frames = 5
        >>> get_inbetweens({1: 5, 3: 6})
        0    5.0
        1    5.0
        2    5.5
        3    6.0
        4    6.0
        dtype: float64

        >>> get_inbetweens({1: 5, 3: 6}, integer=True)
        0    5
        1    5
        2    5
        3    6
        4    6
        dtype: int64
        """
        key_frame_series = pd.Series([np.nan for a in range(max_frames)])

        for i, value in key_frames.items():
            key_frame_series[i] = value
        key_frame_series = key_frame_series.astype(float)
        
        interp_method = interp_spline

        if interp_method == 'Cubic' and len(key_frames.items()) <=3:
            interp_method = 'Quadratic'
        
        if interp_method == 'Quadratic' and len(key_frames.items()) <= 2:
            interp_method = 'Linear'
        
        
        key_frame_series[0] = key_frame_series[key_frame_series.first_valid_index()]
        key_frame_series[max_frames-1] = key_frame_series[key_frame_series.last_valid_index()]
        # key_frame_series = key_frame_series.interpolate(method=intrp_method,order=1, limit_direction='both')
        key_frame_series = key_frame_series.interpolate(method=interp_method.lower(),limit_direction='both')
        if integer:
            return key_frame_series.astype(int)
        return key_frame_series

    def split_prompts(prompts,max_frames):
        prompt_series = pd.Series([np.nan for a in range(max_frames)])
        for i, prompt in prompts.items():
            prompt_series[i] = prompt
        # prompt_series = prompt_series.astype(str)
        prompt_series = prompt_series.ffill().bfill()
        return prompt_series

    def move_files(start_num, end_num, old_folder, new_folder,batch_name,batchNum):
        for i in range(start_num, end_num):
            old_file = old_folder + f'/{batch_name}({batchNum})_{i:04}.png'
            new_file = new_folder + f'/{batch_name}({batchNum})_{i:04}.png'
            os.rename(old_file, new_file)

