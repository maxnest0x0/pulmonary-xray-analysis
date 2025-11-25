import torch
import torch.nn as nn
import torchxrayvision as xrv
import torch.nn.functional as F
from PIL import Image

from cam_and_viz import compute_gradcam, show_imgs, resize_cam
from image_transfroms import val_transform  
from hooks import ActivationHook, GradientHook

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLASS_NAMES = ["BACTERIA","NORMAL","VIRUS"]


def load_trained_model(weights_path: str = "best_model.pth",
                       device: torch.device = DEVICE):
    """
    Создаёт такую же архитектуру CheXNet, как при обучении, и загружает веса.
    """
    model = xrv.models.DenseNet(weights="densenet121-res224-chex")

    in_feats = model.classifier.in_features
    model.classifier = nn.Linear(in_feats, len(CLASS_NAMES))

    model.op_threshs = None
    model.pathologies = CLASS_NAMES

    state_dict = torch.load(weights_path, map_location=device)
    model.load_state_dict(state_dict)

    model.to(device)
    model.eval()
    return model


def prepare_model_for_viz_and_predict(weights_path: str = "best_model.pth",
                          device: torch.device = DEVICE):
    """
    Загружает модель и вешает forward-хуки на выбранный слой.
    """
    model = load_trained_model(weights_path, device)

    hooks = {
        "denseblock4": ActivationHook(model.features.denseblock4),
        "denseblock4_grad": GradientHook(model.features.denseblock4)
    }

    return model, hooks


def run_model_with_features(image_path: str,
                                model,
                                hooks: dict,
                                device: torch.device = DEVICE):

    img = Image.open(image_path).convert("L")
    tensor = val_transform(img)
    tensor = tensor.unsqueeze(0).to(device)       
    
    model.zero_grad()

    logits = model(tensor)              
    probs = F.softmax(logits, dim=1)

    pred_idx = int(probs.argmax())
    pred_class = CLASS_NAMES[pred_idx]

    if pred_idx != 1:
        score = logits[0, pred_idx]
        score.backward()

        feature_maps = hooks["denseblock4"].output
        gradients    = hooks["denseblock4_grad"].grad

        cam = compute_gradcam(feature_maps, gradients)

        H, W = img.height, img.width
        cam_resized = resize_cam(cam, target_size=(H, W))
        show_imgs(image_path, cam_resized, pred_class)
    return pred_class

