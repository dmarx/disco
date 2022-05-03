import datetime
import gc
import json
import math
from types import SimpleNamespace
from PIL import Image, ImageOps
import torch
from torchvision import transforms
from tqdm.notebook import tqdm
from modules.generators.generator_disco.guided_diffusion_disco.guided_diffusion.script_util import create_model_and_diffusion, model_and_diffusion_defaults
import os
from modules.generators.base.generator import GeneratorBase
import requests
import json
        
class GeneratorGoBig(GeneratorBase):

    args = None
    
    settings = {
     'init_image': "",
     'input_width': 512,
     'input_height': 512
        }
    
    model_config = None
    model_path = None
    diffusion_model = None
    
    # FUNCTIONS FOR GO BIG MODE
    global slices_todo
    slices_todo = 5 # Number of chunks to slice up from the original image

    def do_run(self):

        # curl -i -F files[]=@yourfile.jpeg https://tmp.ninja/upload.php (JSON Response)

        files = {
            'files[]': open(self.settings['init_image'], 'rb'),
        }
        response = requests.post('https://tmp.ninja/upload.php', files=files)
        print(response)

        data = {
            'style': 'art',
            'noise': '3',
            'x2': '1',
            'input': response.json()['files'][0]['url']
        }

        r = requests.post(
            url='https://bigjpg.com/api/task/',
            headers={'X-API-KEY': '06838332753e420eb27110b20199b244'},
            data={'conf': json.dumps(data)}
        )
        
        tid = r.json()['tid']
        
        while True:
            r = requests.get(url='https://bigjpg.com/api/task/'+tid)
            if (r.json()[tid]['status'] == 'success'):
                r2 = requests.get(r.json()[tid]['url'], allow_redirects=True)
                open('static/output/output_go_big.png', 'wb').write(r2.content)
                break
        #     print(r.json())
        # print(r.json()['tid'])

        return "output_go_big.png"
  
        
    # def do_run(self):
    #     #self.chain.output_message("doing run", prompt, prefix, input_seed)

    #     device = self.device
        
    #     #wget("https://github.com/lowfuel/progrockdiffusion/blob/main/maskv.png", PROJECT_DIR)
    #     current_time = datetime.datetime.now().strftime('%y%m%d-%H%M%S_%f')
    #     # Resize initial progress.png to new size
    #     original_output_image = self.settings['init_image'] #(f'{batchFolder}/{batch_name}_original_output_{current_time}.png')
    #     os.system("cp " + self.settings['init_image'] + " content/output_go_big/progress.png") #final_output_image + " static/output/output_go_big.png")
    #     final_output_image = f'content/output_go_big/output_{current_time}.png'
    #     progress_image = f'content/output_go_big/progress.png'
    #     input_image = Image.open(progress_image).convert('RGBA')
    #     input_image.save(original_output_image)
    #     slice_image = (f'content/output_go_big/slice.png')
    #     reside_x = self.settings['input_width'] * 2
    #     reside_y = self.settings['input_height'] * 2
    #     source_image = input_image.resize((reside_x, reside_y), Image.LANCZOS)
    #     input_image.close()
    #     # Slice source_image into 4 overlapping slices
    #     slices = self.slice(source_image)
    #     # Run PRD again for each slice, with init image paramaters, etc.
    #     i = 1 # just to number the slices as they save
    #     betterslices = []
    #     for chunk in slices:
    #         # Reset underlying systems for another run
    #         self.chain.output_message('Prepping model for next run...')
    #         # model, diffusion = create_model_and_diffusion(**self.model_config)
    #         # model.load_state_dict(
    #         #     torch.load(f'{self.model_path}/{self.diffusion_model}.pt', map_location='cpu'))
    #         # model.requires_grad_(False).eval().to(device)
    #         # for name, param in model.named_parameters():
    #         #     if 'qkv' in name or 'norm' in name or 'proj' in name:
    #         #         param.requires_grad_()
    #         # if self.model_config['use_fp16']:
    #         #     model.convert_to_fp16()
    #         # gc.collect()
    #         # torch.cuda.empty_cache()
    #         #now do the next run
    #         chunk.save(slice_image)
    #         self.args.init_image = slice_image
    #         self.args.skip_steps = int(self.steps * .6)
    #         self.args.side_x, self.args.side_y = chunk.size
    #         self.do_run()
    #         print(f'Finished run, grabbing {progress_image} and adding it to betterslices.')
    #         resultslice = Image.open(progress_image).convert('RGBA')
    #         betterslices.append(resultslice.copy())
    #         resultslice.save(f'content/output_go_big_slice_output_{current_time}_{i}.png')
    #         resultslice.close() # hopefully this will allow subsequent images to actually save.
    #         i += 1
    #     # For each slice, use addalpha to add an alpha mask
    #     alpha_gradient = Image.new('L', (self.args.side_x, 1), color=0xFF)
    #     a = 0
    #     for x in range(self.args.side_x):
    #         a +=4 # add 4 to alpha at each pixel, to give us a 64 pixel overlap gradient
    #         if a < 255:
    #             alpha_gradient.putpixel((x, 0), a)
    #         else:
    #             alpha_gradient.putpixel((x, 0), 255)
    #         # print '{}, {:.2f}, {}'.format(x, float(x) / width, a)
    #     alpha = alpha_gradient.resize(betterslices[0].size)

    #     mask = Image.new('RGBA', (self.args.side_x, self.args.side_y), color=0)
    #     mask.putalpha(alpha)
    #     i = 1 # start at 1 in the list instead of 0, because we don't need/want a mask on the first (0) image
    #     while i < self.slices_todo:
    #         betterslices[i] = self.addalpha(betterslices[i], mask)
    #         i += 1
    #     # Once we have all our images, mergeimgs back onto source.png, then save
    #     final_output = self.mergeimgs(source_image, betterslices)
    #     final_output.save(final_output_image)
    #     print(f'\n\nGO BIG is complete!\n\n ***** NOTE *****\nYour output is saved as {final_output_image}!')


    #     os.system("cp content/output_go_big/" + final_output_image +
    #               " static/output/output_go_big.png")

    #     return "output_go_big.png"


    # # Input is an image, return image with mask added as an alpha channel
    # def addalpha(im, mask):
    #     imr, img, imb, ima = im.split()
    #     mmr, mmg, mmb, mma = mask.split()
    #     im = Image.merge('RGBA', [imr, img, imb, mma]) # we want the RGB from the original, but the transparency from the mask
    #     return(im)

    # # take a source image and layer in the slices on top
    # def mergeimgs(source, slices):
    #     source.convert("RGBA")
    #     width, height = source.size
    #     slice_width = int(width / slices_todo)
    #     slice_width = 64 * math.floor(slice_width / 64) #round slice width up to the nearest 64
    #     paste_x = 0
    #     for slice in slices:
    #         source.alpha_composite(slice, (paste_x,0))
    #         paste_x += slice_width
    #     return source

    # # Slices an image into the configured number of chunks. Overlap is a quarter of the size of a chunk
    # def slice(self,source):
    #     width, height = source.size
    #     overlap = 64 #int(height / slices_todo / 4)
    #     slice_width = int(width / slices_todo)
    #     slice_width = 64 * math.floor(slice_width / 64) #round slice width up to the nearest 64
    #     slice_width += overlap
    #     print(f'rounded slice_width is {slice_width} with overlap')
    #     i = 0
    #     slices = []
    #     x = 0
    #     y = 0
    #     edgex = slice_width
    #     while i < slices_todo:
    #         slices.append(source.crop((x, y, edgex, height)))
    #         x += slice_width - overlap
    #         edgex = x + slice_width
    #         i += 1
    #     return (slices)



    # #def load_models(self):
        
    #     # self.model_state_dict = torch.load(
    #     #     self.args.model_path, map_location='cuda')

    #     # #self.update_model_params()

    #     # # if self.args.cpu:
    #     # #     self.model_config['use_fp16'] = False

    #     # # Load models
    #     # self.model, self.diffusion = create_model_and_diffusion(
    #     #     **self.model_config)
    #     # self.model.load_state_dict(self.model_state_dict, strict=False)
    #     # self.model.requires_grad_(
    #     #     self.args.clip_guidance).eval().to(self.device)

    #     # if self.model_config['use_fp16']:
    #     #     self.model.convert_to_fp16()
    #     # else:
    #     #     self.model.convert_to_fp32()

    #     # def set_requires_grad(model, value):
    #     #     for param in model.parameters():
    #     #         param.requires_grad = value

    #     # # vae
    #     # self.ldm = torch.load(self.args.kl_path, map_location="cuda")
    #     # self.ldm.to(self.device)
    #     # self.ldm.eval()
    #     # self.ldm.requires_grad_(self.args.clip_guidance)
    #     # set_requires_grad(self.ldm, self.args.clip_guidance)

    #     # self.bert = BERTEmbedder(1280, 32)
    #     # sd = torch.load(self.args.bert_path, map_location="cuda")
    #     # self.bert.load_state_dict(sd)

    #     # self.bert.to(self.device)
    #     # self.bert.half().eval()
    #     # set_requires_grad(self.bert, False)

    #     # # clip
    #     # self.clip_model, self.clip_preprocess = clip.load(
    #     #     'ViT-L/14@336px', device=self.device, jit=False)
    #     # self.clip_model.eval().requires_grad_(False)
    #     # self.normalize = transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[
    #     #                                       0.26862954, 0.26130258, 0.27577711])



    def init_settings(self, override_settings=None):
                
        settings = self.settings

        if override_settings!=None:
            settings = self.json_override(settings, override_settings)
            
        # self.args.steps = settings["steps"]
        
        #self.update_model_params()
        


    def __init__(self,chain, load_models=True):
        super().__init__(chain)
        self.title = "Go Big"
    
        self.args = json.loads(json.dumps(self.settings), object_hook=lambda d: SimpleNamespace(**d))
        
        # self.args.width = 256
        # self.args.height = 256
        # self.args.clip_guidance = False

        # self.device = torch.device('cuda:0' if (
        #     torch.cuda.is_available() and not self.args.cpu) else 'cpu')
        # self.chain.output_message('Using device:', self.device)


   #Update Model Settings
   
        # self.model_config = model_and_diffusion_defaults()
        # self.diffusion_model = '512x512_diffusion_uncond_finetune_008100'
        # if self.diffusion_model == '512x512_diffusion_uncond_finetune_008100':
        #     self.model_config.update({
        #         'attention_resolutions': '32, 16, 8',
        #         'class_cond': False,
        #         'diffusion_steps': 1000, #No need to edit this, it is taken care of later.
        #         'rescale_timesteps': True,
        #         'timestep_respacing': 250, #No need to edit this, it is taken care of later.
        #         'image_size': 512,
        #         'learn_sigma': True,
        #         'noise_schedule': 'linear',
        #         'num_channels': 256,
        #         'num_head_channels': 64,
        #         'num_res_blocks': 2,
        #         'resblock_updown': True,
        #         'use_checkpoint': True,
        #         'use_fp16': True,
        #         'use_scale_shift_norm': True,
        #     })


        # self.steps = 150    
        # self.timestep_respacing = f'ddim{self.steps}'
        # self.diffusion_steps = (1000//self.steps)*self.steps if self.steps < 1000 else self.steps
        # self.model_config.update({
        #     'timestep_respacing': self.timestep_respacing,
        #     'diffusion_steps': self.diffusion_steps,
        # })


        # self.root_path = os.getcwd()
        # self.model_path = f'{self.root_path}/content/models'
        # self.diffusion_model = "512x512_diffusion_uncond_finetune_008100" #@param ["256x256_diffusion_uncond", "512x512_diffusion_uncond_finetune_008100"]

        # self.chain.output_message('Prepping model...')
        # self.model, self.diffusion = create_model_and_diffusion(**self.model_config)
        # self.model.load_state_dict(torch.load(f'{self.model_path}/{self.diffusion_model}.pt', map_location='cpu'))
        # self.model.requires_grad_(False).eval().to(self.device)
        # for name, param in self.model.named_parameters():
        #     if 'qkv' in name or 'norm' in name or 'proj' in name:
        #         param.requires_grad_()
        # if self.model_config['use_fp16']:
        #     self.model.convert_to_fp16()

        # if load_models:
        #     self.load_models()
