echo "Installing imsearch"
pip install nmslib
pip install torch==1.5.0+cpu torchvision==0.6.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install -r requirements.txt
pip install .