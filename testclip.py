import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

image = preprocess(Image.open("test.jpg")).unsqueeze(0).to(device)
text = clip.tokenize(["black wallet"]).to(device)

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)

similarity = torch.cosine_similarity(image_features, text_features)
print("CLIP similarity score:", similarity.item())
