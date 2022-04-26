
import json
import os
from flask import Flask, jsonify, request,make_response,send_file,Response
from flask_cors import CORS, cross_origin
import pandas as pd
from twilio.twiml.messaging_response import MessagingResponse
from modules.manager.chain.chain import Chain
from modules.manager.projects.api import Api
# from modules.manager.projects.api import api

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

