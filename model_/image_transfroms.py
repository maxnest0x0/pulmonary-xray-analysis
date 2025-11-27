from torchvision.transforms import transforms

val_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224)),
    transforms.Normalize(mean=[0.5],
                         std=[0.5]),
])


