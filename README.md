# NeuroScience App For Predicting Emotional States

We predict emotional states using

- audio
- text
- image (facial component)

## Install Dependencies

if one server, first clone the repo using `git clone https://github.com/umruhaya/mental-wellness-app`

```bash
pip install -r requirements.txt
```

## Run Server For Development with Hot reload

```bash
uvicorn app:app --reload --reload-include="*.html" --reload-include="*.css" --reload-include="*.js"
```

## Run Server For Production

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Project Directory Structure

This document provides an overview of the directory structure for the project, which is built using FastAPI with Jinja2 for templating. The project implements various prediction services, including audio, text, and facial predictions, using state-of-the-art machine learning models.

### Root Directory

- **.gitignore**: Specifies files and directories that should be ignored by Git.
- **README.md**: Contains information about the project, including setup instructions and usage.
- **app.py**: The main application file that defines all the API endpoints using FastAPI.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **scripts/**: Contains shell scripts for various tasks.
  - **create-iac-backend.sh**: A script to create infrastructure as code backend.

### infra

This directory contains infrastructure-related files, primarily for managing cloud resources.

- **.gitignore**: Specifies files and directories within `infra` that should be ignored by Git.
- **Pulumi.default.yaml**: Default configuration for Pulumi, a tool for managing cloud infrastructure.
- **Pulumi.yaml**: Main configuration file for Pulumi.
- **index.ts**: TypeScript file for defining infrastructure resources using Pulumi.
- **package.json**: Lists Node.js dependencies and scripts for the infrastructure setup.
- **pnpm-lock.yaml**: Lock file for `pnpm`, ensuring consistent dependency versions.
- **tsconfig.json**: TypeScript configuration file.

### services

This directory contains the implementation of various prediction services.

- **__init__.py**: Marks the directory as a Python package.
- **audio_prediction/**: Contains files related to audio prediction.
  - **__init__.py**: Initializes the audio prediction module.
  - **custom_interface.py**: Custom interface for handling audio predictions.
  - **main.py**: Main logic for audio prediction using the `speechbrain/emotion-recognition-wav2vec2-IEMOCAP` model.
- **facial_prediction/**: Contains files related to facial prediction.
  - **__init__.py**: Initializes the facial prediction module.
  - **main.py**: Main logic for facial prediction using the `trpakov/vit-face-expression` model.
- **text_prediction/**: Contains files related to text prediction.
  - **__init__.py**: Initializes the text prediction module.
  - **main.py**: Main logic for text prediction using the `ayoubkirouane/BERT-Emotions-Classifier` model.

## static

This directory contains static assets such as images.

### templates

This directory contains HTML templates used by Jinja2 for rendering web pages.

- **404.html**: Template for the 404 error page.
- **dashboard.html**: Template for the user dashboard.
- **index.html**: Template for the homepage.
- **predict-audio.html**: Template for the audio prediction page.
- **predict-facial.html**: Template for the facial prediction page.
- **predict-text.html**: Template for the text prediction page.
- **test-selection.html**: Template for selecting tests.

## Infra

more details in the [Infrastructure As Code Doc](infrastructure-as-code.md)

### Setup

Make sure to have these cli installed

- pulumi
- gcloud
- node
- npm
- pnpm (installed using `npm i -g pnpm`)

```bash
# Authenticate
gcloud init

gcloud auth application-default login

pulumi login gs://mental-wellness-lums-pulumi

cd infra

pnpm i
```

### Update

Make changes to index.ts and run `pulumi up`

## Server Deployment

### Install Dependencies

server requires all of these packages

- `ffmpeg` for torchaudio backend
- `libgl1-mesa-glx libgl1-mesa-dri` for numpy
- `python3` and `pip` 

```bash
sudo apt update
sudo apt install ffmpeg libgl1-mesa-glx libgl1-mesa-dri python3 python3-pip -y
```

### Server Setup

Instead of directly running the uvicorn command, we would use `systemd` to manage the server process.

First Create a systemd config file

```bash
sudo vim /etc/systemd/system/mental-wellness.service
```

```ini
[Unit]
Description=Mental Wellness Uvicorn Daemon
After=network.target

[Service]
User=umernaeem135acc
Group=umernaeem135acc
WorkingDirectory=/home/umernaeem135acc/mental-wellness-app
ExecStart=/home/umernaeem135acc/.local/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

After creating this file, follow these steps to reload `systemd` and start the service:

```bash
# Reload systemd to recognize the new service file
sudo systemctl daemon-reload

# Start the uvicorn service
sudo systemctl start mental-wellness.service

# Enable the service to start on boot
sudo systemctl enable mental-wellness.service
```

### Server Restart For Update

Whenever you want to refresh the server, (lets say you just ran `git pull` and updated the source code) then run 

```bash
sudo systemctl restart mental-wellness.service
```

### View Server Logs

T see th logs of the server run 

```bash
journalctl -u mental-wellness.service
```