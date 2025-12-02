#!/usr/bin/env python3
"""
QUICK TEST - Test nhanh các tính năng cơ bản
Tệp này giúp bạn test mà không cần model hoặc dữ liệu phức tạp
"""

import sys
import os

def test_1_time_extraction():
    """Test 1: Trích xuất thời gian"""
    print("\n" + "="*60)
    print("TEST 1: TRÍCH XUẤT THỜI GIAN")
    print("="*60)
    
    try:
        from time_extractor import TimeExtractor
        from datetime import datetime
        
        extractor = TimeExtractor()
        
        # Test với thời gian hiện tại
        time_info = extractor.extract_time_components()
        
        print(f"\n✅ Trích xuất thành công!")
        print(f"  Ngày giờ: {time_info['formatted']}")
        print(f"  Năm: {time_info['year']}")
        print(f"  Tháng: {time_info['month']}")
        print(f"  Ngày: {time_info['day']}")
        print(f"  Giờ: {time_info['hour']:02d}")
        print(f"  Phút: {time_info['minute']:02d}")
        print(f"  Giây: {time_info['second']:02d}")
        print(f"  Ngày trong tuần: {time_info['week_day']}")
        print(f"  Tháng: {time_info['month_name']}")
        print(f"  Quý: Q{time_info['quarter']}")
        print(f"  Tuần ISO: {time_info['iso_week']}")
        print(f"  Ngày trong năm: {time_info['day_of_year']}")
        print(f"  Unix timestamp: {time_info['unix_timestamp']}")
        
        return True
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        return False

def test_2_record_analysis():
    """Test 2: Ghi lại phân tích"""
    print("\n" + "="*60)
    print("TEST 2: GHI LẠI PHÂN TÍCH")
    print("="*60)
    
    try:
        from time_extractor import TimeExtractor
        
        extractor = TimeExtractor()
        
        # Ghi lại 3 phân tích giả
        analyses = [
            {'image': 'test_001.jpg', 'pred': 'Sunny', 'conf': 0.95, 'dur': 0.234},
            {'image': 'test_002.jpg', 'pred': 'Rainy', 'conf': 0.87, 'dur': 0.201},
            {'image': 'test_003.jpg', 'pred': 'Snowy', 'conf': 0.92, 'dur': 0.218},
        ]
        
        print(f"\n✅ Ghi lại phân tích:")
        for analysis in analyses:
            record = extractor.record_analysis(
                image_name=analysis['image'],
                prediction=analysis['pred'],
                confidence=analysis['conf'],
                duration=analysis['dur'],
                notes=f"Test record for {analysis['image']}"
            )
            print(f"  ID {record['id']}: {analysis['image']} -> "
                  f"{analysis['pred']} ({analysis['conf']:.0%})")
        
        return True
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        return False

def test_3_get_history():
    """Test 3: Lấy lịch sử"""
    print("\n" + "="*60)
    print("TEST 3: LẤY LỊCH SỬ PHÂN TÍCH")
    print("="*60)
    
    try:
        from time_extractor import TimeExtractor
        from datetime import datetime
        
        extractor = TimeExtractor()
        today = datetime.now()
        
        # Lấy lịch sử hôm nay
        records = extractor.get_analysis_by_date(
            year=today.year,
            month=today.month,
            day=today.day
        )
        
        print(f"\n✅ Lấy lịch sử hôm nay:")
        print(f"  Tìm thấy {len(records)} phân tích")
        
        if records:
            print(f"\n  Chi tiết (3 phân tích đầu):")
            for i, record in enumerate(records[:3], 1):
                print(f"    #{i}: {record['image_name']} -> {record['prediction']} "
                      f"({record['confidence']:.0%})" if record['confidence'] else f"    #{i}: {record['image_name']}")
        
        return True
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        return False

def test_4_statistics():
    """Test 4: Thống kê"""
    print("\n" + "="*60)
    print("TEST 4: THỐNG KÊ PHÂN TÍCH")
    print("="*60)
    
    try:
        from time_extractor import TimeExtractor
        from datetime import datetime
        
        extractor = TimeExtractor()
        today = datetime.now()
        
        # Lấy thống kê hôm nay
        stats = extractor.get_statistics_by_date(
            year=today.year,
            month=today.month,
            day=today.day
        )
        
        print(f"\n✅ Thống kê hôm nay:")
        print(f"  Tổng phân tích: {stats['total']}")
        print(f"  Phân loại: {stats['by_prediction']}")
        
        if stats['total'] > 0:
            print(f"  Độ tin cậy:")
            print(f"    - Trung bình: {stats['average_confidence']:.2%}")
            print(f"    - Cao nhất: {stats['max_confidence']:.2%}")
            print(f"    - Thấp nhất: {stats['min_confidence']:.2%}")
            print(f"  Thời gian xử lý:")
            print(f"    - Tổng: {stats['total_duration']:.2f}s")
            print(f"    - Trung bình: {stats['average_duration']:.4f}s")
        
        return True
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        return False

def test_5_hourly_stats():
    """Test 5: Thống kê theo giờ"""
    print("\n" + "="*60)
    print("TEST 5: THỐNG KÊ THEO GIỜ")
    print("="*60)
    
    try:
        from time_extractor import TimeExtractor
        from datetime import datetime
        
        extractor = TimeExtractor()
        today = datetime.now()
        
        # Lấy thống kê theo giờ
        hourly = extractor.get_hourly_statistics(
            year=today.year,
            month=today.month,
            day=today.day
        )
        
        print(f"\n✅ Thống kê theo giờ:")
        
        hours_with_data = [h for h in range(24) if hourly[h]['count'] > 0]
        
        if hours_with_data:
            print(f"  Các giờ có dữ liệu: {', '.join(f'{h:02d}' for h in hours_with_data)}")
            
            for hour in hours_with_data[:3]:
                stats = hourly[hour]
                print(f"\n  Giờ {hour:02d}:00:")
                print(f"    Số lượng: {stats['count']}")
                print(f"    Dự đoán: {stats['predictions']}")
                if stats['count'] > 0:
                    print(f"    Độ tin cậy TB: {stats['average_confidence']:.2%}")
        else:
            print(f"  Không có dữ liệu cho giờ nào (đây là bình thường)")
        
        return True
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        return False

def test_6_time_range():
    """Test 6: Lấy lịch sử trong khoảng thời gian"""
    print("\n" + "="*60)
    print("TEST 6: LỊCH SỬ TRONG KHOẢNG THỜI GIAN")
    print("="*60)
    
    try:
        from time_extractor import TimeExtractor
        from datetime import datetime
        
        extractor = TimeExtractor()
        today = datetime.now()
        
        # Lấy từ 8h đến 18h
        records = extractor.get_analysis_by_time_range(
            start_hour=8,
            end_hour=18,
            year=today.year,
            month=today.month,
            day=today.day
        )
        
        print(f"\n✅ Lịch sử từ 8h đến 18h:")
        print(f"  Tìm thấy {len(records)} phân tích")
        
        if records:
            print(f"  Giờ của các phân tích: {', '.join(set(str(r['hour']) for r in records))}")
        
        return True
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        return False

def test_7_export():
    """Test 7: Xuất dữ liệu"""
    print("\n" + "="*60)
    print("TEST 7: XUẤT DỮ LIỆU JSON")
    print("="*60)
    
    try:
        from time_extractor import TimeExtractor
        from datetime import datetime
        import os
        
        extractor = TimeExtractor()
        today = datetime.now()
        
        # Xuất dữ liệu
        export_file = f'test_export_{today.strftime("%Y%m%d_%H%M%S")}.json'
        result = extractor.export_history_to_json(
            output_path=export_file,
            year=today.year,
            month=today.month,
            day=today.day
        )
        
        print(f"\n✅ Xuất thành công!")
        print(f"  File: {export_file}")
        
        # Kiểm tra file
        if os.path.isfile(export_file):
            size = os.path.getsize(export_file)
            print(f"  Kích thước: {size} bytes")
            
            # Xóa file test
            os.remove(export_file)
            print(f"  ✅ File test đã xóa")
        
        return True
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        return False

def test_8_database():
    """Test 8: Database"""
    print("\n" + "="*60)
    print("TEST 8: DATABASE")
    print("="*60)
    
    try:
        from time_extractor import TimeExtractor
        import os
        
        db_file = 'analysis_history.db'
        extractor = TimeExtractor(db_file=db_file)
        
        print(f"\n✅ Database kiểm tra:")
        
        if os.path.isfile(db_file):
            size = os.path.getsize(db_file)
            print(f"  File: {db_file}")
            print(f"  Kích thước: {size} bytes ({size/1024:.1f} KB)")
        else:
            print(f"  File: {db_file} (sẽ tạo khi sử dụng)")
        
        return True
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        return False

def main():
    """Chạy tất cả test"""
    print("\n" + "="*60)
    print("🔬 QUICK TEST - TEST NHANH CÁC TÍNH NĂNG")
    print("="*60)
    
    tests = [
        ("Trích xuất thời gian", test_1_time_extraction),
        ("Ghi lại phân tích", test_2_record_analysis),
        ("Lấy lịch sử", test_3_get_history),
        ("Thống kê", test_4_statistics),
        ("Thống kê theo giờ", test_5_hourly_stats),
        ("Lịch sử trong khoảng thời gian", test_6_time_range),
        ("Xuất dữ liệu", test_7_export),
        ("Database", test_8_database),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Lỗi bất ngờ trong {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Báo cáo
    print("\n" + "="*60)
    print("📊 KẾT QUẢ TEST")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nKết quả: {passed}/{total} test thành công")
    
    print("\nChiết tiết:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print("\n" + "="*60)
    
    if passed == total:
        print("✅ TẤT CẢ TEST THÀNH CÔNG!")
        print("\nBạn có thể:")
        print("  1. Chạy web app: python app_simple.py")
        print("  2. Thử ví dụ: python example_time_extractor.py")
        print("  3. Xem tài liệu: GETTING_STARTED.md")
    else:
        print(f"⚠️  {total - passed} test thất bại")
        print("\nChiều khắc phục:")
        print("  1. Kiểm tra file cơ bản: python check_basic.py")
        print("  2. Cài đặt thư viện: pip install -r requirements.txt")
        print("  3. Xem logs để tìm hiểu thêm")
    
    print("="*60 + "\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
