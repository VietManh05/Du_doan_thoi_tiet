import tensorflow as tf
import numpy as np
from PIL import Image
import os
import datetime
import logging
import time
from time_extractor import TimeExtractor

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherPredictor:
    def __init__(self, model_path, data_dir='data'):
        """Khởi tạo model dự đoán"""
        try:
            # Khởi tạo time extractor
            self.time_extractor = TimeExtractor()
            
            # Kiểm tra và tải model
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            logger.info(f"Loading model from {model_path}")
            self.model = tf.keras.models.load_model(model_path)
            
            # Lấy tên classes từ thư mục data để đảm bảo thứ tự nhất quán
            if os.path.exists(data_dir):
                self.class_names = sorted(os.listdir(data_dir))
                logger.info(f"Using class names from data directory: {self.class_names}")
            else:
                self.class_names = sorted(['Mưa', 'Nắng', 'Tuyết'])
                logger.warning(f"Data directory not found at {data_dir}, using default class names: {self.class_names}")
            
            # Cấu hình model
            self.img_size = 224
            logger.info("Model initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            raise

    def preprocess_image(self, image_path):
        """Tiền xử lý ảnh đầu vào"""
        try:
            # Kiểm tra file tồn tại
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            # Đọc và kiểm tra ảnh
            img = Image.open(image_path)
            if img is None:
                raise ValueError("Failed to load image")
                
            # Chuyển đổi sang RGB
            img = img.convert('RGB')
            
            # Resize với chất lượng cao
            img = img.resize((self.img_size, self.img_size), Image.Resampling.LANCZOS)
            
            # Chuyển đổi sang array và chuẩn hóa
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
            img_array = img_array / 255.0
            
            return img_array
            
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")

    def predict(self, image_path, record_history=True):
        """Dự đoán thời tiết từ ảnh"""
        try:
            start_time = time.time()
            
            # Tiền xử lý ảnh
            processed_image = self.preprocess_image(image_path)
            
            # Dự đoán với timeout
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Lấy kết quả và độ tin cậy
            predicted_class_index = np.argmax(predictions[0])
            confidences = predictions[0]
            
            # Chuẩn hóa độ tin cậy bằng softmax
            confidences = tf.nn.softmax(confidences).numpy()
            confidence = float(confidences[predicted_class_index])
            
            # Tính toán độ tin cậy cho từng lớp
            class_confidences = {class_name: float(conf) 
                               for class_name, conf in zip(self.class_names, confidences)}
            
            # In thông tin debug
            print(f"Debug - all confidences: {class_confidences}")
            
            # Kiểm tra độ tin cậy
            if confidence < 0.4:
                print(f"Warning: Low confidence prediction ({confidence:.2%})")
            
            # Tính thời gian xử lý
            duration = time.time() - start_time
            
            # Ghi lại lịch sử phân tích nếu được yêu cầu
            prediction_class = self.class_names[predicted_class_index]
            if record_history:
                analysis_record = self.time_extractor.record_analysis(
                    image_name=os.path.basename(image_path),
                    prediction=prediction_class,
                    confidence=confidence,
                    duration=duration,
                    notes=None
                )
                logger.info(f"Analysis recorded: ID={analysis_record['id']}")
            
            # Trả về kết quả với thông tin chi tiết
            return {
                'class': prediction_class,
                'confidence': confidence,
                'confidences': class_confidences,
                'timestamp': datetime.datetime.now().isoformat(),
                'duration': duration,
                'time_components': self.time_extractor.extract_time_components()
            }
            
        except Exception as e:
            raise Exception(f"Error during prediction: {str(e)}")

if __name__ == "__main__":
    # Ví dụ sử dụng
    predictor = WeatherPredictor('checkpoints/simple_model_best.h5')
    
    # Thử nghiệm với một số ảnh
    test_images = [
        'test/sunny/test1.jpg',
        'test/cloudy/test1.jpg'
    ]
    
    for image_path in test_images:
        try:
            result = predictor.predict(image_path)
            print(f"\nẢnh: {image_path}")
            print(f"Dự đoán: {result['class']}")
            print(f"Độ tin cậy: {result['confidence']:.2%}")
        except Exception as e:
            print(f"Lỗi khi xử lý ảnh {image_path}: {str(e)}")