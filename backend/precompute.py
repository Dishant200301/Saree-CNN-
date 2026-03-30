"""
Precompute MobileNet feature vectors for all images in the dataset folder.
Saves (vectors, paths) to vectors.pkl.
"""

import os
import pickle
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "vectors.pkl")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def load_model():
    """Load MobileNetV2 pretrained model for feature extraction."""
    print("Loading MobileNetV2 model...")
    model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
    print("Model loaded successfully!")
    return model


def extract_features(model, image_path):
    """Extract feature vector from a single image."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    arr = img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    features = model.predict(arr, verbose=0)
    return features.flatten()


def main():
    if not os.path.isdir(DATASET_DIR):
        print(f"ERROR: Dataset directory not found: {DATASET_DIR}")
        print("Run generate_demo_dataset.py first, or place your saree images there.")
        return

    # Collect image paths
    image_paths = []
    for fname in sorted(os.listdir(DATASET_DIR)):
        ext = os.path.splitext(fname)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            image_paths.append(os.path.join(DATASET_DIR, fname))

    if not image_paths:
        print("No images found in dataset directory!")
        return

    print(f"Found {len(image_paths)} images in {DATASET_DIR}")

    model = load_model()

    vectors = []
    valid_paths = []

    for i, path in enumerate(image_paths):
        try:
            features = extract_features(model, path)
            vectors.append(features)
            # Store relative path from dataset dir
            valid_paths.append(os.path.basename(path))
            print(f"  [{i + 1}/{len(image_paths)}] Processed: {os.path.basename(path)}")
        except Exception as e:
            print(f"  [{i + 1}/{len(image_paths)}] FAILED: {os.path.basename(path)} — {e}")

    vectors = np.array(vectors)

    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump((vectors, valid_paths), f)

    print(f"\nDone! Saved {len(valid_paths)} vectors to {OUTPUT_FILE}")
    print(f"Vector shape: {vectors.shape}")


if __name__ == "__main__":
    main()
