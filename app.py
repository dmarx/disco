
import gc
import requests, sys, os

import torch

from flask import Flask, flash, jsonify, request, redirect, url_for, render_template,make_response,send_file,Response
from werkzeug.utils import secure_filename
from twilio.twiml.messaging_response import MessagingResponse, Message, Redirect, Body
from twilio.rest import Client 

from modules.manager.chain.chain import Chain
from modules.manager.projects.api import api

from random import randint, seed

UPLOAD_FOLDER = 'static/uploads/'

os.system("export TOKENIZERS_PARALLELISM=false")

app = Flask(__name__)

app.secret_key = "1923493493"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['mp4', 'mp3', 'wav','.mov'])

chain = None

@app.route('/make/<prompt>', methods=['GET', 'POST'])
def make(prompt):
    filename = chain.run_chain(prompt)
    return send_file("static/output/" + filename, mimetype='image/png')

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
   
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

    response_string = str(resp)
    print ("response", response_string)
    # response = MessagingResponse()
    # message = Message()
    # message.body('Hello World!')
    # response.append(message)
    # # return make_response(str(response))

    response = make_response(response_string)
    response.headers["Content-Type"] = "text/xml"
    return response



@app.route('/fetch_projects', methods=['POST'])
def fetch_projects():
    project_names = api.fetch_all()
    projects=[]
    for project_name in project_names:
        project = api.fetch_project(project_name)
        projects.append(project)
    return jsonify(projects)


def load_chain():
    global chain
    chain = Chain()
    # global generator_ld
    # if (generator_disco==None): generator_disco = GeneratorDisco()
    # if (generator_ld==None): generator_ld =  GeneratorLatentDiffusion()
    
if __name__ == '__main__':
    print("running")
    load_chain()
    app.run(debug=False,host = "0.0.0.0")
