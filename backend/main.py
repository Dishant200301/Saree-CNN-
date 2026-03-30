"""
Saree Image Similarity Search — FastAPI Backend
"""

import os
import io
import pickle
import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

# ─── Configuration ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
VECTORS_FILE = os.path.join(BASE_DIR, "vectors.pkl")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "bmp"}
TOP_K = 5

# ─── App Setup ─────────────────────────────────────────────────
app = FastAPI(
    title="Saree Image Similarity Search",
    description="Upload a saree image to find visually similar sarees",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve dataset images as static files
if os.path.isdir(DATASET_DIR):
    app.mount("/images", StaticFiles(directory=DATASET_DIR), name="images")

# ─── Load Model & Vectors ─────────────────────────────────────
print("Loading MobileNetV2 model...")
model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
print("Model loaded!")

# Load precomputed vectors
if os.path.isfile(VECTORS_FILE):
    with open(VECTORS_FILE, "rb") as f:
        stored_vectors, stored_paths = pickle.load(f)
    stored_vectors = np.array(stored_vectors)
    print(f"Loaded {len(stored_paths)} precomputed vectors from vectors.pkl")
else:
    stored_vectors = None
    stored_paths = []
    print("WARNING: vectors.pkl not found! Run precompute.py first.")


# ─── Helper Functions ──────────────────────────────────────────
def validate_file(filename: str) -> bool:
    """Check if uploaded file has an allowed image extension."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def extract_features(image: Image.Image) -> np.ndarray:
    """Extract feature vector from a PIL Image using MobileNetV2."""
    img = image.convert("RGB").resize((224, 224))
    arr = img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    features = model.predict(arr, verbose=0)
    return features.flatten()


def find_similar(query_vector: np.ndarray, top_k: int = TOP_K):
    """Find the top-k most similar images using cosine similarity."""
    if stored_vectors is None or len(stored_vectors) == 0:
        return []

    query = query_vector.reshape(1, -1)
    similarities = cosine_similarity(query, stored_vectors)[0]

    # Get top-k indices (sorted descending)
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "filename": stored_paths[idx],
            "image_url": f"/images/{stored_paths[idx]}",
            "similarity_score": round(float(similarities[idx]) * 100, 2),
        })
    return results


# ─── Endpoints ─────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "message": "Saree Image Similarity Search API",
        "endpoints": {
            "POST /search": "Upload an image to find similar sarees",
            "GET /health": "Health check",
        },
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "vectors_loaded": stored_vectors is not None,
        "dataset_size": len(stored_paths),
    }


@app.post("/search")
async def search_similar(file: UploadFile = File(...)):
    """
    Upload a saree image and get the top 5 most similar images.
    """
    # Validate file
    if not validate_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Check vectors are loaded
    if stored_vectors is None or len(stored_vectors) == 0:
        raise HTTPException(
            status_code=503,
            detail="Dataset vectors not loaded. Please run precompute.py first.",
        )

    try:
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Extract features
        query_vector = extract_features(image)

        # Find similar images
        results = find_similar(query_vector, TOP_K)

        return {
            "success": True,
            "query_filename": file.filename,
            "results": results,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
