import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_image_embedding(path):
    image = preprocess(Image.open(path)).unsqueeze(0).to(device)
    with torch.no_grad():
        return model.encode_image(image).cpu().numpy()

def get_text_embedding(text):
    tokens = clip.tokenize([text]).to(device)
    with torch.no_grad():
        return model.encode_text(tokens).cpu().numpy()
