import cv2
import numpy as np
from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="ayoubkirouane/BERT-Emotions-Classifier", top_k=None)

def softmax(scores):
    exp_scores = np.exp(scores - np.max(scores))  # Subtract max for numerical stability
    return exp_scores / exp_scores.sum()

def predict_text_for_emotions(image_file_path: str):
    results = classifier(image_file_path)[0]
    
    print(results)
    return results