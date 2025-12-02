import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import os
import numpy as np

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15
NUM_CLASSES = 3

print("\n" + "="*60)
print("🚀 TRAINING MODEL CÓ CẢI THIỆN")
print("="*60)

# Bước 1: Tính class weights để cân bằng
print("\n📊 Bước 1: Tính class weights")
from pathlib import Path

class_counts = {}
data_path = Path('data')
for class_name in ['Mưa', 'Nắng', 'Tuyết']:
    count = len(list((data_path / class_name).glob('*.[jJ][pP]*[gG]')))
    class_counts[class_name] = count
    print(f"   {class_name}: {count} ảnh")

total_samples = sum(class_counts.values())
class_weights = {}
for i, class_name in enumerate(['Mưa', 'Nắng', 'Tuyết']):
    weight = total_samples / (NUM_CLASSES * class_counts[class_name])
    class_weights[i] = weight
    print(f"   Weight cho {class_name}: {weight:.2f}")

# Bước 2: Chuẩn bị dữ liệu với augmentation mạnh hơn
print("\n🖼️  Bước 2: Chuẩn bị dữ liệu")

data_gen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=30,          # Tăng từ 20 lên 30
    horizontal_flip=True,
    vertical_flip=True,         # Thêm flip dọc
    brightness_range=[0.7, 1.3],  # Tăng range
    width_shift_range=0.2,      # Thêm shift
    height_shift_range=0.2,
    shear_range=0.2,            # Thêm shear
    zoom_range=0.2,             # Thêm zoom
    fill_mode='nearest'
)

train_gen = data_gen.flow_from_directory(
    'data',
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

valid_gen = data_gen.flow_from_directory(
    'data',
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

print(f"   Training: {train_gen.samples} ảnh")
print(f"   Validation: {valid_gen.samples} ảnh")

# Bước 3: Xây dựng model cải thiện
print("\n🏗️  Bước 3: Xây dựng model")

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
    BatchNormalization(),
    Conv2D(32, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    Flatten(),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(128, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),
    Dense(NUM_CLASSES, activation='softmax')
])

# Compile với learning rate thấp hơn
optimizer = Adam(learning_rate=0.0001)
model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("   Model architecture:")
model.summary()

# Bước 4: Training với class weights
print("\n⚙️  Bước 4: Training model")

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    'checkpoints/simple_model_best.h5',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy',
    patience=3,
    restore_best_weights=True,
    verbose=1
)

# QUAN TRỌNG: Sử dụng class_weights
history = model.fit(
    train_gen,
    validation_data=valid_gen,
    epochs=EPOCHS,
    class_weight=class_weights,  # ← KEY LINE
    callbacks=[checkpoint, early_stopping],
    verbose=1
)

model.save('checkpoints/simple_model.h5')

# Bước 5: Kết quả
print("\n" + "="*60)
print("✅ HOÀN THÀNH TRAINING")
print("="*60)
print(f"\n📈 Kết quả:")
print(f"   Accuracy cao nhất (training): {max(history.history['accuracy']):.2%}")
print(f"   Accuracy cao nhất (validation): {max(history.history['val_accuracy']):.2%}")
print(f"\n💾 Model đã lưu:")
print(f"   • checkpoints/simple_model_best.h5")
print(f"   • checkpoints/simple_model.h5")

print(f"\n🎯 Cải thiện:")
print(f"   ✅ Sử dụng class_weight để cân bằng dữ liệu")
print(f"   ✅ Tăng data augmentation (30 độ rotation, zoom, shift, shear)")
print(f"   ✅ Thêm Batch Normalization")
print(f"   ✅ Tăng Dropout (lên 0.5)")
print(f"   ✅ Giảm learning rate (0.0001)")
