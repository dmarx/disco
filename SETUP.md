
# first
python3 -m pip install --upgrade pip

# env
Firstly, create a venv: python3 -m venv env ... then activate the venv: source env/bin/activate
Activate or create your conda env, e.g conda activate disco

# pytorch
If you need to, setup pytorch etc for your GPU, e.g.
pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html

# pip things
pip install Cython
pip install piq ftfy ipywidgets lpips imageio imgtag stegano GPUtil
pip install pytorch_lit pandas timm pip pytorch-lightning 
pip install einops omegaconf flask_cors dependency-injector twilio encoders dill dalle2_pytorch matplotlib opencv-python kornia
pip install -U clip_client

# install libs
python install.py

# for vm such as gradient
apt-get update
apt-get upgrade
apt install libgl1-mesa-glx
pip install opencv-python

# to configure UI
npm install --global yarn
cd ui
yarn install
yarn build
cd ..

# to run api (and serve built UI)
flask run

# to run debug version of ui
yarn serve

# ngrok - to serve from a vm
download ngrok binary to project root
chmod 0777 ngrok
./ngrok config add-authtoken <get new auth token from ngrok site>
ngrok http 5000 --host-header="localhost:5000"
then (from a different process/terminal) flask run


#yarn issue
nvm install v14.7.0
nvm use --delete-prefix v14.7.0
npm install --global yarn