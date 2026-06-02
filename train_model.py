import os
import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout,
    BatchNormalization,
    GlobalAveragePooling2D,
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import cv2
from pathlib import Path
import json

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 8
EPOCHS = 30
MODEL_PATH = "models/oral_cancer_model.h5"
MODEL_INFO_PATH = "models/model_info.json"


def create_model():
    """Create model using MobileNetV2 transfer learning."""
    base_model = MobileNetV2(
        weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.5)(x)
    outputs = Dense(1, activation="sigmoid")(x)

    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    return model


def train_model():
    """Train the model on the dataset"""
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)

    # Image data augmentation
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        shear_range=0.2,
        fill_mode="nearest",
        validation_split=0.2,  # reserve 20% for validation
    )

    # Load training and validation data
    train_generator = train_datagen.flow_from_directory(
        "dataset",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="binary",  # cancer=1, non_cancer=0
        classes=["non_cancer", "cancer"],
        subset="training",
    )

    val_generator = train_datagen.flow_from_directory(
        "dataset",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="binary",
        classes=["non_cancer", "cancer"],
        subset="validation",
    )

    # Create and train model
    model = create_model()
    print("Model created. Starting training...")

    # compute simple class weights to help with imbalance
    classes, counts = np.unique(train_generator.classes, return_counts=True)
    total = counts.sum()
    class_weight = {
        int(c): float(total / (len(classes) * cnt)) for c, cnt in zip(classes, counts)
    }

    # Callbacks
    checkpoint = ModelCheckpoint(
        MODEL_PATH, monitor="val_loss", save_best_only=True, verbose=1
    )
    earlystop = EarlyStopping(
        monitor="val_loss", patience=6, restore_best_weights=True, verbose=1
    )

    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        steps_per_epoch=max(1, len(train_generator)),
        validation_data=val_generator,
        validation_steps=max(1, len(val_generator)),
        class_weight=class_weight,
        callbacks=[checkpoint, earlystop],
        verbose=1,
    )

    # Save model
    # Ensure final best model is saved (ModelCheckpoint already saved best)
    if not os.path.exists(MODEL_PATH):
        model.save(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    # Save model info
    model_info = {
        "input_size": IMG_SIZE,
        "model_type": "CNN",
        "classes": ["non_cancer", "cancer"],
        "accuracy": float(history.history["accuracy"][-1]),
    }

    with open(MODEL_INFO_PATH, "w") as f:
        json.dump(model_info, f, indent=4)

    print(f"Model info saved to {MODEL_INFO_PATH}")
    return model


if __name__ == "__main__":
    train_model()
