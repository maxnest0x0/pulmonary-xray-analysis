import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def compute_gradcam(feature_maps: torch.Tensor,
                    gradients: torch.Tensor):
    
    weights = gradients.mean(dim=(0, 2, 3))

    cam = (weights[None, :, None, None] * feature_maps).sum(dim=1)
    cam = cam.squeeze(0)

    cam = F.relu(cam)

    if cam.max() > 0:
        cam = cam / cam.max()

    return cam


def resize_cam(cam: torch.Tensor, target_size: tuple[int, int]):
    """
    Ресайз карты Grad-CAM до размера исходного изображения.
    """
    cam_resized = F.interpolate(
        cam.unsqueeze(0).unsqueeze(0),
        size=target_size,
        mode="bilinear",
        align_corners=False
    )[0, 0]

    return cam_resized


def show_imgs(image_path: str,
                 cam_resized: torch.Tensor,
                 pred_class: str,
                 alpha: float = 0.4):
    
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)

    cam_np = cam_resized.detach().cpu().numpy()

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(img_np, cmap="gray")
    axes[0].set_title("Исходный снимок")
    axes[0].axis("off")

    axes[1].imshow(img_np, cmap="gray")
    im = axes[1].imshow(cam_np, cmap="jet", alpha=alpha)
    axes[1].set_title(f"Grad-CAM (класс: {pred_class})")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()