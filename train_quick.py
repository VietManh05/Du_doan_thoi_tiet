import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 5
NUM_CLASSES = 3

print('=== BẮT ĐẦU TRAINING MODEL NHANH ===')
print('Bước 1: Chuẩn bị dữ liệu')

data_gen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2]
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

print(f'Training images: {train_gen.samples}, Validation images: {valid_gen.samples}')

print('\nBước 2: Xây dựng model')
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(*IMAGE_SIZE, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(NUM_CLASSES, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print('\nBước 3: Training model (5 epochs)')
checkpoint = tf.keras.callbacks.ModelCheckpoint(
    'checkpoints/simple_model_best.h5',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

history = model.fit(
    train_gen,
    validation_data=valid_gen,
    epochs=EPOCHS,
    callbacks=[checkpoint],
    verbose=1
)

model.save('checkpoints/simple_model.h5')
print(f'\n✅ Hoàn thành! Độ chính xác: {max(history.history["val_accuracy"]):.2%}')
