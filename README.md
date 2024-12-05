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