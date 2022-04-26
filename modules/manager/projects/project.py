
from genericpath import exists
import os
import dill
# from flask import jsonify
# from modules.generators.generator_disco.generator import GeneratorDisco
# from modules.generators.generator_ld.generator import GeneratorLatentDiffusion
from datetime import date

class Project:
    
    id = 0
    title = ""
    created = ""
    
    chain = None
    
    generators= None
    generators_json = None
        
    def load_data(self):
        self.generators = []
        self.chain = []
        self.title = ""
        if exists(self.project_dir()):
            file_data = dill.load(open(self.project_dir() + "/data.obj", "rb"))
            self.title = file_data.title
            self.created = file_data.created
            self.chain = file_data.chain
            
            generator_data = dill.load(open(self.project_dir() + "/generators.obj", "rb"))
            if generator_data != None:
                self.generators = generator_data
                for name in filter(lambda x: len(x.get("label")>0),self.generators):
                    generator = self.fetch_by_name(name)
                    generator.settings = dill.load(open(self.project_path + "/generators/" + str.lower(name).replace(" ","_")) + "settings.json" , "rb")
                    #json.loads(generator_data.json)
        else:
            self.created = str(date.today())          
              
        # else:
            # data_obj = AudioData(tempo,beats,onsets_hfc,downbeat_times)
            # s =json.dumps(data_obj, indent=4, cls=AudioDataEncoder)
            # pickle.dump(s, file = open(file, "wb"))

    def save(self):
        # self.project_path = 
        if not exists(self.project_dir()): os.makedirs(self.project_dir())
        
        updated = Project(self.id)
        updated.title = self.title
        updated.chain = self.chain
        updated.created = self.created
        print("saviing updated",updated)
        
        dill.dump(updated, file=open(updated.project_dir() + "/data.obj", "wb"))
        
        #self.data_path = 
        
        # self.generators_json = jsonify(self.generators)
        dill.dump(updated.generators, file=open(updated.project_dir() + "/generators.obj", "wb"))
        # self.generators_json = generator_data.json
        
        
        # for name in self.generators.items.filter(lambda x: len(x.get("label"))>0):
        #     generator = self.fetch_by_name(name)
        #     generator.settings = dill.load(open(self.project_path + "/generators/" + str.lower(name).replace(" ","_")) + "settings.json" , "rb")
        #     #json.loads(generator_data.json)
    

    def project_dir(self):
        root_path = os.getcwd()
        return root_path + "/static/data/projects/" + str(self.id)
    
    
    def __init__(self,id):
        self.id = id
    
    
    # # def get(self):
    # #     return {}
    # def load(self):
        
    # def fetch_generator(self):
    #     if self.name == "Latent Diffusion":
    #         return GeneratorLatentDiffusion(None)
    #     if name == "Disco Diffusion":
    #         return GeneratorDisco(None)
        
    #     return None
    
        # if name == "Superres":
        #         break
        
        
    #           elements: [
    #     { id: "1", type: "input", label: "Grid-3-ML", position: { x: 250, y: 5 } },
    #     { id: "2", label: "Superres", position: { x: 100, y: 100 } },
    #     { id: "3", label: "Disco Diffusion", position: { x: 400, y: 100 } },
    #     { id: "4", label: "Superres", position: { x: 400, y: 200 } },
    #     { id: "e1-2", source: "1", target: "2", animated: true },
    #     { id: "e1-3", source: "1", target: "3" },
    #     { id: "e1-3", source: "3", target: "4" },
    #     { id: "e1-4", source: "4", target: "5" },
    #   ] as Elements,
      