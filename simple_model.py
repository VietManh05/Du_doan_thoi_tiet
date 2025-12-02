import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

def create_model(input_shape=(224, 224, 3), num_classes=3):
    """Tạo mô hình CNN đơn giản cho phân loại thời tiết"""
    model = models.Sequential([
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.BatchNormalization(),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.BatchNormalization(),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.BatchNormalization(),
        
        # Fully Connected layers
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def plot_training_history(history):
    """Vẽ đồ thị lịch sử huấn luyện"""
    plt.figure(figsize=(12, 4))
    
    # Vẽ độ chính xác
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Độ chính xác (training)')
    plt.plot(history.history['val_accuracy'], label='Độ chính xác (validation)')
    plt.title('Độ chính xác qua các epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Độ chính xác')
    plt.legend()
    
    # Vẽ loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Loss (training)')
    plt.plot(history.history['val_loss'], label='Loss (validation)')
    plt.title('Loss qua các epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.show()  