#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phân tích chất lượng dữ liệu và cải thiện model
"""

import os
import numpy as np
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt

print("="*60)
print("📊 PHÂN TÍCH DỮ LIỆU VÀ CẢI THIỆN MODEL")
print("="*60)

# 1. Check data distribution
print("\n1️⃣  PHÂN TÍCH PHÂN PHỐI DỮ LIỆU")
print("-"*60)

data_path = Path('data')
class_stats = {}

for class_name in ['Mưa', 'Nắng', 'Tuyết']:
    class_path = data_path / class_name
    images = list(class_path.glob('*.[jJ][pP]*[gG]'))
    class_stats[class_name] = len(images)
    print(f"  {class_name}: {len(images)} ảnh")

total = sum(class_stats.values())
print(f"\n  📦 Tổng: {total} ảnh")

# Check imbalance
print("\n  🔍 Tỷ lệ phân phối:")
for class_name, count in class_stats.items():
    percentage = (count / total) * 100
    print(f"     {class_name}: {percentage:.1f}%")

# 2. Check image dimensions
print("\n2️⃣  KIỂM TRA KÍCH THƯỚC ẢNH")
print("-"*60)

sample_images = {}
for class_name in ['Mưa', 'Nắng', 'Tuyết']:
    class_path = data_path / class_name
    images = list(class_path.glob('*.[jJ][pP]*[gG]'))[:3]  # Sample 3 images
    
    if images:
        sizes = []
        for img_path in images:
            try:
                img = Image.open(img_path)
                sizes.append(img.size)
            except:
                pass
        
        if sizes:
            avg_size = (int(np.mean([s[0] for s in sizes])), int(np.mean([s[1] for s in sizes])))
            print(f"  {class_name}: {avg_size[0]}x{avg_size[1]} (trung bình)")

# 3. Recommendations
print("\n3️⃣  KHUYẾN NGHỊ CẢI THIỆN")
print("-"*60)

recommendations = [
    "✅ Dữ liệu: 6445 ảnh - Đủ tốt",
    "⚠️  Cân bằng: Nắng 87% vs Mưa 3%, Tuyết 10%",
    "💡 Giải pháp:",
    "   1. Thu thêm ảnh Mưa và Tuyết",
    "   2. Dùng class_weight để cân bằng",
    "   3. Tăng data augmentation",
    "   4. Dùng model đơn giản hơn để tránh overfitting"
]

for rec in recommendations:
    print(f"  {rec}")

# 4. Check image quality
print("\n4️⃣  KIỂM TRA CHẤT LƯỢNG ẢNH")
print("-"*60)

issue_count = 0
for class_name in ['Mưa', 'Nắng', 'Tuyết']:
    class_path = data_path / class_name
    images = list(class_path.glob('*.[jJ][pP]*[gG]'))
    
    print(f"\n  {class_name}:")
    for img_path in images[:5]:  # Check first 5
        try:
            img = Image.open(img_path)
            size_mb = img_path.stat().st_size / (1024*1024)
            
            if size_mb < 0.01:
                print(f"    ⚠️  {img_path.name} - Quá nhỏ ({size_mb:.3f}MB)")
                issue_count += 1
            elif size_mb > 10:
                print(f"    ⚠️  {img_path.name} - Quá lớn ({size_mb:.1f}MB)")
                issue_count += 1
            else:
                print(f"    ✅ {img_path.name} - OK ({img.size})")
        except Exception as e:
            print(f"    ❌ {img_path.name} - Lỗi: {e}")
            issue_count += 1

print("\n5️⃣  CÁCH CẢI THIỆN MODEL")
print("-"*60)
improvements = """
  A. Ngay lập tức:
     • Sử dụng class_weight để cân bằng dữ liệu
     • Tăng augmentation (rotation, brightness, flip)
     • Điều chỉnh learning rate

  B. Tối ưu hóa model:
     • Dùng pre-trained model (MobileNet, ResNet)
     • Thêm Batch Normalization
     • Tăng dropout rate

  C. Thu thập dữ liệu:
     • Thu thêm ảnh Mưa (hiện tại chỉ 3%)
     • Thu thêm ảnh Tuyết (hiện tại 10%)
     • Đa dạng hóa điều kiện thời tiết

  D. Tiền xử lý:
     • Chuẩn hóa histogram
     • Xóa ảnh nhiễu
     • Kiểm tra nhãn sai
"""
print(improvements)

print("="*60)
print("🎯 KHUYẾN NGHỊ: Tập trung vào cân bằng dữ liệu!")
print("="*60)
