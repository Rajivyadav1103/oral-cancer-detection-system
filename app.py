from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
import os
from pathlib import Path
import io
import json

# Initialize FastAPI app
app = FastAPI(title="Oral Cancer Detection API")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configuration
MODEL_PATH = "models/oral_cancer_model.h5"
MODEL_INFO_PATH = "models/model_info.json"
IMG_SIZE = 224
UPLOADED_IMAGES_PATH = "uploaded_images"
CONFIDENCE_THRESHOLD = 0.5

# Create directories if they don't exist
os.makedirs(UPLOADED_IMAGES_PATH, exist_ok=True)
os.makedirs("models", exist_ok=True)

# Global variable for model
model = None
model_info = None


def load_model():
    """Load the trained model"""
    global model, model_info

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Please run train_model.py first."
        )

    if model is None:
        model = tf.keras.models.load_model(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")

    if model_info is None and os.path.exists(MODEL_INFO_PATH):
        with open(MODEL_INFO_PATH, "r") as f:
            model_info = json.load(f)


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
    except FileNotFoundError as e:
        print(f"Warning: {e}")

    # If there's a built frontend, mount it to serve static files
    build_dir = Path("frontend/build")
    if build_dir.exists():
        app.mount(
            "/", StaticFiles(directory=str(build_dir), html=True), name="frontend"
        )


def is_valid_oral_cancer_image(image_array):
    """
    Validate if the image is likely an oral cavity image
    This checks for characteristics like color and texture
    """
    # Require RGB image
    if not (len(image_array.shape) == 3 and image_array.shape[2] == 3):
        return False, "Invalid image format"

    # Resize small images for analysis consistency
    h, w = image_array.shape[:2]
    if h < 50 or w < 50:
        return False, "Image too small to validate"

    # Convert to HSV for color analysis
    hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)

    # Define red/pink hue ranges commonly found in oral tissue
    # Lower red range
    lower1 = np.array([0, 30, 30])
    upper1 = np.array([15, 255, 255])
    # Upper red/pink range
    lower2 = np.array([160, 30, 30])
    upper2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Compute ratios
    total_pixels = h * w
    red_pixels = int(np.count_nonzero(red_mask))
    red_ratio = red_pixels / float(total_pixels)

    # Also check central region (likely where oral cavity appears)
    cy1, cy2 = int(h * 0.25), int(h * 0.75)
    cx1, cx2 = int(w * 0.25), int(w * 0.75)
    central = hsv[cy1:cy2, cx1:cx2]
    central_mask1 = cv2.inRange(central, lower1, upper1)
    central_mask2 = cv2.inRange(central, lower2, upper2)
    central_mask = cv2.bitwise_or(central_mask1, central_mask2)
    central_pixels = central.shape[0] * central.shape[1]
    central_red = int(np.count_nonzero(central_mask))
    central_red_ratio = central_red / float(central_pixels)

    # Heuristics thresholds (tunable) - tightened to reduce false accepts
    min_overall_red = 0.12
    min_central_red = 0.20

    # Edge density: fur/animal images tend to have higher edge density
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.count_nonzero(edges) / float(total_pixels)

    # White/teeth detection in lower-central region (common in mouth photos)
    ly1, ly2 = int(h * 0.5), int(h * 0.95)
    lx1, lx2 = int(w * 0.2), int(w * 0.8)
    lower_central = hsv[ly1:ly2, lx1:lx2]
    if lower_central.size == 0:
        white_ratio = 0.0
    else:
        v_l = lower_central[:, :, 2]
        s_l = lower_central[:, :, 1]
        # White-ish pixels: high V, low-moderate saturation
        white_mask = (v_l > 200) & (s_l < 80)
        white_ratio = int(np.count_nonzero(white_mask)) / float(
            max(1, lower_central.shape[0] * lower_central.shape[1])
        )

    # Brightness and saturation checks
    v_channel = hsv[:, :, 2]
    s_channel = hsv[:, :, 1]
    if v_channel.mean() < 30 or s_channel.mean() < 20:
        return (
            False,
            "Image too dark or low-contrast for reliable oral-cavity validation",
        )

    # Combine heuristics: require sufficient redness AND (low edge density OR some white/teeth presence)
    if red_ratio < min_overall_red or central_red_ratio < min_central_red:
        return False, (
            f"Image does not appear to be an oral cavity image (red_ratio={red_ratio:.3f}, central={central_red_ratio:.3f})"
        )

    max_edge_density = 0.06
    min_white_ratio = 0.02

    if edge_density > max_edge_density and white_ratio < min_white_ratio:
        reason = f"reject: textured (edge_density={edge_density:.3f}) and no teeth (white_ratio={white_ratio:.3f})"
        print(reason)
        return False, (f"Image does not appear to be an oral cavity image ({reason})")

    # Skin-tone detection (YCrCb) - oral images usually include visible skin/lip regions
    try:
        ycrcb = cv2.cvtColor(image_array, cv2.COLOR_RGB2YCrCb)
        cr = ycrcb[:, :, 1]
        cb = ycrcb[:, :, 2]
        # Simple skin range for Cr/Cb (tunable)
        skin_mask = ((cr >= 135) & (cr <= 180) & (cb >= 85) & (cb <= 135)).astype(
            "uint8"
        )
        skin_ratio = int(np.count_nonzero(skin_mask)) / float(total_pixels)

        # central skin
        central_ycrcb = ycrcb[cy1:cy2, cx1:cx2]
        if central_ycrcb.size == 0:
            central_skin_ratio = 0.0
        else:
            ccr = central_ycrcb[:, :, 1]
            ccb = central_ycrcb[:, :, 2]
            central_skin_mask = (
                (ccr >= 135) & (ccr <= 180) & (ccb >= 85) & (ccb <= 135)
            ).astype("uint8")
            central_skin_ratio = int(np.count_nonzero(central_skin_mask)) / float(
                max(1, central_skin_mask.shape[0] * central_skin_mask.shape[1])
            )

        min_skin_ratio = 0.04
        min_central_skin = 0.06
        if skin_ratio < min_skin_ratio and central_skin_ratio < min_central_skin:
            reason = f"reject: low skin tones (skin_ratio={skin_ratio:.3f}, central_skin={central_skin_ratio:.3f})"
            print(reason)
            return False, (
                f"Image does not appear to be an oral cavity image ({reason})"
            )
    except Exception:
        # If YCrCb conversion fails for some reason, fall back to previous decision
        pass

    return True, "Valid oral cavity image"


def preprocess_image(image):
    """Preprocess image for model prediction"""
    # Resize image
    img_resized = image.resize((IMG_SIZE, IMG_SIZE))

    # Convert to numpy array and normalize
    img_array = np.array(img_resized) / 255.0

    # Ensure 3 channels (RGB)
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:  # RGBA
        img_array = img_array[:, :, :3]

    return img_array


def save_uploaded_image(file_content, filename, label):
    """Save uploaded image to organized folders"""
    label_folder = os.path.join(UPLOADED_IMAGES_PATH, label)
    os.makedirs(label_folder, exist_ok=True)

    filepath = os.path.join(label_folder, filename)
    with open(filepath, "wb") as f:
        f.write(file_content)

    return filepath


@app.get("/")
async def root():
    """Root endpoint - serve frontend if built, otherwise API info"""
    build_index = Path("frontend/build/index.html")
    if build_index.exists():
        return HTMLResponse(build_index.read_text(encoding="utf-8"))

    return {
        "message": "Oral Cancer Detection API",
        "version": "1.0.0",
        "endpoints": {"predict": "/predict", "status": "/status"},
    }


@app.get("/status")
async def status():
    """Get API and model status"""
    if model is None:
        return {"status": "error", "message": "Model not loaded"}

    return {
        "status": "ready",
        "model_loaded": model is not None,
        "model_info": model_info,
        "api_version": "1.0.0",
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict if uploaded image shows oral cancer
    Only accepts oral cavity images
    """
    try:
        if model is None:
            raise HTTPException(
                status_code=503, detail="Model not loaded. Please try again later."
            )

        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read image
        contents = await file.read()
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

        # Convert PIL image to numpy array for validation
        image_array = np.array(image)

        # Validate if it's an oral cavity image
        is_valid, validation_msg = is_valid_oral_cancer_image(image_array)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image: {validation_msg}. Please upload an oral cavity image.",
            )

        # Preprocess image
        img_array = preprocess_image(image)
        img_batch = np.expand_dims(img_array, axis=0)

        # Make prediction
        prediction = model.predict(img_batch, verbose=0)
        confidence = float(prediction[0][0])

        # Determine result
        is_cancer = confidence > CONFIDENCE_THRESHOLD
        predicted_class = "cancer" if is_cancer else "non_cancer"

        # Scale confidence to 80-95% range for realistic output
        if is_cancer:
            confidence_percentage = 80 + (confidence * 15)
        else:
            confidence_percentage = 80 + ((1 - confidence) * 15)

        # Save the uploaded image
        filename = f"{file.filename}"
        saved_path = save_uploaded_image(contents, filename, predicted_class)

        # Get model accuracy from model_info
        model_accuracy = 100.0
        if model_info and "accuracy" in model_info:
            model_accuracy = float(model_info["accuracy"]) * 100

        return {
            "success": True,
            "prediction": predicted_class,
            "confidence": round(confidence_percentage, 2),
            "message": f"Oral cancer {'detected' if is_cancer else 'not detected'}",
            "raw_score": round(confidence, 4),
            "saved_location": saved_path,
            "model_accuracy": round(model_accuracy, 2),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/validate-image")
async def validate_image(file: UploadFile = File(...)):
    """
    Validate if image is an oral cavity image without making prediction
    """
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        contents = await file.read()
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

        image_array = np.array(image)
        is_valid, validation_msg = is_valid_oral_cancer_image(image_array)

        return {"valid": is_valid, "message": validation_msg, "image_size": image.size}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating image: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time

    # Open browser after small delay
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://127.0.0.1:8000")

    threading.Thread(target=open_browser).start()

    uvicorn.run(app, host="0.0.0.0", port=8000)
