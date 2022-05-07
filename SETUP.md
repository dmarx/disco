
# first
python3 -m pip install --upgrade pip

# env
Firstly, create a venv: python3 -m venv env ... then activate the venv: source env/bin/activate
Activate or create your conda env, e.g conda activate disco

# pytorch
If you need to, setup pytorch etc for your GPU, e.g.
pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html

# pip things
pip install piq ftfy ipywidgets lpips pytorch_lit pandas timm pip pytorch-lightning einops omegaconf flask_cors dependency-injector twilio encoders dill dalle2_pytorch matplotlib opencv-python

# install libs
python install.py

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

