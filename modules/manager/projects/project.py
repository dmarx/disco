
from genericpath import exists
import dill
from modules.generators.generator_disco.generator import GeneratorDisco

from modules.generators.generator_ld.generator import GeneratorLatentDiffusion

class Project:
    
    project_path = ""
    data_path = ""
    
    title = ""
    created = ""
    
    generators= None
    generators_json = None
    
    def __init__(self, project_path):
        self.project_path = project_path
        
    def load(self):
        
        self.data_path = self.project_path + "/data.obj"
        if exists(self.data_path):
            file_data = dill.load(open(self.data_path, "rb"))
            self.title = file_data.title
            self.created = file_data.created
            
            generator_data = dill.load(open(self.project_path + "/generators.obj", "rb"))
            self.generators_json = generator_data.json
            
            
            self.generators = []
            for name in self.generators.items.filter(lambda x: len(x.get("label"))>0):
               generator = self.fetch_by_name(name)
               generator.settings = dill.load(open(self.project_path + "/generators/" + str.lower(name).replace(" ","_")) + "settings.json" , "rb")
                #json.loads(generator_data.json)
                       
        # else:
            # data_obj = AudioData(tempo,beats,onsets_hfc,downbeat_times)
            # s =json.dumps(data_obj, indent=4, cls=AudioDataEncoder)
            # pickle.dump(s, file = open(file, "wb"))


    # def get(self):
    #     return {}

    def fetch_by_name(name):
        if name == "Latent Diffusion":
            return GeneratorLatentDiffusion(None)
        if name == "Disco Diffusion":
            return GeneratorDisco(None)
        
        return None
    
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
      