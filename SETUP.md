
# first
python3 -m pip install --upgrade pip

sudo apt update &&   sudo apt upgrade
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
sudo apt-get install python3.9-dev

# env
apt-get install python3-venv
python3 -m venv env 
source env/bin/activate
Activate or create your conda env, e.g conda activate disco

# pytorch
If you need to, setup pytorch etc for your GPU, e.g.
# pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

# pip things
sudo pip3 install --upgrade pip
python -m pip install --upgrade pip
sudo apt install python3-pip
sudo apt install python3.9-distutils

python3 -m pip install opencv-python
pip install Cython
pip install  ftfy ipywidgets lpips imageio imgtag stegano GPUtil imgtag
pip install pytorch_lit pandas timm pip pytorch-lightning transformers
pip install einops omegaconf flask_cors twilio encoders dill  matplotlib opencv-python kornia 
pip install clip_client discord regex requests timm
pip install taming-transformers
pip install git+https://github.com/CompVis/taming-transformers

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.9
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2


# install libs
python install.py

# fix glid-3
mv ./modules/generators/generator_ld/glid_3_xl ./lib/

# Install PyTTI-Tools
pip install gdown loguru einops seaborn PyGLM ftfy regex tqdm hydra-core adjustText exrex matplotlib-label-lines
pip install --upgrade git+https://github.com/pytti-tools/AdaBins.git
pip install --upgrade git+https://github.com/pytti-tools/GMA.git
#pip install --upgrade git+https://github.com/pytti-tools/taming-transformers.git
#pip install --upgrade git+https://github.com/openai/CLIP.git
pip install --upgrade git+https://github.com/pytti-tools/pytti-core.git
python -m pytti.warmup

# install MMC for additional perceptors
git clone https://github.com/dmarx/Multi-Modal-Comparators
pip install poetry
cd Multi-Modal-Comparators
poetry build
pip install dist/mmc*.whl
python src/mmc/napm_installs/__init__.py
cd ..


# for vm such as gradient
apt-get update
apt-get upgrade
apt install libgl1-mesa-glx
pip install opencv-python

# to configure UI
sudo apt install nodejs
sudo apt-get install nodejs-dev node-gyp libssl1.0-dev
sudo apt-get install build-essential checkinstall libssl-dev
sudo apt-get install npm
sudo n stable
sudo npm install npm@latest -g 
sudo npm install --global yarn
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

# other 
