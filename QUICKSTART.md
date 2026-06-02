# 🚀 Quick Start Guide

Follow these steps to get the Oral Cancer Detection System up and running.

## Step 1: Train the Model

```bash
# Navigate to the project directory
cd "path\to\ui"

# Install Python dependencies
pip install -r requirements.txt

# Train the model (this will take 15-30 minutes)
python train_model.py
```

**Expected Output:**

- `models/oral_cancer_model.h5` (trained model)
- `models/model_info.json` (model info)

## Step 2: Start the Backend API

```bash
# In the same directory
python app.py
```

**Expected Output:**

```
Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is ready at: `http://localhost:8000`

## Step 3: Start the Frontend

**Open a new terminal/PowerShell window:**

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start React development server
npm start
```

**Expected Output:**

```
Compiled successfully!
You can now view oral-cancer-detection in the browser.
```

✅ Frontend is ready at: `http://localhost:3000`

## Step 4: Use the Application

1. Open browser to `http://localhost:3000`
2. Click "Choose Image" and select an oral cavity image
3. Click "Analyze Image"
4. View results and confidence score

## ⏰ Timeline

| Step                    | Duration  | Notes                   |
| ----------------------- | --------- | ----------------------- |
| Dependency Installation | 5-10 min  | One-time                |
| Model Training          | 15-30 min | Depends on dataset size |
| Backend Start           | Instant   | Loads trained model     |
| Frontend Install        | 3-5 min   | One-time                |
| Frontend Start          | Instant   | Hot reload enabled      |

## 🎯 What Each Component Does

### Backend (app.py)

- Loads trained model
- Validates images (checks if it's an oral cavity image)
- Runs predictions
- Organizes uploaded images in folders

### Model Training (train_model.py)

- Loads images from `dataset/cancer` and `dataset/non_cancer`
- Trains CNN model
- Saves model for backend to use

### Frontend (React)

- Beautiful UI for users
- Upload and preview images
- Shows prediction results
- Displays error messages

## 📁 Folder Structure After Setup

```
ui/
├── dataset/
│   ├── cancer/           # Your training images
│   └── non_cancer/       # Your training images
├── models/               # ✅ Created after training
│   ├── oral_cancer_model.h5
│   └── model_info.json
├── uploaded_images/      # ✅ Created after first prediction
│   ├── cancer/           # Positive predictions saved here
│   └── non_cancer/       # Negative predictions saved here
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
├── app.py
├── train_model.py
└── requirements.txt
```

## 🔧 Troubleshooting Quick Fixes

### "Model not found" Error

```bash
# Make sure you ran training first
python train_model.py
```

### "Port 8000 already in use"

```bash
# Change port in app.py or kill existing process
# Or use a different port: uvicorn app:app --port 8001
```

### "Frontend can't connect to backend"

- ✅ Make sure backend is running on port 8000
- ✅ Check browser console (F12) for errors
- ✅ Verify firewall isn't blocking connections

### "ImportError: No module named 'tensorflow'"

```bash
pip install -r requirements.txt
```

## 📱 What to Upload

### ✅ Good Images

- Clear oral cavity images
- High quality, well-lit
- Unobstructed views

### ❌ Bad Images (Will Be Rejected)

- Animals, birds, insects
- Persons/faces
- Everyday objects
- Blurry or low quality
- File size > 10MB

## 💡 Tips

1. **Keep Terminals Open**
   - Keep backend terminal running while using the app
   - Keep frontend terminal running for hot reload

2. **First Run Patience**
   - Model training takes time (first run only)
   - Backend loads model on startup
   - Be patient during image prediction (5-10 seconds)

3. **Better Results**
   - Use high-quality images
   - Good lighting for clear oral cavity view
   - Multiple angles for validation

## 🎓 Understanding Results

**Example Result:**

```
Prediction: cancer
Confidence: 87.45%
Message: Oral cancer detected
```

This means:

- The model thinks this IS an oral cavity with cancer
- It's 87.45% confident
- The image was saved to `uploaded_images/cancer/`

## 📊 Monitor Backend

Visit `http://localhost:8000/docs` to see:

- All API endpoints
- Test predictions directly
- View request/response formats

## ✨ Next Steps

1. ✅ Train your model
2. ✅ Start backend
3. ✅ Start frontend
4. ✅ Upload and test images
5. 📊 Analyze results
6. 🚀 Deploy when ready

---

**Questions?** Check the main README.md for detailed documentation.
