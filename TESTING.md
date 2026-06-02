# 🧪 Testing Guide

How to test the Oral Cancer Detection System.

## Pre-Testing Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] Dataset in `dataset/cancer` and `dataset/non_cancer`
- [ ] All dependencies installed
- [ ] Model trained (`python train_model.py`)
- [ ] Backend can start (`python app.py`)
- [ ] Frontend can start (`npm start`)

## Testing Phases

### Phase 1: Unit Tests

#### Test Model Training

```bash
python train_model.py
```

**Expected Output**:

```
Epoch 1/20
... training progress ...
Epoch 20/20
Model saved to models/oral_cancer_model.h5
Model info saved to models/model_info.json
```

**Verify**:

- [ ] Model file created (~100-200 MB)
- [ ] Model info file created (~1 KB)
- [ ] No errors during training

#### Test Backend Loading

```python
# Create test_backend.py
import tensorflow as tf
import os

MODEL_PATH = "models/oral_cancer_model.h5"
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✓ Model loaded successfully")
    print(f"  Input shape: {model.input_shape}")
    print(f"  Output shape: {model.output_shape}")
else:
    print("✗ Model not found")
```

Run:

```bash
python test_backend.py
```

### Phase 2: API Testing

#### Start Backend

```bash
python app.py
```

#### Test Endpoints Using Browser

**Test 1: Root Endpoint**

```
GET http://localhost:8000/
```

**Expected Response**:

```json
{
  "message": "Oral Cancer Detection API",
  "version": "1.0.0",
  "endpoints": {
    "predict": "/predict",
    "status": "/status"
  }
}
```

**Test 2: Status Endpoint**

```
GET http://localhost:8000/status
```

**Expected Response**:

```json
{
  "status": "ready",
  "model_loaded": true,
  "model_info": { ... }
}
```

**Test 3: Swagger Documentation**

```
GET http://localhost:8000/docs
```

Should open interactive API documentation.

#### Test Prediction with Real Image

**Using Python Requests**:

```python
import requests
from pathlib import Path

# Test with real image
image_path = "path/to/test/image.jpg"

with open(image_path, "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/predict", files=files)

print(response.json())
```

**Expected Response**:

```json
{
  "success": true,
  "prediction": "cancer" or "non_cancer",
  "confidence": 87.45,
  "message": "Oral cancer detected" or "Oral cancer not detected",
  "raw_score": 0.8745,
  "saved_location": "uploaded_images/cancer/image.jpg"
}
```

#### Test Image Validation

```python
# Test with non-oral image (animal)
with open("animal.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/validate-image", files=files)

print(response.json())
```

**Expected Response**:

```json
{
  "valid": false,
  "message": "Image does not appear to be an oral cavity image",
  "image_size": [1920, 1080]
}
```

### Phase 3: Frontend Testing

#### Test React App Loading

1. Start frontend: `npm start`
2. Browser should open `http://localhost:3000`
3. Verify no console errors (F12 → Console)
4. Check API status indicator

**Tests**:

- [ ] Page loads without errors
- [ ] API status shows "ready" (green)
- [ ] All buttons visible
- [ ] Instructions displayed

#### Test File Upload

1. Click "Choose Image"
2. Select a valid image file
3. Preview should appear
4. Filename should display

**Verify**:

- [ ] File input opens dialog
- [ ] Preview image displays
- [ ] Filename shows below image
- [ ] Clear button becomes enabled

#### Test Prediction

1. Upload valid oral cavity image
2. Click "Analyze Image"
3. Wait for results (5-10 seconds)
4. Results should display

**Verify**:

- [ ] Loading indicator shows during processing
- [ ] Results display with badge
- [ ] Confidence percentage shown
- [ ] Message appropriate to result
- [ ] Image saved to correct folder

#### Test Error Handling

**Test with Non-Oral Image**:

1. Upload animal/bird/person image
2. Click "Analyze Image"

**Expected**: Error message "Image does not appear to be an oral cavity image"

**Test with Non-Image File**:

1. Try to upload text file

**Expected**: Error message "File must be an image"

**Test with Large File**:

1. Upload image > 10MB

**Expected**: Error message "File size must be less than 10MB"

### Phase 4: Integration Testing

#### Test Full Workflow

1. **Setup**: Models trained ✓
2. **Backend**: Started and ready ✓
3. **Frontend**: Running ✓
4. **Upload**: Select oral image
5. **Predict**: Get results
6. **Verify**: Image saved, results correct
7. **Clear**: Clear and test again
8. **Error**: Test with invalid image

#### Test API-Frontend Communication

```python
# Monitor network traffic
# Open browser console (F12) → Network tab
# Upload image and watch requests
```

**Expected Flow**:

1. POST /predict with image file
2. Status 200 response
3. JSON result received
4. Frontend displays results

### Phase 5: Performance Testing

#### Test Backend Response Time

```python
import requests
import time

image_path = "test_image.jpg"
times = []

for i in range(10):
    start = time.time()
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post("http://localhost:8000/predict", files=files)
    elapsed = time.time() - start
    times.append(elapsed)
    print(f"Request {i+1}: {elapsed:.2f}s")

avg_time = sum(times) / len(times)
print(f"Average response time: {avg_time:.2f}s")
print(f"Min: {min(times):.2f}s, Max: {max(times):.2f}s")
```

**Expected Performance**:

- First request: 5-15 seconds (model loading)
- Subsequent requests: 2-5 seconds
- Average: 3-7 seconds

#### Test Frontend Response Time

```javascript
// In browser console
let startTime = performance.now();
// Trigger prediction
// Check time when result appears
let endTime = performance.now();
console.log(`Total time: ${endTime - startTime}ms`);
```

**Expected**: < 1 second for UI response, < 10 seconds total

### Phase 6: Data Validation Testing

#### Test Image Preprocessing

```python
# Create test script
from PIL import Image
import numpy as np
import cv2

# Test images
test_images = [
    ("test_oral_cancer.jpg", "cancer"),
    ("test_oral_normal.jpg", "non_cancer"),
    ("test_animal.jpg", "animal - should reject"),
]

from app import is_valid_oral_cancer_image, preprocess_image

for img_path, label in test_images:
    img = Image.open(img_path).convert('RGB')
    img_array = np.array(img)

    is_valid, msg = is_valid_oral_cancer_image(img_array)
    print(f"{label}: Valid={is_valid}, Message={msg}")

    if is_valid:
        preprocessed = preprocess_image(img)
        print(f"  Shape: {preprocessed.shape}, Min: {preprocessed.min()}, Max: {preprocessed.max()}")
```

### Phase 7: Security Testing

#### Test File Upload Security

**Test 1: Malicious Filename**

- Filename: `../../etc/passwd.jpg`
- Expected: Safely handled, saved without path traversal

**Test 2: Large File Upload**

- File: > 100MB
- Expected: Rejected with size limit message

**Test 3: Non-Image File with .jpg Extension**

- File: Text file renamed to .jpg
- Expected: Rejected as invalid image

**Test 4: Concurrent Uploads**

```bash
# Use curl to test multiple uploads simultaneously
for i in {1..10}; do
  curl -F "file=@image.jpg" http://localhost:8000/predict &
done
```

Expected: All handled correctly without crashes

### Phase 8: Browser Compatibility Testing

Test on:

- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

**Verify**:

- [ ] Layout responsive
- [ ] File upload works
- [ ] Results display correctly
- [ ] No console errors

### Phase 9: Edge Case Testing

#### Test Empty Dataset

```bash
# Temporarily rename dataset
mv dataset dataset.bak
python train_model.py
```

Expected: Error message about no images found

#### Test Corrupt Model File

```bash
# Temporarily corrupt model
echo "corrupted" > models/oral_cancer_model.h5
```

Expected: Backend error on startup

#### Test Missing Model

```bash
# Temporarily delete model
rm models/oral_cancer_model.h5
python app.py
```

Expected: API starts but predict endpoint errors

#### Test Network Issues

```bash
# Test with backend stopped
# Try to upload image in frontend
```

Expected: Clear error message about backend unavailable

### Phase 10: Model Accuracy Testing

#### Manual Verification

```python
# Test known cancer images
cancer_images = [
    "dataset/cancer/image1.jpg",
    "dataset/cancer/image2.jpg",
    # ... more cancer images
]

# Test known non-cancer images
normal_images = [
    "dataset/non_cancer/image1.jpg",
    "dataset/non_cancer/image2.jpg",
    # ... more normal images
]

# Run predictions and verify accuracy
from app import model, preprocess_image
from PIL import Image

correct = 0
total = 0

for img_path in cancer_images:
    img = Image.open(img_path).convert('RGB')
    preprocessed = preprocess_image(img)
    prediction = model.predict(np.expand_dims(preprocessed, 0))
    predicted = prediction[0][0] > 0.5  # True = cancer

    if predicted:
        correct += 1
    total += 1
    print(f"Cancer image: Predicted={'Cancer' if predicted else 'Normal'}, Score={prediction[0][0]:.2%}")

accuracy = correct / total
print(f"Accuracy on cancer images: {accuracy:.1%}")
```

## Testing Tools

### API Testing Tools

- **Postman**: GUI for API testing
- **Insomnia**: REST client
- **curl**: Command-line tool
- **Python Requests**: Programmatic testing

### Frontend Testing Tools

- **Browser DevTools**: F12
- **React DevTools**: Browser extension
- **Network Tab**: Monitor API calls
- **Console**: Check JavaScript errors

### Performance Tools

- **Lighthouse**: Chrome DevTools
- **WebPageTest**: Online tool
- **Apache JMeter**: Load testing
- **Locust**: Load testing in Python

### Security Tools

- **OWASP ZAP**: Security scanner
- **Burp Suite**: Security testing
- **SQL Map**: SQL injection testing

## Test Report Template

```markdown
# Test Report - [Date]

## Backend Tests

- [x] Model training: PASS
- [x] API startup: PASS
- [x] Endpoints accessible: PASS
- [x] Prediction endpoint: PASS
- [x] Validation endpoint: PASS

## Frontend Tests

- [x] App loads: PASS
- [x] File upload: PASS
- [x] Image preview: PASS
- [x] Prediction display: PASS
- [x] Error handling: PASS

## Integration Tests

- [x] Full workflow: PASS
- [x] API communication: PASS
- [x] Image saving: PASS

## Performance Tests

- [x] Response time: 3-7 seconds (PASS)
- [x] Concurrent requests: PASS
- [x] Memory usage: PASS

## Security Tests

- [x] File upload validation: PASS
- [x] CORS settings: PASS
- [x] Error messages safe: PASS

## Issues Found

1. [Issue description] - [Status: Fixed/Pending]

## Approved For: [Production/Development]
```

## Continuous Testing

### Monitor These Metrics

- Average response time
- Error rate
- Prediction accuracy
- API uptime
- User feedback

### Regular Testing Schedule

- Daily: Manual smoke tests
- Weekly: Full integration tests
- Monthly: Performance tests
- Quarterly: Security audit

---

**Questions?** See README.md or DEPLOYMENT.md
