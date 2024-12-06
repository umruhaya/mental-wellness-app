import cv2
import numpy as np
from transformers import pipeline

classifier = pipeline("image-classification", model="trpakov/vit-face-expression")

def softmax(scores):
    exp_scores = np.exp(scores - np.max(scores))  # Subtract max for numerical stability
    return exp_scores / exp_scores.sum()

def predict_face_for_emotions(image_file_path: str):
    results = classifier(image_file_path)
    
    # Extract the scores from the results
    scores = np.array([result['score'] for result in results])
    
    # Normalize the scores using softmax
    normalized_scores = softmax(scores)
    
    # Update the results with normalized scores
    for i, result in enumerate(results):
        result['score'] = normalized_scores[i]
    
    print(results)
    return results