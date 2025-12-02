from flask import Flask, render_template, request, jsonify
import os
from predict_simple import WeatherPredictor
from time_extractor import TimeExtractor
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cấu hình
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MODEL_PATH = os.path.join(BASE_DIR, 'checkpoints', 'simple_model_best.h5')

# Tạo các thư mục cần thiết
required_dirs = [
    os.path.join(BASE_DIR, 'static'),
    UPLOAD_FOLDER,
    os.path.join(BASE_DIR, 'checkpoints')
]

for directory in required_dirs:
    os.makedirs(directory, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Khởi tạo model
try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    predictor = WeatherPredictor(MODEL_PATH, data_dir=os.path.join(BASE_DIR, 'data'))
    time_extractor = TimeExtractor()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise

def allowed_file(filename):
    """Kiểm tra phần mở rộng của file có được cho phép không"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    """Trang chủ"""
    return render_template('index_simple.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API dự đoán thời tiết"""
    try:
        if 'file' not in request.files:
            logger.warning("No file part in request")
            return jsonify({'error': 'Không tìm thấy file'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.warning("No file selected")
            return jsonify({'error': 'Chưa chọn file'}), 400
        
        if file and allowed_file(file.filename):
            # Lưu file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            try:
                file.save(filepath)
                logger.info(f"File saved successfully: {filepath}")
                
                # Dự đoán
                result = predictor.predict(filepath, record_history=True)
                logger.info(f"Prediction successful: {result}")
                
                # Kiểm tra độ tin cậy của dự đoán
                confidence = float(result['confidence'])
                prediction_class = result['class']
                
                response_data = {
                    'class': prediction_class,
                    'confidence': confidence,
                    'confidences': result.get('confidences', {}),
                    'timestamp': result.get('timestamp', ''),
                    'duration': result.get('duration', 0),
                    'time_components': result.get('time_components', {}),
                    'warning': 'Dự đoán có độ tin cậy thấp' if confidence < 0.4 else None
                }
                
                logger.info(f"Successful prediction: {prediction_class} with {confidence:.2%} confidence")
                return jsonify(response_data)
            except Exception as e:
                logger.error(f"Error during prediction: {str(e)}")
                return jsonify({'error': f'Lỗi khi dự đoán: {str(e)}'}), 500
            finally:
                # Xóa file tạm sau khi xử lý
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                        logger.info(f"Temporary file removed: {filepath}")
                    except Exception as e:
                        logger.warning(f"Could not remove temporary file: {str(e)}")
        
        logger.warning("Unsupported file type")
        return jsonify({'error': 'File không được hỗ trợ'}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Lỗi hệ thống'}), 500

@app.route('/api/history/date', methods=['GET'])
def get_history_by_date():
    """Lấy lịch sử phân tích theo năm/tháng/ngày"""
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        day = request.args.get('day', type=int)
        
        if not year:
            return jsonify({'error': 'Năm là bắt buộc'}), 400
        
        records = time_extractor.get_analysis_by_date(year, month, day)
        
        return jsonify({
            'success': True,
            'count': len(records),
            'records': records
        })
    except Exception as e:
        logger.error(f"Error getting history by date: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/time-range', methods=['GET'])
def get_history_by_time_range():
    """Lấy lịch sử phân tích trong khoảng thời gian (giờ)"""
    try:
        start_hour = request.args.get('start_hour', type=int)
        end_hour = request.args.get('end_hour', type=int)
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        day = request.args.get('day', type=int)
        
        if start_hour is None or end_hour is None:
            return jsonify({'error': 'start_hour và end_hour là bắt buộc'}), 400
        
        records = time_extractor.get_analysis_by_time_range(
            start_hour, end_hour, year, month, day
        )
        
        return jsonify({
            'success': True,
            'count': len(records),
            'records': records
        })
    except Exception as e:
        logger.error(f"Error getting history by time range: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/statistics', methods=['GET'])
def get_statistics():
    """Lấy thống kê phân tích"""
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        day = request.args.get('day', type=int)
        
        if not year:
            return jsonify({'error': 'Năm là bắt buộc'}), 400
        
        stats = time_extractor.get_statistics_by_date(year, month, day)
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/hourly', methods=['GET'])
def get_hourly_statistics():
    """Lấy thống kê phân tích theo từng giờ"""
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        day = request.args.get('day', type=int)
        
        if not (year and month and day):
            return jsonify({'error': 'year, month, day là bắt buộc'}), 400
        
        stats = time_extractor.get_hourly_statistics(year, month, day)
        
        return jsonify({
            'success': True,
            'hourly_statistics': stats
        })
    except Exception as e:
        logger.error(f"Error getting hourly statistics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/all', methods=['GET'])
def get_all_history():
    """Lấy toàn bộ lịch sử phân tích"""
    try:
        limit = request.args.get('limit', 100, type=int)
        records = time_extractor.get_all_history(limit)
        
        return jsonify({
            'success': True,
            'count': len(records),
            'records': records
        })
    except Exception as e:
        logger.error(f"Error getting all history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/export', methods=['GET'])
def export_history():
    """Xuất lịch sử phân tích ra file JSON"""
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        day = request.args.get('day', type=int)
        
        export_path = time_extractor.export_history_to_json(
            output_path=os.path.join(BASE_DIR, 'analysis_history_export.json'),
            year=year, month=month, day=day
        )
        
        return jsonify({
            'success': True,
            'export_file': export_path
        })
    except Exception as e:
        logger.error(f"Error exporting history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/cleanup', methods=['POST'])
def cleanup_old_records():
    """Xóa các bản ghi cũ"""
    try:
        days_old = request.json.get('days_old', 30) if request.json else 30
        deleted_count = time_extractor.clear_old_records(days_old)
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count
        })
    except Exception as e:
        logger.error(f"Error cleaning up records: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Kiểm tra môi trường
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Model file not found at {MODEL_PATH}")
        print(f"Error: Model file not found at {MODEL_PATH}")
        exit(1)
        
    # Chạy ứng dụng
    logger.info("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)