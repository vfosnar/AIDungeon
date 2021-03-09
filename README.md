# AIDungeon2
Modified and conda-compatible version of AIDungeon.
Clone of [this](https://github.com/Latitude-Archives/AIDungeon).
# Installation
    git clone https://github.com/vfosnar/AIDungeon.git
    cd AIDungeon/
    conda create -n AID python=3.7.9 tensorflow-gpu=1.15
    conda activate AID
    pip install -r "requirements.txt"
Then download the model using torrent at model_v5.torrent.zip, then put the files in generator/gpt2/models/model_v5/
# Running
    conda activate AID
    python play.py
The original repo is meant to run on linux but this version should work on Windows too.
