import json
import torch
import numpy as np

from pathlib import Path

from core.arquitectura import CNNRegularizada
from core.preprocess import preprocesar_frame


def cargar_predictor():

    config = json.loads(
        Path("model_config.json").read_text(
            encoding="utf-8"
        )
    )

    model = CNNRegularizada(
        num_classes=config["num_classes"]
    )

    model.load_state_dict(
        torch.load(
            "modelo/model_lsc.pth",
            map_location="cpu"
        )
    )

    model.eval()

    return model, config["clases"]


def predecir(
    model,
    clases,
    frame_rgb: np.ndarray
):

    tensor = preprocesar_frame(frame_rgb)

    with torch.no_grad():

        logits = model(tensor)

        probs = torch.softmax(
            logits,
            dim=1
        )

    idx = probs.argmax(dim=1).item()

    return clases[idx].strip().lower()