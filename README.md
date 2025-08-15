# wetherstation-pi
small project for a raspberry pi as wether station
 

## Install

```bash
sudo apt install python3-pip -y
```

```bash
pip install pillow python-dotenv requests
```


## Run script on change
```bash
sudo apt install entr
```

```bash
ls app.py  | entr -r python app.py
```

## Preview / Idea
```
  1. Jan 2025 | (A) 12 °C / 40%
    12:34     |------------------
--------------| (B) 13 °C / 40%
   Outdoor    |------------------
  11°C / 50%  | (C) 14 °C / 40%
```