#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Health Check for Weather Classification Project
Kiểm tra toàn bộ hệ thống
"""

import os
import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check_mark(passed):
    return "✅" if passed else "❌"

def print_section(text):
    print(f"\n{text}")
    print("-" * 60)

# Main checks
print_header("🔍 KIỂM TRA HỆ THỐNG PHÂN LOẠI THỜI TIẾT")

# 1. Check project structure
print_section("1️⃣  KIỂM TRA CẤU TRÚC THƯ MỤC")
required_dirs = {
    'data': ['Mưa', 'Nắng', 'Tuyết'],
    'checkpoints': [],
    'templates': [],
    'static': ['uploads', 'images'],
    'logs': []
}

structure_ok = True
for dir_name, subdirs in required_dirs.items():
    path = Path(dir_name)
    exists = path.exists()
    print(f"{check_mark(exists)} {dir_name}/", end="")
    
    if exists and subdirs:
        subdir_status = []
        for subdir in subdirs:
            subdir_path = path / subdir
            subdir_ok = subdir_path.exists()
            subdir_status.append(subdir_ok)
            print(f" {subdir}{'✓' if subdir_ok else '✗'}", end="")
        structure_ok = structure_ok and all(subdir_status)
    
    print()
    structure_ok = structure_ok and exists

# 2. Check required Python files
print_section("2️⃣  KIỂM TRA CÁC TỆPPY CHÍNH")
required_files = [
    'app_simple.py',
    'predict_simple.py',
    'time_extractor.py',
    'train_simple.py',
    'train_quick.py',
    'check_basic.py',
    'requirements.txt'
]

files_ok = True
for filename in required_files:
    exists = os.path.exists(filename)
    print(f"{check_mark(exists)} {filename}")
    files_ok = files_ok and exists

# 3. Check model files
print_section("3️⃣  KIỂM TRA CÁC MÔ HÌNH")
model_files = {
    'checkpoints/simple_model_best.h5': 'Model chính',
    'checkpoints/simple_model.h5': 'Model dự phòng',
}

models_ok = True
for model_path, description in model_files.items():
    exists = os.path.exists(model_path)
    if exists:
        size_mb = os.path.getsize(model_path) / (1024*1024)
        print(f"{check_mark(exists)} {model_path} ({size_mb:.1f} MB) - {description}")
    else:
        print(f"{check_mark(exists)} {model_path} - {description}")
    models_ok = models_ok and exists

# 4. Check database
print_section("4️⃣  KIỂM TRA CƠ SỮ DỮ LIỆU")
try:
    conn = sqlite3.connect('analysis_history.db')
    cursor = conn.cursor()
    
    # Check table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analysis_history'")
    table_exists = cursor.fetchone() is not None
    print(f"{check_mark(table_exists)} Bảng analysis_history")
    
    # Count records
    cursor.execute("SELECT COUNT(*) FROM analysis_history")
    record_count = cursor.fetchone()[0]
    print(f"   📊 Số bản ghi: {record_count}")
    
    # Get recent records
    if record_count > 0:
        cursor.execute("""
            SELECT id, timestamp, prediction, confidence, duration 
            FROM analysis_history 
            ORDER BY timestamp DESC 
            LIMIT 3
        """)
        print("   📋 3 bản ghi gần đây nhất:")
        for row in cursor.fetchall():
            rec_id, timestamp, prediction, confidence, duration = row
            conf_pct = (confidence * 100) if confidence else 0
            print(f"      • ID={rec_id}: {prediction} ({conf_pct:.1f}%) @ {timestamp}")
    
    conn.close()
    db_ok = True
except Exception as e:
    print(f"{check_mark(False)} Lỗi kết nối database: {e}")
    db_ok = False

# 5. Check Python modules
print_section("5️⃣  KIỂM TRA CÁC MODULE PYTHON")
modules_to_check = {
    'tensorflow': 'TensorFlow/Keras',
    'flask': 'Flask',
    'PIL': 'Pillow',
    'numpy': 'NumPy',
    'sqlite3': 'SQLite3'
}

modules_ok = True
for module_name, description in modules_to_check.items():
    try:
        if module_name == 'PIL':
            from PIL import Image
        else:
            __import__(module_name)
        print(f"{check_mark(True)} {description} ({module_name})")
    except ImportError:
        print(f"{check_mark(False)} {description} ({module_name})")
        modules_ok = False

# 6. Check TimeExtractor functionality
print_section("6️⃣  KIỂM TRA TIMEEXTRACTOR")
try:
    from time_extractor import TimeExtractor
    te = TimeExtractor()
    
    # Test extraction
    components = te.extract_time_components()
    print(f"{check_mark(True)} TimeExtractor initialized")
    print(f"   📅 Thời gian hiện tại: {components['formatted']}")
    print(f"   🕐 Thành phần: {components['year']}-{components['month']}-{components['day']} {components['hour']}:{components['minute']}:{components['second']}")
    
    time_extractor_ok = True
except Exception as e:
    print(f"{check_mark(False)} Lỗi TimeExtractor: {e}")
    time_extractor_ok = False

# 7. Check Model Loading
print_section("7️⃣  KIỂM TRA LOADING MÔ HÌNH")
try:
    from predict_simple import WeatherPredictor
    predictor = WeatherPredictor('checkpoints/simple_model_best.h5', data_dir='data')
    print(f"{check_mark(True)} WeatherPredictor initialized")
    print(f"   🎯 Classes: {predictor.class_names}")
    print(f"   📐 Input size: {predictor.img_size}x{predictor.img_size}")
    model_load_ok = True
except Exception as e:
    print(f"{check_mark(False)} Lỗi loading model: {e}")
    model_load_ok = False

# 8. Check data statistics
print_section("8️⃣  THỐNG KÊ DỮ LIỆU")
data_path = Path('data')
class_stats = {}
total_images = 0

for class_dir in ['Mưa', 'Nắng', 'Tuyết']:
    class_path = data_path / class_dir
    if class_path.exists():
        images = len(list(class_path.glob('*.[jJ][pP]*[gG]')))
        class_stats[class_dir] = images
        total_images += images
        print(f"   {class_dir}: {images} images")

print(f"   📦 Tổng cộng: {total_images} images")

# 9. Check Flask app
print_section("9️⃣  KIỂM TRA FLASK APP")
try:
    from flask import Flask
    print(f"{check_mark(True)} Flask module available")
    
    # Check if app_simple.py is valid Python
    with open('app_simple.py', 'r', encoding='utf-8') as f:
        code = f.read()
        compile(code, 'app_simple.py', 'exec')
    print(f"{check_mark(True)} app_simple.py syntax OK")
    flask_ok = True
except Exception as e:
    print(f"{check_mark(False)} Lỗi Flask: {e}")
    flask_ok = False

# 10. Summary
print_header("📊 TÓM TẮT KIỂM TRA")

all_checks = {
    '✅ Cấu trúc thư mục': structure_ok,
    '✅ Tệp Python chính': files_ok,
    '✅ Tệp mô hình': models_ok,
    '✅ Cơ sở dữ liệu': db_ok,
    '✅ Module Python': modules_ok,
    '✅ TimeExtractor': time_extractor_ok,
    '✅ Loading Model': model_load_ok,
    '✅ Flask': flask_ok
}

print("\nKết quả chi tiết:")
for check_name, result in all_checks.items():
    print(f"{check_mark(result)} {check_name}")

# Final status
all_passed = all(all_checks.values())
print("\n" + "="*60)
if all_passed:
    print("🎉 TẤT CẢ KIỂM TRA THÀNH CÔNG! HỆ THỐNG SẴN SÀNG!")
else:
    print("⚠️  CÓ MỘT SỐ VẤN ĐỀ CẦN KHẮC PHỤC")
print("="*60)

# Additional info
print("\n📝 THÔNG TIN HỮU DỤ:")
print(f"   • Ngày kiểm tra: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   • Python version: {sys.version}")
print(f"   • Working directory: {os.getcwd()}")
print(f"   • Database records: {record_count if db_ok else 'N/A'}")
print(f"   • Data images: {total_images}")

sys.exit(0 if all_passed else 1)
