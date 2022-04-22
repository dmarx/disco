
import datetime

import requests
from generator.generator import Generator

from flask import Flask, flash, request, redirect, url_for, render_template,make_response,send_file,Response
from werkzeug.utils import secure_filename
from twilio.twiml.messaging_response import MessagingResponse, Message, Redirect, Body
from twilio.rest import Client 

from random import randint, seed
from random import random

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)

app.secret_key = "1923493493"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['mp4', 'mp3', 'wav','.mov'])

gen = None

@app.route('/bot', methods=['POST'])
def bot():
    #add webhook logic here and return a response
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        print("quote",quote)
        msg.body(quote)
        responded = True
    # if 'cat' in incoming_msg:
    #     # return a cat pic
    #     msg.media('https://cataas.com/cat')
    #     responded = True

    if 'make' in incoming_msg:
        #print("making")
        #np.random.seed(seed)
        #random.seed(1000)
        input_seed = "" #str(100)
        prefix = str(randint(0,1000000))#--steps 50
        prompt = incoming_msg.replace("make ","")
        #print("making", prompt,prefix,input_seed)
        path_to_image = gen.do_run(prompt,prefix,input_seed)
        #print("finished", prompt,prefix,input_seed)
        msg.body(prompt)
        msg.media("https://ce1c-86-170-32-104.eu.ngrok.io/static/output/" + path_to_image)
        responded = True
        print ("constructed message")
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')

    #msg.body('this is the response text')
    #return make_response(str(resp))

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

@app.route('/makefast/<prompt>', methods=['GET', 'POST'])
def makefast(prompt):

    seed(1)
    input_seed = str(100)
    prefix = str(randint(0,1000000))#--steps 50
    filename = gen.do_run(prompt,prefix,input_seed)
    
    # filename = run_gen(prompt)
    #os.system("python glid-3-xl/sample.py --model_path glid-3-xl/finetune.pt --kl_path glid-3-xl/kl-f8.pt --bert_path glid-3-xl/bert.pt --prefix " + prefix +" --batch_size 1 --num_batches 1 --text \"" + prompt + "\"")
    #os.system("cp output/" + prefix + "00000.png static/output")
    return send_file("static/output/" + filename, mimetype='image/png')
    #return make_response("/static/output/" + prefix + "00000.png")

def load_gen():
    global gen
    if (gen==None): gen = Generator()
    gen.init_variables()
    gen.init_run()
    gen.do_run()

if __name__ == '__main__':
    print("running")
    load_gen()
    app.run(debug=False,host = "0.0.0.0")
