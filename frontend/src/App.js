import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [validationWarning, setValidationWarning] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const confirmButtonRef = useRef(null);
  const [showValidationModal, setShowValidationModal] = useState(false);
  const validationButtonRef = useRef(null);
  const [apiStatus, setApiStatus] = useState({ status: 'checking', message: 'Checking backend status...' });

  const API_URL = 'http://127.0.0.1:8000';

  // Check API status on component mount
  useEffect(() => {
    checkApiStatus();
    const interval = setInterval(checkApiStatus, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get(`${API_URL}/status`);
      if (response.data?.status === 'ready') {
        setApiStatus({ status: 'ready', message: 'Backend API is ready on port 8000' });
      } else {
        setApiStatus({ status: 'error', message: response.data?.message || 'Backend responded with an error' });
      }
    } catch (err) {
      setApiStatus({ status: 'offline', message: 'Backend not running on port 8000' });
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    setValidationWarning(null);
    
    if (file) {
      // Validate file type
      const validFormats = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif'];
      if (!validFormats.includes(file.type)) {
        setError('❌ Invalid file format. Please upload JPG, PNG, WebP, or GIF images only.');
        setShowValidationModal(true);
        setSelectedFile(null);
        setPreview(null);
        return;
      }

      // Validate file size (max 10MB)
      const maxSize = 10 * 1024 * 1024;
      if (file.size > maxSize) {
        setError(`❌ File too large (${(file.size / (1024 * 1024)).toFixed(2)}MB). Maximum size is 10MB.`);
        setShowValidationModal(true);
        setSelectedFile(null);
        setPreview(null);
        return;
      }

      setSelectedFile(file);
      setError(null);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
        setValidationWarning(null);
      };
      reader.readAsDataURL(file);
    }
  };

  const handlePrediction = async () => {
    if (!selectedFile) {
      setError('❌ Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setValidationWarning(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await axios.post(`${API_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err) {
      if (err.response?.data?.detail) {
        const errorMsg = err.response.data.detail;
        if (errorMsg.includes('not an oral') || errorMsg.includes('oral')) {
          setValidationWarning(`⚠️ Image Validation Failed: ${errorMsg}`);
          setShowValidationModal(true);
        } else {
          setError(`❌ ${errorMsg}`);
          setShowValidationModal(true);
        }
      } else if (err.response?.status === 422) {
        setError('❌ Image format not recognized. Please upload a clear oral cavity image.');
        setShowValidationModal(true);
      } else if (err.message === 'Network Error') {
        setError('❌ Cannot connect to backend. Make sure the API server is running on port 8000.');
      } else {
        setError('❌ Analysis failed. Please try with another image.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    // show custom centered confirmation modal
    setShowConfirm(true);
  };

  const confirmClear = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
    setShowConfirm(false);
  };

  const cancelClear = () => {
    setShowConfirm(false);
  };

  useEffect(() => {
    // focus confirm button and disable background scrolling when modal is open
    if (showConfirm) {
      confirmButtonRef.current?.focus();
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    const onKey = (e) => {
      if (e.key === 'Escape') cancelClear();
    };

    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [showConfirm]);

  // Validation modal keyboard and scroll handling
  useEffect(() => {
    if (showValidationModal) {
      validationButtonRef.current?.focus();
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    const onKey = (e) => {
      if (e.key === 'Escape') {
        setShowValidationModal(false);
        setValidationWarning(null);
        setError(null);
      }
    };

    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [showValidationModal]);

  return (
    <div className="app">
      <header className="header">
        <h1>🏥 Oral Cancer Detection System</h1>
        <p>AI-Powered Medical Image Analysis for Early Detection</p>
      </header>

      <div className="container">
        <div className="main-content">
          <div className="preview-panel">
            <div className="preview-card">
              <div className="preview-header">
                <h2>IMAGE PREVIEW</h2>
              </div>
              <div className="preview-area">
                {preview ? (
                  <img src={preview} alt="Preview" className="preview-image" />
                ) : (
                  <div className="preview-placeholder">
                    <p>Select an oral cavity image to preview here.</p>
                    <p>Supported formats: JPG, PNG, WebP, GIF</p>
                  </div>
                )}
              </div>
              {preview && (
                <div className="preview-meta">
                  <span>{selectedFile?.name}</span>
                  <span>{(selectedFile?.size / (1024 * 1024)).toFixed(2)} MB</span>
                </div>
              )}
            </div>
          </div>

          <div className="control-panel">
            <div className="control-card">
              <div className={`api-status ${apiStatus.status === 'ready' ? 'ready' : apiStatus.status === 'offline' ? 'offline' : 'error'}`}>
                <div className="status-indicator">
                  {apiStatus.status === 'ready' ? '🟢' : apiStatus.status === 'offline' ? '🔴' : '🟠'}
                  <strong>Backend Status:</strong>
                  <span>{apiStatus.status === 'ready' ? 'Ready' : apiStatus.status === 'offline' ? 'Offline' : 'Error'}</span>
                </div>
                <div className="status-message">{apiStatus.message}</div>
              </div>

              <div className="button-group">
                <label htmlFor="file-input" className="control-button select-button">
                  📁 SELECT IMAGE
                  <input
                    type="file"
                    id="file-input"
                    accept="image/jpeg,image/jpg,image/png,image/webp,image/gif"
                    onChange={handleFileSelect}
                    disabled={loading}
                    className="file-input"
                  />
                </label>
                <button
                  onClick={handlePrediction}
                  disabled={!selectedFile || loading || apiStatus?.status !== 'ready'}
                  className="control-button analyze-button"
                >
                  {loading ? '⏳ ANALYZING...' : '🔍 ANALYZE'}
                </button>
                <button
                  type="button"
                  onClick={handleClear}
                  disabled={!preview && !result}
                  className="control-button clear-button"
                >
                  🧹 CLEAR
                </button>
              </div>

              {error && <div className="error-message">{error}</div>}
              {validationWarning && <div className="warning-message">{validationWarning}</div>}

              <div className="result-card">
                <h2>ANALYSIS RESULT</h2>
                {result ? (
                  <>
                    <div className={`result-badge ${result.prediction}`}>
                      {result.prediction === 'cancer' ? '⚠️ CANCER DETECTED' : '✅ NO CANCER DETECTED'}
                    </div>
                    <div className="result-summary-row">
                      <div className="result-summary">
                        <p className="result-label">Prediction</p>
                        <p className={`result-value ${result.prediction}`}>{result.prediction === 'cancer' ? 'Positive' : 'Negative'}</p>
                      </div>
                      <div className="result-summary">
                        <p className="result-label">Confidence</p>
                        <p className="result-value">{result.confidence}%</p>
                      </div>
                      <div className="result-summary">
                        <p className="result-label">Model Accuracy</p>
                        <p className="result-value accuracy">{result.model_accuracy}%</p>
                      </div>
                    </div>
                    <div className="result-summary">
                      <p className="result-label">Message</p>
                      <p className="result-value small">{result.message}</p>
                    </div>
                  </>
                ) : (
                  <div className="empty-result">
                    <p>No analysis yet.</p>
                    <p>Upload an oral cavity image and click ANALYZE.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {showConfirm && (
        <div className="modal-overlay">
          <div className="modal" role="dialog" aria-modal="true">
            <h3>Clear Image</h3>
            <p>Are you sure you want to clear the selected image? This action cannot be undone.</p>
            <div className="modal-actions">
              <button ref={confirmButtonRef} type="button" className="control-button modal-confirm" onClick={confirmClear}>Confirm</button>
              <button type="button" className="control-button modal-cancel" onClick={cancelClear}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {showValidationModal && (
        <div className="modal-overlay">
          <div className="modal" role="dialog" aria-modal="true">
            <h3>Invalid Image</h3>
            <p>{validationWarning || error || 'The selected image is not acceptable. Please choose an oral cavity image.'}</p>
            <div className="modal-actions">
              <button ref={validationButtonRef} type="button" className="control-button modal-cancel" onClick={() => { setShowValidationModal(false); setValidationWarning(null); setError(null); }}>OK</button>
            </div>
          </div>
        </div>
      )}

      <footer className="footer">
        <p>© 2026 Oral Cancer Detection System | AI-Powered Medical Screening Tool</p>
        <p className="footer-disclaimer">Design by Rajiv Yadav</p>
      </footer>
    </div>
  );
}

export default App;
