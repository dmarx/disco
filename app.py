
import json
import os
from flask import Flask, jsonify, request,send_file,Response
from flask_cors import CORS, cross_origin
from modules.manager.chain.chain import Chain
from modules.manager.projects.api import Api
from subprocess import Popen, PIPE
from subprocess import check_output
import asyncio
import sys


PROJECT_DIR=os.getcwd()
sys.path.append(f'{PROJECT_DIR}/CLIP')
sys.path.append(f'{PROJECT_DIR}/MiDaS')
sys.path.append(f'{PROJECT_DIR}/AdaBins')
sys.path.append(f'{PROJECT_DIR}/latent-diffusion')
sys.path.append(f'{PROJECT_DIR}/ResizeRight')
sys.path.append(f'{PROJECT_DIR}./pytorch3d-lite')
        
        
# from celery import Celery
# from job import run

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['mp4', 'mp3', 'wav','.mov'])

apiURL = "http://localhost:5000"
chain = None

os.system("export TOKENIZERS_PARALLELISM=false")

from flask_cors import CORS

app = Flask(__name__,
            static_url_path='', 
            static_folder='static'
            )
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

# cors = CORS(app,    resources={r"/api/*": {"origins": "*"}})
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = "1923493493"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS']='Content-Type'
app.run(debug=False,host = "0.0.0.0")

session = None
stdout, stderr = None, None
line = ""

proc = None

@app.route('/')
def serve_results():
    # Haven't used the secure way to send files yet
    return send_file( 'static/index.html')

@asyncio.coroutine
def run_base(id):
    global chain 
    project =Api.fetch(id)
    if chain == None: chain = Chain()
    chain.output = ""
    filename = chain.run_project(project)
    return filename
    
@asyncio.coroutine
def run_base_preview(id,frame):
    global chain 
    project =Api.fetch(id)
    if chain == None: chain = Chain()
    chain.output = ""
    filename = chain.run_project_preview(project,frame)
    return filename
    
@asyncio.coroutine
async def run_project(id):
    global proc
    proc = asyncio.create_task(run_base(id))
    response = await proc
    proc = None
    return response

@asyncio.coroutine
async def run_project_preview(id,frame):
    global proc
    proc = asyncio.create_task(run_base_preview(id,frame))
    response = await proc
    proc = None
    return response

@app.route('/api/task/start/<int:id>', methods=['POST'])
@cross_origin()
def api_task_start(id):
    global proc, output
    
    if (proc==None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        responses = loop.run_until_complete(run_project(id))
        return "Finished"
        # return Response({}, status=200, mimetype='application/json')

    return "Busy"


@app.route('/api/task/preview/<int:id>/<int:frame>', methods=['POST'])
@cross_origin()
def api_task_preview(id,frame):
    global proc, output
    
    if (proc==None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        responses = loop.run_until_complete(run_project_preview(id,frame))
        return responses
        # return Response({}, status=200, mimetype='application/json')

    return "Busy"


@app.route('/api/task/update', methods=['POST'])
@cross_origin()
def api_task_update():
    global proc, chain
    global session,stdout,stderr
   
    res = {
            'output':chain.output.replace("\n","<br />") if chain != None else "",
            'busy':chain.busy if chain != None else False,
            'progress':chain.progress if chain != None else 0,
            }
    
    # if proc!=None and chain != None:
    #     res = {
    #         'output':chain.output,
    #         'busy':chain.busy,
    #         'progress':chain.progress
    #         } 
        
    
    #.replace("\\n","<br />") + "_" +  str(proc!=None)
    #command = shlex.split("python cli_test.py")
    #stdout = check_output(command).decode('utf-8')
    return res

@app.route('/api/projects', methods=['POST'])
@cross_origin()
def projects_get():
    items = Api.fetch_all()
    obj = json.dumps(items, default=lambda obj: obj.__dict__)
    return Response(obj, status=200, mimetype='application/json')

@app.route('/api/project/add', methods=['POST'])
@cross_origin()
def project_add():
    project = Api.add()
    #dill.dump(project, file=open(project.project_dir, "wb"))
    obj = json.dumps(project, default=lambda obj: obj.__dict__)
    return Response(obj, status=200, mimetype='application/json')
    

@app.route('/api/project/save/<int:id>', methods=['POST'])
@cross_origin()
def project_update(id):
    project =Api.fetch(id)
    data = request.get_json()
    print(data)
    project.title = data['title']
    project.generators = data['generators']
    Api.save(project)
    # return jsonify(project)
    obj = json.dumps(project, default=lambda obj: obj.__dict__)
    return Response(obj, status=200, mimetype='application/json')
    # , default=lambda obj: obj.__dict__) #, default=lambda obj: obj.__dict__)


@app.route('/api/project/<int:id>', methods=['POST'])
@cross_origin()
def project_get(id):
    print("get project",id)
    project =Api.fetch(id)
    #Api.save(project)
    # return jsonify(project)
    obj = json.dumps(project, default=lambda obj: obj.__dict__)
    return Response(obj, status=200, mimetype='application/json')
    # , default=lambda obj: obj.__dict__) #, default=lambda obj: obj.__dict__)


@app.route('/api/project/<int:id>', methods=['DELETE'])
@cross_origin()
def project_delete(id):
    Api.delete(id)
    return jsonify(None)

def load_chain():
    global chain
    chain = Chain()
    # global generator_ld
    # if (generator_disco==None): generator_disco = GeneratorDisco()
    # if (generator_ld==None): generator_ld =  GeneratorLatentDiffusion()

if __name__ == '__main__':
    # asyncio.get_event_loop().run_forever()
    load_chain()
    print("running")


# @app.route('/make/<prompt>', methods=['GET', 'POST'])
# def make(prompt):
#     filename = chain.run_chain(prompt)
#     return send_file("static/output/" + filename, mimetype='image/png')

# @app.route('/bot', methods=['POST'])
# def bot():
#     incoming_msg = request.values.get('Body', '').lower()
#     print(incoming_msg)
#     resp = MessagingResponse()
#     msg = resp.message()
#     responded = False
   
    # if 'make' in incoming_msg:
    #     input_seed = "" #str(100)
    #     prefix = str(randint(0,1000000))#--steps 50
    #     prompt = incoming_msg.replace("make ","")
    #     #print("making", prompt,prefix,input_seed)
    #     path_to_image = gen.do_run(prompt,prefix,input_seed)
    #     #print("finished", prompt,prefix,input_seed)
    #     msg.body(prompt)
    #     msg.media("https://ce1c-86-170-32-104.eu.ngrok.io/static/output/" + path_to_image)
    #     responded = True
    #     print ("constructed message")
    # if not responded:
    #     msg.body('I only know about famous quotes and cats, sorry!')

    # response_string = str(resp)
    # print ("response", response_string)
    # # response = MessagingResponse()
    # # message = Message()
    # # message.body('Hello World!')
    # # response.append(message)
    # # # return make_response(str(response))

    # response = make_response(response_string)
    # response.headers["Content-Type"] = "text/xml"   
    # return response

