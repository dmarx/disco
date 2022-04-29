from modules.manager.chain.chain import Chain
from modules.manager.projects.api import Api
import sys

id = sys.argv[1].replace("--id ","")
print("Starting project run for project: " + str(id))
project =Api.fetch(id)
#prompt = "A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."
chain = Chain()
filename = chain.run_project(project)
print("Finished project run for project: " + str(project.id))
# chain.run_ld = False

