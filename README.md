Flask must be kicked off using:
flask run --host=0.0.0.0

To avoid CORS issue.`

"console": "integratedTerminal",
"justMyCode": true,
"args" :  ["run" ,"--host=0.0.0.0"] 

INSTALL

pip install 
piq install ftfy 
pip install ipywidgets 
pip install lpips 
pip install pytorch_lit 
pip install pandas 
pip install timm 
pip install pytorch-lightning 
pip install einops 
pip install omegaconf
dll


cpythn install CMD

#Pytorch3d
git clone https://github.com/facebookresearch/pytorch3d.git
cd pytorch3d 
python3 setup.py install


#Glid-3-xl
git clone https://github.com/Jack000/glid-3-xl
rename this folder to underscores
cd glid-3-xl
pip install -e .


# ngrok - to serve from a vm
download ngrok binary to project root
chmod 0777 ngrok
./ngrok config add-authtoken <get new auth token from ngrok site>
ngrok http 5000 --host-header="localhost:5000"
then (from a different process/terminal) flask run
