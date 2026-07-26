import torch
import json
import numpy as np
import joblib
from transformers import AutoTokenizer, AutoModel

# load bert
tokenizer = AutoTokenizer.from_pretrained("bert")
bert = AutoModel.from_pretrained("bert").eval()

# load models
ae = torch.load("artifacts/ae.pt", map_location="cpu")
classifier = torch.load("artifacts/classifier.pt", map_location="cpu")
calibrator = joblib.load("artifacts/calibrator.pkl")
gmm = joblib.load("artifacts/gmm.pkl")

with open("artifacts/thresholds.json") as f:
    thresholds = json.load(f)

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        out = bert(**inputs)
        cls = out.last_hidden_state[:, 0, :]

        _, z = ae(cls)
        logits = classifier(z)

    probs = torch.softmax(logits, dim=1).numpy()
    probs = calibrator.transform(probs)

    conf = probs.max()
    ood_score = gmm.score_samples(z.numpy())[0]

    if ood_score < thresholds["tau_ood"]:
        decision = "Ragu (OOD)"
    elif conf < thresholds["tau_conf"]:
        decision = "Ragu"
    elif probs.argmax() == 0:
        decision = "Hoaks"
    else:
        decision = "Valid"

    return {
        "p_hoaks": float(probs[0][0]),
        "p_valid": float(probs[0][1]),
        "confidence": float(conf),
        "ood_score": float(ood_score),
        "decision": decision
    }
