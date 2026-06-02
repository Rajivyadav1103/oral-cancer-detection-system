# Oral Cancer Detection - Project Configuration

## Project Information

- **Name**: Oral Cancer Detection System
- **Version**: 1.0.0
- **Type**: Medical AI Application
- **Purpose**: AI-powered detection of oral cancer from medical images

## Technology Stack

### Backend

- Framework: FastAPI (Python)
- Server: Uvicorn
- Deep Learning: TensorFlow/Keras
- Image Processing: OpenCV, Pillow

### Frontend

- Framework: React 18
- Build Tool: React Scripts
- HTTP Client: Axios
- Styling: CSS3 with Flexbox/Grid

### Database (Optional)

- PostgreSQL (for storing predictions)
- SQLAlchemy (ORM)

### Deployment

- Docker (containerization)
- Nginx (reverse proxy)
- Gunicorn (ASGI server)

## Project Structure

```
ui/
├── Backend Components
│   ├── app.py                 # FastAPI server
│   ├── train_model.py         # Model training
│   └── requirements.txt       # Python deps
│
├── Frontend Components
│   ├── frontend/src/          # React components
│   ├── frontend/public/       # Static files
│   └── frontend/package.json  # Node deps
│
├── Data
│   ├── dataset/               # Training data
│   ├── models/                # Trained models (auto-generated)
│   └── uploaded_images/       # User uploads (auto-generated)
│
├── Documentation
│   ├── README.md              # Main docs
│   ├── QUICKSTART.md          # Quick setup
│   ├── DEPLOYMENT.md          # Production guide
│   ├── TESTING.md             # Testing guide
│   └── FILES.md               # File reference
│
└── Configuration
    ├── .gitignore
    ├── setup.bat
    ├── start_backend.bat
    └── start_frontend.bat
```

## Port Configuration

- **Frontend**: 3000 (localhost:3000)
- **Backend**: 8000 (localhost:8000)
- **Database**: 5432 (if PostgreSQL used)

## Environment Configuration

### Backend Environment Variables

```
DEBUG=False
MODEL_PATH=models/oral_cancer_model.h5
IMG_SIZE=224
CONFIDENCE_THRESHOLD=0.5
MAX_FILE_SIZE=10485760
```

### Frontend Environment Variables

```
REACT_APP_API_URL=http://localhost:8000
```

## Model Configuration

### CNN Architecture

- Input: 224x224 RGB images
- Output: Binary classification (cancer/non-cancer)
- Layers: 4 Conv blocks + Dense layers
- Training: 20 epochs, batch size 32

### Image Validation

- Color analysis for oral cavity detection
- Rejects: animals, birds, persons, objects
- Accepted formats: JPEG, PNG, WebP, GIF
- Max file size: 10MB

## API Endpoints

| Method | Endpoint        | Purpose         |
| ------ | --------------- | --------------- |
| GET    | /               | API info        |
| GET    | /status         | API status      |
| GET    | /docs           | Swagger docs    |
| POST   | /predict        | Make prediction |
| POST   | /validate-image | Validate image  |

## File Organization After Prediction

```
uploaded_images/
├── cancer/        # Positive predictions
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── non_cancer/    # Negative predictions
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

## Development Workflow

1. **Setup Phase**
   - Install dependencies
   - Train model
   - Generate models directory

2. **Development Phase**
   - Backend: `python app.py` (auto-reload with changes)
   - Frontend: `npm start` (hot reload enabled)
   - Test: Use browser and API tools

3. **Testing Phase**
   - Unit tests
   - Integration tests
   - API tests
   - UI tests

4. **Deployment Phase**
   - Build frontend: `npm run build`
   - Setup production server
   - Configure SSL/HTTPS
   - Enable monitoring

## Performance Metrics

### Target Performance

- API Response: < 10 seconds
- Frontend Render: < 1 second
- Model Accuracy: > 85%

### Resource Requirements

- RAM: Minimum 2GB
- CPU: 2+ cores recommended
- Storage: 1-2GB (including dependencies)
- GPU: Optional (for faster training)

## Security Features

- [x] CORS configured
- [x] Image validation
- [x] File size limits
- [x] Error handling
- [x] Input validation

### To Add (Production)

- [ ] User authentication
- [ ] Rate limiting
- [ ] HTTPS/SSL
- [ ] API key validation
- [ ] Audit logging

## Database Schema (Optional)

```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    image_name VARCHAR(255),
    prediction VARCHAR(50),
    confidence DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## CI/CD Pipeline

### Development

```
Code Push → Tests → Build → Dev Deploy
```

### Production

```
Code Push → Tests → Build → Staging → Production
```

## Monitoring & Logging

- Backend logs: `logs/app.log`
- Frontend errors: Browser console
- API requests: Uvicorn logs
- Predictions: Saved with images

## Backup Strategy

### Regular Backups

- Models: `models/oral_cancer_model.h5`
- Uploaded images: `uploaded_images/`
- Database: If using PostgreSQL

### Backup Frequency

- Daily: Uploaded images
- Weekly: Models and configuration
- Monthly: Full system

## Dependencies Version Lock

### Python (from requirements.txt)

- FastAPI 0.104.1
- TensorFlow 2.14.0
- Uvicorn 0.24.0

### Node (from package.json)

- React ^18.2.0
- Axios ^1.6.0

## Known Limitations

1. Model accuracy depends on training data quality
2. Requires good image quality for predictions
3. Currently binary classification only (cancer/non-cancer)
4. No user persistence (stateless API)

## Scalability Considerations

### Horizontal Scaling

- Multiple backend instances behind load balancer
- Separate database server
- Shared model storage

### Vertical Scaling

- Increase server RAM (for larger datasets)
- Better GPU (for faster training)
- Faster storage (SSD)

## Testing Coverage

- [x] API endpoints
- [x] Image validation
- [x] Model inference
- [x] Frontend UI
- [x] Error handling
- [ ] User authentication (if needed)
- [ ] Database operations (if used)

## Maintenance Schedule

- **Daily**: Monitor API uptime
- **Weekly**: Check model predictions accuracy
- **Monthly**: Update dependencies
- **Quarterly**: Security audit
- **Annually**: Model retraining

## Support & Documentation

- Main Documentation: `README.md`
- Quick Setup: `QUICKSTART.md`
- Testing Guide: `TESTING.md`
- Deployment: `DEPLOYMENT.md`
- Files Reference: `FILES.md`

## Contact & Attribution

- Purpose: Medical education and research
- License: [Add your license]
- Support: [Add support contact]

## Version History

| Version | Date | Changes         |
| ------- | ---- | --------------- |
| 1.0.0   | 2024 | Initial release |

---

**Project Status**: ✅ Ready for Development
**Last Updated**: 2024
