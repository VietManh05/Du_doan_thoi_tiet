import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

"""
Mini project phân loại ảnh thời tiết
Model này được thiết kế đơn giản để:
1. Dễ hiểu cho người mới học
2. Train nhanh trên CPU
3. Độ chính xác tốt cho mini project
"""

# 1. Cấu hình cơ bản
IMAGE_SIZE = (128, 128)    # Kích thước ảnh nhỏ để train nhanh hơn
BATCH_SIZE = 32           # Số ảnh xử lý mỗi lần
EPOCHS = 20              # Số lần train lại toàn bộ dữ liệu
NUM_CLASSES = 3          # Số loại thời tiết (Nắng, Mưa, Tuyết)

# 2. Chuẩn bị dữ liệu
def prepare_data():
    """Chuẩn bị dữ liệu train và validation"""
    print("\n--- Bước 1: Chuẩn bị dữ liệu ---")
    
    # Tăng cường dữ liệu (Data Augmentation) đơn giản
    data_gen = ImageDataGenerator(
        rescale=1./255,          # Chuẩn hóa pixel về khoảng [0,1]
        validation_split=0.2,    # 20% dữ liệu dùng để validation
        rotation_range=20,       # Xoay ảnh trong khoảng ±20 độ
        horizontal_flip=True,    # Lật ảnh ngang
        brightness_range=[0.8, 1.2]  # Điều chỉnh độ sáng
    )
    
    # Load dữ liệu training
    train_gen = data_gen.flow_from_directory(
        'data',
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Load dữ liệu validation
    valid_gen = data_gen.flow_from_directory(
        'data',
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    print(f"Số lớp phân loại: {len(train_gen.class_indices)}")
    print(f"Tên các lớp: {train_gen.class_indices}")
    print(f"Số lượng ảnh training: {train_gen.samples}")
    print(f"Số lượng ảnh validation: {valid_gen.samples}")
    
    return train_gen, valid_gen

# 3. Xây dựng model
def create_model():
    """Tạo model CNN đơn giản nhưng hiệu quả"""
    print("\n--- Bước 2: Xây dựng model ---")
    
    model = Sequential([
        # Block 1: Trích xuất đặc trưng cơ bản
        Conv2D(32, (3, 3), activation='relu', padding='same', 
               input_shape=(*IMAGE_SIZE, 3)),
        MaxPooling2D((2, 2)),
        
        # Block 2: Trích xuất đặc trưng phức tạp
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        
        # Block 3: Trích xuất đặc trưng chi tiết
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        
        # Chuyển đổi thành vector
        Flatten(),
        
        # Các lớp fully connected để phân loại
        Dense(128, activation='relu'),
        Dropout(0.5),  # Tránh overfitting
        Dense(NUM_CLASSES, activation='softmax')  # Layer output
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # In tổng quan model
    model.summary()
    
    return model

# 4. Training
def train_model(model, train_gen, valid_gen):
    """Training model và lưu kết quả tốt nhất"""
    print("\n--- Bước 3: Training model ---")
    
    # Tạo thư mục lưu model
    os.makedirs('checkpoints', exist_ok=True)
    
    # Callback để lưu model tốt nhất
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        'checkpoints/model_mini_best.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    # Callback dừng sớm nếu model không cải thiện
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    # Training
    history = model.fit(
        train_gen,
        validation_data=valid_gen,
        epochs=EPOCHS,
        callbacks=[checkpoint, early_stopping],
        verbose=1
    )
    
    # Lưu model cuối cùng
    model.save('checkpoints/model_mini_final.h5')
    print("\nĐã lưu model tại checkpoints/model_mini_final.h5")
    
    return history

def main():
    """Hàm chính chạy toàn bộ quá trình"""
    print("=== BẮT ĐẦU TRAINING MODEL PHÂN LOẠI THỜI TIẾT ===")
    
    # 1. Chuẩn bị dữ liệu
    train_gen, valid_gen = prepare_data()
    
    # 2. Tạo model
    model = create_model()
    
    # 3. Training
    history = train_model(model, train_gen, valid_gen)
    
    print("\n=== HOÀN THÀNH TRAINING ===")
    print(f"Độ chính xác cao nhất trên tập validation: {max(history.history['val_accuracy']):.2%}")

if __name__ == "__main__":
    main()