# ✅ Getting Started Checklist

Complete checklist to get the Oral Cancer Detection System running.

## Pre-Installation Checklist

### System Requirements

- [ ] Windows 10/11, Mac, or Linux
- [ ] At least 2GB RAM available
- [ ] At least 2GB free disk space (more for large datasets)
- [ ] Internet connection for downloading dependencies

### Software Requirements

- [ ] Python 3.8 or higher installed
  - Check: `python --version`
- [ ] Node.js 14+ and npm installed
  - Check: `node --version` and `npm --version`
- [ ] Git installed (optional, for version control)
- [ ] Terminal/PowerShell ready to use

## Installation Checklist

### Step 1: Backend Setup

- [ ] Navigate to project directory: `cd "path\to\ui"`
- [ ] Check Python installation: `python --version`
- [ ] Read `requirements.txt`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify installations: `pip list`

### Step 2: Dataset Preparation

- [ ] Organize cancer images in `dataset/cancer/`
- [ ] Organize non-cancer images in `dataset/non_cancer/`
- [ ] Verify at least 50 images per category
- [ ] Check image formats (JPG, PNG)
- [ ] Verify images are clear and well-labeled

### Step 3: Model Training

- [ ] Check dataset directory structure
- [ ] Run training: `python train_model.py`
- [ ] **⏰ WAIT 15-30 minutes** (depends on dataset size)
- [ ] Verify model created: `ls models/`
- [ ] Check `models/oral_cancer_model.h5` exists (~100-200MB)
- [ ] Check `models/model_info.json` exists

### Step 4: Backend Verification

- [ ] Start backend: `python app.py`
- [ ] See "Uvicorn running on http://0.0.0.0:8000"
- [ ] Open browser to: `http://localhost:8000/status`
- [ ] See JSON response with status "ready"
- [ ] Check `http://localhost:8000/docs` for API docs
- [ ] **Keep backend running** (don't close terminal)

### Step 5: Frontend Setup

- [ ] Open new terminal/PowerShell window
- [ ] Navigate to frontend: `cd frontend`
- [ ] Install dependencies: `npm install`
- [ ] **⏰ WAIT 3-5 minutes** (downloads ~300-500MB)
- [ ] Start React: `npm start`
- [ ] Browser should open automatically to `http://localhost:3000`
- [ ] See React app load without errors

## Verification Checklist

### Backend Verification

- [ ] Backend running on port 8000
- [ ] Status endpoint shows "ready"
- [ ] Swagger docs accessible at `/docs`
- [ ] No errors in backend terminal
- [ ] Model file exists and is not corrupted

### Frontend Verification

- [ ] React app loaded
- [ ] No red errors in console (F12)
- [ ] File upload button visible
- [ ] Instructions displayed
- [ ] API status indicator shows "ready" (green)

### Image Preview

- [ ] Click "Choose Image"
- [ ] Select a test image from your computer
- [ ] Image preview appears
- [ ] Filename displays below preview

### Prediction Test

- [ ] With image selected, click "Analyze Image"
- [ ] Loading indicator shows
- [ ] After 5-10 seconds, results appear
- [ ] See prediction (cancer/non_cancer)
- [ ] See confidence percentage
- [ ] See message explaining result
- [ ] Image saved to `uploaded_images/`

## Success Indicators

### Visual Indicators

- ✅ Frontend shows green "ready" status
- ✅ No red error messages
- ✅ Prediction badge appears with results
- ✅ Image preview loads and displays
- ✅ Results show confidence score

### File Indicators

- ✅ `models/oral_cancer_model.h5` exists
- ✅ `models/model_info.json` exists
- ✅ `uploaded_images/cancer/` created after prediction
- ✅ `uploaded_images/non_cancer/` created after prediction
- ✅ Test image appears in appropriate folder

### Performance Indicators

- ✅ First prediction takes 5-10 seconds
- ✅ Subsequent predictions faster (2-5 seconds)
- ✅ No crashes or errors
- ✅ Backend handles requests correctly

## Troubleshooting Checklist

### If Backend Won't Start

- [ ] Python installed? Check: `python --version`
- [ ] Dependencies installed? Check: `pip list | grep fastapi`
- [ ] Model exists? Check: `ls models/oral_cancer_model.h5`
- [ ] Port 8000 available? Try: `python app.py --port 8001`
- [ ] Firewall blocking? Check firewall settings

### If Frontend Won't Load

- [ ] Node installed? Check: `node --version` and `npm --version`
- [ ] Dependencies installed? Check: `npm list`
- [ ] Port 3000 available? Check if another app using it
- [ ] Internet connection? Required for first load
- [ ] Clear browser cache and try again

### If Prediction Fails

- [ ] Backend running? Check terminal for errors
- [ ] Backend status showing "ready"? Visit `/status` endpoint
- [ ] Image is valid? Try with clear oral image
- [ ] File size < 10MB? Check file properties
- [ ] Browser console errors? Press F12 to check
- [ ] API logs? Check backend terminal for errors

### If Model Training Fails

- [ ] Dataset exists? Check `dataset/` folder
- [ ] Images in cancer folder? Check `dataset/cancer/`
- [ ] Images in non_cancer folder? Check `dataset/non_cancer/`
- [ ] At least 50 images? Check count
- [ ] Images are readable? Try opening one manually
- [ ] Enough disk space? Check free space
- [ ] Enough RAM? Check system resources

## Testing Checklist

### Basic Testing

- [ ] Test with valid oral image
- [ ] Get cancer prediction (confidence > 50%)
- [ ] Test with valid oral image
- [ ] Get non-cancer prediction (confidence < 50%)
- [ ] Test with non-oral image (should show error)

### Error Testing

- [ ] Upload animal image → Error message appears
- [ ] Upload person image → Error message appears
- [ ] Upload non-image file → Error message appears
- [ ] Upload file > 10MB → Error message appears

### UI Testing

- [ ] File input dialog opens
- [ ] Image preview displays
- [ ] Clear button works
- [ ] Results display correctly
- [ ] Instructions visible
- [ ] Responsive on different screen sizes

## Post-Setup Checklist

### Documentation Review

- [ ] Read `README.md` for detailed info
- [ ] Skim `QUICKSTART.md` for commands
- [ ] Check `FILES.md` for project structure
- [ ] Review `TESTING.md` for test procedures

### Customization (Optional)

- [ ] Adjust confidence threshold in `app.py`
- [ ] Change styling in `frontend/src/App.css`
- [ ] Modify validation in `app.py`
- [ ] Add more training epochs in `train_model.py`

### Backup Setup (Recommended)

- [ ] Backup trained model file
- [ ] Backup dataset
- [ ] Backup configuration files
- [ ] Create Git repository (optional)

## Daily Use Checklist

### Starting the Application

- [ ] Open terminal 1: `python app.py`
- [ ] ✅ Wait for "Uvicorn running..." message
- [ ] Open terminal 2: `cd frontend && npm start`
- [ ] ✅ Wait for "Compiled successfully" message
- [ ] Open browser to `http://localhost:3000`

### After Using

- [ ] Check results saved in `uploaded_images/`
- [ ] Review logs for any errors
- [ ] Backup important images/models if needed
- [ ] Keep backend terminal window open while working

## Monthly Checklist

- [ ] Review model accuracy on new images
- [ ] Check disk space usage
- [ ] Update dependencies: `pip list --outdated`
- [ ] Backup uploaded images
- [ ] Review logs for errors
- [ ] Test with variety of images

## Before Deployment

- [ ] Model accuracy verified (> 85%)
- [ ] All tests passing
- [ ] Documentation up to date
- [ ] Security review completed
- [ ] Performance tested
- [ ] Backup strategy in place
- [ ] Monitoring enabled
- [ ] Error handling verified

## Common Issues & Quick Fixes

| Issue                        | Quick Fix                                         |
| ---------------------------- | ------------------------------------------------- |
| "Port 8000 in use"           | Use different port: `uvicorn app:app --port 8001` |
| "ModuleNotFoundError"        | Install deps: `pip install -r requirements.txt`   |
| "Cannot find module 'axios'" | Install: `npm install` in frontend folder         |
| "Model not found"            | Train model: `python train_model.py`              |
| "Frontend can't connect"     | Ensure backend running on 8000                    |

## Quick Command Reference

```bash
# Backend
python train_model.py          # Train model
python app.py                  # Start backend
python app.py --port 8001      # Use different port

# Frontend
cd frontend
npm install                    # Install dependencies
npm start                      # Start dev server
npm run build                  # Build for production

# Testing
python test_backend.py         # Test model loading
curl http://localhost:8000     # Test backend

# Cleanup
rmdir uploaded_images          # Remove uploaded images
del models\*.h5               # Remove trained model
rm -rf node_modules           # Remove frontend deps
```

## Success! 🎉

If all items are checked, your Oral Cancer Detection System is ready to use!

### Next Steps

1. ✅ System is set up and running
2. 📖 Read detailed documentation as needed
3. 🧪 Test with various images
4. 🚀 Consider production deployment
5. 📊 Monitor accuracy and performance

### Need Help?

- **Setup Issues**: See `QUICKSTART.md`
- **Detailed Docs**: See `README.md`
- **Testing**: See `TESTING.md`
- **Production**: See `DEPLOYMENT.md`

---

**Congratulations! You're all set! 🚀**

Visit `http://localhost:3000` to start using the application.
