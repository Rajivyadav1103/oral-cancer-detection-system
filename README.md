# Oral Cancer Detection System

An AI-powered medical image analysis tool for detecting oral cancer from images. Uses FastAPI backend and React frontend.

## Project Structure

```
.
├── dataset/                 # Your training dataset
│   ├── cancer/             # Cancer images
│   └── non_cancer/         # Non-cancer images
├── models/                 # Trained model storage
├── uploaded_images/        # User uploaded images (organized by prediction)
├── frontend/              # React frontend application
├── app.py                # FastAPI backend
├── train_model.py        # Model training script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Features

✅ **AI-Powered Detection**: CNN model trained to detect oral cancer  
✅ **Image Validation**: Only accepts oral cavity images, rejects animals, birds, persons, etc.  
✅ **Web UI**: Beautiful React frontend for easy interaction  
✅ **Organized Storage**: Automatically saves uploaded images to folders based on predictions  
✅ **Error Handling**: Comprehensive error messages for invalid images  
✅ **Confidence Scores**: Shows prediction confidence percentage  
✅ **Medical Disclaimer**: Clear disclaimers about AI limitations

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- At least 2GB RAM for model training
- Oral cavity images dataset (cancer and non_cancer folders)

## Installation & Setup

### 1. Backend Setup

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Train the Model

Place your dataset images in the following structure:

```
dataset/
├── cancer/        # Oral cancer images
└── non_cancer/    # Non-cancer oral images
```

Then train the model:

```bash
python train_model.py
```

This will:

- Train a CNN model on your dataset
- Save the model to `models/oral_cancer_model.h5`
- Save model info to `models/model_info.json`

⏱️ Training time depends on dataset size (typically 15-30 minutes)

#### Run the Backend API

```bash
python app.py
```

The API will start at `http://localhost:8000`

### 2. Frontend Setup

#### Install Node Dependencies

```bash
cd frontend
npm install
```

#### Start the Development Server

```bash
npm start
```

The React app will open at `http://localhost:3000`

## Usage

1. **Open the Application**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000

2. **Upload an Image**
   - Click "Choose Image" button
   - Select an oral cavity image
   - Image preview will appear

3. **Analyze the Image**
   - Click "Analyze Image" button
   - Wait for the model to process (usually 5-10 seconds)
   - View results with confidence score

4. **Check Results**
   - Prediction: Cancer or Non-cancer
   - Confidence: Percentage of certainty
   - Saved Location: Where the image was stored

## API Endpoints

### GET `/`

Get API information

### GET `/status`

Check API and model status

### POST `/predict`

Make a prediction on an uploaded image

- **Input**: Image file (multipart/form-data)
- **Output**: Prediction, confidence score, and saved location

### POST `/validate-image`

Validate if image is an oral cavity image without making prediction

## Image Validation

The system validates images based on:

- **Color Analysis**: Checks for oral tissue/skin colors (reddish/pinkish tones)
- **File Type**: Ensures valid image format
- **File Size**: Maximum 10MB

**Rejected Images**:

- Animals, birds, insects
- Persons/faces
- Objects without oral characteristics
- Non-image files

## Model Architecture

The CNN model uses:

- 4 Convolutional blocks with batch normalization
- Max pooling for feature reduction
- Dropout layers (0.5) to prevent overfitting
- Dense layers with ReLU activation
- Sigmoid activation for binary classification

## File Organization

After predictions, images are automatically saved to:

```
uploaded_images/
├── cancer/         # Positive predictions
└── non_cancer/     # Negative predictions
```

## Configuration

### Backend (app.py)

- `MODEL_PATH`: Location of trained model
- `IMG_SIZE`: Image size for model (224x224)
- `CONFIDENCE_THRESHOLD`: Threshold for cancer detection (0.5)

### Frontend

- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)

## Important Notes

⚠️ **Medical Disclaimer**

- This tool is for **educational and informational purposes** only
- It is **NOT a substitute** for professional medical diagnosis
- Always consult with qualified healthcare professionals
- Never rely solely on this tool for medical decisions

## Troubleshooting

### Backend API not responding

- Ensure backend is running: `python app.py`
- Check if port 8000 is available
- Verify all dependencies are installed

### Model not found

- Run `python train_model.py` first to train the model
- Ensure `models/` directory exists

### Frontend can't connect to backend

- Check backend is running on http://localhost:8000
- Verify CORS is enabled (should be in app.py)
- Check browser console for errors

### Poor prediction accuracy

- Ensure training dataset has sufficient images
- Verify images are clear and properly labeled
- Consider training with more epochs

## Dependencies

### Python (Backend)

- fastapi: Web framework
- uvicorn: ASGI server
- tensorflow: Deep learning
- pillow: Image processing
- numpy: Numerical computing
- scikit-learn: ML utilities
- opencv-python: Computer vision
- python-multipart: File upload handling

### Node.js (Frontend)

- react: UI library
- axios: HTTP client
- react-scripts: Build tools

## Performance Tips

1. **Model Training**
   - Use GPU if available (faster training)
   - More diverse images improve accuracy
   - Higher resolution images (224x224+) work better

2. **Predictions**
   - Ensure good lighting in images
   - Clear, unobstructed oral cavity views
   - High-quality images give better results

3. **Deployment**
   - Use production-grade server (Gunicorn/uWSGI for Python)
   - Use production build for React (`npm run build`)
   - Consider using HTTPS in production

## Security Considerations

- Never share model training data
- Protect patient privacy
- Store uploaded images securely
- Use HTTPS in production
- Implement user authentication if needed
- Add rate limiting for API endpoints

## License & Attribution

Created for medical education and research purposes.

## Support

For issues or questions:

1. Check the Troubleshooting section
2. Review error messages in browser console
3. Check backend logs for API errors
4. Verify all dependencies are correctly installed

---

**Last Updated**: 2024
**Version**: 1.0.0
