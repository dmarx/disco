
import os
from random import seed

from modules.manager.projects.project import Project


class api:

    root_path = os.getcwd()
    projects_path = root_path + "/static/data/projects"
    
    def fetch_all(self):
        
        results = []
        
        try: lst = os.listdir(self.projects_path)
        except OSError:
            pass #ignore errors
        else:
            for name in lst:
                fn = os.path.join(self.projects_path, name)
                if os.path.isdir(fn):
                    # tree['children'].append(make_tree(fn))
                    results.append(fn)
                # else:
                    #tree['children'].append(dict(name=name))
        return results
    
    def fetch(self,name):
        item = Project.fetch_by_name(name)
        return item

    def __init__(self):
        seed(1)
        self.load_cuda()
        
        
        
        