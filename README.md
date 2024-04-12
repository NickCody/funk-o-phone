# Rumple Sexyphone

Tested to work on MacOS Sonoma and Windows 11

## Installation

Version 99 of Touch Designer requires Python 3.11.x. You need to install that, and then use that installation to create the virtual environment.

```bash
brew install portaudio    # macOS only
python3 -m venv venv      # Must use Python 3.11.x
source .venv/bin/activate
pip install -r requirements.txt
```

NOTE: Every terminal you open needs to have the virtual environment activated.
      You can do this by running `source .venv/bin/activate` in the terminal.
      The other steps (creating the virtual environment and installing the requirements) only need to be done once.

NOTE: Also, touch designer's path has been appended with `.venv/lib/python3.11/site-packages`.
      On Windows, you can name .venv, just venv, it doesn't matter from Touch Designer's perspectoive.

### Windows

Additionally, on Windows, you'll want o run this to install pyaudio:

```bash  
    pip install pipwin
    pipwin install pyaudio
```

Download CUDA toolkit.
<https://docs.nvidia.com/cuda/cuda-installation-guide-linux/#conda-installation>

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Try some sample programs

```bash

source .venv/bin/activate
cd demos
python3 -m basic-capture
python3 -m utensils
python3 -m chord
python3 -m play
python3 -m roboflow
