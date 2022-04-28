
from datetime import datetime
import os
from random import seed
from random import randint

from modules.manager.projects.project import Project

class Api:

    def fetch_all():
        
        
        root_path = os.getcwd()
        projects_path = root_path + "/static/data/projects"
        results = []
        
        try: lst = os.listdir(projects_path)
        except OSError:
            pass #ignore errors
        else:
            for id in lst:
                fn = os.path.join(projects_path, id)
                if os.path.isdir(fn):
                    results.append(id)
                    
                     
        projects=[]
        for id in results:
            project = Project(id)
            project.load_data()
            projects.append(project)
            
        return projects
    
    def fetch(id):
        project = Project(id)
        project.load_data()
        return project

    def add():
        id = str(randint(0,1000000))
        item = Project(id )
        item.title = "New Project"
        item.created = str(datetime.now())
        item.generators= []
        item.save()
        return item
    
    def save(project):
        project.save()
        #item = Project(self.id)
        #item.save()
        return project
    
    def delete(id):
        item = Project(id)
        os.rmdir(item.dir())
        return True

    # @staticmethod
    # def __init__(self):
    #     seed(1)
    #     #self.load_cuda()
        
        
        
        