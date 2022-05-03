
from genericpath import exists
import json
import os
from types import SimpleNamespace
import dill
# from flask import jsonify
# from modules.generators.generator_disco.generator import GeneratorDisco
# from modules.generators.generator_ld.generator import GeneratorLatentDiffusion
from datetime import date

class Project:
    
    id = 0
    title = ""
    created = ""
    
    generators = None
    generators_json = None
        
    def load_data(self):
        self.generators = []
        self.title = ""
        if exists(self.project_dir()):
            with open(self.project_dir() + "/data.json") as json_file:
                data = json.load(json_file)
#                 data = json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))
                
                # print(data)
                self.title = data.title
                self.created = data.created
                self.generators = data.generators
                
                
            # file_data = dill.load(open(self.project_dir() + "/data.obj", "rb"))
            # file_data = json.loads(open(self.project_dir() + "/data.obj", "rb"))
            # self.title = file_data.title
            # self.created = file_data.created
            # self.chain = file_data.chain
            
            # generator_data = dill.load(open(self.project_dir() + "/generators.obj", "rb"))
            # if generator_data != None:
            #     self.generators = generator_data
            #     for name in filter(lambda x: len(x.get("label")>0),self.generators):
            #         generator = self.fetch_by_name(name)
            #         generator.settings = dill.load(open(self.project_path + "/generators/" + str.lower(name).replace(" ","_")) + "settings.json" , "rb")
            #         #json.loads(generator_data.json)
        else:
            self.created = str(date.today())          
              
    def save(self):
        # self.project_path = 
        if not exists(self.project_dir()): os.makedirs(self.project_dir())
        
        updated = Project(self.id)
        updated.title = self.title
        updated.generators = self.generators
        updated.created = self.created
        print("Saving Updated",updated.generators)
        
        
        jsonStr = json.dumps(updated.__dict__, default=lambda obj: obj.__dict__)
        with open(updated.project_dir() + "/data.json", "w") as outfile:
            outfile.write(jsonStr)
    

    def project_dir(self):
        root_path = os.getcwd()
        return root_path + "/static/data/projects/" + str(self.id)
    
    
    def __init__(self,id):
        self.id = id
        self.generators = []
    