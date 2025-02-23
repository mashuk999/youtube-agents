echo 'y' | conda create --prefix /tmp/py39 python=3.9
conda activate /tmp/py39
pip install openai kokoro soundfile
sudo apt-get install espeak-ng -y