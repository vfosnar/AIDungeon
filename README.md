# AIDungeon2
Modified and anaconda-compatible version of AIDungeon.
Clone of [this](https://github.com/Latitude-Archives/AIDungeon).
# Added features
- Windows compatible install
- Disabled uploading, rating
- Added argument parser for tuning GPT2
- Loads game from local storage by default
- Uses "save name" instead of random uuid (but game will now not save on Ctrl-C)
- Added aliases to /quit
- Reworked whole UI
# Installation
```bash
git clone https://github.com/vfosnar/AIDungeon.git
cd AIDungeon/

conda create -n AID python=3.7.9 tensorflow-gpu=1.15
conda activate AID

pip install -r "requirements.txt"
```
Then download the model using [torrent](/model_v5.torrent.zip), then put the files in generator/gpt2/models/model_v5/
# Running
```bash
conda activate AID
python play.py
```
This repository should now work on Windows too.
