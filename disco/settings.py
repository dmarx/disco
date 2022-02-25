
# def save_settings():
#   setting_list = {
#     'text_prompts': text_prompts,
#     'image_prompts': image_prompts,
#     'clip_guidance_scale': clip_guidance_scale,
#     'tv_scale': tv_scale,
#     'range_scale': range_scale,
#     'sat_scale': sat_scale,
#     # 'cutn': cutn,
#     'cutn_batches': cutn_batches,
#     'max_frames': max_frames,
#     'interp_spline': interp_spline,
#     # 'rotation_per_frame': rotation_per_frame,
#     'init_image': init_image,
#     'init_scale': init_scale,
#     'skip_steps': skip_steps,
#     # 'zoom_per_frame': zoom_per_frame,
#     'frames_scale': frames_scale,
#     'frames_skip_steps': frames_skip_steps,
#     'perlin_init': perlin_init,
#     'perlin_mode': perlin_mode,
#     'skip_augs': skip_augs,
#     'randomize_class': randomize_class,
#     'clip_denoised': clip_denoised,
#     'clamp_grad': clamp_grad,
#     'clamp_max': clamp_max,
#     'seed': seed,
#     'fuzzy_prompt': fuzzy_prompt,
#     'rand_mag': rand_mag,
#     'eta': eta,
#     'width': width_height[0],
#     'height': width_height[1],
#     'diffusion_model': diffusion_model,
#     'use_secondary_model': use_secondary_model,
#     'steps': steps,
#     'diffusion_steps': diffusion_steps,
#     'ViTB32': ViTB32,
#     'ViTB16': ViTB16,
#     'RN101': RN101,
#     'RN50': RN50,
#     'RN50x4': RN50x4,
#     'RN50x16': RN50x16,
#     'cut_overview': str(cut_overview),
#     'cut_innercut': str(cut_innercut),
#     'cut_ic_pow': cut_ic_pow,
#     'cut_icgray_p': str(cut_icgray_p),
#     'key_frames': key_frames,
#     'max_frames': max_frames,
#     'angle': angle,
#     'zoom': zoom,
#     'translation_x': translation_x,
#     'translation_y': translation_y,
#     'video_init_path':video_init_path,
#     'extract_nth_frame':extract_nth_frame,
#   }
#   # print('Settings:', setting_list)
#   with open(f"{batchFolder}/{batch_name}({batchNum})_settings.txt", "w+") as f:   #save settings
#     json.dump(setting_list, f, ensure_ascii=False, indent=4)
