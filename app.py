
import json
import os
import time
from flask import Flask, jsonify, request,make_response,send_file,Response
from flask_cors import CORS, cross_origin
import pandas as pd
from twilio.twiml.messaging_response import MessagingResponse
from modules.manager.chain.chain import Chain
from modules.manager.projects.api import Api
# from modules.manager.projects.api import api
import asyncio
import async_timeout
import aiohttp

import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
import shlex

# from celery import Celery

# from job import run

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['mp4', 'mp3', 'wav','.mov'])

apiURL = "http://localhost:5000"
chain = None

os.system("export TOKENIZERS_PARALLELISM=false")

from flask_cors import CORS

app = Flask(__name__)
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

@asyncio.coroutine
def run_base(id):
    global chain 
    project =Api.fetch(id)
    #prompt = "A scenic view underwater of large sea monsters and volumetric light, by David Noton and Asher Brown Durand, matte painting trending on artstation HQ."
    if chain == None: chain = Chain()
    chain.output = ""
    filename = chain.run_project(project)
    
@asyncio.coroutine
async def run_project(id):
    global proc
    # proc = yield from asyncio.create_subprocess_exec(
    #     "python", 'job.py', "--id " + str(id), # python --help | grep '\-u'
    #     stdin=asyncio.subprocess.PIPE,
    #     stdout=asyncio.subprocess.PIPE)
    
    proc = asyncio.create_task(run_base(id))
    await proc

    # try:
    #     while True:
    #         line = (yield from proc.stdout.readline()).decode()
    #         # print((yield from proc.stdout.readline()).decode())
    #         print(line)
    #         output += line + "<br />"
    #         # note what sign of new line is required
    #         #proc.stdin.write(b'test\n')
    #         drain = proc.stdin.drain()
    #         if drain != ():
    #             yield from drain
    # except ConnectionResetError:
    #     pass
    
    # print("fin open")
    proc = None
        

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


@app.route('/api/task/update', methods=['POST'])
@cross_origin()
def api_task_update():
    global proc
    global session,stdout,stderr
   
    res =""
    if proc!=None:
        res = chain.output #.replace("\\n","<br />") + "_" +  str(proc!=None)
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

