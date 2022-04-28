
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

# asyncio.set_event_loop(asyncio.SelectorEventLoop())
# loop = asyncio.new_event_loop()


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


async def fetch(url):
    async with aiohttp.ClientSession() as session, async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()
        
def fight(responses):
    return "Why can't we all just get along?"


session = None
stdout, stderr = None, None
line = ""

# Configure the redis server
# app.config['CELERY_BROKER_URL'] =  os.environ.get("CELERY_BROKER_URL")  #'amqp://imran:fish@localhost/imran_host'
# app.config["CELERY_BACKEND_URL"] = os.environ.get("CELERY_BACKEND_URL")   #'amqp://imran:fish@localhost/imran_host'
# app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")


# # create a Celery object
# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config["CELERY_BACKEND_URL"],
#         broker=app.config["CELERY_BROKER_URL"],
#     )
#     celery.conf.update(app.config)

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery


# # celery = make_celery(app)
# # run = celery.task(run)


# def get_shell_script_output_using_communicate():
#     global session,stdout,stderr
    
#     if (session==None):
#         command = shlex.split("python cli_test.py")
#         session = Popen(command, stdout=PIPE, stderr=PIPE)
#     # stdout, stderr = session.communicate()
#     # if stderr:
#     #     raise Exception("Error "+str(stderr))
#     # return stdout.decode('utf-8')
#         while True:
#             line = session.stdout.readline().rstrip()
#             if not line:
#                 break
#             yield line

# def get_shell_script_output_using_check_output():
#     global session,stdout,stderr
   
#     #command = shlex.split("python cli_test.py")
#     #stdout = check_output(command).decode('utf-8')
#     return line
# def run_job():
#     global session,stdout,stderr
    
#     if (session==None):
#         command = shlex.split("python cli_test.py")
#         session = Popen(command, stdout=PIPE, stderr=PIPE)
#         stdout, stderr = session.communicate()
#         if stderr:
#             raise Exception("Error "+str(stderr))
#         return stdout.decode('utf-8')
    
#async def start(self):
#     if self.is_active:
#         print(f"[Cluster {self.id}] Already active.")
#         return
#     self.started_at = time.time()
#     self._process = await asyncio.create_subprocess_shell(
#         self.command,
#         stdin=asyncio.subprocess.DEVNULL,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE,
#         preexec_fn=os.setsid,
#         limit=1024 * 256,
#     )
#     self.status = "running"
#     self.started_at = time.time()
#     print(f"[Cluster {self.id}] The cluster is starting.")
#     await asyncio.wait([self.read_stream(self._process.stdout), self.read_stream(self._process.stderr)])
#     return self 

# @app.route('/api/run', methods=['GET'])
# @cross_origin()
# def project_run():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     responses = loop.run_until_complete(asyncio.gather(
#         run_job()
#         # fetch("https://google.com/"),
#         # fetch("https://bing.com/"),
#         # fetch("https://duckduckgo.com"),
#         # fetch("http://www.dogpile.com"),
#     ))

#     # do something with the results
#     return "Finished"
#     # return Response({}, status=200, mimetype='application/json')
    # return session.stdout.decode('utf-8')

output = ""
proc = None

@asyncio.coroutine
def run_project(id):
    global output, proc
    proc = yield from asyncio.create_subprocess_exec(
        "python", 'job.py', str(id), # python --help | grep '\-u'
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE)
    
    try:
        while True:
            line = (yield from proc.stdout.readline()).decode()
            # print((yield from proc.stdout.readline()).decode())
            print(line)
            output += line + "\n"
            # note what sign of new line is required
            #proc.stdin.write(b'test\n')
            drain = proc.stdin.drain()
            if drain != ():
                yield from drain
    except ConnectionResetError:
        pass
    
    print("fin open")
    proc = None
        


@app.route('/api/task/start/<int:id>', methods=['POST'])
@cross_origin()
def api_task_start(id):
    global proc
    
    if (proc==None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        output = ""
        # responses = loop.run_until_complete(asyncio.gather(
        responses = loop.run_until_complete(run_project(id))
        #     run_job()
        #     # fetch("https://google.com/"),
        #     # fetch("https://bing.com/"),
        #     # fetch("https://duckduckgo.com"),
        #     # fetch("http://www.dogpile.com"),
        # )

        # do something with the results
        return "Finished"
        # return Response({}, status=200, mimetype='application/json')

    return "Busy"


@app.route('/api/task/update', methods=['POST'])
@cross_origin()
def api_task_update():
    global output,proc
    global session,stdout,stderr
   
    res = output.replace("\\n","<br />") + "_" +  str(proc!=None)
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
    
    # json.dumps(project, default=lambda obj: obj.__dict__)
    # return json.dumps(, default=lambda obj: obj.__dict__)
    # return jsonify(project)
    # return jso
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


# def flat_dict(data: dict, prefix=''):
#     result = dict()
#     for key in data:
#         if len(prefix):
#             field = prefix + '_' + key
#         else:
#             field = key
#         if isinstance(data[key], dict):
#             result.update(
#                 flat_dict(data[key], key)
#             )
#         else:
#             result[field] = data[key]
#     return result
    
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

