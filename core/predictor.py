import json
import torch
import numpy as np
from pathlib import Path
from core.arquitectura import CNNRegularizada
from core.preprocess import preprocesar_frame

def cargar_predictor():
    config = json.loads(Path("model_config.json").read_text())
    model = CNNRegularizada(num_classes=config["num_classes"])
    model.load_state_dict(torch.load("modelo/model_lsc.pth", map_location="cpu"))
    model.eval()
    return model, config["clases"]

def predecir(model, clases: list, frame_rgb: np.ndarray) -> tuple[str, float]:
    tensor = preprocesar_frame(frame_rgb)
    with torch.no_grad():
        logits = model(tensor)
        probs  = torch.softmax(logits, dim=1)
    idx       = probs.argmax().item()
    confianza = probs[0, idx].item()
    return clases[idx], round(confianza, 4)