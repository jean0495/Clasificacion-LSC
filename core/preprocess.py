import cv2
import torch
import numpy as np

IMG_SIZE = 64


def preprocesar_frame(frame_rgb: np.ndarray) -> torch.Tensor:
    """
    Recibe un recorte RGB (numpy uint8) y retorna un tensor
    normalizado listo para el modelo: shape (1, 3, 64, 64).
    """
    img = cv2.resize(frame_rgb, (IMG_SIZE, IMG_SIZE))
    img = img.astype(np.float32) / 255.0

    # Normalización ImageNet
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std  = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img = (img - mean) / std

    # HWC -> CHW -> batch
    tensor = torch.from_numpy(img.transpose(2, 0, 1)).unsqueeze(0)
    return tensor