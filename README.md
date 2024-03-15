# Grove of the Ancients Core Engine

Tested to work on MacOS Sonoma and Windows 11.

## Installation

```bash
brew install portaudio    # macOS only
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

NOTE: Every terminal you open needs to have the virtual environment activated. 
      You can do this by running `source .venv/bin/activate` in the terminal.
      The other steps (creating the virtual environment and installing the requirements) only need to be done once.

### Windows

Additionally, on Windows, you'll want o run this to install pyaudio:

```bash  
    pip install pipwin
    pipwin install pyaudio
```

## Try some sample programs

```bash

python3 -m main
python3 -m chord
python3 -m play
python3 -m roboflow