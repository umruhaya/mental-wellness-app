import os
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from services.audio_prediction import predict_audio_for_emotions
from services.facial_prediction import predict_face_for_emotions
from services.text_prediction import predict_text_for_emotions

app = FastAPI()

# Mount the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    # Render the 'index.html' template with the 'title' variable
    return templates.TemplateResponse('index.html', {"request": request, "title": "Home Page"})

@app.get("/dashboard", response_class=HTMLResponse)
async def home_page(request: Request):
    # Render the 'index.html' template with the 'title' variable
    return templates.TemplateResponse('dashboard.html', {"request": request, "title": "Dashboard"})

@app.get("/test-selection", response_class=HTMLResponse)
async def home_page(request: Request):
    # Render the 'index.html' template with the 'title' variable
    return templates.TemplateResponse('test-selection.html', {"request": request, "title": "Test Selection"})

# Sample prediction function (to be replaced with actual logic)
def predict_audio(file_path: str):
    # Dummy prediction logic for illustrative purposes
    return [
        {"label": "Happy", "score": 0.12},
        {"label": "Angry", "score": 0.88},
        {"label": "Neutral", "score": 0.0000018},
    ]

# GET endpoint to render the HTML template
@app.get("/predict/audio", response_class=HTMLResponse)
async def get_audio_form(request: Request):
    return templates.TemplateResponse("predict-audio.html", {"request": request, "title": "Audio Prediction"})

# POST endpoint to handle audio file upload and prediction
@app.post("/predict/audio", response_class=HTMLResponse)
async def post_audio_form(request: Request, audio_file: UploadFile = File(...)):

    print(audio_file.content_type)

    # Check file extension
    if audio_file.content_type not in ["audio/mpeg", "audio/wav", "audio/x-wav"]:
        raise HTTPException(status_code=400, detail="Invalid audio format. Only MP3 and WAV are supported.")

    # Save the uploaded file to a temporary location
    file_location = f"temp_{audio_file.filename}"
    with open(file_location, "wb") as f:
        f.write(await audio_file.read())

    # Predict the uploaded audio file
    predictions = predict_audio_for_emotions(file_location)

    # Delete the temporary file after processing
    os.remove(file_location)

    # Render the template with prediction results
    return templates.TemplateResponse("predict-audio.html", {"request": request, "title": "Audio Prediction", "predictions": predictions})

# GET endpoint to render the HTML template
@app.get("/predict/facial", response_class=HTMLResponse)
async def get_facial_form(request: Request):
    return templates.TemplateResponse("predict-facial.html", {"request": request, "title": "Facial Prediction"})

# POST endpoint to handle image file upload and prediction
@app.post("/predict/facial", response_class=HTMLResponse)
async def post_facial_form(request: Request, image_file: UploadFile = File(...)):
    print(image_file.content_type)
    # Check file extension
    if image_file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")
    
    # Save the uploaded file to a temporary location
    file_location = f"temp_{image_file.filename}"
    with open(file_location, "wb") as f:
        f.write(await image_file.read())
    
    # Predict the uploaded image file
    predictions = predict_face_for_emotions(file_location)
    
    # Delete the temporary file after processing
    os.remove(file_location)
    
    # Render the template with prediction results
    return templates.TemplateResponse("predict-facial.html", {"request": request, "title": "Facial Prediction", "predictions": predictions})

# GET endpoint to render the HTML template for text prediction
@app.get("/predict/text", response_class=HTMLResponse)
async def get_text_form(request: Request):
    return templates.TemplateResponse("predict-text.html", {"request": request, "title": "Text Prediction"})

# POST endpoint to handle text input and prediction
@app.post("/predict/text", response_class=HTMLResponse)
async def post_text_form(request: Request, text_input: str = Form(...)):
    # Process the text input and make predictions
    predictions = predict_text_for_emotions(text_input)
    
    # Render the template with prediction results
    return templates.TemplateResponse("predict-text.html", {"request": request, "title": "Text Prediction", "predictions": predictions})

# Add a custom 404 not found handler
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse("404.html", {"request": request, "title": "Page Not Found"}, status_code=404)

# Optionally, handle request validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )