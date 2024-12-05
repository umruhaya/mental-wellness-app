from speechbrain.inference.interfaces import foreign_class

_classifier = foreign_class(
    source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
    # not sure why would need this, See Example at https://huggingface.co/speechbrain/emotion-recognition-wav2vec2-IEMOCAP/blob/main/custom_interface.py
    pymodule_file="custom_interface.py", 
    classname="CustomEncoderWav2vec2Classifier"
)

def predict_audio_for_emotions(audio_file_path: str):
    out_prob, score, index, text_lab = _classifier.classify_file(audio_file_path)

    # out_prob is of the format tensor([[p1, p2, p3, p4]])

    probabilities = out_prob[0]

    print(out_prob)

    # Label Encoder Mapping can ve viewed in this file: https://huggingface.co/speechbrain/emotion-recognition-wav2vec2-IEMOCAP/blob/main/label_encoder.txt
    return [
        {"label": "Neutral", "score": str(probabilities[0].item())},    
        {"label": "Angry", "score": str(probabilities[1].item())},
        {"label": "Happy", "score": str(probabilities[2].item())},
        {"label": "Sad", "score": str(probabilities[3].item())},
    ]
