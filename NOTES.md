y main changes: 
- clip models: RN16/32 + rn50x4
- eta: 0.9
- clamp_max: 0.05
and the most important:
- skip_augs: true
- secondary: false

rtx on
beautiful landscape full of grass and flowers by Noah Bradley, matte painting, Trending on Artstation
    'prompt': "A scenic view of a beautiful landscape full of grass and flowers by Noah Bradley, blue sky, mountains, matte painting trending on Artstation",

  'prompt': "A traveller at lightspeed in hyperspace, matte painting trending on Artstation", #by Asher Brown Durand
    'prompt': "Garden hall at Petra, matte painting trending on artstation", #by Asher Brown Durand

pip install piq
pip install ftfy
pip install ipywidgets
pip install lpips
pip install pytorch_lit
pip install pandas
pip install timm
pip install pytorch-lightning
pip install einops
pip install omegaconf


# for guided-diffusion-plms
# Notebooks are not updated yet and may not be updated today 
# However if you want to try it you can replace diffusion.(p/ddim)_sample_loop(_progressive)
# With diffusion.plms_sample_loop(_progressive)
# PLMS has an order parameter, 2 by default
# It can be 1-4. When 1 it is equivalent to DDIM. 
# Also it seems to not like TV loss very much, less so at higher orders 
# Like 150 seems to work with order 2 but breaks higher orders.
# TV loss is more tolerable with more timesteps, for any order.
# you should, if your tv loss value is not too high, first try just putting in order 2 plms in place of whatever you are doing now

<!-- 
diffusion2 full shot of the into the void vortex of  The incandescent magical clockwork tesla reactor light trail of the lotus  of electric corona fusion reaction fractal  of Fairy deity, eldritch origami duality, magical sunflower halo, eternal revelation, untamed perfection depth shader, opposed symmetry  by ross tran, artstation CGSociety -w 19200 -h 10800  -clip_guidance_scale 20000 -tv_scale 20000 -range_scale 175 -cutn 128 -cutn_batches 2
 -cutn_whole_portion 1 -cutn_bw_portion 0.5 -cut_pow 50 -seed 0 -skip_timesteps 30 -->
<!-- 

 Clip_guidance_scale = With two perceptors, effective guidance scale is ~2x because they are added together.

Tv_scale = Smooths out the image

Sat_scale = Tries to prevent pixel values from going out of range

Cutn= Effective cutn is cut_batches * this

Cut_pow = Affects the size of cutouts. Larger cut_pow -> smaller cutouts

Cut_batches = Multiplies the amount of cutn

Steps = Number of steps for sampling. Generally, more = better. (edited)
maybe this will help a bit -->


#Discodiffusion #VQGAN #CLIP #AI #AIart #digitalart #generativeart #DeepLearning #MachineLearning #ArtistOnTwitter #ESRGAN #GANart #creativecoding #art 

a_laser_canon_powered_by_embedded_aura_quartz_monolith_crystal_cluster_o.mp4

a_laser_canon_powered_by_embedded_aura_quartz_monolith_crystal_cluster_o.mp4


Disco Diffusion works best for me. Brian Froud lends itself well in the prompt to a soft, natural look. The first two used that..

    'prompt': "The Gateway to the Great Temple at Baalbec, matte painting trending on artstation",
    'prompt': "Assassin's Creed Valhalla, by Calleva Atrebatum, matte painting trending on artstation",
    'prompt': "Greek temple, by Carl Jungheim, matte painting trending on artstation",



#prompts
"A scenic view of the Hanging Gardens of Babylon, matte painting trending on artstation",

ANTONYMS FOR blur
MOST RELEVANT
brighten
illuminate
lighten
clarify
clean
cleanse
clear
purify
uncloud
unsmudge