# NeuroScience App For Predicting Emotional States

We predict emotional states using

- audio
- text
- image (facial component)

## Install Dependencies

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