from PIL import Image
import numpy as np
import torch

IMG_SIZE = (64, 64)

def preprocesar_frame(frame_rgb: np.ndarray) -> torch.Tensor:
    img = Image.fromarray(frame_rgb).convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0       # [0,1]
    tensor = torch.tensor(arr).permute(2, 0, 1)          # (C,H,W)
    return tensor.unsqueeze(0)                            # (1,C,H,W)