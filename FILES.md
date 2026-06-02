# 📋 Project Files Overview

Complete guide to all files in the Oral Cancer Detection System.

## Directory Structure

```
ui/
│
├── 📄 app.py                    # FastAPI backend (main file)
├── 📄 train_model.py            # Model training script
├── 📄 requirements.txt          # Python dependencies
│
├── 🎨 frontend/                 # React frontend
│   ├── public/
│   │   └── index.html           # HTML entry point
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── App.css              # Styles
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Global styles
│   ├── package.json             # Node.js dependencies
│   └── .env.local               # Environment variables
│
├── 📁 dataset/                  # Training dataset
│   ├── cancer/                  # Cancer images
│   └── non_cancer/              # Non-cancer images
│
├── 📁 models/                   # ✨ Created after training
│   ├── oral_cancer_model.h5     # Trained model
│   └── model_info.json          # Model metadata
│
├── 📁 uploaded_images/          # ✨ Created after predictions
│   ├── cancer/                  # Positive predictions
│   └── non_cancer/              # Negative predictions
│
├── 📚 Documentation
│   ├── README.md                # Full documentation
│   ├── QUICKSTART.md            # Quick setup guide
│   ├── DEPLOYMENT.md            # Production deployment
│   └── FILES.md                 # This file
│
├── 🔧 Setup Scripts
│   ├── setup.bat                # Automated setup (Windows)
│   ├── start_backend.bat        # Start backend (Windows)
│   └── start_frontend.bat       # Start frontend (Windows)
│
└── 📝 Configuration
    └── .gitignore              # Git ignore rules
```

## 📄 Core Files Explained

### Backend Files

#### `app.py` - FastAPI Backend

**Purpose**: Main backend server for model inference
**Key Functions**:

- `/predict` - Main prediction endpoint
- `/validate-image` - Validate if image is oral cavity
- `/status` - Check API and model status
- Image validation using color analysis
- Automatic file organization

**Key Features**:

- CORS enabled for React frontend
- Error handling with detailed messages
- Image validation to reject non-oral images
- Confidence scoring
- Automatic image saving

#### `train_model.py` - Model Training

**Purpose**: Train CNN model on dataset
**What it does**:

1. Loads images from `dataset/cancer` and `dataset/non_cancer`
2. Applies data augmentation
3. Trains 4-layer CNN model
4. Saves model to `models/oral_cancer_model.h5`
5. Saves metadata to `models/model_info.json`

**Training Configuration**:

- Input size: 224x224 pixels
- Batch size: 32
- Epochs: 20
- Optimizer: Adam (learning_rate=0.0001)
- Loss: Binary Crossentropy

#### `requirements.txt` - Python Dependencies

**Contains**:

- FastAPI - Web framework
- Uvicorn - ASGI server
- TensorFlow - Deep learning
- Keras - Neural networks
- OpenCV - Image processing
- NumPy - Numerical computing
- Pillow - Image manipulation

### Frontend Files

#### `frontend/src/App.js` - Main React Component

**Purpose**: Main UI component for the application
**Features**:

- File upload with preview
- Image selection with validation
- Prediction request handling
- Result display with styling
- Error message handling
- API status checking

#### `frontend/src/App.css` - Styling

**Contains**:

- Beautiful gradient design
- Responsive layout (mobile-friendly)
- Animations and transitions
- Color-coded results (green=negative, red=positive)
- Professional medical app styling

#### `frontend/src/index.js` - React Entry

**Purpose**: Root React component mounting point

#### `frontend/public/index.html` - HTML Template

**Purpose**: Base HTML file that React mounts to

#### `frontend/package.json` - Node Dependencies

**Contains**:

- React - UI library
- Axios - HTTP client
- React Scripts - Build tools

### Configuration Files

#### `.env.local` - Environment Variables

**Purpose**: Frontend configuration
**Contains**:

- Backend API URL
- Environment settings

#### `.gitignore` - Git Ignore Rules

**Purpose**: Exclude unnecessary files from version control
**Excludes**:

- `node_modules/`
- `__pycache__/`
- `models/*.h5`
- `uploaded_images/`
- `.env`

### Documentation Files

#### `README.md` - Main Documentation

**Sections**:

- Project overview
- Features list
- Installation instructions
- Usage guide
- API endpoints
- Model architecture
- Troubleshooting

#### `QUICKSTART.md` - Quick Setup Guide

**Contains**:

- Step-by-step setup (5 steps)
- Timeline for each step
- Troubleshooting quick fixes
- Tips for better results
- What to upload

#### `DEPLOYMENT.md` - Production Guide

**Sections**:

- Backend deployment options (Gunicorn, Docker)
- Frontend build and hosting
- Security setup (SSL, HTTPS)
- Performance optimization
- Monitoring and logging
- Scaling strategies
- Deployment checklist

### Setup Scripts (Windows Batch Files)

#### `setup.bat` - Automated Setup

**Does**:

1. Checks Python installation
2. Installs Python dependencies
3. Installs Node.js dependencies
4. Trains the model
5. Provides next steps

**Usage**: Double-click to run

#### `start_backend.bat` - Start Backend

**Does**:

1. Checks if model exists
2. Starts FastAPI server on port 8000

**Usage**: Double-click to run

#### `start_frontend.bat` - Start Frontend

**Does**:

1. Checks Node modules
2. Starts React dev server on port 3000

**Usage**: Double-click to run

## 🗂️ Auto-Generated Directories

### `models/` - Created After Training

**Contains**:

- `oral_cancer_model.h5` - Trained TensorFlow model (~100-200MB)
- `model_info.json` - Model metadata (input size, classes, accuracy)

### `uploaded_images/` - Created After First Prediction

**Structure**:

```
uploaded_images/
├── cancer/        # Positive predictions saved here
└── non_cancer/    # Negative predictions saved here
```

Each image is automatically organized by prediction result.

## 📊 Data Flow

```
1. User uploads image via frontend
   ↓
2. React sends image to backend API
   ↓
3. FastAPI receives and validates image
   ↓
4. Image is preprocessed (resized, normalized)
   ↓
5. TensorFlow model makes prediction
   ↓
6. Confidence score calculated
   ↓
7. Image saved to uploaded_images/[cancer|non_cancer]/
   ↓
8. Results sent back to frontend
   ↓
9. React displays results to user
```

## 🔄 Model Flow

```
Training Phase:
dataset/ → train_model.py → CNN Model → models/oral_cancer_model.h5

Inference Phase:
uploaded_image → app.py → loaded_model → prediction + confidence → result
```

## 📝 File Sizes (Approximate)

| File                 | Size       | Notes                             |
| -------------------- | ---------- | --------------------------------- |
| app.py               | 8 KB       | Backend code                      |
| train_model.py       | 4 KB       | Training code                     |
| App.js               | 6 KB       | React component                   |
| requirements.txt     | 1 KB       | Dependencies list                 |
| oral_cancer_model.h5 | 100-200 MB | Trained model (varies by dataset) |
| node_modules/        | 300-500 MB | After npm install                 |

## 🎯 Which File to Edit?

### To Change...

- **UI/Frontend** → Edit `frontend/src/App.js` and `App.css`
- **Backend Logic** → Edit `app.py`
- **Model Architecture** → Edit `train_model.py`
- **Predictions** → Edit `app.py` predict function
- **Image Validation** → Edit `is_valid_oral_cancer_image()` in `app.py`
- **Styling** → Edit `frontend/src/App.css`
- **Dependencies** → Edit `requirements.txt` (Python) or `package.json` (Node)

## 🚀 Deployment Files

When deploying to production, include:

- ✅ `app.py`
- ✅ `train_model.py`
- ✅ `requirements.txt`
- ✅ `frontend/` (entire folder)
- ✅ `models/oral_cancer_model.h5`
- ❌ `node_modules/` (regenerate with npm install)
- ❌ `.git/` (remove if using Git)

## 📦 Total Project Size

| Component             | Size           |
| --------------------- | -------------- |
| Source Code           | ~50 KB         |
| Dependencies (Python) | ~500 MB        |
| Dependencies (Node)   | ~300-500 MB    |
| Trained Model         | ~100-200 MB    |
| Dataset               | Depends on you |
| **Total**             | ~1-2 GB        |

## ✅ Verification

To verify all files are in place:

```bash
# Check backend files
python app.py --help

# Check training script
python train_model.py --help

# Check frontend
cd frontend
npm list

# List all files
dir /s
```

## 🔐 Important Files to Protect

- `models/oral_cancer_model.h5` - Backup regularly
- `uploaded_images/` - Backup for analysis
- `.env.local` - Keep secrets safe (don't commit)
- `dataset/` - Keep training data secure

## 📞 Need Help?

1. **Setup Issues** → See `QUICKSTART.md`
2. **Deployment Issues** → See `DEPLOYMENT.md`
3. **General Questions** → See `README.md`
4. **Code Issues** → Check file comments in source code

---

**Last Updated**: 2024
**Version**: 1.0.0
