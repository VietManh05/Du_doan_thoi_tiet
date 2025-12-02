#!/usr/bin/env python3
"""
KIỂM TRA CƠ BẢN - Basic Health Check
Tệp này giúp người mới kiểm tra xem mọi thứ hoạt động đúng không
"""

import sys
import os

def print_header(title):
    """In tiêu đề"""
    print("\n" + "="*60)
    print(f"✓ {title}")
    print("="*60)

def check_python_version():
    """Kiểm tra phiên bản Python"""
    print_header("1. KIỂM TRA PHIÊN BẢN PYTHON")
    
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✅ OK - Phiên bản Python hỗ trợ")
        return True
    else:
        print("❌ LỖI - Cần Python 3.7+")
        return False

def check_imports():
    """Kiểm tra các thư viện cần thiết"""
    print_header("2. KIỂM TRA THƯ VIỆN CẦN THIẾT")
    
    required_packages = {
        'tensorflow': 'TensorFlow',
        'PIL': 'Pillow',
        'flask': 'Flask',
        'numpy': 'NumPy',
        'sqlite3': 'SQLite3'
    }
    
    all_ok = True
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name:15} - OK")
        except ImportError:
            print(f"❌ {name:15} - THIẾU (cần cài: pip install {name})")
            all_ok = False
    
    return all_ok

def check_directory_structure():
    """Kiểm tra cấu trúc thư mục"""
    print_header("3. KIỂM TRA CẤU TRÚC THƯ MỤC")
    
    required_dirs = [
        'data',
        'checkpoints',
        'static',
        'templates',
        'logs'
    ]
    
    all_ok = True
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✅ {dir_name:20} - OK")
        else:
            print(f"⚠️  {dir_name:20} - THIẾU (tạo nó)")
            os.makedirs(dir_name, exist_ok=True)
    
    return all_ok

def check_model_file():
    """Kiểm tra file model"""
    print_header("4. KIỂM TRA FILE MODEL")
    
    model_paths = [
        'checkpoints/simple_model_best.h5',
        'checkpoints/simple_model.h5',
        'checkpoints/model.h5'
    ]
    
    found = False
    for path in model_paths:
        if os.path.isfile(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"✅ {path:40} ({size_mb:.1f} MB)")
            found = True
            break
    
    if not found:
        print("⚠️  KHÔNG TÌM THẤY MODEL")
        print("   Cách giải quyết:")
        print("   1. Chạy: python train_simple.py")
        print("   2. Hoặc sao chép model từ nơi khác")
    
    return found

def check_python_files():
    """Kiểm tra các tệp Python chính"""
    print_header("5. KIỂM TRA TẬP TIN PYTHON CHÍNH")
    
    required_files = {
        'time_extractor.py': 'Module trích xuất thời gian',
        'predict_simple.py': 'Module dự đoán',
        'app_simple.py': 'Flask app',
        'simple_model.py': 'Định nghĩa model',
        'train_simple.py': 'Script huấn luyện'
    }
    
    all_ok = True
    for filename, description in required_files.items():
        if os.path.isfile(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename:25} ({size} bytes) - {description}")
        else:
            print(f"❌ {filename:25} - THIẾU")
            all_ok = False
    
    return all_ok

def check_database():
    """Kiểm tra database"""
    print_header("6. KIỂM TRA DATABASE")
    
    db_file = 'analysis_history.db'
    if os.path.isfile(db_file):
        size_kb = os.path.getsize(db_file) / 1024
        print(f"✅ {db_file:40} ({size_kb:.1f} KB)")
        print("   Database sẽ được tạo khi chạy app lần đầu nếu chưa có")
    else:
        print(f"⚠️  {db_file:40} - Chưa tạo")
        print("   Nó sẽ tự động tạo khi chạy ứng dụng")
    
    return True

def check_imports_in_files():
    """Kiểm tra import trong các file Python"""
    print_header("7. KIỂM TRA IMPORTS TRONG FILE PYTHON")
    
    files_to_check = {
        'time_extractor.py': ['json', 'sqlite3', 'datetime'],
        'predict_simple.py': ['tensorflow', 'PIL', 'time_extractor'],
        'app_simple.py': ['flask', 'predict_simple', 'time_extractor']
    }
    
    all_ok = True
    for filename, imports in files_to_check.items():
        if os.path.isfile(filename):
            print(f"\n📄 {filename}:")
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                for imp in imports:
                    if imp.lower() in content.lower():
                        print(f"  ✅ {imp:20} - OK")
                    else:
                        print(f"  ❌ {imp:20} - THIẾU")
                        all_ok = False
        else:
            print(f"\n❌ {filename} - KHÔNG TÌMTHẤY")
            all_ok = False
    
    return all_ok

def test_time_extractor():
    """Test module TimeExtractor"""
    print_header("8. TEST MODULE TIME EXTRACTOR")
    
    try:
        from time_extractor import TimeExtractor
        
        # Tạo instance
        extractor = TimeExtractor()
        print("✅ Khởi tạo TimeExtractor - OK")
        
        # Test trích xuất thời gian
        time_info = extractor.extract_time_components()
        print(f"✅ Trích xuất thời gian - OK")
        print(f"   Ngày: {time_info['formatted']}")
        print(f"   Các thành phần: Year={time_info['year']}, Month={time_info['month']}, "
              f"Day={time_info['day']}, Hour={time_info['hour']}")
        
        # Test ghi lại phân tích (không thực sự ghi)
        print("✅ TimeExtractor sẵn sàng sử dụng")
        
        return True
    except Exception as e:
        print(f"❌ LỖI: {str(e)}")
        return False

def test_predict_module():
    """Test module WeatherPredictor"""
    print_header("9. TEST MODULE PREDICT")
    
    try:
        from predict_simple import WeatherPredictor
        
        # Kiểm tra file model
        model_path = None
        for path in ['checkpoints/simple_model_best.h5', 'checkpoints/simple_model.h5', 'checkpoints/model.h5']:
            if os.path.isfile(path):
                model_path = path
                break
        
        if not model_path:
            print("⚠️  KHÔNG CÓ FILE MODEL - BỎ QUAT TEST NÀY")
            print("   Chạy: python train_simple.py")
            return False
        
        # Tạo predictor
        predictor = WeatherPredictor(model_path, data_dir='data')
        print(f"✅ Khởi tạo WeatherPredictor với model: {model_path} - OK")
        print(f"   Classes: {', '.join(predictor.class_names)}")
        
        return True
    except Exception as e:
        print(f"❌ LỖI: {str(e)}")
        return False

def test_flask_app():
    """Test Flask app"""
    print_header("10. TEST FLASK APP")
    
    try:
        from app_simple import app
        
        print("✅ Import app_simple - OK")
        print(f"   Flask app name: {app.name}")
        print("✅ Flask app sẵn sàng")
        
        return True
    except Exception as e:
        print(f"❌ LỖI: {str(e)}")
        return False

def generate_report(results):
    """Tạo báo cáo kết quả"""
    print("\n" + "="*60)
    print("📊 BÁOO CÁO KIỂM TRA")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results if r[1])
    failed = total - passed
    
    print(f"\nKết quả: {passed}/{total} kiểm tra thành công")
    
    if failed > 0:
        print(f"\n❌ Có {failed} kiểm tra thất bại")
        failed_tests = [r[0] for r in results if not r[1]]
        print("Các kiểm tra thất bại:")
        for test in failed_tests:
            print(f"  - {test}")
    else:
        print("\n✅ TẤT CẢ KIỂM TRA THÀNH CÔNG!")
        print("\n🚀 Bạn có thể:")
        print("  1. Chạy Flask app: python app_simple.py")
        print("  2. Thử ví dụ: python example_time_extractor.py")
        print("  3. Huấn luyện model: python train_simple.py")
    
    return failed == 0

def main():
    """Chạy tất cả kiểm tra"""
    print("\n" + "="*60)
    print("🔍 KIỂM TRA CƠ BẢN - HEALTH CHECK")
    print("="*60)
    print("\nTệp này giúp bạn kiểm tra xem mọi thứ có hoạt động đúng không")
    print("Nó sẽ kiểm tra:")
    print("  1. Python version")
    print("  2. Thư viện cần thiết")
    print("  3. Cấu trúc thư mục")
    print("  4. File model")
    print("  5. File Python chính")
    print("  6. Database")
    print("  7. Imports trong file")
    print("  8. TimeExtractor module")
    print("  9. WeatherPredictor module")
    print("  10. Flask app")
    
    results = [
        ("Python version", check_python_version()),
        ("Thư viện cần thiết", check_imports()),
        ("Cấu trúc thư mục", check_directory_structure()),
        ("File model", check_model_file()),
        ("File Python chính", check_python_files()),
        ("Database", check_database()),
        ("Imports", check_imports_in_files()),
        ("TimeExtractor", test_time_extractor()),
        ("WeatherPredictor", test_predict_module()),
        ("Flask app", test_flask_app()),
    ]
    
    success = generate_report(results)
    
    print("\n" + "="*60)
    if success:
        print("✅ KIỂM TRA HOÀN THÀNH - MỌI THỨ OK")
    else:
        print("⚠️  KIỂM TRA HOÀN THÀNH - CÓ MỘT SỐ VẤN ĐỀ")
    print("="*60 + "\n")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
