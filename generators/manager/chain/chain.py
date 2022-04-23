import os, sys
from random import randint, seed
import torch
from generator_disco.generator import GeneratorDisco
from generator_ld.generator import GeneratorLatentDiffusion

class Chain:

    DEVICE = None
    device = None
    output_filename = None
    
    generator_disco = None
    generator_ld = None
    
    run_disco = True
    run_ld = True
    
    def load_cuda(self):
        
        self.DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        print('Using device:', self.DEVICE)
        self.device = self.DEVICE # At least one of the modules expects this name..

        if torch.cuda.get_device_capability(self.DEVICE) == (8,0): ## A100 fix thanks to Emad
            print('Disabling CUDNN for A100 gpu', file=sys.stderr)
            torch.backends.cudnn.enabled = False
            
    def run_chain(self,prompt):
        print (prompt)

        if self.run_ld:
            if self.generator_ld == None: self.generator_ld =  GeneratorLatentDiffusion(self)
            self.generator_ld.args.prefix = str(randint(0,1000000))
            self.output_filename = self.generator_ld.do_run(prompt,self.generator_ld.args.prefix,str(100))

        if self.run_disco:
            if self.generator_disco == None: self.generator_disco = GeneratorDisco(self,100,[512,512])
            self.generator_disco.settings["prompt"] = [prompt]
            if self.run_ld: 
                self.generator_disco.settings["skip_steps"] = 25
                self.generator_disco.settings["init_image"] = os.getcwd() + "/static/output/" + self.output_filename
            self.generator_disco.init_settings()
            self.output_filename = self.generator_disco.do_run()
        
        return self.output_filename

    def __init__(self):
        seed(1)
        self.load_cuda()
        
        
        
        