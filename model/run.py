from arch_model import prepare_model_for_viz_and_predict, run_model_with_features, DEVICE

image_path = "12.jpg"

model, hooks = prepare_model_for_viz_and_predict("best_model.pth", device=DEVICE)

disease = run_model_with_features(image_path, model, hooks, device=DEVICE)

print("Предсказание:", disease)
